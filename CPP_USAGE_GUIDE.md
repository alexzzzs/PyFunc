# C++ Backend Usage Guide

PyFunc provides multiple ways to control when and how the C++ backend is used for performance-critical operations.

## Backend Control Methods

### 1. Automatic with Threshold (Default)

The C++ backend can be enabled with a size threshold. Operations on data larger than the threshold will automatically use C++ when supported.

```python
from pyfunc import pipe, _, enable_cpp_backend

# Enable C++ for data with 1000+ elements
enable_cpp_backend(threshold=1000)

data = list(range(2000))  # Large enough to trigger C++
result = pipe(data).map(_ * 2).filter(_ > 1000).sum().get()
```

### 2. Force C++ for All Operations

Use C++ for all supported operations regardless of data size.

```python
from pyfunc import pipe, _, use_cpp_backend

# Force C++ for all supported operations
use_cpp_backend()

data = [1, 2, 3, 4, 5]  # Even small data uses C++
result = pipe(data).map(_ * 2).sum().get()
```

### 3. Explicit C++ Methods

Use specific C++ methods when you want explicit control.

```python
from pyfunc import pipe, _, disable_cpp_backend

# Disable automatic C++ usage
disable_cpp_backend()

data = list(range(1000))
result = (pipe(data)
         .map_cpp(_ * 2)      # Explicitly use C++ for map
         .filter_cpp(_ > 500) # Explicitly use C++ for filter
         .sum_cpp()           # Explicitly use C++ for sum
         .get())
```

### 4. Mixed Usage

Combine Python and C++ operations as needed.

```python
from pyfunc import pipe, _

data = list(range(1000))
result = (pipe(data)
         .map(_ * 2)          # Python (or automatic C++)
         .filter_cpp(_ > 500) # Explicitly C++
         .take(100)           # Python (not supported in C++)
         .sum()               # Python (or automatic C++)
         .get())
```

## Available C++ Methods

| Python Method | C++ Explicit Method | Description |
|---------------|-------------------|-------------|
| `map(func)` | `map_cpp(func)` | Apply function to each element |
| `filter(pred)` | `filter_cpp(pred)` | Filter elements by predicate |
| `sum()` | `sum_cpp()` | Sum all elements |
| `reduce(func)` | `reduce_cpp(func)` | Reduce with binary function |

## Supported Operations

The C++ backend currently supports:

- **Map operations**: `_ * n`, `_ + n`, `_ - n`, `_ / n`
- **Filter operations**: `_ > n`, `_ < n`, `_ >= n`, `_ <= n`, `_ == n`, `_ != n`
- **Aggregations**: `sum()`, `min()`, `max()`, `count()`
- **Reduce operations**: Binary operations with placeholders

## Data Type Support

- **Supported**: Lists and tuples of numeric types (int, float)
- **Not supported**: Strings, bytes, complex objects, mixed types

## Performance Guidelines

### When to Use C++

✅ **Good candidates for C++:**
- Large datasets (1000+ elements)
- Simple numeric operations
- Computation-heavy pipelines
- Performance-critical code

❌ **Not ideal for C++:**
- Small datasets (< 100 elements)
- Complex object manipulations
- String processing
- One-off operations

### Example Performance Comparison

```python
import time
from pyfunc import pipe, _, enable_cpp_backend, disable_cpp_backend

data = list(range(100000))

# Python backend
disable_cpp_backend()
start = time.time()
python_result = pipe(data).map(_ * 2).filter(_ > 50000).sum().get()
python_time = time.time() - start

# C++ backend
enable_cpp_backend(threshold=1000)
start = time.time()
cpp_result = pipe(data).map(_ * 2).filter(_ > 50000).sum().get()
cpp_time = time.time() - start

print(f"Python: {python_time:.4f}s")
print(f"C++: {cpp_time:.4f}s")
print(f"Speedup: {python_time/cpp_time:.2f}x")
```

## Error Handling

When using explicit C++ methods, errors will be raised if:
- C++ backend is not available
- Operation is not supported
- Data type is incompatible

```python
from pyfunc import pipe, _, disable_cpp_backend

disable_cpp_backend()

try:
    result = pipe([1, 2, 3]).map_cpp(_ * 2).get()
except Exception as e:
    print(f"Error: {e}")
    # Fallback to Python
    result = pipe([1, 2, 3]).map(_ * 2).to_list()
```

## Best Practices

1. **Start with Python**: Use the default Python backend for development and small datasets
2. **Profile first**: Measure performance before optimizing with C++
3. **Use thresholds**: Enable automatic C++ with appropriate thresholds for production
4. **Explicit when needed**: Use explicit C++ methods for performance-critical sections
5. **Handle errors**: Always have fallback strategies for C++ failures
6. **Test both backends**: Ensure your code works with both Python and C++ backends

## Installation

To use the C++ backend, you need to build the extension:

```bash
# Install build dependencies
pip install pybind11

# Build the C++ extension
python setup.py build_ext --inplace

# Or install with C++ support
pip install pyfunc-pipeline[cpp]
```

## Checking Availability

```python
from pyfunc import is_cpp_available

if is_cpp_available():
    print("C++ backend is available")
else:
    print("C++ backend not available - using Python only")
```