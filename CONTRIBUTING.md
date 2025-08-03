# Contributing to PyFunc

We welcome contributions to PyFunc! Here are some guidelines to help you get started.

## How to Contribute

1.  **Fork the repository** on GitHub.
2.  **Clone your forked repository** to your local machine.
    ```bash
    git clone https://github.com/your_username/pyfunc.git
    cd pyfunc
    ```
3.  **Create a new branch** for your feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/your-bug-fix-name
    ```
4.  **Make your changes** and write tests for them. Ensure all existing tests pass and new tests cover your changes.
5.  **Run type checks** using MyPy to ensure type consistency.
    ```bash
    mypy pyfunc/
    ```
6.  **Run tests** to ensure everything is working as expected.
    ```bash
    python -m unittest tests/test_pipeline.py
    ```
7.  **Commit your changes** with a clear and concise commit message.
    ```bash
    git commit -m "feat: Add new feature X" # or "fix: Fix bug Y"
    ```
8.  **Push your changes** to your forked repository.
    ```bash
    git push origin feature/your-feature-name
    ```
9.  **Open a Pull Request** on the main PyFunc repository. Provide a detailed description of your changes.

## Code Style

*   Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
*   Use clear and concise docstrings for all functions, classes, and methods.
*   Add type hints to your code.

## Reporting Bugs

If you find a bug, please open an issue on the [GitHub issue tracker](https://github.com/your_username/pyfunc/issues). Provide as much detail as possible, including:

*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Screenshots (if applicable).
*   Your Python version and operating system.

## Feature Requests

If you have an idea for a new feature, please open an issue on the [GitHub issue tracker](https://github.com/your_username/pyfunc/issues). Describe your idea clearly and explain why it would be a valuable addition to PyFunc.

## License

By contributing to PyFunc, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
