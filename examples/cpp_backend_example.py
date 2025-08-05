#!/usr/bin/env python3
"""
C++ Backend Example for PyFunc

This example demonstrates the C++ backend acceleration for computation-heavy operations.
"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _
from pyfunc.backends import enable_cpp_backend, disable_cpp_backend, is_cpp_available

def benchmark_operation(name, operation, data_size=100000):
    """Benchmark an operation with and without C++ backend."""
    print(f"\n🔬 Benchmarking {name} (n={data_size:,})")
    
    # Generate test data
    data = list(range(data_size))
    
    # Test with Python backend
    disable_cpp_backend()
    start_time = time.time()
    python_result = operation(data)
    python_time = time.time() - start_time
    
    # Test with C++ backend (if available)
    if is_cpp_available():
        enable_cpp_backend(threshold=1000)  # Low threshold for testing
        start_time = time.time()
        cpp_result = operation(data)
        cpp_time = time.time() - start_time
        
        # Verify results are the same
        if isinstance(python_result, list) and isinstance(cpp_result, list):
            results_match = python_result == cpp_result
        else:
            results_match = abs(python_result - cpp_result) < 1e-10
        
        speedup = python_time / cpp_time if cpp_time > 0 else float('inf')
        
        print(f"   🐍 Python: {python_time:.4f}s")
        print(f"   ⚡ C++:    {cpp_time:.4f}s")
        print(f"   🚀 Speedup: {speedup:.2f}x")
        print(f"   ✅ Results match: {results_match}")
        
        return speedup
    else:
        print(f"   🐍 Python: {python_time:.4f}s")
        print(f"   ❌ C++ backend not available")
        return 1.0

def main():
    print("🚀 PyFunc C++ Backend Performance Demo")
    print("=" * 50)
    
    # Check if C++ backend is available
    if is_cpp_available():
        print("✅ C++ backend is available!")
        enable_cpp_backend(threshold=10000)
    else:
        print("❌ C++ backend not available")
        print("   To enable: pip install pyfunc-pipeline[cpp]")
        print("   Or build from source with: PYFUNC_BUILD_CPP=1 pip install -e .")
    
    # Test data sizes
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        print(f"\n{'='*20} Data Size: {size:,} {'='*20}")
        
        # Test map operations
        speedups = []
        
        # Map with multiplication
        speedup = benchmark_operation(
            "Map (_ * 2)",
            lambda data: pipe(data).map(_ * 2).to_list(),
            size
        )
        speedups.append(speedup)
        
        # Map with addition
        speedup = benchmark_operation(
            "Map (_ + 10)",
            lambda data: pipe(data).map(_ + 10).to_list(),
            size
        )
        speedups.append(speedup)
        
        # Filter operations
        speedup = benchmark_operation(
            "Filter (_ > 5000)",
            lambda data: pipe(data).filter(_ > size//2).to_list(),
            size
        )
        speedups.append(speedup)
        
        # Sum operation
        speedup = benchmark_operation(
            "Sum",
            lambda data: pipe(data).sum().get(),
            size
        )
        speedups.append(speedup)
        
        # Combined operations
        speedup = benchmark_operation(
            "Combined (map + filter + sum)",
            lambda data: pipe(data).map(_ * 2).filter(_ > size).sum().get(),
            size
        )
        speedups.append(speedup)
        
        if is_cpp_available():
            avg_speedup = sum(speedups) / len(speedups)
            print(f"\n   📊 Average speedup: {avg_speedup:.2f}x")
    
    # Real-world example
    print(f"\n{'='*20} Real-World Example {'='*20}")
    
    # Financial data processing
    print("\n💰 Financial Data Processing")
    
    # Generate sample financial data
    prices = [100 + i * 0.1 + (i % 10) * 2 for i in range(50000)]
    
    def process_financial_data(prices):
        return (pipe(prices)
                .map(_ * 1.02)  # Apply 2% growth
                .filter(_ > 150)  # Filter high-value stocks
                .map(_ * 0.95)  # Apply 5% discount
                .sum()  # Total portfolio value
                .get())
    
    benchmark_operation(
        "Financial Pipeline",
        process_financial_data,
        len(prices)
    )
    
    # Scientific computation
    print("\n🔬 Scientific Computation")
    
    def scientific_computation(data):
        return (pipe(data)
                .map(_ ** 2)  # Square each value
                .filter(_ > 1000)  # Filter significant values
                .map(_ / 100)  # Normalize
                .sum()  # Total energy
                .get())
    
    benchmark_operation(
        "Scientific Pipeline",
        lambda data: scientific_computation(data),
        50000
    )
    
    print(f"\n🎉 Performance testing completed!")
    
    if is_cpp_available():
        print("\n💡 Tips for maximum performance:")
        print("• Use simple arithmetic operations (_ * 2, _ + 5)")
        print("• Use simple comparisons (_ > 10, _ <= 100)")
        print("• Process large datasets (>10,000 elements)")
        print("• Chain operations for compound speedups")
    else:
        print("\n🔧 To enable C++ acceleration:")
        print("1. Install with C++ support: pip install pyfunc-pipeline[cpp]")
        print("2. Or build from source: PYFUNC_BUILD_CPP=1 pip install -e .")
        print("3. Requires: C++ compiler, pybind11")

if __name__ == "__main__":
    main()