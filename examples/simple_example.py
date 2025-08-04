import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _

# Example 1: Chaining operations with pipe and _
result1 = pipe([1, 2, 3, 4]).filter(_ > 2).map(_ * 10).to_list()

print(f"Example 1 Result: {result1}")

# Example 2: Scalar operations
result2 = pipe(10).apply(_ * 2).apply(str).get()

print(f"Example 2 Result: {result2}")

# Example 3: String manipulation
result3 = pipe("  Hello World  ").apply(str.strip).apply(str.lower).get()

print(f"Example 3 Result: {result3}")

# Example 4: New string methods
result4 = pipe("hello world").explode(" ").map(_.capitalize()).implode(" ").get()

print(f"Example 4 Result (explode/implode): {result4}")

# Example 5: Dictionary operations
data = {"name": "alice", "age": 30, "city": "new york"}
result5 = pipe(data).map_values(lambda v: v.title() if isinstance(v, str) else v).get()

print(f"Example 5 Result (map_values): {result5}")

# Example 6: Function composition
double = _ * 2
square = _ ** 2
composed = double >> square  # square(double(x))

result6 = pipe(5).apply(composed).get()
print(f"Example 6 Result (composition): {result6}")

# Example 7: Side effects with debugging
result7 = pipe([1, 2, 3, 4]).debug("Input").filter(_ > 2).debug("After filter").map(_ * 10).to_list()
print(f"Example 7 Result (with debug): {result7}")
