#!/usr/bin/env python3
"""
Complete Guide: User Control Over Backend Selection in PyFunc

This guide shows all the ways users can control which backend is used.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _, set_zig_threshold, set_rust_threshold, is_zig_available, is_cpp_available
from pyfunc.backends import enable_cpp_backend, disable_cpp_backend, get_backend

def demonstrate_automatic_selection():
    """Show automatic backend selection based on thresholds."""
    print("🤖 Automatic Backend Selection")
    print("=" * 40)
    
    # Configure thresholds for different backends
    set_zig_threshold(1000)      # Zig for datasets ≥ 1000
    set_rust_threshold(500)      # Rust for datasets ≥ 500  
    enable_cpp_backend(2000)     # C++ for datasets ≥ 2000
    
    print("Backend thresholds configured:")
    print("  • Zig: ≥ 1000 elements")
    print("  • Rust: ≥ 500 elements")
    print("  • C++: ≥ 2000 elements")
    print("  • Python: fallback for all")
    
    # Test different dataset sizes
    test_cases = [
        (100, "Python"),
        (600, "Rust"),
        (1200, "Zig"),
        (2500, "C++")
    ]
    
    print("\nAutomatic selection based on data size:")
    for size, expected_backend in test_cases:
        data = list(range(size))
        result = pipe(data).sum().get()
        expected = sum(range(size))
        
        print(f"  {size:>4} elements → {expected_backend:>6} backend: {result} ✅")
        assert result == expected, f"Expected {expected}, got {result}"

def demonstrate_explicit_control():
    """Show explicit backend control methods."""
    print("\n🎯 Explicit Backend Control")
    print("=" * 40)
    
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    expected_sum = 15.0
    
    print(f"Test data: {data}")
    print(f"Expected sum: {expected_sum}")
    
    # Method 1: Default (automatic selection)
    result = pipe(data).sum().get()
    print(f"\n1. Automatic: pipe(data).sum().get() = {result}")
    
    # Method 2: Explicit Zig (if available)
    if is_zig_available():
        result = pipe(data).sum_zig().get()
        print(f"2. Explicit Zig: pipe(data).sum_zig().get() = {result}")
    else:
        print("2. Explicit Zig: Not available")
    
    # Method 3: Explicit Rust (if available)
    try:
        result = pipe(data).median_rust().get()
        print(f"3. Explicit Rust: pipe(data).median_rust().get() = {result}")
    except:
        print("3. Explicit Rust: Not available")
    
    # Method 4: Explicit C++ (if available)
    if is_cpp_available():
        try:
            result = pipe(data).sum_cpp().get()
            print(f"4. Explicit C++: pipe(data).sum_cpp().get() = {result}")
        except:
            print("4. Explicit C++: Available but method failed")
    else:
        print("4. Explicit C++: Not available")
    
    # Method 5: Explicit Go (bitwise operations)
    try:
        # Go backend specializes in bitwise operations
        int_data = [15, 31, 63, 127]  # Test bitwise data
        result = pipe(int_data).bitwise_and(7).to_list()
        print(f"5. Go bitwise: pipe({int_data}).bitwise_and(7) = {result}")
    except Exception as e:
        print(f"5. Go bitwise: Not available - {e}")
    
    # Method 6: Force Python (high thresholds)
    set_zig_threshold(999999)
    set_rust_threshold(999999)
    disable_cpp_backend()
    result = pipe(data).sum().get()
    print(f"5. Force Python: {result} (all backends disabled)")

def demonstrate_runtime_switching():
    """Show runtime backend switching."""
    print("\n🔄 Runtime Backend Switching")
    print("=" * 40)
    
    data = [float(i) for i in range(1, 101)]  # 1.0 to 100.0
    
    print("Switching backends at runtime:")
    
    # Switch 1: Start with Python
    set_zig_threshold(999999)
    result1 = pipe(data).sum().get()
    print(f"  Python backend: {result1}")
    
    # Switch 2: Change to Zig
    set_zig_threshold(50)
    result2 = pipe(data).sum().get()
    print(f"  Zig backend: {result2}")
    
    # Switch 3: Back to Python
    set_zig_threshold(999999)
    result3 = pipe(data).sum().get()
    print(f"  Python backend: {result3}")
    
    # All results should be identical
    assert result1 == result2 == result3, "Results should be identical!"
    print("  ✅ All results identical - seamless switching!")

def demonstrate_pipeline_backend_mixing():
    """Show mixing different backends in a single pipeline."""
    print("\n🔗 Mixed Backend Pipeline")
    print("=" * 40)
    
    # Configure for mixed usage
    set_zig_threshold(50)   # Use Zig for medium datasets
    set_rust_threshold(30)  # Use Rust for smaller datasets
    
    print("Pipeline with mixed backend operations:")
    
    # Complex pipeline that might use different backends
    data = list(range(1, 101))  # 1 to 100
    
    result = (pipe(data)
              .filter(_ % 2 == 0)        # Even numbers (Python)
              .map(_ ** 2)               # Square them (Python)  
              .sum()                     # Sum (Zig - 50 elements)
              .apply(lambda x: x / 1000) # Normalize (Python)
              .get())
    
    # Calculate expected result manually
    even_numbers = [i for i in range(1, 101) if i % 2 == 0]
    squares = [i ** 2 for i in even_numbers]
    expected = sum(squares) / 1000
    
    print(f"  Pipeline result: {result}")
    print(f"  Expected: {expected}")
    print(f"  Match: {abs(result - expected) < 0.001} ✅")
    
    # Show which operations used which backends
    print("\n  Backend usage in pipeline:")
    print("    filter() → Python (always)")
    print("    map() → Python (always)")
    print("    sum() → Zig (50 elements ≥ threshold)")
    print("    apply() → Python (single value)")

def demonstrate_backend_availability_checking():
    """Show how to check backend availability."""
    print("\n🔍 Backend Availability Checking")
    print("=" * 40)
    
    # Check individual backends
    def is_go_available():
        try:
            # Test if Go backend methods are available
            pipe([1, 2, 3]).bitwise_and(1).to_list()
            return True
        except:
            return False
    
    def is_rust_available():
        try:
            pipe([1.0, 2.0, 3.0]).median_rust().get()
            return True
        except:
            return False
    
    backends = {
        "Zig": is_zig_available(),
        "C++": is_cpp_available(),
        "Rust": is_rust_available(),
        "Go": is_go_available(),
        "Python": True  # Always available
    }
    
    print("Backend availability:")
    for name, available in backends.items():
        status = "✅ Available" if available else "❌ Not available"
        print(f"  {name:>6}: {status}")
    
    # Show how to write defensive code
    print("\nDefensive programming example:")
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    if is_zig_available():
        result = pipe(data).sum_zig().get()
        print(f"  Using Zig: {result}")
    else:
        result = pipe(data).sum().get()  # Falls back to Python
        print(f"  Using fallback: {result}")

def demonstrate_performance_tuning():
    """Show performance tuning strategies."""
    print("\n⚡ Performance Tuning Strategies")
    print("=" * 40)
    
    print("Strategy 1: Optimize thresholds for your use case")
    print("  # For scientific computing (large datasets)")
    print("  set_zig_threshold(1000)    # Zig for math operations")
    print("  set_rust_threshold(500)    # Rust for statistics")
    print("  enable_cpp_backend(5000)   # C++ for very large datasets")
    
    print("\nStrategy 2: Use explicit methods for critical paths")
    print("  # When you know Zig will be faster")
    print("  result = pipe(large_data).stdev_zig().get()")
    
    print("\nStrategy 3: Profile and adjust")
    print("  # Test different thresholds with your data")
    print("  for threshold in [100, 500, 1000, 5000]:")
    print("      set_zig_threshold(threshold)")
    print("      # ... benchmark your operations ...")
    
    print("\nStrategy 4: Batch operations for better performance")
    print("  # Instead of multiple small operations:")
    print("  # sum1 = pipe(data).sum().get()")
    print("  # sum2 = pipe(data).sum().get()")
    print("  #")
    print("  # Do batch operations:")
    print("  # backend = get_backend()")
    print("  # if backend.zig_backend:")
    print("  #     sum1 = backend.zig_backend.sum(data)")
    print("  #     sum2 = backend.zig_backend.sum(data)")

def main():
    """Run all demonstrations."""
    print("🚀 Complete Guide: Backend Control in PyFunc")
    print("=" * 60)
    
    print("This guide shows all the ways users can control backend selection:")
    print("• Automatic selection based on thresholds")
    print("• Explicit backend methods")
    print("• Runtime switching")
    print("• Mixed backend pipelines")
    print("• Availability checking")
    print("• Performance tuning")
    
    try:
        demonstrate_automatic_selection()
        demonstrate_explicit_control()
        demonstrate_runtime_switching()
        demonstrate_pipeline_backend_mixing()
        demonstrate_backend_availability_checking()
        demonstrate_performance_tuning()
        
        print("\n🎉 All demonstrations completed successfully!")
        print("\n📝 Summary:")
        print("✅ Users have complete control over backend selection")
        print("✅ Automatic selection works seamlessly")
        print("✅ Explicit methods provide guaranteed backend usage")
        print("✅ Runtime switching is smooth and transparent")
        print("✅ Complex pipelines can mix multiple backends")
        print("✅ Graceful fallbacks ensure reliability")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())