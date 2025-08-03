from pyfunc import pipe, _

# Example 1: Chaining operations with pipe and _
result1 = pipe([1, 2, 3, 4])     .filter(_ > 2)     .map(_ * 10)     .get()

print(f"Example 1 Result: {result1}")

# Example 2: Scalar operations
result2 = pipe(10)     .apply(_ * 2)     .apply(str)     .get()

print(f"Example 2 Result: {result2}")

# Example 3: String manipulation
result3 = pipe("  Hello World  ")     .apply(str.strip)     .apply(str.lower)     .get()

print(f"Example 3 Result: {result3}")
