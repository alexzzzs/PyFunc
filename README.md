# PyFunc: Functional Programming Pipeline for Python

PyFunc is a Python library designed to bring functional programming fluency to Python, enabling chainable, composable, lazy, and debuggable operations on various data structures.

## Goals

*   Bring true FP fluency to Python (similar to Haskell or Clojure) without leaving Pythonic readability behind.
*   Allow chainable, composable, lazy, and debuggable operations on any data structure.
*   Work seamlessly with scalars, iterables, generators, dicts, and side-effectful IO.
*   Make lambdas almost obsolete with placeholder-based expressions.
*   Be expressive enough to replace toolz, fn.py, funcy, and even partial pandas pipelines.

## Core Concepts

### 1. Pipeline Chaining with `.then()` or `>>`

Every object can be lifted into a pipeline, and transformations are chained:

```python
from pyfunc import pipe, _

result = pipe([1, 2, 3, 4]) \
  .filter(_ > 2) \
  .map(_ * 10) \
  .reduce(_ + _)
# result will be 70
```

Or as an expression:

```python
from pyfunc import pipe

result = pipe("  Hello  ") >> str.strip >> str.lower
# result will be "hello"
```

### 2. Placeholder `_` Syntax

A magic `_` is used in lambdaless expressions:

```python
from pyfunc import pipe, _

result = pipe([1, 2, 3]).map(_ ** 2).filter(_ % 2 == 1).to_list()
# result will be [1, 9]
```

### 3. Lazy Evaluation & Streaming

All operations default to lazy, using generators under the hood — but you can `.to_list()` to evaluate:

```python
from pyfunc import pipe, _

result = pipe(range(1_000_000)).map(_ + 1).filter(_ % 5 == 0).take(10).to_list()
# result will be [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
```

### 4. Unified Pipe for Scalars & Collections

Even a single number, string, or dict can be lifted and transformed fluently.

```python
from pyfunc import pipe, _

pipe(10).then(_ * 2).then(str).get()   # '20'
pipe("Hello").map(str.lower).to_list()    # ['h', 'e', 'l', 'l', 'o']
pipe({"a": 1, "b": 2}).map_values(_ * 10).get() # {"a": 10, "b": 20}
```

### 5. Composable Functions with `.compose()`

Functional composition as first-class citizens:

```python
from pyfunc import pipe, _

double = _ * 2
square = _ ** 2
pipeline_func = pipe.compose(square, double)

pipeline_func(3)  # (3 * 2) ** 2 = 36
```

Also supports reverse composition (`>>` and `<<`):

```python
from pyfunc import _

f = (_ * 2) >> (_ ** 2) # square(double(x))
# f(3) will be 36
```

### 6. Control Flow Primitives

Chainable conditionals and partials:

```python
from pyfunc import pipe, _

pipe(10).when(_ > 5, _ * 2).unless(_ < 5, _ + 1).get()
# result will be 20

pipe(3).if_else(_ > 5, _ * 2, _ + 1).get()
# result will be 4
```

### 7. Debug and Trace

Built-in `.debug()` to inspect intermediate states:

```python
from pyfunc import pipe, _

pipe(range(5)).map(_ + 1).debug().filter(_ % 2 == 0).to_list()
# DEBUG: <generator object Pipeline.map.<locals>._map_func at 0x...>
# result will be [2, 4]
```

You can also do `.trace("stage 1")` to label steps.

### 8. Advanced Transformations

Includes:

*   `.chunk(n)`
*   `.unique()`
*   `.flatten(depth=1)`
*   `.group_by(key)`
*   `.zip_with(other)`
*   `.window(size, step)`
*   `.sliding_pairs()`
*   `.product(), .combinations()`
*   `.take(n)`
*   `.skip(n)`
*   `.take_while(predicate)`
*   `.skip_while(predicate)`
*   `.first()`
*   `.last()`
*   `.nth(n)`
*   `.is_empty()`
*   `.count()`
*   `.sum()`
*   `.min()`
*   `.max()`
*   `.reverse()`

### 9. Optional Static Typing

Gradual typing using `Protocol`, `TypeVar`, and `Generic`. Auto-inferred return types where possible.

### 10. Side Effects Are Explicit

Use `.do()` or `.tap()` to apply side-effectful functions:

```python
from pyfunc import pipe

pipe(range(3)).do(print).to_list()
# 0
# 1
# 2
# result will be [0, 1, 2]
```

## Example: Real Use Case

```python
from pyfunc import pipe, _

names = pipe([" Alice ", "BOB", "eve", "Charlie  "]) \
    .map(_.strip().capitalize()) \
    .filter(len(_) > 3) \
    .sort() \
    .to_list()

# ['Alice', 'Charlie']
```

Or with `.compose()`:

```python
from pyfunc import pipe, _

clean_name = pipe.compose(_.strip(), _.capitalize())
pipe([" alice ", "bob"]).map(clean_name).to_list()
# ['Alice', 'Bob']
```

## Extensibility

*   **`Pipeline.register_custom_type()`**: Supports registering custom type handlers for specific operations.
*   **`Pipeline.extend()`**: Allows users to extend the `Pipeline` class with new methods.

## Installation (Coming Soon)

Installation instructions will be provided here once the package is published.

## Usage (Coming Soon)

More detailed usage examples will be provided here.

## Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
