#!/usr/bin/env python3
"""
Example demonstrating different ways to control C++ backend usage in PyFunc.
"""

from pyfunc import pipe, _, enable_cpp_backend, disable_cpp_backend, use_cpp_backend, is_cpp_available

def main():
    print("🚀 PyFunc C++ Backend Control Examples")
    print("=" * 50)
    
    # Check if C++ backend is available
    if not is_cpp_available():
        print("❌ C++ backend not available. Please build with: python setup.py build_ext --inplace")
        return
    
    # Sample data
    data = list(range(1000))
    
    print("\n1. Default Python Backend")
    print("-" * 30)
    disable_cpp_backend()
    result = pipe(data).map(_ * 2).filter(_ > 1000).sum().get()
    print(f"Result: {result}")
    
    print("\n2. Automatic C++ Backend (with threshold)")
    print("-" * 40)
    enable_cpp_backend(threshold=500)  # Use C++ for data size >= 500
    result = pipe(data).map(_ * 2).filter(_ > 1000).sum().get()
    print(f"Result: {result}")
    
    print("\n3. Force C++ Backend (no threshold)")
    print("-" * 35)
    use_cpp_backend()  # Use C++ for all supported operations
    result = pipe(data).map(_ * 2).filter(_ > 1000).sum().get()
    print(f"Result: {result}")
    
    print("\n4. Explicit C++ Methods")
    print("-" * 25)
    disable_cpp_backend()  # Disable automatic C++ usage
    try:
        # Use explicit C++ methods
        result = (pipe(data)
                 .map_cpp(_ * 2)      # Explicitly use C++ for map
                 .filter_cpp(_ > 1000) # Explicitly use C++ for filter
                 .sum_cpp()           # Explicitly use C++ for sum
                 .get())
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n5. Mixed Usage")
    print("-" * 15)
    disable_cpp_backend()
    try:
        # Mix Python and C++ operations
        result = (pipe(data)
                 .map(_ * 2)          # Python (automatic)
                 .filter_cpp(_ > 1000) # C++ (explicit)
                 .sum()               # Python (automatic)
                 .get())
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n6. Performance Comparison")
    print("-" * 25)
    import time
    
    large_data = list(range(100000))
    
    # Python backend
    disable_cpp_backend()
    start = time.time()
    python_result = pipe(large_data).map(_ * 2).filter(_ > 100000).sum().get()
    python_time = time.time() - start
    
    # C++ backend
    use_cpp_backend()
    start = time.time()
    cpp_result = pipe(large_data).map(_ * 2).filter(_ > 100000).sum().get()
    cpp_time = time.time() - start
    
    print(f"Python result: {python_result} (time: {python_time:.4f}s)")
    print(f"C++ result: {cpp_result} (time: {cpp_time:.4f}s)")
    print(f"Speedup: {python_time/cpp_time:.2f}x")
    
    print("\n7. Error Handling")
    print("-" * 18)
    disable_cpp_backend()
    
    # This will fail because C++ backend is disabled
    try:
        result = pipe([1, 2, 3]).map_cpp(_ * 2).get()
        print(f"Unexpected success: {list(result)}")
    except Exception as e:
        print(f"Expected error: {e}")
    
    # This will work because we're using regular map
    result = pipe([1, 2, 3]).map(_ * 2).to_list()
    print(f"Python fallback works: {result}")
    
    print("\n✅ All examples completed!")

if __name__ == "__main__":
    main()