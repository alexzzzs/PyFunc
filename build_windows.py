#!/usr/bin/env python3
"""
Windows-specific build script for PyFunc C++ backend.
"""

import subprocess
import sys
import os
import sysconfig

def get_python_info():
    """Get Python library information for Windows."""
    # Get Python installation directory
    python_base = sys.prefix
    python_lib_dir = os.path.join(python_base, 'libs')
    
    # Python version for Windows (e.g., python313)
    version_info = sys.version_info
    version_nodot = f"{version_info.major}{version_info.minor}"
    python_lib_name = f"python{version_nodot}"
    
    return python_lib_dir, python_lib_name

def get_pybind11_info():
    """Get pybind11 include directories."""
    try:
        import pybind11
        import sysconfig
        
        includes = [
            f"-I{pybind11.get_include()}",
            f"-I{pybind11.get_include(user=True)}"
        ]
        
        # Add Python include directory
        python_include = sysconfig.get_path('include')
        if python_include:
            includes.append(f"-I{python_include}")
            print(f"✅ Python include dir: {python_include}")
            
            # Check if Python.h exists
            python_h = os.path.join(python_include, 'Python.h')
            if os.path.exists(python_h):
                print(f"✅ Python.h found: {python_h}")
            else:
                print(f"❌ Python.h not found at: {python_h}")
        
        # Also try the platinclude path
        python_platinclude = sysconfig.get_path('platinclude')
        if python_platinclude and python_platinclude != python_include:
            includes.append(f"-I{python_platinclude}")
            print(f"✅ Python platinclude dir: {python_platinclude}")
            
            # Check if Python.h exists in platinclude
            python_h_plat = os.path.join(python_platinclude, 'Python.h')
            if os.path.exists(python_h_plat):
                print(f"✅ Python.h found in platinclude: {python_h_plat}")
        
        # If Python.h is still not found, try some common locations
        if not any(os.path.exists(os.path.join(inc.replace('-I', ''), 'Python.h')) for inc in includes if inc.startswith('-I')):
            print("⚠️  Python.h not found in standard locations, trying alternatives...")
            
            # Try the Python installation directory
            python_base = sys.prefix
            alt_include = os.path.join(python_base, 'include')
            if os.path.exists(alt_include):
                includes.append(f"-I{alt_include}")
                python_h_alt = os.path.join(alt_include, 'Python.h')
                if os.path.exists(python_h_alt):
                    print(f"✅ Python.h found in alternative location: {python_h_alt}")
                else:
                    print(f"❌ Python.h not found in alternative location: {python_h_alt}")
        
        return includes
    except ImportError:
        print("❌ pybind11 not found. Install with: pip install pybind11")
        return None

def build_cpp_module():
    """Build the C++ module for Windows."""
    print("🔧 Building PyFunc C++ module for Windows...")
    
    # Check for required tools
    try:
        subprocess.run(["g++", "--version"], capture_output=True, check=True)
        print("✅ g++ compiler found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ g++ compiler not found. Please install MinGW-w64 or similar.")
        return False
    
    # Get pybind11 includes
    includes = get_pybind11_info()
    if not includes:
        return False
    
    # Get Python library info
    try:
        python_lib_dir, python_lib_name = get_python_info()
        print(f"✅ Python lib dir: {python_lib_dir}")
        print(f"✅ Python lib name: {python_lib_name}")
        
        # Verify the library file exists
        lib_file = os.path.join(python_lib_dir, f"{python_lib_name}.lib")
        if not os.path.exists(lib_file):
            print(f"❌ Python library not found: {lib_file}")
            return False
        print(f"✅ Python library found: {lib_file}")
        
    except Exception as e:
        print(f"❌ Failed to get Python library info: {e}")
        return False
    
    # Build the compile command
    compile_cmd = [
        "g++",
        "-O3",
        "-Wall", 
        "-shared",
        "-std=c++17",
        *includes,
        f"-I{os.path.join(os.getcwd(), 'pyfunc', 'native')}",
        f"-L{python_lib_dir}",
        f"-l{python_lib_name}",
        "pyfunc/native/operations.cpp",
        "pyfunc/native/bindings.cpp",
        "-o", "pyfunc_native.pyd"
    ]
    
    print("🔨 Compiling C++ module...")
    print("Command:", " ".join(compile_cmd))
    
    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
        print("✅ C++ module compiled successfully!")
        
        # Test the module
        return test_module()
        
    except subprocess.CalledProcessError as e:
        print("❌ Compilation failed:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        
        # Try alternative linking approach
        print("\n🔄 Trying alternative linking approach...")
        return try_alternative_build()

def try_alternative_build():
    """Try building with different linking flags."""
    includes = get_pybind11_info()
    if not includes:
        return False
    
    # Alternative approach: link directly to python DLL
    python_dll = os.path.join(sys.prefix, f"python{sys.version_info.major}{sys.version_info.minor}.dll")
    
    compile_cmd = [
        "g++",
        "-O3",
        "-Wall",
        "-shared", 
        "-std=c++17",
        *includes,
        f"-I{os.path.join(os.getcwd(), 'pyfunc', 'native')}",
        "pyfunc/native/operations.cpp",
        "pyfunc/native/bindings.cpp",
        python_dll,  # Link directly to Python DLL
        "-o", "pyfunc_native.pyd"
    ]
    
    print("🔨 Trying alternative compilation...")
    print("Command:", " ".join(compile_cmd))
    
    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
        print("✅ Alternative compilation successful!")
        return test_module()
        
    except subprocess.CalledProcessError as e:
        print("❌ Alternative compilation also failed:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def test_module():
    """Test if the compiled module works."""
    print("\n🧪 Testing compiled module...")
    
    try:
        # Add current directory to path for import
        if os.getcwd() not in sys.path:
            sys.path.insert(0, os.getcwd())
        
        import pyfunc_native
        print("✅ Module imports successfully!")
        
        # Test basic operations
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        # Test sum
        result = pyfunc_native.sum_operation(test_data)
        expected = 15.0
        if abs(result - expected) < 1e-10:
            print(f"✅ Sum test passed: {result}")
        else:
            print(f"❌ Sum test failed: expected {expected}, got {result}")
            return False
        
        # Test map operation
        result = pyfunc_native.map_operation(test_data, "mul_2")
        expected = [2.0, 4.0, 6.0, 8.0, 10.0]
        if result == expected:
            print(f"✅ Map test passed: {result}")
        else:
            print(f"❌ Map test failed: expected {expected}, got {result}")
            return False
        
        # Test filter operation
        result = pyfunc_native.filter_operation(test_data, "gt_3")
        expected = [4.0, 5.0]
        if result == expected:
            print(f"✅ Filter test passed: {result}")
        else:
            print(f"❌ Filter test failed: expected {expected}, got {result}")
            return False
        
        print("🎉 All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Module test failed: {e}")
        return False

def main():
    print("🚀 PyFunc Windows C++ Build Script")
    print("=" * 40)
    
    if build_cpp_module():
        print("\n🎉 Build completed successfully!")
        print("\nTo test the C++ backend:")
        print("  python examples/cpp_backend_example.py")
        print("  python -m unittest tests.test_cpp_backend")
    else:
        print("\n❌ Build failed")
        print("\nTroubleshooting:")
        print("1. Make sure MinGW-w64 is installed and in PATH")
        print("2. Verify pybind11 is installed: pip install pybind11")
        print("3. Check that Python development files are available")

if __name__ == "__main__":
    main()