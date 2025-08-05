#!/usr/bin/env python3
"""
Setup script for PyFunc with optional C++ backend.
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11
from setuptools import setup, Extension, find_namespace_packages
import os
import sys
import subprocess
import shutil

# Define a custom Extension class for Go
class GoExtension(Extension):
    def __init__(self, name, go_source_dir, **kwargs):
        super().__init__(name, sources=[], **kwargs)
        self.go_source_dir = go_source_dir

# Custom build_ext to handle Go compilation
class GoBuildExt(build_ext):
    def build_extension(self, ext):
        if isinstance(ext, GoExtension):
            # Compile Go shared library
            go_output_name = ext.name.split('.')[-1] # e.g., 'native_go'
            go_output_path = os.path.join(self.build_temp, go_output_name)
            
            # Ensure build_temp exists
            os.makedirs(self.build_temp, exist_ok=True)

            go_command = [
                "go", "build",
                "-buildmode=c-shared",
                "-o", f"{go_output_path}.dll", # Windows DLL
                "."
            ]
            
            print(f"Running Go build command: {' '.join(go_command)}")
            try:
                subprocess.run(go_command, check=True, cwd=ext.go_source_dir)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Go build failed: {e}")

            # Copy the compiled Go library to the final build directory
            # This is crucial for pybind11 to find it
            final_go_lib_name = f"{go_output_name}.dll" # Windows DLL
            final_go_lib_path = os.path.join(self.build_lib, final_go_lib_name)
            
            # Ensure the target directory exists
            os.makedirs(os.path.dirname(final_go_lib_path), exist_ok=True)

            shutil.copy(f"{go_output_path}.dll", final_go_lib_path)
            print(f"Copied Go shared library to: {final_go_lib_path}")

            # Create a temporary C++ wrapper for pybind11
            wrapper_cpp_content = f"""
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "{go_output_name}.h" // Include the Go-generated C header

namespace py = pybind11;

// Declare the C functions from the Go shared library
extern void bitwise_and_go(int* data, int size, int operand);
extern void bitwise_or_go(int* data, int size, int operand);
extern void bitwise_xor_go(int* data, int size, int operand);
extern void bitwise_not_go(int* data, int size);
extern void left_shift_go(int* data, int size, int bits);
extern void right_shift_go(int* data, int size, int bits);

// Wrapper functions that handle the conversion from Python list to C array
std::vector<int> bitwise_and_wrapper(std::vector<int> data, int operand) {{
    bitwise_and_go(data.data(), data.size(), operand);
    return data;
}}

std::vector<int> bitwise_or_wrapper(std::vector<int> data, int operand) {{
    bitwise_or_go(data.data(), data.size(), operand);
    return data;
}}

std::vector<int> bitwise_xor_wrapper(std::vector<int> data, int operand) {{
    bitwise_xor_go(data.data(), data.size(), operand);
    return data;
}}

std::vector<int> bitwise_not_wrapper(std::vector<int> data) {{
    bitwise_not_go(data.data(), data.size());
    return data;
}}

std::vector<int> left_shift_wrapper(std::vector<int> data, int bits) {{
    left_shift_go(data.data(), data.size(), bits);
    return data;
}}

std::vector<int> right_shift_wrapper(std::vector<int> data, int bits) {{
    right_shift_go(data.data(), data.size(), bits);
    return data;
}}

PYBIND11_MODULE({go_output_name}, m) {{
    m.doc() = "PyFunc Go backend for high-performance bitwise operations";

    m.def("bitwise_and", &bitwise_and_wrapper, "Perform bitwise AND on a list of integers");
    m.def("bitwise_or", &bitwise_or_wrapper, "Perform bitwise OR on a list of integers");
    m.def("bitwise_xor", &bitwise_xor_wrapper, "Perform bitwise XOR on a list of integers");
    m.def("bitwise_not", &bitwise_not_wrapper, "Perform bitwise NOT on a list of integers");
    m.def("left_shift", &left_shift_wrapper, "Perform bitwise left shift on a list of integers");
    m.def("right_shift", &right_shift_wrapper, "Perform bitwise right shift on a list of integers");
}}
            """
            temp_wrapper_path = os.path.join(self.build_temp, f"{go_output_name}_wrapper.cpp")
            with open(temp_wrapper_path, "w") as f:
                f.write(wrapper_cpp_content)

            # Now, call the original build_extension for the pybind11 part
            # This will compile the C++ wrapper and link against the Go DLL
            super().build_extension(
                Pybind11Extension(
                    ext.name, # Use the original name (e.g., "pyfunc.native_go")
                    sources=[temp_wrapper_path],
                    include_dirs=[
                        pybind11.get_include(),
                        ext.go_source_dir, # Include path for the Go-generated header
                    ],
                    library_dirs=[self.build_lib], # Directory where the Go DLL is copied
                    libraries=[go_output_name], # Link against the Go DLL
                    language='c++',
                    cxx_std=17,
                )
            )
        else:
            super().build_extension(ext)

# Check if we should build C++ extension
BUILD_CPP = os.environ.get('PYFUNC_BUILD_CPP', '1') == '1'

ext_modules = []

if BUILD_CPP:
    try:
        import sysconfig
        
        # Get Python library information for proper linking
        def get_python_link_info():
            if os.name == 'nt':  # Windows
                # Get Python installation directory
                python_lib_dir = sysconfig.get_path('stdlib')
                python_lib_dir = os.path.dirname(python_lib_dir)  # Go up to Python root
                python_lib_dir = os.path.join(python_lib_dir, 'libs')
                
                # Python version for Windows (e.g., python313)
                version_nodot = sysconfig.get_config_var('py_version_nodot')
                python_lib_name = f"python{version_nodot}"
                
                return [f"-L{python_lib_dir}", f"-l{python_lib_name}"]
            else:  # Unix-like systems
                python_lib_dir = sysconfig.get_config_var('LIBDIR')
                python_version = sysconfig.get_config_var('VERSION')
                python_lib_name = f"python{python_version}"
                
                return [f"-L{python_lib_dir}", f"-l{python_lib_name}"]
        
        # Get linking flags
        link_args = get_python_link_info()
        
        # Define the extension module
        ext_modules = [
            Pybind11Extension(
                "pyfunc_native",
                [
                    "pyfunc/native/operations.cpp",
                    "pyfunc/native/bindings.cpp",
                ],
                include_dirs=[
                    # Path to pybind11 headers
                    pybind11.get_include(),
                    "pyfunc/native",
                ],
                language='c++',
                cxx_std=17,  # Use C++17 standard
                extra_link_args=link_args,
            ),
            GoExtension(
                "pyfunc.native_go", # Name of the Python module
                "pyfunc/native_go", # Path to the Go source directory
                include_dirs=[pybind11.get_include()], # pybind11 headers
                language='c++', # pybind11 part is C++
                cxx_std=17,
            ),
        ]
        print("C++ extension will be built")
    except Exception as e:
        print(f"C++ extension build failed: {e}")
        print("Falling back to Python-only build")
        ext_modules = []
else:
    print("Building Python-only version (set PYFUNC_BUILD_CPP=1 to enable C++)")


# Read version from pyproject.toml
def get_version():
    import re
    with open('pyproject.toml', 'r') as f:
        content = f.read()
    match = re.search(r'version = "([^"]*)"', content)
    if match:
        return match.group(1)
    return "0.3.0"

# Read long description
def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="pyfunc-pipeline",
    version=get_version(),
    author="Alex",
    author_email="alex@example.com",
    description="Functional programming pipeline for Python with optional C++ backend",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexzzzs/PyFunc",
    packages=find_namespace_packages(include=["pyfunc", "pyfunc.*", "pyfunc.native", "pyfunc.native_c"]) + ["pyfunc.native", "pyfunc.native_c"],
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "cpp": ["pybind11>=2.6.0"],
        "dev": [
            "pytest>=6.0",
            "mypy>=0.900", 
            "black>=21.0",
            "flake8>=3.8",
            "pybind11>=2.6.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    zip_safe=False,  # Required for C++ extensions
)