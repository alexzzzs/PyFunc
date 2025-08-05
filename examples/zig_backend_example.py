#!/usr/bin/env python3
"""
Zig Backend Example for PyFunc

This example demonstrates the Zig backend for high-performance mathematical operations.
"""

import sys
import os
import time
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _, set_zig_threshold
from pyfunc.backends import is_zig_available

def benchmark_operation(name, operation, data_size=50000):
    """Benchmark an operation with and without Zig backend."""
    print(f"\n🔬 Benchmarking {name} (n={data_size:,})")
    
    # Generate test data
    data = [random.uniform(1.0, 100.0) for _ in range(data_size)]
    
    # Test with Python backend (disable Zig)
    set_zig_threshold(999999)  # Very high threshold
    start_time = time.time()
    python_result = operation(data)
    python_time = time.time() - start_time
    
    # Test with Zig backend (if available)
    if is_zig_available():
        set_zig_threshold(1000)  # Low threshold for testing
        start_time = time.time()
        zig_result = operation(data)
        zig_time = time.time() - start_time
        
        # Verify results are close (floating point precision)
        if isinstance(python_result, (int, float)) and isinstance(zig_result, (int, float)):
            results_match = abs(python_result - zig_result) < 1e-6
        else:
            results_match = python_result == zig_result
        
        speedup = python_time / zig_time if zig_time > 0 else float('inf')
        
        print(f"   🐍 Python: {python_time:.4f}s")
        print(f"   ⚡ Zig:    {zig_time:.4f}s")
        print(f"   🚀 Speedup: {speedup:.2f}x")
        print(f"   ✅ Results match: {results_match}")
        
        return speedup
    else:
        print(f"   🐍 Python: {python_time:.4f}s")
        print(f"   ❌ Zig backend not available")
        return 1.0

def demonstrate_zig_specializations():
    """Demonstrate Zig backend specializations."""
    print("\n⚡ Zig Backend Specializations")
    print("=" * 40)
    
    if not is_zig_available():
        print("❌ Zig backend not available")
        print("   Build with: python build_zig.py")
        return
    
    # Mathematical operations
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    
    print("📊 Basic Mathematical Operations:")
    print(f"   Data: {data}")
    
    # Sum
    result = pipe(data).sum_zig().get()
    print(f"   Sum (Zig): {result}")
    
    # Mean
    result = pipe(data).mean_zig().get()
    print(f"   Mean (Zig): {result}")
    
    # Standard deviation
    result = pipe(data).stdev_zig().get()
    print(f"   Std Dev (Zig): {result:.4f}")
    
    # Vector operations (if we add them to pipeline)
    print("\n🔢 Advanced Mathematical Operations:")
    
    # Demonstrate explicit Zig usage
    try:
        from pyfunc.backends import get_backend
        backend = get_backend()
        
        if backend.zig_backend:
            # Dot product
            vec_a = [1.0, 2.0, 3.0]
            vec_b = [4.0, 5.0, 6.0]
            dot_result = backend.zig_backend.dot_product(vec_a, vec_b)
            print(f"   Dot product {vec_a} · {vec_b} = {dot_result}")
            
            # Vector magnitude
            magnitude = backend.zig_backend.vector_magnitude(vec_a)
            print(f"   Magnitude of {vec_a} = {magnitude:.4f}")
            
            # Map operations
            original = [1.0, 2.0, 3.0, 4.0, 5.0]
            multiplied = backend.zig_backend.map_multiply(original.copy(), 2.0)
            print(f"   Map multiply by 2: {original} → {multiplied}")
            
            powered = backend.zig_backend.map_power([2.0, 3.0, 4.0], 2.0)
            print(f"   Map power of 2: [2, 3, 4] → {powered}")
    
    except Exception as e:
        print(f"   ⚠️  Advanced operations error: {e}")

def performance_comparison():
    """Compare performance across different data sizes."""
    print("\n📈 Performance Scaling Analysis")
    print("=" * 40)
    
    if not is_zig_available():
        print("❌ Zig backend not available for performance testing")
        return
    
    sizes = [1000, 5000, 10000, 50000, 100000]
    
    for size in sizes:
        print(f"\n📊 Dataset size: {size:,}")
        
        speedups = []
        
        # Sum operation
        speedup = benchmark_operation(
            "Sum",
            lambda data: pipe(data).sum().get(),
            size
        )
        speedups.append(speedup)
        
        # Mean operation (if available)
        try:
            speedup = benchmark_operation(
                "Mean (explicit Zig)",
                lambda data: pipe(data).mean_zig().get(),
                size
            )
            speedups.append(speedup)
        except:
            pass
        
        if speedups:
            avg_speedup = sum(speedups) / len(speedups)
            print(f"   📊 Average speedup: {avg_speedup:.2f}x")

def real_world_example():
    """Real-world mathematical computation example."""
    print("\n🌍 Real-World Example: Financial Analysis")
    print("=" * 50)
    
    # Generate sample financial data
    print("📈 Analyzing stock price data...")
    
    # Simulate daily stock prices for a year
    base_price = 100.0
    prices = []
    
    for day in range(365):
        # Simulate price movement with some randomness
        change = random.uniform(-0.05, 0.05)  # ±5% daily change
        base_price *= (1 + change)
        prices.append(base_price)
    
    print(f"   Generated {len(prices)} daily prices")
    print(f"   Starting price: ${prices[0]:.2f}")
    print(f"   Ending price: ${prices[-1]:.2f}")
    
    # Perform financial analysis
    set_zig_threshold(100)  # Use Zig for datasets > 100
    
    start_time = time.time()
    
    analysis = {
        "mean_price": pipe(prices).sum().get() / len(prices),
        "max_price": pipe(prices).max().get(),
        "min_price": pipe(prices).min().get(),
        "volatility": pipe(prices).stdev().get(),
        "total_return": (prices[-1] - prices[0]) / prices[0] * 100
    }
    
    analysis_time = time.time() - start_time
    
    print(f"\n📊 Financial Analysis Results:")
    print(f"   Mean Price: ${analysis['mean_price']:.2f}")
    print(f"   Max Price: ${analysis['max_price']:.2f}")
    print(f"   Min Price: ${analysis['min_price']:.2f}")
    print(f"   Volatility (σ): ${analysis['volatility']:.2f}")
    print(f"   Total Return: {analysis['total_return']:.2f}%")
    print(f"   Analysis Time: {analysis_time:.4f}s")
    
    backend_used = "Zig" if is_zig_available() and len(prices) >= 100 else "Python"
    print(f"   Backend Used: {backend_used}")

def main():
    """Run all Zig backend demonstrations."""
    print("🚀 PyFunc Zig Backend Performance Demo")
    print("=" * 50)
    
    # Check if Zig backend is available
    if is_zig_available():
        print("✅ Zig backend is available!")
        set_zig_threshold(5000)  # Default threshold
    else:
        print("❌ Zig backend not available")
        print("   To enable: python build_zig.py")
        print("   Continuing with Python backend only...")
    
    demonstrate_zig_specializations()
    performance_comparison()
    real_world_example()
    
    print(f"\n🎉 Zig backend demonstration completed!")
    
    if is_zig_available():
        print("\n💡 Tips for maximum Zig performance:")
        print("• Use for mathematical operations (sum, mean, stdev)")
        print("• Best for medium to large datasets (5,000+ elements)")
        print("• Excellent for vector operations and linear algebra")
        print("• Use explicit _zig() methods for guaranteed Zig usage")
    else:
        print("\n🔧 To enable Zig acceleration:")
        print("1. Install Zig: https://ziglang.org/download/")
        print("2. Build backend: python build_zig.py")
        print("3. Enjoy blazing fast mathematical operations!")

if __name__ == "__main__":
    main()