# PyFunc C++ Backend

The PyFunc C++ backend provides significant performance improvements for computation-heavy operations while maintaining full API compatibility.

## 🚀 Quick Start

### Installation

```bash
# Install with C++ support
pip install pyfunc-pipeline[cpp]

# Or build from source
git clone https://github.com/alexzzzs/PyFunc.git
cd PyFunc
PYFUNC_BUILD_CPP=1 pip install -e .
```

### Basic Usage

```python
from pyfunc import pipe, _, enable_cpp_backend

# Enable C++ acceleration
enable_cpp_backend()

# Same API, faster execution for large datasets
result = pipe(range(100000)).map(_ * 2).filter(_ > 50000).sum().get()
```

## 🎯 Supported Operations

### Map Operations
- **Arithmetic**: `_ * 2`, `_ + 10`, `_ - 5`, `_ / 3`
- **Automatic detection**: C++ backend activates for simple arithmetic operations

```python
# These operations are accelerated
pipe(data).map(_ * 2)      # Multiplication
pipe(data).map(_ + 100)    # Addition  
pipe(data).map(_ - 50)     # Subtraction
pipe(data).map(_ / 4)      # Division
```

### Filter Operations
- **Comparisons**: `_ > 10`, `_ < 100`, `_ >= 50`, `_ <= 200`, `_ == 42`, `_ != 0`

```python
# These operations are accelerated
pipe(data).filter(_ > 1000)    # Greater than
pipe(data).filter(_ <= 500)    # Less than or equal
pipe(data).filter(_ == 42)     # Equality
```

### Aggregation Operations
- **Sum**: `sum()` - Fast parallel summation
- **Min/Max**: `min()`, `max()` - Optimized finding
- **Count**: `count()` - Element counting

```python
# These operations are accelerated
pipe(data).sum()     # Fast summation
pipe(data).min()     # Minimum value
pipe(data).max()     # Maximum value
pipe(data).count()   # Element count
```

## ⚙️ Configuration

### Enable/Disable Backend

```python
from pyfunc import enable_cpp_backend, disable_cpp_backend, is_cpp_available

# Check availability
if is_cpp_available():
    print("C++ backend available!")

# Enable with custom threshold
enable_cpp_backend(threshold=5000)  # Use C++ for datasets > 5000 elements

# Disable C++ backend
disable_cpp_backend()  # Use Python only
```

### Automatic Fallback

The backend automatically falls back to Python for:
- Unsupported operations
- Non-numeric data
- Complex placeholders
- Small datasets (below threshold)

```python
# These automatically use Python backend
pipe(strings).map(_.upper())           # String operations
pipe(dicts).map(_["key"])              # Dictionary access
pipe(data).map(lambda x: x ** 2.5)     # Complex functions
pipe(small_data).map(_ * 2)            # Below threshold
```

## 📊 Performance

### Benchmarks

Typical performance improvements on large datasets (100k+ elements):

| Operation | Speedup |
|-----------|---------|
| `map(_ * 2)` | 5-15x |
| `filter(_ > 1000)` | 3-8x |
| `sum()` | 10-25x |
| Combined pipeline | 8-20x |

### Real-World Example

```python
# Financial data processing
prices = list(range(1000000))

# This pipeline gets significant acceleration
result = (pipe(prices)
          .map(_ * 1.02)      # Apply growth rate
          .filter(_ > 500000) # Filter high values  
          .map(_ * 0.95)      # Apply discount
          .sum()              # Total value
          .get())
```

## 🔧 Building from Source

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# macOS
xcode-select --install

# Windows
# Install Visual Studio Build Tools
```

### Build Steps

```bash
# Clone repository
git clone https://github.com/alexzzzs/PyFunc.git
cd PyFunc

# Install dependencies
pip install pybind11

# Build C++ extension
python build_cpp.py

# Or use setup.py directly
PYFUNC_BUILD_CPP=1 python setup.py build_ext --inplace

# Test the build
python examples/cpp_backend_example.py
```

## 🧪 Testing

```bash
# Run C++ backend tests
python -m pytest tests/test_cpp_backend.py

# Run performance benchmarks
python examples/cpp_backend_example.py

# Run all tests
python -m pytest tests/
```

## 🔍 How It Works

### Architecture

```
Python API Layer
       ↓
Backend Selector
    ↙        ↘
Python     C++ Backend
Backend    (pyfunc_native)
    ↓           ↓
Original   Optimized C++
Python     Implementation
Code       (pybind11)
```

### Operation Detection

The backend selector analyzes:
1. **Data size**: Must exceed threshold (default: 10,000)
2. **Data type**: Must be numeric (int, float)
3. **Operation type**: Must be supported (arithmetic, comparison)
4. **Placeholder complexity**: Must be simple binary operation

### Code Generation

Simple placeholders are converted to C++ operations:

```python
# Python placeholder
_ * 2

# Becomes C++ operation
"mul_2"

# Executed as
for (double x : data) {
    result.push_back(x * 2.0);
}
```

## 🚨 Limitations

### Current Limitations

1. **Numeric data only**: Strings, objects not supported
2. **Simple operations**: Complex lambdas fall back to Python
3. **Memory overhead**: Data conversion between Python/C++
4. **Platform specific**: Requires compilation for each platform

### Unsupported Operations

```python
# These will use Python backend
pipe(data).map(lambda x: x ** 2.5)     # Complex lambda
pipe(data).map(_["key"])                # Dictionary access
pipe(strings).map(_.upper())            # String methods
pipe(data).group_by(_)                  # Complex operations
```

## 🛠️ Troubleshooting

### Build Issues

```bash
# Missing compiler
sudo apt-get install build-essential  # Ubuntu
xcode-select --install                 # macOS

# Missing Python headers
sudo apt-get install python3-dev      # Ubuntu

# Missing pybind11
pip install pybind11
```

### Runtime Issues

```python
# Check if C++ backend is working
from pyfunc.backends import is_cpp_available
print(f"C++ available: {is_cpp_available()}")

# Enable debug output
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

1. **Threshold too high**: Lower the threshold for smaller datasets
2. **Data conversion overhead**: Use numeric data types
3. **Unsupported operations**: Check if operations are supported

## 🔮 Future Enhancements

### Planned Features

1. **String operations**: C++ acceleration for string processing
2. **Parallel processing**: Multi-threaded operations
3. **SIMD optimization**: Vector instructions for arithmetic
4. **Memory mapping**: Zero-copy data transfer
5. **GPU acceleration**: CUDA/OpenCL support

### Contributing

```bash
# Development setup
git clone https://github.com/alexzzzs/PyFunc.git
cd PyFunc
pip install -e .[dev,cpp]

# Add new C++ operations in:
# - pyfunc/native/operations.hpp
# - pyfunc/native/operations.cpp
# - pyfunc/native/bindings.cpp

# Test your changes
python build_cpp.py
python -m pytest tests/test_cpp_backend.py
```

## 📚 API Reference

### Backend Control

```python
enable_cpp_backend(threshold: int = 10000)
disable_cpp_backend()
is_cpp_available() -> bool
```

### Supported Placeholder Operations

```python
# Arithmetic
_ + value    # Addition
_ - value    # Subtraction  
_ * value    # Multiplication
_ / value    # Division

# Comparison
_ > value    # Greater than
_ < value    # Less than
_ >= value   # Greater than or equal
_ <= value   # Less than or equal
_ == value   # Equal to
_ != value   # Not equal to
```

### Performance Tips

1. **Use simple operations**: Stick to basic arithmetic and comparisons
2. **Process large datasets**: C++ overhead only pays off for large data
3. **Chain operations**: Multiple operations in one pipeline get compound speedups
4. **Use numeric data**: Ensure your data is int or float
5. **Set appropriate threshold**: Balance overhead vs. speedup

---

For more examples and advanced usage, see the [examples/cpp_backend_example.py](examples/cpp_backend_example.py) file.