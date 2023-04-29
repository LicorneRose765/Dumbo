from .symbols_table import symbols_table

verbose = True

current_scope_depth = 0

states = (
    ("IN", "exclusive"),  # state 'IN'  : when inside dumbo code
)


def assign(variable_name, value, scope_depth):
    """Assigns the value 'value' to the variable named 'variable_name' at the scope depth 'scope_depth' via the symbols.py table."""
    symbols_table.assign(variable_name, value, scope_depth)


def get(variable_name, scope_depth):
    return symbols_table.get(variable_name, scope_depth)


def p_stringlistinterior_double(p):
    """
    STRING_LIST_INTERIOR : STRING COMMA STRING_LIST_INTERIOR
    """
    if verbose:
        print("Call to method p_stringlistinterior_double : STRING_LIST_INTERIOR : STRING COMMA STRING_LIST_INTERIOR")
        print(f"{p[1]:}")
        print(f"{p[3]:}")
    p[0] = [p[1][1:-1]] + p[3]


def p_stringlistinterior_single(p):
    """
    STRING_LIST_INTERIOR : STRING
    """
    if verbose:
        print("Call to method p_stringlistinterior_single : STRING_LIST_INTERIOR : STRING")
    p[0] = [p[1][1:-1]]


def p_stringlist(p):
    """
    STRING_LIST : LPAREN STRING_LIST_INTERIOR RPAREN
    """
    if verbose:
        print("Call to method p_stringlist : STRING_LIST : LPAREN STRING_LIST_INTERIOR RPAREN")
    p[0] = p[2]


def p_expression_assignments(p):
    """
    EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION
               | VARIABLE ASSIGN STRING_LIST
               | VARIABLE ASSIGN MATH_EXPRESSION
               | VARIABLE ASSIGN BOOLEAN_EXPRESSION
    """
    if verbose:
        print("Call to method p_expression_assignments : EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION\n           | VARIABLE ASSIGN STRING_LIST\n           | VARIABLE ASSIGN MATH_EXPRESSION")
    value = p[3]
    variable_name = p[1]
    assign(variable_name, value, current_scope_depth)
    p[0] = ''


def p_stringexpression_double(p):
    """
    STRING_EXPRESSION : STRING_EXPRESSION DOT STRING_EXPRESSION
    """
    if verbose:
        print("Call to method p_stringexpression_double : STRING_EXPRESSION : STRING_EXPRESSION DOT STRING_EXPRESSION")
    p[0] = p[1] + p[3]


def p_string_expression_string(p):
    """
    STRING_EXPRESSION : STRING
    """
    if verbose:
        print("Call to method p_stringexpression_string : STRING_EXPRESSION : STRING")
    p[0] = p[1][1:-1]


def p_string_expression_variable(p):
    """
    STRING_EXPRESSION : VARIABLE
    """
    if verbose:
        print("Call to method p_stringexpression_variable : STRING_EXPRESSION : VARIABLE")
    value = get(p[1], current_scope_depth)
    if type(value) == str:
        p[0] = value
    elif type(value) == list or type(value) == tuple:
        p[0] = ", ".join(value)
    else:
        p[0] = str(value)


def p_expression_strlistfor(p):
    """
    EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR
    """
    if verbose:
        print("Call to method p_expression_strlistfor : EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR")
    p[0] = "should have been a for result :("


def p_expression_varfor(p):
    """
    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR
    """
    if verbose:
        print("Call to method p_expression_varfor : EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR")
    global current_scope_depth
    iterate_over = p[4]
    iterate_over_value = get(p[4], current_scope_depth)
    if iterate_over_value is None:
        p[0] = ""
    else:
        iterator_name = p[2]
        assign(iterator_name, iterate_over_value[0], current_scope_depth)
        p[0] = "should have been a for result :("


def p_expression_print(p):
    """
    EXPRESSION : PRINT STRING_EXPRESSION
    """
    if verbose:
        print("Call to method p_expression_print : EXPRESSION : PRINT STRING_EXPRESSION")
    p[0] = p[2]


def p_expression_mathexpression(p):
    """
    EXPRESSION : MATH_EXPRESSION
    """
    if verbose:
        print("Call to method p_expression_mathexpression : EXPRESSION : MATH_EXPRESSION")
    p[0] = p[1]  # TODO : str(p[1]) ?


def p_expression_booleanexpression(p):
    """
    EXPRESSION : BOOLEAN_EXPRESSION
    """
    if verbose:
        print("Call to method p_expression_booleanexpression : EXPRESSION : BOOLEAN_EXPRESSION")
    p[0] = p[1]  # TODO : str(p[1]) ?


def p_expression_ifexpression(p):
    """
    EXPRESSION : IF_EXPRESSION
    """
    if verbose:
        print("Call to method p_expression_ifexpression : EXPRESSION : IF_EXPRESSION")
    p[0] = p[1]


def p_dumboblock(p):
    """
    DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING
    """
    if verbose:
        print("Call to method p_dumboblock : DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING")
    p[0] = "".join(p[2])


def p_expression_list_single(p):
    """
    EXPRESSION_LIST : EXPRESSION SEMICOLON
    """
    if verbose:
        print("Call to method p_expression_list_single : EXPRESSION_LIST : EXPRESSION SEMICOLON")
    p[0] = [p[1]]


def p_expression_list_multiple(p):
    """
    EXPRESSION_LIST : EXPRESSION SEMICOLON EXPRESSION_LIST
    """
    if verbose:
        print("Call to method p_expression_list_multiple : EXPRESSION_LIST : EXPRESSION SEMICOLON EXPRESSION_LIST")
    p[0] = [p[1]] + p[3]


def p_program_double(p):
    """
    PROGRAM : DUMBO_BLOCK PROGRAM
            | TXT PROGRAM
    """
    if verbose:
        print("Call to method p_program_double : PROGRAM : DUMBO_BLOCK PROGRAM\n        | TXT PROGRAM")
    p[0] = p[1] + p[2]


def p_program_single(p):
    """
    PROGRAM : DUMBO_BLOCK
            | TXT
    """
    if verbose:
        print("Call to method p_program_single : PROGRAM : DUMBO_BLOCK\n        | TXT")
    p[0] = p[1]


def p_IN_ifexpression(p):
    """
    IF_EXPRESSION : IF BOOLEAN_EXPRESSION DO EXPRESSION_LIST ENDIF
    """
    print("Call to method p_IN_ifexpression : IF_EXPRESSION : IF BOOLEAN_EXPRESSION DO EXPRESSION_LIST ENDIF")
    condition = p[2]
    if condition:
        global current_scope_depth
        current_scope_depth += 1
        # TODO what about expression list ?
    else:
        p[0] = ""
