from .operation import MathOperation, GetOperation
from .symbols_table import symbols_table
from . import params


def p_mathexpression_plus(p):
    """
    MATH_EXPRESSION : MATH_EXPRESSION ADD TERM
    """
    p[0] = MathOperation(p[1], p[2], p[3], params.current_scope_depth)


def p_mathexpression_minus(p):
    """
    MATH_EXPRESSION : MATH_EXPRESSION SUB TERM
    """
    p[0] = MathOperation(p[1], p[2], p[3], params.current_scope_depth)


def p_mathexpression_TERM(p):
    """
    MATH_EXPRESSION : TERM
    """
    p[0] = p[1]


def p_term_times(p):
    """
    TERM : TERM MUL FACTOR
    """
    p[0] = MathOperation(p[1], p[2], p[3], params.current_scope_depth)


def p_term_div(p):
    """
    TERM : TERM DIV FACTOR
    """
    p[0] = MathOperation(p[1], p[2], p[3], params.current_scope_depth)


def p_term_factor(p):
    """
    TERM : FACTOR
    """
    p[0] = p[1]


def p_factor_num(p):
    """
    FACTOR : INTEGER
    """
    p[0] = int(p[1])


def p_factor_var(p):
    """
    FACTOR : VARIABLE
    """
    p[0] = GetOperation(p[1], params.current_scope_depth)
