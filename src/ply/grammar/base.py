from .symbols_table import symbols_table
from .operation import *
from . import params

states = (
    ("IN", "exclusive"),  # state 'IN'  : when inside dumbo code
)


def p_stringlistinterior_double(p):
    """
    STRING_LIST_INTERIOR : STRING COMMA STRING_LIST_INTERIOR
    """
    if params.verbose:
        print("Call to method p_stringlistinterior_double : STRING_LIST_INTERIOR : STRING COMMA STRING_LIST_INTERIOR")
        print(f"{p[1]:}")
        print(f"{p[3]:}")
    p[0] = [p[1][1:-1]] + p[3]


def p_stringlistinterior_single(p):
    """
    STRING_LIST_INTERIOR : STRING
    """
    if params.verbose:
        print("Call to method p_stringlistinterior_single : STRING_LIST_INTERIOR : STRING")
    p[0] = [p[1][1:-1]]


def p_stringlist(p):
    """
    STRING_LIST : LPAREN STRING_LIST_INTERIOR RPAREN
    """
    if params.verbose:
        print("Call to method p_stringlist : STRING_LIST : LPAREN STRING_LIST_INTERIOR RPAREN")
    p[0] = p[2]


def p_expression_assignments(p):
    """
    EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION
               | VARIABLE ASSIGN STRING_LIST
               | VARIABLE ASSIGN MATH_EXPRESSION
               | VARIABLE ASSIGN BOOLEAN_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_expression_assignments : EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION\n           | VARIABLE ASSIGN STRING_LIST\n           | VARIABLE ASSIGN MATH_EXPRESSION")
    value = p[3]
    variable_name = p[1]
    if isinstance(value, StringExpressionNode):
        value = value.execute()
    p[0] = AssignOperation(variable_name, value, params.current_scope_depth)


def p_stringexpression_double(p):
    """
    STRING_EXPRESSION : STRING_EXPRESSION DOT STRING_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_stringexpression_double : STRING_EXPRESSION : STRING_EXPRESSION DOT STRING_EXPRESSION")
    p[0] = StringExpressionNode(None, False, params.current_scope_depth, p[1], p[3])


def p_string_expression_string(p):
    """
    STRING_EXPRESSION : STRING
    """
    if params.verbose:
        print("Call to method p_stringexpression_string : STRING_EXPRESSION : STRING")
    p[0] = StringExpressionNode(p[1][1:-1], False, params.current_scope_depth, None, None)
    # p[0] = p[1][1:-1]


def p_string_expression_variable(p):
    """
    STRING_EXPRESSION : VARIABLE
    """
    if params.verbose:
        print("Call to method p_stringexpression_variable : STRING_EXPRESSION : VARIABLE")
    p[0] = StringExpressionNode(p[1], True, params.current_scope_depth, None, None)
    """
    value = get(p[1], params.current_scope_depth)
    if type(value) == str:
        p[0] = value
    elif type(value) == list or type(value) == tuple:
        p[0] = ", ".join(value)
    else:
        p[0] = str(value)
    """

def p_expression_strlistfor(p):
    """
    EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR
    """
    if params.verbose:
        print("Call to method p_expression_strlistfor : EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR")
    temporary_variable_name = p[2]
    string_list = p[4]
    body = p[6]
    p[0] = ForOperation(temporary_variable_name, string_list, body, params.current_scope_depth)


def p_expression_varfor(p):
    """
    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR
    """
    if params.verbose:
        print("Call to method p_expression_varfor : EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR")
    temporary_variable_name = p[2]
    string_list = get(p[4], params.current_scope_depth - 1)
    body = p[6]
    p[0] = ForOperation(temporary_variable_name, string_list, body, params.current_scope_depth)


def p_expression_print(p):
    """
    EXPRESSION : PRINT STRING_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_expression_print : EXPRESSION : PRINT STRING_EXPRESSION")
    p[0] = PrintOperation(p[2])


def p_expression_mathexpression(p):
    """
    EXPRESSION : MATH_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_expression_mathexpression : EXPRESSION : MATH_EXPRESSION")
    p[0] = p[1]


def p_expression_booleanexpression(p):
    """
    EXPRESSION : BOOLEAN_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_expression_booleanexpression : EXPRESSION : BOOLEAN_EXPRESSION")
    p[0] = p[1]


def p_expression_ifexpression(p):
    """
    EXPRESSION : IF_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_expression_ifexpression : EXPRESSION : IF_EXPRESSION")
    p[0] = p[1]


def p_ifexpression(p):
    """
    IF_EXPRESSION : IF BOOLEAN_EXPRESSION DO EXPRESSION_LIST ENDIF
    """
    if params.verbose:
        print("Call to method p_ifexpression : IF_EXPRESSION : IF BOOLEAN_EXPRESSION DO EXPRESSION_LIST ENDIF")
    params.current_scope_depth += 1
    condition = p[2]
    body = p[4]
    p[0] = IfOperation(condition, body, params.current_scope_depth)


def p_expression_list_single(p):
    """
    EXPRESSION_LIST : EXPRESSION SEMICOLON
    """
    if params.verbose:
        print("Call to method p_expression_list_single : EXPRESSION_LIST : EXPRESSION SEMICOLON")
    p[0] = [p[1]]


def p_expression_list_multiple(p):
    """
    EXPRESSION_LIST : EXPRESSION SEMICOLON EXPRESSION_LIST
    """
    if params.verbose:
        print("Call to method p_expression_list_multiple : EXPRESSION_LIST : EXPRESSION SEMICOLON EXPRESSION_LIST")
    p[0] = [p[1]] + p[3]


def p_dumboblock(p):
    """
    DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING
    """
    if params.verbose:
        print("Call to method p_dumboblock : DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING")
    p[0] = p[2]


def p_program_double_dbp(p):
    """
    PROGRAM : DUMBO_BLOCK PROGRAM
    """
    if params.verbose:
        print("Call to method p_program_double : PROGRAM : DUMBO_BLOCK PROGRAM")
    p[0] = [p[1], p[2]]


def p_program_double_tp(p):
    """
    PROGRAM : TXT PROGRAM
    """
    if params.verbose:
        print("Call to method p_program_double : PROGRAM : TXT PROGRAM")
    p[0] = [TextBlock(p[1]), p[2]]


def p_program_single_db(p):
    """
    PROGRAM : DUMBO_BLOCK
    """
    if params.verbose:
        print("Call to method p_program_single_db : PROGRAM : DUMBO_BLOCK")
    p[0] = p[1]


def p_program_single_txt(p):
    """
    PROGRAM : TXT
    """
    if params.verbose:
        print("Call to method p_program_single : PROGRAM : TXT")
    p[0] = TextBlock(p[1])
