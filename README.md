# PyFunc: Functional Programming Pipeline for Python

PyFunc is a Python library that brings functional programming fluency to Python, enabling chainable, composable, lazy, and debuggable operations on various data structures.

## ✨ Features

- **🔗 Chainable Operations**: Method chaining for readable data transformations
- **🎯 Placeholder Syntax**: Use `_` to create lambda-free expressions  
- **⚡ Lazy Evaluation**: Operations computed only when needed
- **🔄 Function Composition**: Compose functions with `>>` and `<<` operators
- **📊 Rich Data Operations**: Works with scalars, lists, dicts, generators
- **🐛 Built-in Debugging**: Debug and trace pipeline execution
- **🔧 Extensible**: Register custom types and extend functionality
- **📝 Type Safe**: Full type hints and generic support

## 🚀 Quick Start

```bash
pip install pyfunc-pipeline
```

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

## 🎯 Core Concepts

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

### Placeholder Syntax

The `_` placeholder creates reusable, composable expressions:

```python
from pyfunc import _

# Arithmetic operations
double = _ * 2
add_ten = _ + 10

# Method calls
normalize = _.strip().lower()

# Comparisons  
is_positive = _ > 0

# Composition
process = double >> add_ten  # add_ten(double(x))
```

### Lazy Evaluation

Operations are lazy by default - perfect for large datasets:

```python
# Processes only what's needed from 1 million items
result = pipe(range(1_000_000)).filter(_ > 500_000).take(5).to_list()
```

## 📚 Rich API

### String Operations
```python
pipe("hello,world").explode(",").map(_.capitalize()).implode(" & ").get()
# "Hello & World"

pipe("Hello {name}!").template_fill({"name": "PyFunc"}).get()  
# "Hello PyFunc!"
```

### Dictionary Operations
```python
users = {"alice": 25, "bob": 30}
pipe(users).map_values(_ + 5).map_keys(_.title()).get()
# {"Alice": 30, "Bob": 35}
```

### Advanced Transformations
```python
# Group by
data = [{"name": "Alice", "dept": "Eng"}, {"name": "Bob", "dept": "Sales"}]
pipe(data).group_by(_["dept"]).get()

# Sliding windows
pipe([1, 2, 3, 4, 5]).window(3).to_list()
# [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

# Combinations
pipe([1, 2, 3]).combinations(2).to_list()  
# [(1, 2), (1, 3), (2, 3)]
```

### Side Effects & Debugging
```python
pipe([1, 2, 3, 4])
    .debug("Input")
    .filter(_ > 2) 
    .debug("Filtered")
    .map(_ ** 2)
    .to_list()
```

## 🌟 Real-World Example

```python
from pyfunc import pipe, _

# E-commerce order processing with template mapping
orders = [
    {"id": 1, "customer": "Alice", "items": ["laptop", "mouse"], "total": 1200.50},
    {"id": 2, "customer": "Bob", "items": ["keyboard"], "total": 75.00},
    {"id": 3, "customer": "Charlie", "items": ["monitor", "stand"], "total": 450.25}
]

# Process orders with dictionary and string templates
result = (
    pipe(orders)
    .filter(_["total"] > 100)  # Filter orders > $100
    .map({
        "id": _["id"],
        "customer": _["customer"],
        "discounted_total": _["total"] * 0.9  # 10% discount
    })
    .map("Order #{id} for {customer}: ${discounted_total:.2f}")
    .to_list()
)

print(result)
# ['Order #1 for Alice: $1080.45', 'Order #3 for Charlie: $405.23']
```

### ⚠️ **Important Note**
Use **regular string templates**, not f-strings:
```python
# ❌ Wrong - Don't use f-strings  
.map(f"Order #{_['id']}")  # This will cause an error!

# ✅ Correct - Use regular string templates
.map("Order #{id}")  # PyFunc handles the evaluation
```

## 📖 Documentation

- **[Complete Documentation](DOCUMENTATION.md)** - Full API reference and examples
- **[Examples](examples/)** - Real-world usage examples  
- **[Changelog](CHANGELOG.md)** - Version history and updates

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.
