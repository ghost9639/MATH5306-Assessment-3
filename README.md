# Symbolic Differentiation Engine (Python)

A small symbolic differentiation engine that reads in an equation as a string, parses arithmetic expressions into an AST, and returns the derivative with respect to `x`.

This project focuses on **correct parsing**, **clear error reporting**, and **deterministic transformations** (readable input -> parse -> AST -> differentiate -> readable output).

## Features
- **Recursive-descent parser** with operator precedence:
  - parentheses,
  - exponentiation (`^` and `**`, right-associative),
  - multiplication/division,
  - addition/subtraction.
- **AST representation** for operators and single-argument functions
- Symbolic differentiation rules:
  - `+`, `-` (nothing),
  - `*` (product rule),
  - `/` (quotient rule),
  - `^` / `**` (power rule for natural-number exponents),
  - `sin`, `cos`, `exp`, `log` (chain rule for supported functions).
- **Precedence-aware pretty printer** that reconstructs readable expressions with minimal parentheses!
- Input validation:
  - bracket balance checking,
  - tokenisation rules (single-letter variables; implemented function calls),
  - explicit parse failures for bad entries.

## Usage
```python
from Main import differentiator

print("differentiator expects single letter variables, and brackets wrapping any operations. For now, it cannot parse exponents that aren't natural numbers, but I will update this at some point.")
print(differentiator("(cos(x) * (x^2))"))
print(differentiator("(cos((exp(x))/(x^12))+(x^2))"))
