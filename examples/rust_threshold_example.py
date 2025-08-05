#!/usr/bin/env python3
"""
Rust Backend Threshold Example for PyFunc

This example demonstrates how Rust backend is only used when beneficial,
avoiding overhead for small datasets.
"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _, set_rust_threshold

def benchmark_rust_threshold():
    """Demonstrate Rust threshold behavior."""
    print("🦀 Rust Backend Threshold Demo")
    print("=" * 40)
    
    # Test different data sizes
    sizes = [10, 100, 500, 1000, 5000, 10000]
    
    for size in sizes:
        data = [float(i) for i in range(size)]
        
        print(f"\n📊 Dataset size: {size}")
        
        # Time the median calculation
        start_time = time.time()
        result = pipe(data).median().get()
        execution_time = time.time() - start_time
        
        # Determine which backend was likely used
        backend_used = "🦀 Rust" if size >= 1000 else "🐍 Python"
        
        print(f"   Result: {result:.2f}")
        print(f"   Time: {execution_time:.4f}s")
        print(f"   Backend: {backend_used}")
    
    print(f"\n💡 Default threshold: 1000 elements")
    print(f"   • Small datasets (< 1000): Use Python (avoid overhead)")
    print(f"   • Large datasets (≥ 1000): Use Rust (performance benefit)")

def demonstrate_threshold_configuration():
    """Show how to configure Rust threshold."""
    print(f"\n🔧 Configuring Rust Threshold")
    print("=" * 40)
    
    # Test data
    data = [float(i) for i in range(800)]  # 800 elements
    
    # Default threshold (1000) - should use Python
    print(f"\n1. Default threshold (1000):")
    result = pipe(data).median().get()
    print(f"   Dataset: 800 elements → 🐍 Python backend")
    print(f"   Result: {result:.2f}")
    
    # Lower threshold (500) - should use Rust
    print(f"\n2. Lower threshold (500):")
    set_rust_threshold(500)
    result = pipe(data).median().get()
    print(f"   Dataset: 800 elements → 🦀 Rust backend")
    print(f"   Result: {result:.2f}")
    
    # Higher threshold (2000) - should use Python
    print(f"\n3. Higher threshold (2000):")
    set_rust_threshold(2000)
    result = pipe(data).median().get()
    print(f"   Dataset: 800 elements → 🐍 Python backend")
    print(f"   Result: {result:.2f}")
    
    # Reset to default
    set_rust_threshold(1000)
    print(f"\n✅ Threshold reset to default (1000)")

def show_explicit_rust_usage():
    """Show explicit Rust backend usage."""
    print(f"\n🎯 Explicit Rust Usage")
    print("=" * 40)
    
    data = [1.0, 2.0, 3.0, 4.0, 5.0]  # Small dataset
    
    # Automatic (will use Python due to small size)
    print(f"\n1. Automatic backend selection:")
    result = pipe(data).median().get()
    print(f"   pipe(data).median() → 🐍 Python (small dataset)")
    print(f"   Result: {result}")
    
    # Explicit Rust (forces Rust even for small data)
    print(f"\n2. Explicit Rust backend:")
    try:
        result = pipe(data).median_rust().get()
        print(f"   pipe(data).median_rust() → 🦀 Rust (forced)")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ❌ Rust backend not available: {e}")
    
    print(f"\n💡 Use explicit methods only when you know Rust will be faster")

def main():
    print("🚀 PyFunc Rust Backend Threshold Management")
    print("=" * 50)
    
    benchmark_rust_threshold()
    demonstrate_threshold_configuration()
    show_explicit_rust_usage()
    
    print(f"\n🎉 Demo completed!")
    print(f"\n📝 Key Takeaways:")
    print(f"• Rust has overhead for small datasets")
    print(f"• Default threshold (1000) balances performance vs overhead")
    print(f"• Configure threshold based on your use case")
    print(f"• Use explicit _rust() methods only when needed")
    print(f"• Python fallback ensures reliability")

if __name__ == "__main__":
    main()