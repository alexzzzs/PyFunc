# PyFunc Changelog

## Version 0.3.0 - Template Mapping Update

### 🎯 New Features

#### Template Mapping System
- **Dictionary Template Mapping** - Transform data using dictionary templates with placeholders
- **String Template Mapping** - Format strings using template syntax with formatting specifiers
- **Lambda Function Support** - Use lambda functions within dictionary templates for complex logic
- **Enhanced `.map()` method** - Now supports functions, placeholders, dictionary templates, and string templates

#### Real-World Usage Examples
```python
# Dictionary template mapping
pipe(orders).map({
    "id": _["id"],
    "customer": _["customer"],
    "discounted_total": _["total"] * 0.9,
    "category": lambda x: "premium" if x["total"] > 1000 else "standard"
})

# String template mapping
pipe(users).map("User {name} scored {score:.1f}%")

# Combined pipeline (the exact syntax requested)
pipe(ecommerce_orders)
    .filter(_["total"] > 100)
    .map({"id": _["id"], "customer": _["customer"], "discounted_total": _["total"] * 0.9})
    .map("Order #{id} for {customer}: ${discounted_total:.2f}")
    .to_list()
```

### 🔧 Technical Improvements
- Enhanced `_unwrap()` method to handle dictionary and string templates
- Improved error handling for template evaluation
- Support for formatting specifiers in string templates (e.g., `{value:.2f}`)
- Safe evaluation context for template expressions

### 📚 Documentation & Examples
- New comprehensive template mapping section in DOCUMENTATION.md
- Added `examples/template_mapping_example.py` with real-world scenarios
- Updated API documentation with template mapping examples
- Enhanced test coverage (39 tests passing)

### 🧹 Project Maintenance
- Cleaned up temporary files and build artifacts
- Removed unnecessary development files
- Maintained clean project structure
- Updated documentation to reflect new capabilities

## Version 0.2.0 - Major Feature Update

### 🎉 New Features

#### String Operations
- **`explode(delimiter=None)`** - Split strings into characters or by delimiter
- **`implode(separator="")`** - Join iterables into strings with separator
- **`surround(prefix, suffix)`** - Wrap strings with prefix and suffix
- **`template_fill(values)`** - String templating using format() with dict values

#### Dictionary Operations
- **`with_items()`** - Convert dictionary to iterable of (key, value) pairs
- **`map_keys(func)`** - Apply function to all dictionary keys
- **`map_values(func)`** - Apply function to all dictionary values

#### Side Effects & Debugging
- **`do(func)` / `tap(func)`** - Apply side-effect functions without changing the value
- **`debug(label="DEBUG")`** - Print current value with optional label for debugging
- **`trace(label)`** - Alias for debug with custom label

#### Function Composition
- **`>>` operator on Placeholder** - Forward composition: `f >> g` means `g(f(x))`
- **`<<` operator on Placeholder** - Backward composition: `f << g` means `f(g(x))`

#### Core Improvements
- **`to_list()`** - Convert pipeline result to list (cleaner than `.get()` for iterables)
- **`group_by(key)`** - Fixed and improved implementation for grouping elements

### 🔧 API Improvements

#### Primary Entry Point
- **`pipe()`** is now the recommended primary entry point
- Consistent with functional programming conventions
- Better aligns with README examples

#### Enhanced Type System
- Improved generic type annotations throughout
- Better return type inference for chained operations
- More precise error messages with type information

#### Error Handling
- More descriptive error messages
- Better validation of input types
- Clearer indication of which operations work on which data types

### 📚 Documentation & Examples

#### New Examples
- **`examples/comprehensive_example.py`** - Showcases all features in real-world scenarios
- **Updated `examples/simple_example.py`** - Demonstrates new string and composition features
- **`test_new_features.py`** - Comprehensive test suite for all new functionality

#### Performance Testing
- **`performance_test.py`** - Validates lazy evaluation and memory efficiency
- Confirms generators are properly chained
- Tests memory usage with large datasets

### 🚀 Performance & Quality

#### Lazy Evaluation
- All new operations maintain lazy evaluation
- Generators are properly chained without intermediate materialization
- Memory efficient processing of large datasets

#### Backward Compatibility
- 100% backward compatible - all existing code continues to work
- No breaking changes to existing API
- All existing tests pass without modification

#### Test Coverage
- Comprehensive test suite for all new features
- Performance tests validate lazy evaluation
- Real-world examples demonstrate practical usage

### 📦 Package Structure

#### Updated Exports
- Added `__all__` to control public API
- `pipe` is now the primary export
- All new functions properly exported

#### Code Organization
- Clean separation of concerns
- Consistent error handling patterns
- Improved code documentation

### 🔄 Migration Guide

No migration needed! All existing code continues to work. To take advantage of new features:

```python
# Old style (still works)
from pyfunc import Pipeline
result = Pipeline([1, 2, 3]).map(lambda x: x * 2).get()

# New recommended style
from pyfunc import pipe, _
result = pipe([1, 2, 3]).map(_ * 2).to_list()
```

### 🎯 Use Cases

This update makes PyFunc suitable for:
- **Data Processing Pipelines** - Clean, readable data transformations
- **Text Processing** - Rich string manipulation capabilities
- **ETL Operations** - Extract, transform, load with functional style
- **API Response Processing** - Transform JSON/dict data elegantly
- **Log Analysis** - Process and analyze log files functionally
- **Configuration Management** - Transform and validate config data

### 🔮 Future Roadmap

- Async/await support for I/O operations
- Integration with popular data libraries (pandas, numpy)
- Plugin system for custom operations
- Performance optimizations for specific use cases
- Additional statistical and mathematical operations

---

**Full Changelog**: Compare v0.1.0...v0.2.0