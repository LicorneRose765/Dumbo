from .operation import MathOperation, GetOperation
from . import params


def p_mathexpression_addsubmuldiv(p):
    """
    MATH_EXPRESSION : MATH_EXPRESSION SUB TERM
                    | MATH_EXPRESSION ADD TERM
                    | TERM MUL FACTOR
                    | TERM DIV FACTOR
    """
    p[0] = MathOperation(p[1], p[2], p[3], params.current_scope_depth)


def p_mathexpression_term(p):
    """
    MATH_EXPRESSION : TERM
    """
    p[0] = p[1]


def p_term_factor(p):
    """
    TERM : FACTOR
    """
    p[0] = p[1]


def p_factor_int(p):
    """
    FACTOR : INTEGER
    """
    p[0] = int(p[1])


def p_factor_var(p):
    """
    FACTOR : VARIABLE
    """
    p[0] = GetOperation(p[1], params.current_scope_depth)
