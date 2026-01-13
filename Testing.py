"""Unit Testing for differentiator"""

import pytest
from Main import differentiator

@pytest.mark.parametrize("expr", [
    "(x^x)",
    "(x^-2)",
    "a+",
    "sinx",
    "(-x)",
    "(sin(x)",
    "(a+3"
])

# Tests exceptions to well-formed terms
def test_bad_inputs_return_None(expr):
    assert differentiator(expr) is None

# Checks chain rule works     
def test_chain_rule():
    output = differentiator("(sin(x)^2)")
    assert output is not None
    assert "cos(x)" in output

# Checks Quotient rule works
def test_quotient_rule():
    output = differentiator("(cos(x)/(x^2))")
    assert output is not None
    assert "x^2*sin(x)" in output
    assert "x^(2-1)*cos(x)" or "x*cos(x)" in output
    assert "x^2*x^2" or "x^4" in output
