note (if we already having something similar implemted, keep it)

 Goals
Bring true FP fluency to Python (similar to Haskell or Clojure) without leaving Pythonic readability behind.

Allow chainable, composable, lazy, and debuggable operations on any data structure.

Work seamlessly with scalars, iterables, generators, dicts, and side-effectful IO.

Make lambdas almost obsolete with placeholder-based expressions.

Be expressive enough to replace toolz, fn.py, funcy, and even partial pandas pipelines.

🔩 Core Concepts
1. Pipeline Chaining with .then() or >>
Every object can be lifted into a pipeline, and transformations are chained:

python
Copy
Edit
from flowpy import pipe

result = pipe([1, 2, 3, 4]) \
  .filter(_ > 2) \
  .map(_ * 10) \
  .reduce(_ + _)
Or as an expression:

python
Copy
Edit
result = pipe("  Hello  ") >> str.strip >> str.lower
2. Placeholder _ Syntax
A magic _ is used in lambdaless expressions:

python
Copy
Edit
pipe([1, 2, 3]).map(_ ** 2).filter(_ % 2 == 1)
Under the hood it uses AST transformation or dynamic expression evaluation, e.g. via expressionparser.

3. Lazy Evaluation & Streaming
All operations default to lazy, using generators under the hood — but you can .force() to evaluate.

python
Copy
Edit
pipe(range(1_000_000)).map(_ + 1).filter(_ % 5 == 0).take(10).to_list()
4. Unified Pipe for Scalars & Collections
Even a single number, string, or dict can be lifted and transformed fluently.

python
Copy
Edit
pipe(10).then(_ * 2).then(str)   # '20'
pipe("Hello").map(str.lower)    # ['h', 'e', 'l', 'l', 'o']
pipe({"a": 1, "b": 2}).map_values(_ * 10)
5. Composable Functions with .compose()
Functional composition as first-class citizens:

python
Copy
Edit
double = _ * 2
square = _ ** 2
pipeline = pipe.compose(square, double)

pipeline(3)  # (3 * 2) ** 2 = 36
Also supports reverse composition (>> and <<):

python
Copy
Edit
f = double >> square    # square(double(x))
6. Control Flow Primitives
Chainable conditionals and partials:

python
Copy
Edit
pipe(10).when(_ > 5, _ * 2).unless(_ < 5, _ + 1)
Supports .if_else(pred, then_fn, else_fn) for more complex flows.

7. Debug and Trace
Built-in .debug() to inspect intermediate states:

python
Copy
Edit
pipe(range(5)).map(_ + 1).debug().filter(_ % 2 == 0)
You can also do .trace("stage 1") to label steps.

8. Advanced Transformations
Includes:

.chunk(n)

.unique()

.flatten(depth=1)

.group_by(key)

.zip_with(other)

.window(size, step)

.sliding_pairs()

.product(), .combinations()

9. Optional Static Typing
Gradual typing using Protocol, TypeVar, and Generic. Auto-inferred return types where possible.

10. Side Effects Are Explicit
Use .do() to apply side-effectful functions:

python
Copy
Edit
pipe(range(3)).do(print).to_list()
No silent effects unless explicitly intended.

🧰 Example: Real Use Case
python
Copy
Edit
from flowpy import pipe, _

names = pipe([" Alice ", "BOB", "eve", "Charlie  "]) \
    .map(_.strip().capitalize()) \
    .filter(len(_) > 3) \
    .sort() \
    .to_list()

# ['Alice', 'Charlie']
Or with .compose():

python
Copy
Edit
clean_name = pipe.compose(_.strip(), _.capitalize())
pipe([" alice ", "bob"]).map(clean_name).to_list()
🧱 Architecture
Core is a generic Pipe object that wraps any data.

Uses dynamic dispatch and functools.singledispatch to support different types.

Placeholder _ uses an expression parser or symbolic evaluator.

Built to interop with async, pandas, numpy, itertools, and toolz.

🔌 Extensibility
Supports .register_custom_type() for your own classes.

Users can .extend() with custom transforms.

Integrates with Jupyter: .viz() shows pipeline graph.

🤯 Bonus Ideas
Pattern matching pipelines.

DSL for defining declarative pipelines.

Integration with tracing libraries (opentelemetry, etc).

Pluggable parallelization backend: sequential, threads, async, multiprocessing.

