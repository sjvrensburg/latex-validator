# LaTeX Validator

A Python package to validate LaTeX expressions, usable as a command-line tool or a library.

## Installation

Install directly from GitHub using `uv` or `pip`:

```bash
uv pip install git+https://github.com/sjvrensburg/latex-validator.git
```

Or with `pip`:

```bash
pip install git+https://github.com/sjvrensburg/latex-validator.git
```

## Usage

### As a Command-Line Tool

Validate LaTeX expressions from standard input:

```bash
echo "\\textbf{test}" | latex-validator
```

Validate from a file:

```bash
latex-validator -f input.tex -o output.json --encoding utf-8 --verbose
```

Options:
- `-f`, `--file`: Path to input file with LaTeX expressions (one per line).
- `-o`, `--output`: Path to output JSON file (default: stdout).
- `--encoding`: File encoding (default: utf-8).
- `--verbose`: Enable verbose output.
- `--version`: Show version and exit.

### As a Library

```python
from latex_validator import validate_latex

result = validate_latex(r"\textbf{test}")
print(result)  # {"expression": "\\textbf{test}", "is_valid": True, "error": None}
```

## License

MIT License
