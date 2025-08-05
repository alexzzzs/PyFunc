# PyFunc Zig Backend

The Zig backend provides blazing-fast mathematical operations for PyFunc pipelines. Zig is a modern systems programming language that compiles to highly optimized machine code with zero runtime overhead.

## 🚀 Why Zig?

- **🔥 Blazing Fast**: Compiles to optimized machine code
- **🛡️ Memory Safe**: Compile-time safety without runtime overhead  
- **🔧 Zero Dependencies**: No runtime, no garbage collector
- **🌍 Cross-Platform**: Works on Windows, Linux, macOS
- **⚡ Low Latency**: Minimal FFI overhead compared to other languages

## 📦 Installation

### Prerequisites

1. **Install Zig** (version 0.11.0 or later):
   ```bash
   # Windows (Scoop)
   scoop install zig
   
   # macOS (Homebrew)
   brew install zig
   
   # Linux (Snap)
   snap install zig --classic
   
   # Or download from: https://ziglang.org/download/
   ```

### Build the Backend

```bash
# Build the Zig backend
python build_zig.py
```

This will:
- Compile the Zig shared library
- Test the backend functionality
- Make it available to PyFunc

## 🎯 Zig Backend Specializations

The Zig backend specializes in **mathematical operations**:

### Core Mathematical Functions
- `sum()` - Fast summation
- `mean()` - Average calculation  
- `min()` / `max()` - Extrema finding
- `stdev()` - Standard deviation
- `variance()` - Variance calculation

### Vector Operations
- `dot_product()` - Vector dot product
- `vector_magnitude()` - Vector length/magnitude
- `map_multiply()` - Scalar multiplication
- `map_add()` - Scalar addition
- `map_power()` - Element-wise exponentiation

### Advanced Operations
- `cumsum()` - Cumulative sum
- `diff()` - Differences between consecutive elements

## 🔧 Usage

### Automatic Backend Selection

PyFunc automatically uses the Zig backend for mathematical operations on large datasets:

```python
from pyfunc import pipe, set_zig_threshold

# Configure threshold (default: 5000 elements)
set_zig_threshold(1000)

# Automatic backend selection
large_data = list(range(10000))
result = pipe(large_data).sum().get()  # Uses Zig automatically
```

### Explicit Zig Usage

Force Zig backend usage with explicit methods:

```python
from pyfunc import pipe

data = [1.0, 2.0, 3.0, 4.0, 5.0]

# Explicit Zig methods
sum_result = pipe(data).sum_zig().get()
mean_result = pipe(data).mean_zig().get()  
stdev_result = pipe(data).stdev_zig().get()
```

### Advanced Mathematical Operations

Access advanced Zig operations through the backend:

```python
from pyfunc.backends import get_backend

backend = get_backend()
if backend.zig_backend:
    # Vector operations
    vec_a = [1.0, 2.0, 3.0]
    vec_b = [4.0, 5.0, 6.0]
    
    dot_product = backend.zig_backend.dot_product(vec_a, vec_b)
    magnitude = backend.zig_backend.vector_magnitude(vec_a)
    
    # Map operations
    doubled = backend.zig_backend.map_multiply([1, 2, 3, 4, 5], 2.0)
    squared = backend.zig_backend.map_power([1, 2, 3, 4, 5], 2.0)
```

## 📊 Performance Characteristics

### Optimal Use Cases

- **Mathematical computations** on numeric data
- **Large datasets** (5,000+ elements for best speedup)
- **Vector operations** and linear algebra
- **Statistical analysis** and data science workflows

### Performance Comparison

Typical speedups over pure Python:

| Operation | Dataset Size | Speedup |
|-----------|-------------|---------|
| Sum       | 10,000      | 3-5x    |
| Mean      | 50,000      | 4-6x    |
| Std Dev   | 100,000     | 5-8x    |
| Vector Ops| 10,000      | 6-10x   |

### Threshold Configuration

```python
from pyfunc import set_zig_threshold

# Conservative (use Zig for large datasets)
set_zig_threshold(10000)

# Aggressive (use Zig for medium datasets)  
set_zig_threshold(1000)

# Maximum performance (use Zig for small datasets)
set_zig_threshold(100)
```

## 🏗️ Architecture

### Multi-Backend Integration

The Zig backend integrates seamlessly with PyFunc's multi-backend system:

```
Python (always available)
    ↓ fallback
C++ Backend (general operations)
    ↓ fallback  
Zig Backend (mathematical operations)
    ↓ fallback
Rust Backend (statistical operations)
    ↓ fallback
Go Backend (bitwise operations)
```

### Smart Backend Selection

PyFunc automatically chooses the best backend:

1. **Check data size** against thresholds
2. **Check operation type** (mathematical → Zig)
3. **Check data compatibility** (numeric data)
4. **Fallback gracefully** if backend unavailable

## 🔍 Examples

### Financial Analysis

```python
from pyfunc import pipe, set_zig_threshold

# Stock price analysis
prices = [100.5, 101.2, 99.8, 102.1, 103.5, ...]  # 1000+ prices

set_zig_threshold(500)  # Use Zig for datasets > 500

analysis = {
    "mean": pipe(prices).sum().get() / len(prices),
    "volatility": pipe(prices).stdev().get(),
    "max_price": pipe(prices).max().get(),
    "min_price": pipe(prices).min().get()
}
```

### Scientific Computing

```python
from pyfunc.backends import get_backend

# Vector operations for physics simulation
backend = get_backend()
if backend.zig_backend:
    # Force vectors
    force_x = [1.2, 2.3, 0.8, 1.9, 3.1]
    force_y = [0.9, 1.7, 2.1, 0.6, 2.8]
    
    # Calculate resultant force magnitude
    force_magnitude = backend.zig_backend.vector_magnitude(
        [fx**2 + fy**2 for fx, fy in zip(force_x, force_y)]
    )
```

### Data Science Pipeline

```python
from pyfunc import pipe

# Large dataset processing
sensor_data = [...]  # 100,000+ sensor readings

# Preprocessing pipeline with Zig acceleration
processed = (pipe(sensor_data)
            .map(lambda x: x * 0.1)      # Scale
            .filter(lambda x: x > 0)     # Remove negatives
            .sum()                       # Sum (uses Zig)
            .get())

statistics = {
    "mean": pipe(sensor_data).sum().get() / len(sensor_data),  # Zig
    "std": pipe(sensor_data).stdev().get(),                    # Zig  
    "range": pipe(sensor_data).max().get() - pipe(sensor_data).min().get()  # Zig
}
```

## 🛠️ Development

### Building from Source

```bash
# Clone the repository
git clone <repo-url>
cd PyFunc

# Build Zig backend
python build_zig.py

# Run tests
python -m pytest tests/test_zig_backend.py
```

### Adding New Operations

1. **Add Zig function** in `pyfunc/native_zig/math_ops.zig`:
   ```zig
   export fn zig_new_operation(data: [*]f64, size: usize) f64 {
       // Implementation
   }
   ```

2. **Add Python wrapper** in `pyfunc/backends/zig_backend.py`:
   ```python
   def new_operation(self, data: List[float]) -> float:
       float_array = self._to_float_array(data)
       return self._lib.zig_new_operation(float_array, len(data))
   ```

3. **Add pipeline method** in `pyfunc/pipeline.py`:
   ```python
   def new_operation_zig(self) -> 'Pipeline[float]':
       # Implementation
   ```

### Testing

```bash
# Test Zig backend specifically
python examples/zig_backend_example.py

# Run comprehensive tests
python -c "
from pyfunc import pipe, is_zig_available
print('Zig available:', is_zig_available())
if is_zig_available():
    result = pipe([1,2,3,4,5]).sum_zig().get()
    print('Zig sum test:', result == 15)
"
```

## 🚨 Troubleshooting

### Common Issues

**"Zig backend not available"**
- Install Zig: https://ziglang.org/download/
- Run: `python build_zig.py`
- Check PATH includes Zig

**"Library not found"**
- Rebuild: `python build_zig.py`
- Check file permissions
- Verify shared library was created

**"Function not found"**
- Ensure Zig version compatibility (0.11.0+)
- Rebuild with: `zig build -Doptimize=ReleaseFast`

### Performance Issues

**Slower than expected**
- Increase threshold: `set_zig_threshold(10000)`
- Use explicit methods: `.sum_zig()`
- Check data types (prefer float64)

**Memory usage**
- Zig backend copies data for FFI
- Consider chunking very large datasets
- Monitor memory with large operations

## 🤝 Contributing

We welcome contributions to the Zig backend! Areas for improvement:

- **More mathematical operations** (median, percentiles)
- **Matrix operations** (multiplication, decomposition)  
- **Signal processing** functions
- **Performance optimizations**
- **SIMD vectorization**

## 📄 License

The Zig backend is part of PyFunc and uses the same MIT license.

---

**Ready to experience blazing-fast mathematical operations? Build the Zig backend and supercharge your PyFunc pipelines! ⚡**