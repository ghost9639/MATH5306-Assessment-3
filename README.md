# Symbolic Differentiation Engine (Python)

A small symbolic differentiation engine that reads in an equation as a string, parses arithmetic expressions into an AST, and returns the derivative with respect to `x`.

This project focuses on correct parsing, clear error reporting, and deterministic transformations:
* Human readable input,
* Parser,
* AST,
* Differentiate,
* Human readable output.

## Features
- Recursive-descent parser with operator precedence:
  - parentheses,
  - exponentiation (`^` and `**`, right-associative, `-` and `/` are left-associative),
  - multiplication/division,
  - addition/subtraction.
- AST representation for operators and single-argument functions,
- Symbolic differentiation rules:
  - `+`, `-` (base case),
  - `*` (product rule),
  - `/` (quotient rule),
  - `^` / `**` (power rule for natural-number exponents),
  - `sin`, `cos`, `exp`, `log` (chain rule for supported functions).
- Precedence aware printer that reconstructs readable expressions with minimal parentheses.
- Input validation:
  - bracket match checking,
  - tokenisation rules (single-letter variables; implemented function calls),
  - explicit parse failures for bad entries.

## Robustness 
- pytest unit testing:
  - Tests for bad entry,
  - Tests for various differentiation rules,
  - Tests for meaningful function parsing.

## Usage
```python
from Main import differentiator

print("differentiator expects single letter variables, and brackets wrapping any operations. For now, it cannot parse exponents that aren't natural numbers, but I will update this at some point.")
print(differentiator("(cos(x) * (x^2))"))
print(differentiator("(cos((exp(x))/(x^12))+(x^2))"))
```

## Task 1: Basic regex bracket matching

Implemented by:
- Greedy algorithm, make counter (balance);
- Go through string by character, increment balance for (, decrement for );
  WHILE LOOP IS RUNNING:
- Return False if counter is negative;
  AFTER LOOP TERMINATES:
- Return True if counter is 0, False otherwise;
- Should be O(N) complex.


Rules for counting:
- It seems like "()" are the only program recognised brackets. "[]" can finish trailing legally.


## Task 2: Returns content of user entry 

Thanks to the bracket checker, we know we can expect every non-trivial expression in the form 

(val1 operator val2)

Where both values could be composed of the same expression. We want to parse between them in such a way that the program renders:

{ operator 
	{ value1,
	  value2
	}
}

This would be recursively functional, and forwards supportive of whatever differentiation algorithm we use.


Operators have precedence in order: "()","^ **", "*/", "-+"

Implemented by:
- Recursive descent parser

Algorithm:
- For DM-AS, push up the stack, if handed the relevant token, make a node of the left and right sides of the expression with the given operator, push up the stack again, and return the node.
- For I, push up the stack once, if handed the relevant token, make a node of the left and right sides of the expression, recall ^, and return the node.
- For B, if handed "(", iterate forwards once, and pass down the stack to AS, when node is returned, iterate over ")", and return the node 

## Task 3: Well-Formed Terms

This parser automatically fulfills the requirements of Task 3, since it cannot parse most exceptions to our well-formed terms rules. However, we can explicitly add a rule to our \_I\_Parser that any exponent must be a natural number. Additionally, the inclusion of a \_fail() function allows more explicit error signalling within our \_formatter function. If the \_bracket\_ checker returns false, then we can signal bad brackets to the user, if \_tokeniser fails, we can signal to the user that they have written a variable with more than one letter, and if the user inputs a string that otherwise cannot be parsed, then the parsers all go into failure and \_formatter returns bad format.

## Task 4: Extended Functions 

For Task 4, the first step was to adjust tokeniser so that it appended known functions as blocks instead of throwing multi character errors. Then, by adding in functions as a member of the order of operations in the order B-F-I-DM-AS, and preventing the order of operations from rising above it, we can enforce the rules that a function must be of the format "func (well-formed)". Once this is complete, or if the current token is not a known function, control flow passes back up to the \_B\_parser.

The transition to a differentiation function lead to the decision that every previous function should be treated as a utility for differentiator, such that a calculator program could read in user input, read in the decision to differentiate, and consequently call "differentiator(user_entry)" without any other function calls. The Polish notation operator structure makes parsing extremely easy, with four different conditions/

* Terminal condition 1:
* 	If the variable we are looking at is "x", then return 1. 	
* Terminal condition 2:
*	If the variable we are looking at is some naive string, but not "x", then return 0.

Thanks to our restriction that a well-formed term cannot be "2x", but instead of the form "(2*x)", these conditions are guaranteed to be met once we have broken down all functions and parsed all operators at the end of a tree. We also have a more complex set of differentiation rules for splits in the tree.

* If we are looking at an operator:
  * If the operator is +, simply return a node of both sides differentiated and added.
  * If the operator is -, simply return a node of both sides differentiated and subtracted.
  * If the operator is *, then return a node of the product rule, where "u\* v = u'v + v'u".
  * If the operator follows law "left/right", then return the node ((right' \* left) - (right \* left'))/(right \* right), according to the quotient rule.
  * If the operator is ^, we have restricted exponents to natural numbers, so simply return right \* (left ^ (right - 1))

* If we are looking at a function:
  * If the function is sin(x), return a node of x' \* cos(x))
  * If the function is cos(x), return the node (-1 * (x' \* sin(x)))
  * If the function is exp(x), return the node (x' * exp(x))
  * If the function is log(x), return the node (x' * (1 / x))

These deal with the special function rules for our defined list of functions. I initially considered defining a global list of functions, but decided it would be more responsible to make a "master" list in differentiator, that the utility functions could inherit. I initially wanted to put a dictionary defining a set of differentiated functions, but implementing this with functions like log proved overly complex and error prone, so the function definitions in \_diff are hard coded.

After the refactored expression is differentiated, we ideally want to be able to read it. To this end, we add a \_to\_string function, that works on the following principles:

* We receive a node, and an associated parent priority value corresponding to the order of operations,
* 
* If we're looking at a string, simply return it. This is a termination condition on variables and numbers.
* If we're looking at a function, then return the function, and call \_to_string on the internal arguments within brackets.
* If we're looking at an operator:
  * Pull the operator, arguments, and operator priority,
  * Convert the left hand argument into a string,
  * Convert the right hand argument into a string, with lower priority for indexing operations because a\^b\^c should read as a\^(b\^c). 
  * If the current operation has a lower priority than the parent value, return the left hand argument, operation, and right hand argument.

What this finished program does:

Given a properly formatted string entry, it will return the same function differentiated in a similar format. Where this is not possible, it will return None, and attempt to echo a meaningful error message to the console.

## Unit Testing 

Project was written and deployed in modules, which is very clear from the somewhat frenetic and sometimes forward-looking approach outlined in this documentation file until Task 4 (when the whole thing was finally finished). This meant various individual modules like \_B\_Parser and \_diff were modified and broken multiple times. Adding pytest unit test functionality in a [helper file](Testing.py) ensured that regular checking could be done to ensure functions continued to work in the presence of errors caused by alterations done long after the original modules were written. 


## Future steps:

Removing the requirement that only natural numbers can be exponents, and integrate the pre-existing chain rule functionality instead,

Support for more functions,

Better return formatting, things like "x * 1" automatically re-evaluating to "x",

Lazy evaluation of numerical only types, such that "x * (4 + 2)" automatically re-evaluates to "x \* 6",

Management of function derivatives is pretty clumsy, requiring a hard-coded change to \_differentiator in any case where more functions want to be added. It could be possible to generalise this process with lambda functions, allowing us to define a list of functions and a dictionary of the differentiated values of those functions. This isn't worth the effort with 4 functions, but would be valuable if we started extending the differentiator far more.

