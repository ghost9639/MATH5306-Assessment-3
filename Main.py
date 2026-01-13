"""Project File for Assessment 3
Objective of project is to make a program capable of basic differentiation
delivered in single .py package."""

# Task 1
def _bracket_checker (obj):  
    """Checks whether brackets in an expression are balanced.
    Expects str-based user entry, returns boolean"""
    balance = 0                  # counts opened and closed brackets
    
    for char in obj:
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1

        if balance < 0:          # closed bracket that was not opened
            return False

    # if true, then there are no unclosed brackets
    return balance == 0

# Task 2
def _make_node (optor, left, right):   
    """Makes node for any given operator and arguments"""
    return {
        "optor": optor,
        "args": [left, right]
    }

def _tokeniser (tok, functs):     
    """Formats string of equations into operator delineated well-formed
    terms. Expects no white-space, returns a list of strings."""

    operators = ["(", ")", "^", "*", "/", "+", "-"]
    i = 0
    term, tokens = [], []
    
    while i < len(tok):
        # handle values
        if tok[i] not in operators: 
            term.append(tok[i])
            i += 1

        # support for ** indexing
        elif tok[i] == "*" and i+1 < len(tok) and tok[i+1] == "*":
            if len(term) > 0:
                tokens.append(''.join(str(s) for s in term))
                term.clear()
                
            tokens.append("**")
            i += 2

        # after seeing an operator
        else:
            if len(term) > 0:

                current_term = ''.join(term)
                
                if current_term.isalpha() and current_term in functs:
                    tokens.append(current_term)
                    term.clear()
                
                # This prevents letters larger than 1 character getting through
                elif current_term.isalpha() and len(term) > 1:
                    return None, -1
                
                else:
                    tokens.append(current_term)
                    term.clear()
                
            tokens.append(tok[i])
            i += 1

    if ''.join(str(s) for s in term).isalpha() and len(term)>1:
        return None, -1
    if len(term) > 0: tokens.append(''.join(str(s) for s in term))
    
    return tokens, 1

def _fail():  
    """Parser utility to satisfy Task 3.
    If a parser fails, _fail hard returns -1"""
    return None, -1 

def _is_valid_exponent(right):  
    """Checks if the exponent is a natural number greater than 1"""
    if isinstance(right, (str)):
        return right.isdigit() and int(right) >= 1

    else: return False 
        
def _AS_parser (expression, place, functs): 
    """Parses addition for subtraction operators"""
    left, place = _DM_parser (expression, place, functs)
    if place == -1: return _fail()

    while place < len(expression) and expression[place] in ["+", "-"]:
        optor = expression[place]
        right, place = _DM_parser (expression, place + 1, functs)

        if place == -1:
            return _fail()
        left = _make_node (optor, left, right)

    return left, place 

def _DM_parser (expression, place, functs):  
    """Division / multiplication parser utility"""
    
    left, place = _I_parser (expression, place, functs)
    if place == -1: return _fail()
    
    while place < len(expression) and expression[place] in ["*", "/"]:
        optor = expression[place]
        right, place = _I_parser(expression, place + 1, functs)
        if place == -1: return _fail()
        left = _make_node(optor, left, right)
        
    return left, place 

def _I_parser (expression, place, functs):   
    """Indexing operation parser utility, supports ^ and **
    returns a node of expression to the right"""
    
    left, place = _F_parser (expression, place, functs)
    if place == -1: return _fail()

    # originally intended to use ** only but added ^ functionality
    if place < len(expression) and expression[place] in ["**", "^"]:
        optor = expression[place]
        right, place = _I_parser(expression, place + 1, functs)

        if place == -1: return _fail()
        if not _is_valid_exponent(right): return _fail()

        return _make_node(optor, left, right), place 
        
    return left, place

def _F_parser (expression, place, functs):    
    """Function parsing utility, adding functions is simple as adding
    it to the functions list in differentiator"""

    if place < 0 or place >= len(expression):
        return _fail()
    
    func = expression[place]

    if func in functs:
        
        # functions must be followed by (
        if place + 1 >= len(expression) or expression[place+1] != "(":
            return _fail()
        
        nested, place = _AS_parser(expression, place + 2, functs)

        if place == -1:
            return _fail()

        if place >= len(expression) or expression[place] != ")":
            return _fail()

        return {
            "function": func,
            "args": nested 
        }, place + 1            # jumping over )

    return _B_parser(expression, place, functs)

def _B_parser (expression, place, functs):  
    """Bracket parsing utility, consumes (, returns new node"""
    if place < 0 or place >= len(expression):
        return _fail()

    optors = {"+", "-", "*", "/", "^", "**"}
    token = expression[place]

    if token == "(":
        node, place = _AS_parser(expression, place + 1, functs)
        if place == -1:
            return _fail()

        # expression must end ")"
        if place >= len(expression) or expression[place] != ")":
            return _fail()
        return node, place + 1

    # value must follow, blocks entry like "(a+)"
    if token == ")" or token in optors:
        return _fail()

    if token.isdigit():
        return token, place + 1
    if token.isalpha() and len(token) == 1:
        return token, place + 1

    return _fail()

def _formatter (user_entry, functs = ["sin", "cos", "log", "exp"]): 
    """Internal differential utility that turns strings into equations
    that _diff can parse"""
    if not _bracket_checker(user_entry):
        print("Mismatched Brackets Error")
        return None             # handles bad format entry
    
    user_entry = user_entry.replace(" ", "") # no whitespace
    
    tokens, exit_code = _tokeniser(user_entry, functs)
    if exit_code == -1:
        print("Multi-character Unknown Error")
        return None 

    optors = {"^", "**", "*", "/", "+", "-"}
    if any (tok in optors for tok in tokens):
        if not (tokens and tokens[0] == "(" and tokens[-1] == ")"):
            print("Bracket Wrapping Error")
            return None 

    tree, place = _AS_parser(tokens, 0, functs) # starts chain

    if place == -1 or place != len(tokens):
        print("Bad Format Error")
        return None
    
    return tree

def _is_operator (expression):   
    """Checks whether node in differentiator is an operator."""

    return isinstance (expression, dict) and "optor" in expression

def _is_function (expression):  
    """Checks whether the node is a function"""

    return isinstance (expression, dict) and "function" in expression
    
# recursive differentiation    
def _diff (expression, functs = ["sin", "cos", "log", "exp"]): 
    """Recursive differencing function. Terminates variables and splits
    functions / operators"""

    # base case single value differentiation
    if expression == "x": return "1"
    
    elif isinstance(expression, (str)): return "0"

    # Differentiating an operator 
    elif _is_operator(expression):
        op = expression['optor']
        left, right = expression['args']

        # +
        if op == "+":
            return _make_node(op, _diff(left), _diff(right))

        # -
        elif op == "-":
            return _make_node(op, _diff(left), _diff(right))

        # * product rule
        elif op == "*":
            return _make_node("+",
                              _make_node("*", left, _diff(right)),
                              _make_node("*", _diff(left), right))

        # quotient rule 
        elif op == "/":
            return _make_node("/",
                              _make_node("-",
                                         _make_node("*",
                                                    right,
                                                    _diff(left)),
                                         _make_node("*",
                                                    _diff(right),
                                                    left)),
                              _make_node("*",
                                         right,
                                         right))

        # simple exponent rule (why use this when we implement chain rule?)
        elif op == "^" or op == "**":
            diff_exponent = _make_node("-",
                                       right, "1")
            return _make_node("*",
                              _make_node("*",
                                         right,
                                         _make_node("^",
                                                    left, diff_exponent)),
                              _diff(left))

    elif _is_function(expression):

        fun = expression['function']
        arg = expression['args']

        if fun == "sin":
            return _make_node("*",
                              {"function": "cos",
                               "args": arg},
                              _diff(arg))

        if fun == "cos":
            return _make_node("*",
                              _make_node("*",
                                         {"function": "sin",
                                          "args": arg},
                                         _diff(arg)),
                              "-1")
                              

        if fun == "exp":
            return _make_node("*",
                              {"function": "exp",
                               "args": arg},
                              _diff(arg))

        if fun == "log":
            return _make_node("/",
                              _diff(arg),
                              arg)

        else:
            print("Unimplemented differential on function")
            return None
    else:
        print("Unrecognised token")
        return None 

def _priority (optor):
    """Pulls priority value for any given operator"""
    if optor in ["+", "-"]: return 1
    if optor in ["*", "/"]: return 2
    if optor in ["**", "^"]: return 3
    
def _to_string (node, parent_priority = 0): 
    """Converts formatted expression back to user entry format"""

    # termination condition
    if isinstance(node, (str)): return node

    # function refactor
    if isinstance(node, (dict)) and _is_function(node):
        return f"{node['function']}({_to_string(node['args'])})"

    # operator recall
    if isinstance(node, (dict)) and _is_operator(node):
        op = node['optor']
        left, right = node['args']
        priority = _priority(op)

        # recursive call
        left_str = _to_string(left, priority)

        if op in ("^", "**"):
            right_parent_priority = priority - 1
        elif op in ("/", "-"):
            right_parent_priority = priority + 1
        else:
            right_parent_priority = priority  

        right_str = _to_string(right, right_parent_priority)
        
        expr = f"{left_str}{op}{right_str}"

        if priority < parent_priority:
            return f"({expr})"

        return expr

def differentiator (user_entry): 
    """Differentiates Python strings formatted according to API
    all differentiation done with respect to x, any other non-
    function treated as a constant."""

    # considered globally defining a function list but decided better here
    functs = ["sin", "cos", "log", "exp"]

    expression = _formatter(user_entry, functs)

    if expression == None:
        return None 

    differenced = _diff(expression, functs)
    if differenced == None:
        return None 

    return _to_string(differenced)


# example calls 
if __name__ == "__main__":

    differentiator("4")
    differentiator("(-4+4)")
    differentiator("(sin(x)+2)")
    differentiator("(cos(x) * (x^2))")
    differentiator("(cos(x)/(x^2))")
    differentiator("(cos((exp(x))/(x^12))+(x^2))")
