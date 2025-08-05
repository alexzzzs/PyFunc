#!/usr/bin/env python3
"""
Simple test to build just the C++ module without the full setup.
"""

import subprocess
import sys
import os

def get_python_info():
    """Get Python library information for linking."""
    import sysconfig
    import os
    
    # Get Python library path and name
    python_lib_dir = sysconfig.get_config_var('LIBDIR')
    python_version = sysconfig.get_config_var('VERSION')
    python_lib_name = f"python{python_version}"
    
    # On Windows, we need different handling
    if os.name == 'nt':
        # Windows Python library info
        python_lib_dir = sysconfig.get_path('stdlib')
        python_lib_dir = os.path.dirname(python_lib_dir)  # Go up to Python root
        python_lib_dir = os.path.join(python_lib_dir, 'libs')
        
        # Python version for Windows (e.g., python313.lib)
        version_nodot = sysconfig.get_config_var('py_version_nodot')
        python_lib_name = f"python{version_nodot}"
    
    return python_lib_dir, python_lib_name

def test_simple_build():
    """Try a simple pybind11 build with proper Python linking."""
    print("🔧 Testing simple C++ build...")
    
    # Get pybind11 includes
    try:
        result = subprocess.run([sys.executable, "-m", "pybind11", "--includes"], 
                              capture_output=True, text=True, check=True)
        includes = result.stdout.strip().split()
        print(f"✅ Pybind11 includes: {' '.join(includes)}")
    except Exception as e:
        print(f"❌ Failed to get pybind11 includes: {e}")
        assert False, f"Failed to get pybind11 includes: {e}"
    
    # Get Python library information
    try:
        python_lib_dir, python_lib_name = get_python_info()
        print(f"✅ Python lib dir: {python_lib_dir}")
        print(f"✅ Python lib name: {python_lib_name}")
    except Exception as e:
        print(f"❌ Failed to get Python library info: {e}")
        assert False, f"Failed to get Python library info: {e}"
    
    # Build the compile command
    if os.name == 'nt':  # Windows
        compile_cmd = [
            "g++", "-O3", "-Wall", "-shared", "-std=c++17",
            *includes,
            "pyfunc/native/operations.cpp",
            "pyfunc/native/bindings.cpp",
            f"-L{python_lib_dir}",
            f"-l{python_lib_name}",
            "-o", "pyfunc_native.pyd"
        ]
    else:  # Unix-like
        compile_cmd = [
            "g++", "-O3", "-Wall", "-shared", "-std=c++17", "-fPIC",
            *includes,
            "pyfunc/native/operations.cpp",
            "pyfunc/native/bindings.cpp",
            f"-L{python_lib_dir}",
            f"-l{python_lib_name}",
            "-o", "pyfunc_native.so"
        ]
    
    print("🔨 Compiling C++ module...")
    print(" ".join(compile_cmd))
    
    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
        print("✅ C++ module compiled successfully!")
        
        # Test import
        try:
            import pyfunc_native
            print("✅ Module imports successfully!")
            
            # Test basic operation
            test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
            result = pyfunc_native.sum_operation(test_data)
            print(f"✅ Sum test: {result} (expected: 15.0)")
            
            assert result == 15.0
        except ImportError as e:
            print(f"❌ Import failed: {e}")
            assert False, f"Import failed: {e}"
            
    except subprocess.CalledProcessError as e:
        print("❌ Compilation failed:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        assert False, "Compilation failed"
    except Exception as e:
        print(f"❌ Build failed: {e}")
        assert False, f"Build failed: {e}"

if __name__ == "__main__":
    test_simple_build()