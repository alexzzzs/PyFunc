# PyFunc Documentation

Complete API reference and usage guide for PyFunc functional programming pipeline with multi-backend performance optimization.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Performance Backends](#performance-backends)
6. [Backend Configuration](#backend-configuration)
7. [API Reference](#api-reference)
8. [Placeholder Syntax](#placeholder-syntax)
9. [Advanced Features](#advanced-features)
10. [Performance Guide](#performance-guide)
11. [Examples](#examples)
12. [Troubleshooting](#troubleshooting)

## Overview

PyFunc is a Python library that brings functional programming fluency to Python, enabling chainable, composable, lazy, and debuggable operations on various data structures. It provides a clean, readable way to transform data using method chaining and placeholder syntax.

### Key Features

- **🔗 Chainable Operations**: Method chaining for readable data transformations
- **🎯 Placeholder Syntax**: Use `_` to create lambda-free expressions
- **⚡ Lazy Evaluation**: Operations are computed only when needed
- **📝 Type Safety**: Full type hints and generic support
- **🔄 Unified Interface**: Works with scalars, iterables, generators, and dictionaries
- **🔧 Extensible**: Register custom types and extend functionality
- **🚀 Multi-Backend Performance**: 5 specialized backends for optimal performance
  - **Python**: Universal compatibility (always available)
  - **C++**: High-performance general operations
  - **Rust**: Memory-safe statistical functions
  - **Go**: Lightning-fast bitwise operations
  - **Zig**: Blazing mathematical computations (up to 236x speedup!)

## Installation

### Basic Installation

```bash
pip install pyfunc-pipeline
```

### Backend-Specific Installation

```bash
# Install with all backends (recommended for maximum performance)
pip install pyfunc-pipeline[all]

# Install specific backends
pip install pyfunc-pipeline[cpp]    # C++ backend
pip install pyfunc-pipeline[zig]    # Zig backend
pip install pyfunc-pipeline[rust]   # Rust backend
pip install pyfunc-pipeline[go]     # Go backend

# Development installation
pip install pyfunc-pipeline[dev]    # Includes testing and development tools
```

### Building Backends from Source

```bash
# Build individual backends
python build_zig.py    # Build Zig backend (requires Zig compiler)
python build_go.py     # Build Go backend (requires Go compiler)
python build_cpp.py    # Build C++ backend (requires C++ compiler)

# Check backend availability
python -c "from pyfunc import is_zig_available, is_go_available; print(f'Zig: {is_zig_available()}, Go: {is_go_available()}')"
```

## Quick Start

```python
from pyfunc import pipe, _

# Basic pipeline
result = pipe([1, 2, 3, 4]).filter(_ > 2).map(_ * 10).to_list()
# Result: [30, 40]

# String processing
result = pipe("hello world").explode(" ").map(_.capitalize()).implode(" ").get()
# Result: "Hello World"

# Function composition
double = _ * 2
square = _ ** 2
composed = double >> square  # square(double(x))

result = pipe(5).apply(composed).get()
# Result: 100
```

### Performance Backends Quick Start

```python
from pyfunc import pipe, _, set_zig_threshold, set_go_threshold

# Configure performance backends
set_zig_threshold(1000)  # Use Zig for math operations ≥ 1000 elements
set_go_threshold(500)    # Use Go for bitwise operations ≥ 500 elements

# Automatic backend selection
large_data = list(range(5000))
result = pipe(large_data).sum().get()  # Uses Zig automatically

# Explicit backend control
result = pipe([1, 2, 3, 4, 5]).sum_zig().get()           # Force Zig
result = pipe([15, 31, 63]).bitwise_and_go(7).to_list()  # Force Go
result = pipe([1, 2, 3, 4, 5]).median_rust().get()      # Force Rust

# Batch operations for maximum performance
from pyfunc.backends import get_backend
backend = get_backend()
if backend.zig_backend:
    stats = backend.zig_backend.batch_statistics([1, 2, 3, 4, 5])
    # Returns: {'sum': 15.0, 'mean': 3.0, 'min': 1.0, 'max': 5.0, 'stdev': 1.414}
```

## Core Concepts

### Pipeline Chaining

Every value can be lifted into a pipeline for transformation:

```python
from pyfunc import pipe, _

# Numbers
pipe([1, 2, 3, 4]).filter(_ > 2).map(_ ** 2).sum().get()
# Result: 25

# Strings
pipe("  hello world  ").apply(_.strip().title()).explode(" ").to_list()
# Result: ['Hello', 'World']

# Dictionaries
pipe({"a": 1, "b": 2}).map_values(_ * 10).get()
# Result: {"a": 10, "b": 20}
```

### Lazy Evaluation

Operations are lazy by default - perfect for large datasets:

```python
# Processes only what's needed from 1 million items
result = pipe(range(1_000_000)).filter(_ > 500_000).take(5).to_list()
```

## Performance Backends

PyFunc features a sophisticated multi-backend system that automatically selects the optimal implementation based on your data and operations.

### Backend Overview

| Backend | Specialization | Performance | Use Cases |
|---|---|---|---|
| **Python** | Universal fallback | Excellent for small data | Always available, prototyping |
| **C++** | General operations | High performance | Large datasets, general computing |
| **Rust** | Statistical functions | Memory-safe performance | Statistical analysis, data science |
| **Go** | Bitwise operations | Lightning-fast bit manipulation | Systems programming, crypto |
| **Zig** | Mathematical operations | Up to 236x speedup | Scientific computing, math-heavy |

### 🐍 Python Backend

**Always Available** - The reliable fallback that works everywhere.

```python
from pyfunc import pipe

# Always uses Python backend
result = pipe([1, 2, 3, 4, 5]).sum().get()
```

**Strengths:**
- Zero dependencies
- Excellent for small datasets (< 1000 elements)
- Leverages Python's optimized built-ins
- Perfect for prototyping

### ⚡ C++ Backend

**High-Performance General Operations** - Mature and battle-tested.

```python
from pyfunc.backends import enable_cpp_backend

# Enable C++ backend for large datasets
enable_cpp_backend(threshold=10000)

# Automatic selection for large data
large_data = list(range(50000))
result = pipe(large_data).map(_ * 2).sum().get()  # Uses C++

# Explicit C++ usage
result = pipe(large_data).sum_cpp().get()
```

**Strengths:**
- Excellent raw performance
- Memory efficient
- Mature pybind11 integration
- Good for general-purpose operations

### 🦀 Rust Backend

**Memory-Safe Statistical Operations** - Zero-cost abstractions for statistics.

```python
from pyfunc import set_rust_threshold

# Configure Rust backend
set_rust_threshold(500)  # Use Rust for datasets ≥ 500 elements

# Automatic selection
result = pipe(range(1000)).median().get()  # Uses Rust

# Explicit Rust usage
result = pipe([1.0, 2.0, 3.0, 4.0, 5.0]).median_rust().get()
result = pipe([1.0, 2.0, 3.0, 4.0, 5.0]).stdev_rust().get()
```

**Strengths:**
- Memory safe with zero-cost abstractions
- Excellent for statistical operations
- Great ecosystem for numerical computing
- Fearless concurrency

### 🔧 Go Backend

**Lightning-Fast Bitwise Operations** - Optimized for bit manipulation.

```python
from pyfunc import set_go_threshold

# Configure Go backend
set_go_threshold(500)  # Use Go for datasets ≥ 500 elements

# Automatic selection for bitwise operations
result = pipe([15, 31, 63, 127]).bitwise_and(7).to_list()  # Uses Go

# Explicit Go usage
result = pipe([15, 31, 63]).bitwise_and_go(7).to_list()
result = pipe([1, 2, 4]).bitwise_or_go(8).to_list()
result = pipe([1, 2, 4]).left_shift_go(2).to_list()
```

**Strengths:**
- Excellent for bitwise operations
- Fast compilation and execution
- Good concurrency support
- Simple deployment

**Available Operations:**
- `bitwise_and()` / `bitwise_and_go()`
- `bitwise_or()` / `bitwise_or_go()`
- `bitwise_xor()` / `bitwise_xor_go()`
- `bitwise_not()` / `bitwise_not_go()`
- `left_shift()` / `left_shift_go()`
- `right_shift()` / `right_shift_go()`

### ⚡ Zig Backend

**Blazing Mathematical Operations** - Up to 236x speedup for complex math!

```python
from pyfunc import set_zig_threshold

# Configure Zig backend
set_zig_threshold(1000)  # Use Zig for datasets ≥ 1000 elements

# Automatic selection
result = pipe(range(5000)).sum().get()  # Uses Zig

# Explicit Zig usage
result = pipe([1.0, 2.0, 3.0, 4.0, 5.0]).sum_zig().get()
result = pipe([1.0, 2.0, 3.0, 4.0, 5.0]).mean_zig().get()
result = pipe([1.0, 2.0, 3.0, 4.0, 5.0]).stdev_zig().get()

# Batch operations (maximum performance)
from pyfunc.backends import get_backend
backend = get_backend()
if backend.zig_backend:
    # Calculate multiple statistics in one FFI call
    stats = backend.zig_backend.batch_statistics([1, 2, 3, 4, 5])
    # Returns: {'sum': 15.0, 'mean': 3.0, 'min': 1.0, 'max': 5.0, 'stdev': 1.414}
    
    # Vector operations
    dot_product = backend.zig_backend.dot_product([1, 2, 3], [4, 5, 6])  # 32.0
    magnitude = backend.zig_backend.vector_magnitude([3, 4])  # 5.0
```

**Strengths:**
- Exceptional performance for mathematical operations
- Memory safe with zero runtime overhead
- Great for complex calculations (236x speedup on standard deviation!)
- Modern language with excellent optimization

**Available Operations:**
- `sum()` / `sum_zig()`
- `mean_zig()`
- `stdev()` / `stdev_zig()`
- `batch_statistics()` - Multiple stats in one call
- `dot_product()` - Vector dot product
- `vector_magnitude()` - Vector length
- `map_multiply()`, `map_add()`, `map_power()` - Vectorized operations

## Backend Configuration

### Automatic Backend Selection

PyFunc automatically selects the optimal backend based on:

1. **Data size** - Larger datasets benefit from compiled backends
2. **Operation type** - Each backend specializes in different operations
3. **Backend availability** - Graceful fallback if backend not installed

```python
from pyfunc import pipe, set_zig_threshold, set_rust_threshold, set_go_threshold
from pyfunc.backends import enable_cpp_backend

# Configure all backends
set_zig_threshold(1000)      # Zig for math operations ≥ 1000 elements
set_rust_threshold(500)      # Rust for statistics ≥ 500 elements
set_go_threshold(300)        # Go for bitwise operations ≥ 300 elements
enable_cpp_backend(2000)     # C++ for general operations ≥ 2000 elements

# Automatic selection examples
pipe([1, 2, 3]).sum().get()                    # Python (small dataset)
pipe(range(600)).median().get()                # Rust (statistics, ≥500)
pipe(range(1200)).sum().get()                  # Zig (math, ≥1000)
pipe(range(2500)).map(_ * 2).sum().get()       # C++ (general, ≥2000)
pipe([15, 31, 63] * 100).bitwise_and(7).to_list()  # Go (bitwise, ≥300)
```

### Explicit Backend Control

Force specific backends when you know what's optimal:

```python
# Force specific backends
result = pipe(data).sum_zig().get()           # Always use Zig
result = pipe(data).median_rust().get()       # Always use Rust
result = pipe(data).bitwise_and_go(7).to_list()  # Always use Go
result = pipe(data).sum_cpp().get()           # Always use C++

# Check backend availability
from pyfunc import is_zig_available, is_go_available, is_cpp_available

if is_zig_available():
    result = pipe(data).sum_zig().get()
else:
    result = pipe(data).sum().get()  # Fallback to Python
```

### Runtime Backend Switching

Change backend configuration at runtime:

```python
from pyfunc import pipe, set_zig_threshold

# Start with Python
set_zig_threshold(999999)  # Very high threshold
result1 = pipe(data).sum().get()  # Uses Python

# Switch to Zig
set_zig_threshold(100)     # Low threshold
result2 = pipe(data).sum().get()  # Uses Zig

# Results are identical, but performance differs
assert result1 == result2
```

### Performance Monitoring

Monitor which backend is being used:

```python
from pyfunc.backends import get_backend

backend = get_backend()

# Check backend availability
print(f"Zig available: {backend.zig_backend is not None}")
print(f"Go available: {backend.go_backend is not None}")
print(f"C++ available: {backend.cpp_backend is not None}")

# Check thresholds
print(f"Zig threshold: {backend.zig_threshold}")
print(f"Go threshold: {backend.go_threshold}")
print(f"Rust threshold: {backend.rust_threshold}")
```

## API Reference

### Core Methods

#### `pipe(value)`
Creates a new pipeline with the given initial value.

```python
pipe(42)           # Scalar pipeline
pipe([1, 2, 3])    # List pipeline
pipe({"a": 1})     # Dictionary pipeline
```

#### `.get()`
Executes the pipeline and returns the result.

```python
pipe(42).apply(_ * 2).get()  # Returns: 84
```

#### `.to_list()`
Executes the pipeline and converts the result to a list.

```python
pipe([1, 2, 3]).map(_ * 2).to_list()  # Returns: [2, 4, 6]
```

#### `.clone()`
Returns a new Pipeline with the same initial value and accumulated function.

```python
p1 = pipe([1, 2, 3])
p2 = p1.clone()
p1.apply(_ + 1) # p2 is not affected
```

### Transformation Methods

#### `.apply(func)` / `.then(func)`
Apply a function to the current value.

```python
pipe(42).apply(_ * 2).get()           # 84
pipe("hello").then(_.upper()).get()   # "HELLO"
```

#### `.map(func)`
Apply a function to each element in an iterable. Supports functions, placeholders, dictionary templates, and string templates.

```python
# Function mapping
pipe([1, 2, 3]).map(_ * 2).to_list()  # [2, 4, 6]
pipe(["a", "b"]).map(_.upper()).to_list()  # ["A", "B"]

# Dictionary template mapping
pipe([{"name": "Alice", "age": 30}]).map({
    "name": _["name"],
    "category": lambda x: "adult" if x["age"] >= 18 else "minor",
    "age_doubled": _["age"] * 2
}).to_list()
# [{"name": "Alice", "category": "adult", "age_doubled": 60}]

# String template mapping
pipe([{"name": "Alice", "score": 95.5}]).map("{name} scored {score:.1f}%").to_list()
# ["Alice scored 95.5%"]
```

#### `.filter(predicate)`
Filter elements based on a predicate.

```python
pipe([1, 2, 3, 4]).filter(_ > 2).to_list()  # [3, 4]
pipe(["", "hello", ""]).filter(_).to_list()  # ["hello"]
```

#### `.reduce(func, initializer=None)`
Reduce the iterable to a single value.

```python
pipe([1, 2, 3, 4]).reduce(_ + _).get()        # 10
pipe([1, 2, 3]).reduce(_ * _, 1).get()        # 6
```

#### `.reduce_right(func, initializer=None)`
Reduce the iterable from right to left.

```python
pipe(["a", "b", "c"]).reduce_right(_ + _).get() # "cba"
```

### String Methods

#### `.explode(delimiter=None)`
Split a string into characters or by delimiter.

```python
pipe("hello").explode().to_list()        # ['h', 'e', 'l', 'l', 'o']
pipe("a,b,c").explode(",").to_list()     # ['a', 'b', 'c']
```

#### `.implode(separator="")`
Join an iterable into a string.

```python
pipe(['h', 'e', 'l', 'l', 'o']).implode().get()     # "hello"
pipe(['a', 'b', 'c']).implode(",").get()            # "a,b,c"
```

#### `.surround(prefix, suffix)`
Wrap a string with prefix and suffix.

```python
pipe("hello").surround("<", ">").get()  # "<hello>"
pipe("content").surround("**", "**").get()  # "**content**"
```

#### `.template_fill(values)`
Fill a template string with values.

```python
pipe("Hello {name}!").template_fill({"name": "World"}).get()
# Result: "Hello World!"
```

### Dictionary Methods

#### `.with_items()`
Convert a dictionary to (key, value) pairs.

```python
pipe({"a": 1, "b": 2}).with_items().to_list()
# Result: [('a', 1), ('b', 2)]
```

#### `.map_keys(func)`
Apply a function to all dictionary keys.

```python
pipe({"a": 1, "b": 2}).map_keys(_.upper()).get()
# Result: {"A": 1, "B": 2}
```

#### `.map_values(func)`
Apply a function to all dictionary values.

```python
pipe({"a": 1, "b": 2}).map_values(_ * 10).get()
# Result: {"a": 10, "b": 20}
```

### Aggregation Methods

#### `.group_by(key)`
Group elements by a key function.

```python
data = [{"name": "Alice", "dept": "Eng"}, {"name": "Bob", "dept": "Sales"}]
pipe(data).group_by(_["dept"]).get()
# Result: {"Eng": [...], "Sales": [...]}
```

#### `.sort(key=None, reverse=False)`
Sort the iterable.

```python
pipe([3, 1, 4, 1, 5]).sort().to_list()                    # [1, 1, 3, 4, 5]
pipe(["apple", "pie"]).sort(key=len).to_list()            # ["pie", "apple"]
```

#### `.unique()`
Remove duplicates while preserving order.

```python
pipe([1, 2, 2, 3, 1]).unique().to_list()  # [1, 2, 3]
```

### Sequence Methods

#### `.take(n)`
Take the first n elements.

```python
pipe([1, 2, 3, 4, 5]).take(3).to_list()  # [1, 2, 3]
```

#### `.skip(n)`
Skip the first n elements.

```python
pipe([1, 2, 3, 4, 5]).skip(2).to_list()  # [3, 4, 5]
```

#### `.take_while(predicate)`
Take elements while predicate is true.

```python
pipe([1, 2, 3, 4, 1]).take_while(_ < 4).to_list()  # [1, 2, 3]
```

#### `.skip_while(predicate)`
Skip elements while predicate is true.

```python
pipe([1, 2, 3, 4, 5]).skip_while(_ < 3).to_list()  # [3, 4, 5]
```

#### `.chunk(size)`
Break sequence into chunks.

```python
pipe([1, 2, 3, 4, 5, 6]).chunk(2).to_list()
# Result: [[1, 2], [3, 4], [5, 6]]
```

#### `.window(size, step=1)`
Create sliding windows.

```python
pipe([1, 2, 3, 4]).window(2).to_list()
# Result: [[1, 2], [2, 3], [3, 4]]
```

#### `.flatten()`
Flatten one level of nesting.

```python
pipe([[1, 2], [3, 4]]).flatten().to_list()  # [1, 2, 3, 4]
```

#### `.flatten_deep()`
Recursively flatten nested iterables.

```python
pipe([[1, [2, 3]], [4, [5]]]).flatten_deep().to_list() # [1, 2, 3, 4, 5]
```

### Statistical Methods

#### `.count()`
Count elements in the iterable.

```python
pipe([1, 2, 3, 4]).count().get()  # 4
```

#### `.sum()`
Sum all elements.

```python
pipe([1, 2, 3, 4]).sum().get()  # 10
```

#### `.min()` / `.max()`
Find minimum/maximum element.

```python
pipe([3, 1, 4, 1, 5]).min().get()  # 1
pipe([3, 1, 4, 1, 5]).max().get()  # 5
```

#### `.first()` / `.last()`
Get first/last element.

```python
pipe([1, 2, 3]).first().get()  # 1
pipe([1, 2, 3]).last().get()   # 3
```

#### `.nth(n)`
Get the nth element (0-indexed).

```python
pipe([10, 20, 30]).nth(1).get()  # 20
```

#### `.median()`
Calculate the median of the elements in an iterable.

```python
pipe([1, 2, 100]).median().get() # 2
```

#### `.stdev()`
Calculate the standard deviation of the elements in an iterable.

```python
pipe([1, 2, 3, 4, 5]).stdev().get() # 1.414...
```

### Conditional Methods

#### `.when(predicate, func)`
Apply function only if predicate is true.

```python
pipe(10).when(_ > 5, _ * 2).get()  # 20
pipe(3).when(_ > 5, _ * 2).get()   # 3
```

#### `.unless(predicate, func)`
Apply function only if predicate is false.

```python
pipe(3).unless(_ > 5, _ * 2).get()   # 6
pipe(10).unless(_ > 5, _ * 2).get()  # 10
```

#### `.if_else(predicate, then_func, else_func)`
Apply different functions based on condition.

```python
pipe(10).if_else(_ > 5, _ * 2, _ + 1).get()  # 20
pipe(3).if_else(_ > 5, _ * 2, _ + 1).get()   # 4
```

### Side Effect Methods

#### `.do(func)` / `.tap(func)`
Apply side effects without changing the value.

```python
pipe([1, 2, 3]).do(print).map(_ * 2).to_list()
# Prints: [1, 2, 3]
# Returns: [2, 4, 6]
```

#### `.debug(label="DEBUG")`
Print current value for debugging.

```python
pipe([1, 2, 3]).debug("Input").map(_ * 2).debug("Output").to_list()
# Prints: Input: [1, 2, 3]
# Prints: Output: <generator object>
# Returns: [2, 4, 6]
```

#### `.trace(label)`
Print with custom label.

```python
pipe(42).trace("Processing").apply(_ * 2).get()
# Prints: TRACE [Processing]: 42
# Returns: 84
```

### Template Mapping

PyFunc supports advanced template mapping for transforming data structures.

#### Dictionary Templates
Transform objects using dictionary templates with placeholders:

```python
orders = [
    {"id": 1, "customer": "Alice", "total": 1200.50},
    {"id": 2, "customer": "Bob", "total": 450.25}
]

result = pipe(orders).map({
    "order_id": _["id"],
    "customer_name": _["customer"],
    "discounted_price": _["total"] * 0.9,
    "category": lambda x: "premium" if x["total"] > 1000 else "standard"
}).to_list()

# Result: [
#   {"order_id": 1, "customer_name": "Alice", "discounted_price": 1080.45, "category": "premium"},
#   {"order_id": 2, "customer_name": "Bob", "discounted_price": 405.23, "category": "standard"}
# ]
```

#### String Templates
Format strings using template syntax:

```python
users = [{"name": "Alice", "score": 95.5}, {"name": "Bob", "score": 87.2}]

result = pipe(users).map("User {name} achieved {score:.1f}% success rate").to_list()
# Result: ["User Alice achieved 95.5% success rate", "User Bob achieved 87.2% success rate"]
```

**⚠️ Important:** Use regular string templates, **not f-strings**:

```python
# ❌ Wrong - Don't use f-strings
.map(f"Order #{_['id']} for {_['customer']}")  # This will cause an error!

# ✅ Correct - Use regular string templates  
.map("Order #{id} for {customer}")  # The template system handles the evaluation
```

#### Combined Template Pipeline
Chain dictionary and string templates for complex transformations:

```python
ecommerce_orders = [
    {"id": 1, "customer": "Alice", "items": ["laptop", "mouse"], "total": 1200.50},
    {"id": 2, "customer": "Bob", "items": ["keyboard"], "total": 75.00},
    {"id": 3, "customer": "Charlie", "items": ["monitor", "stand"], "total": 450.25}
]

result = (pipe(ecommerce_orders)
          .filter(_["total"] > 100)  # Filter orders > $100
          .map({
              "id": _["id"],
              "customer": _["customer"],
              "discounted_total": _["total"] * 0.9  # 10% discount
          })
          .map("Order #{id} for {customer}: ${discounted_total:.2f}")
          .to_list())

# Result: [
#   "Order #1 for Alice: $1080.45",
#   "Order #3 for Charlie: $405.23"
# ]
```

### Advanced Methods

#### `.chain(*others)`
Concatenate with other iterables.

```python
pipe([1, 2]).chain([3, 4], [5, 6]).to_list()  # [1, 2, 3, 4, 5, 6]
```

#### `.zip_with(other)`
Zip with another iterable.

```python
pipe([1, 2, 3]).zip_with(['a', 'b', 'c']).to_list()
# Result: [(1, 'a'), (2, 'b'), (3, 'c')]
```

#### `.product(*iterables)`
Cartesian product.

```python
pipe([1, 2]).product(['a', 'b']).to_list()
# Result: [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

#### `.combinations(r)`
Generate r-length combinations.

```python
pipe([1, 2, 3]).combinations(2).to_list()
# Result: [(1, 2), (1, 3), (2, 3)]
```

### Function Composition

#### Placeholder Composition
Use `>>` and `<<` operators for function composition.

```python
from pyfunc import _

# Forward composition: f >> g means g(f(x))
double = _ * 2
square = _ ** 2
double_then_square = double >> square

pipe(5).apply(double_then_square).get()  # (5 * 2) ** 2 = 100

# Backward composition: f << g means f(g(x))
square_then_double = square << double
pipe(5).apply(square_then_double).get()  # (5 * 2) ** 2 = 100
```

## Examples

### Data Processing Pipeline

```python
from pyfunc import pipe, _

# Process user data
users = [
    {"name": "  Alice  ", "age": 30, "scores": [85, 92, 78]},
    {"name": "BOB", "age": 25, "scores": [90, 88, 95]},
    {"name": "charlie", "age": 35, "scores": [75, 80, 85]},
]

result = (pipe(users)
          .map(lambda user: {
              "name": pipe(user["name"]).apply(_.strip().title()).get(),
              "age": user["age"],
              "avg_score": pipe(user["scores"]).sum().get() / len(user["scores"])
          })
          .filter(lambda user: user["avg_score"] > 80)
          .sort(key=lambda user: user["avg_score"], reverse=True)
          .to_list())

print(result)
# [{'name': 'Bob', 'age': 25, 'avg_score': 91.0}, 
#  {'name': 'Alice', 'age': 30, 'avg_score': 85.0}]
```

### Text Processing

```python
from pyfunc import pipe, _

text = "  The quick brown fox jumps over the lazy dog.  "

result = (pipe(text)
          .apply(_.strip().lower())
          .apply(lambda s: s.replace('.', ''))
          .explode(" ")
          .filter(lambda w: len(w) > 3)
          .unique()
          .sort()
          .implode(" ")
          .surround("✨ ", " ✨")
          .get())

print(result)
# "✨ brown jumps lazy over quick ✨"
```

### E-commerce Order Processing

```python
from pyfunc import pipe, _

orders = [
    {"id": 1, "customer": "Alice", "items": ["laptop", "mouse"], "total": 1200.50},
    {"id": 2, "customer": "Bob", "items": ["keyboard"], "total": 75.00},
    {"id": 3, "customer": "Charlie", "items": ["monitor", "stand"], "total": 450.25},
]

# Generate order confirmations
confirmations = (pipe(orders)
                .filter(lambda order: order["total"] > 100)
                .map(lambda order: 
                     pipe("Order #{id}: ${total:.2f} for {customer}")
                     .template_fill(order)
                     .surround("📧 ", "")
                     .get())
                .to_list())

for confirmation in confirmations:
    print(confirmation)
# 📧 Order #1: $1200.50 for Alice
# 📧 Order #3: $450.25 for Charlie
```

### Log Analysis

```python
from pyfunc import pipe, _

log_lines = [
    "2024-01-01 10:00:00 INFO User login: alice",
    "2024-01-01 10:01:00 ERROR Database connection failed",
    "2024-01-01 10:02:00 INFO User login: bob",
    "2024-01-01 10:03:00 WARN High memory usage",
]

# Extract error and warning messages
issues = (pipe(log_lines)
          .filter(lambda line: "ERROR" in line or "WARN" in line)
          .map(lambda line: pipe(line).explode(" ").skip(3).implode(" ").get())
          .to_list())

print(issues)
# ['Database connection failed', 'High memory usage']
```

## Performance

### Lazy Evaluation

PyFunc uses lazy evaluation by default, meaning operations are only computed when needed:

```python
# This is instant - no computation happens
pipeline = pipe(range(1_000_000)).filter(_ > 500_000).map(_ * 2)

# Only when you materialize the result does computation happen
result = pipeline.take(5).to_list()  # Only processes what's needed
```

### Memory Efficiency

Large datasets are processed efficiently without loading everything into memory:

```python
# Processes 1M items but only keeps 10 in memory
result = pipe(range(1_000_000)).filter(_ % 1000 == 0).take(10).to_list()
```

### Generator Chaining

Operations are chained as generators, allowing for efficient streaming:

```python
def process_large_file(filename):
    return (pipe(open(filename))
            .map(_.strip())
            .filter(_)  # Remove empty lines
            .map(_.split(','))
            .filter(lambda row: len(row) > 3)
            .take(1000)
            .to_list())
```

## Advanced Usage

### Custom Type Registration

Register custom handlers for your own types:

```python
class MyType:
    def __init__(self, value):
        self.value = value

# Register custom handlers
Pipeline.register_custom_type(MyType, {
    "double": lambda obj: MyType(obj.value * 2)
})

# Use with pipeline
result = pipe(MyType(5)).apply(lambda x: x.double()).get()
```

### Extending Pipeline

Add new methods to the Pipeline class:

```python
def custom_method(self, factor):
    return self.apply(lambda x: x * factor)

Pipeline.extend("multiply_by", custom_method)

# Now you can use it
result = pipe(5).multiply_by(3).get()  # 15
```

### Error Handling

Use assertions and error handling in pipelines:

```python
from pyfunc.errors import PipelineError

try:
    result = (pipe([1, 2, 3])
              .filter(_ > 0)
              .map(_ / 0)  # This will raise an error
              .to_list())
except ZeroDivisionError as e:
    print(f"Pipeline error: {e}")
```

### Type Hints

PyFunc supports full type hints:

```python
from typing import List
from pyfunc import pipe, _

def process_numbers(numbers: List[int]) -> List[int]:
    return pipe(numbers).filter(_ > 0).map(_ * 2).to_list()

result: List[int] = process_numbers([1, -2, 3, -4, 5])
```

### Debugging Complex Pipelines

Use debug methods to trace pipeline execution:

```python
result = (pipe([1, 2, 3, 4, 5])
          .debug("Input")
          .filter(_ > 2)
          .debug("After filter")
          .map(_ ** 2)
          .debug("After map")
          .to_list())
```

## Troubleshooting

### Common Issues

#### "TypeError: unsupported format string passed to Placeholder.__format__"

This error occurs when you use f-strings instead of regular string templates:

```python
# ❌ Wrong - This causes the error
pipe(data).map(f"Hello {_{'name'}}")

# ✅ Correct - Use regular string templates
pipe(data).map("Hello {name}")
```

**Why this happens:** F-strings try to evaluate placeholders immediately, but PyFunc's template system needs to evaluate them in the context of each pipeline item.

#### Template Variables Not Found

Make sure your template variables match the keys in your data:

```python
data = [{"user_name": "Alice", "score": 95}]

# ❌ Wrong - 'name' doesn't exist in the data
pipe(data).map("Hello {name}")

# ✅ Correct - Use the actual key name
pipe(data).map("Hello {user_name}")

# ✅ Or transform the data first
pipe(data).map({"name": _["user_name"], "score": _["score"]}).map("Hello {name}")
```

#### Dictionary Template Issues

When using dictionary templates, make sure to use placeholders or lambda functions for dynamic values:

```python
# ❌ Wrong - Static values only
pipe(data).map({"result": "always the same"})

# ✅ Correct - Use placeholders for dynamic values
pipe(data).map({"name": _["name"], "doubled_score": _["score"] * 2})

# ✅ Correct - Use lambda functions for complex logic
pipe(data).map({
    "name": _["name"],
    "grade": lambda x: "A" if x["score"] > 90 else "B"
})
```

### Performance Tips

- Template mapping is optimized for readability over performance
- For high-performance scenarios, consider using regular `.map()` with lambda functions
- Dictionary templates create new dictionaries for each item - use sparingly for large datasets

This comprehensive documentation covers all the features and capabilities of PyFunc. For more examples, see the `examples/` directory in the repository.
