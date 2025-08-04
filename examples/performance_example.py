#!/usr/bin/env python3
"""Performance example demonstrating lazy evaluation in PyFunc."""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _

def slow_operation(x):
    """Simulate a slow operation."""
    time.sleep(0.001)  # 1ms delay
    return x * 2

def main():
    print("🚀 PyFunc Performance Examples")
    print("=" * 40)
    
    # 1. Lazy Evaluation Demo
    print("\n1. Lazy Evaluation")
    print("Building pipeline (should be instant)...")
    
    start_time = time.time()
    # This creates the pipeline but doesn't execute anything
    pipeline = pipe(range(1000)).filter(_ > 500).map(slow_operation).take(5)
    build_time = time.time() - start_time
    
    print(f"   Pipeline built in: {build_time:.4f}s")
    
    print("Executing pipeline...")
    start_time = time.time()
    result = pipeline.to_list()
    execution_time = time.time() - start_time
    
    print(f"   Pipeline executed in: {execution_time:.4f}s")
    print(f"   Result: {result}")
    print(f"   ✅ Only processed {len(result)} items due to lazy evaluation")
    
    # 2. Memory Efficiency
    print("\n2. Memory Efficiency")
    print("Processing 1 million items...")
    
    start_time = time.time()
    # This processes 1M items but only keeps what's needed in memory
    result = pipe(range(1_000_000)).filter(_ % 10000 == 0).take(10).to_list()
    execution_time = time.time() - start_time
    
    print(f"   Processed in: {execution_time:.4f}s")
    print(f"   Result: {result}")
    print(f"   ✅ Memory efficient - only materialized final result")
    
    # 3. Generator Chaining
    print("\n3. Generator Chaining")
    print("Chaining multiple operations...")
    
    call_count = 0
    def counting_double(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # Reset counter
    call_count = 0
    
    result = pipe(range(100)).map(counting_double).filter(_ > 50).take(5).to_list()
    
    print(f"   Function called: {call_count} times")
    print(f"   Result length: {len(result)}")
    print(f"   ✅ Efficient generator chaining - function called only as needed")
    
    # 4. Complex Pipeline Performance
    print("\n4. Complex Pipeline")
    print("Processing complex data transformation...")
    
    # Generate sample data
    data = [
        {"name": f"User{i}", "scores": [i*10, i*11, i*12], "active": i % 2 == 0}
        for i in range(1000)
    ]
    
    start_time = time.time()
    result = (pipe(data)
              .filter(_["active"])
              .map(lambda user: {
                  **user,
                  "avg_score": pipe(user["scores"]).sum().get() / len(user["scores"])
              })
              .filter(lambda user: user["avg_score"] > 100)
              .sort(key=lambda user: user["avg_score"], reverse=True)
              .take(10)
              .to_list())
    
    execution_time = time.time() - start_time
    
    print(f"   Processed {len(data)} records in: {execution_time:.4f}s")
    print(f"   Top performer: {result[0]['name']} (avg: {result[0]['avg_score']:.1f})")
    print(f"   ✅ Efficient complex transformations")
    
    # 5. String Processing Performance
    print("\n5. String Processing")
    print("Processing large text...")
    
    # Generate large text
    words = ["hello", "world", "python", "functional", "programming"] * 1000
    text = " ".join(words)
    
    start_time = time.time()
    result = (pipe(text)
              .explode(" ")
              .filter(lambda w: len(w) > 5)
              .map(_.capitalize())
              .unique()
              .sort()
              .take(5)
              .to_list())
    
    execution_time = time.time() - start_time
    
    print(f"   Processed text with {len(words)} words in: {execution_time:.4f}s")
    print(f"   Unique long words: {result}")
    print(f"   ✅ Efficient string processing with lazy evaluation")
    
    print("\n🎉 All performance examples completed!")
    print("\nKey Takeaways:")
    print("• Pipeline building is instant (lazy evaluation)")
    print("• Only necessary computations are performed")
    print("• Memory usage stays low even with large datasets")
    print("• Generator chaining enables efficient streaming")

if __name__ == "__main__":
    main()