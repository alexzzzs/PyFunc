import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import Pipeline, square, increment, half, Placeholder

# User-defined placeholder instance
_ = Placeholder()

# Example 1: Numeric transformations
pipeline = Pipeline([1, 2, 3, 4, 5])
result = (
    pipeline
    .map(square)
    .filter(lambda x: x > 10)
    .map(half)
    .get()
)
print("Example 1 Result:", result)

# Example 2: String processing
text_pipeline = Pipeline("  Hello World!  ")
result = (
    text_pipeline
    .apply(str.strip)
    .apply(str.lower)
    .apply(lambda s: s.replace("!", ""))
    .explode(" ")
    .unique()
    .sort()
    .implode(" ")
    .get()
)
print("Example 2 Result:", result)

# Example 3: Dictionary aggregation
data = {
    "alice": [10, 20, 30],
    "bob": [5, 15, 25],
    "carol": [7, 14, 21]
}
result = (
    Pipeline(data)
    .with_items()
    .starmap(lambda name, scores: (name, sum(scores)))
    .filter(lambda pair: pair[1] > 30)
    .sort(key=lambda pair: pair[1], reverse=True)
    .get()
)
print("Example 3 Result:", result)

# Example 4: Using Placeholder for numeric transformations
pipeline = Pipeline([1, 2, 3, 4, 5])
result = (
    pipeline
    .map(_ * 2)  # Double each number
    .filter(_ > 5)  # Keep numbers greater than 5
    .map(_ + 1)  # Increment each remaining number
    .get()
)
print("Example 4 Result (Placeholder with numbers):", result)

# Example 5: Using Placeholder for string processing
text_pipeline = Pipeline(["  Hello  ", "  World!  "])
result = (
    text_pipeline
    .map(_.strip().lower())  # Strip whitespace and convert to lowercase
    .map(_.replace("!", ""))  # Remove exclamation marks
    .get()
)
print("Example 5 Result (Placeholder with strings):", result)

# Example 6: Using Placeholder for dictionary operations
data = {"a": 1, "b": 2, "c": 3}
result = (
    Pipeline(data)
    .with_items()
    .map((_[0], _[1] * 2))  # Double the values in the dictionary
    .get()
)
print("Example 6 Result (Placeholder with dictionary):", result)
