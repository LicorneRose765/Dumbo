from .operation import BoolOperation, GetOperation
from . import params


def p_booleanexpression_or(p):
    """
    BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION OR BOOLEAN_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_booleanexpression_or : BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION OR BOOLEAN_EXPRESSION")
    operator = p[2]
    left = p[1]
    right = p[3]
    p[0] = BoolOperation(left, operator, right, params.current_scope_depth)


def p_booleanexpression(p):
    """
    BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION_AND
    """
    if params.verbose:
        print("Call to method p_booleanexpression : BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION_AND")
    p[0] = p[1]


def p_booleanexpression_simple(p):
    """
    BOOLEAN_EXPRESSION_AND : BOOLEAN
                           | BOOLEAN_MATH_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_booleanexpression_simple : BOOLEAN_EXPRESSION : BOOLEANpression_simple : ")
    p[0] = p[1]


def p_booleanexpression_double(p):
    """
    BOOLEAN_EXPRESSION_AND : BOOLEAN_EXPRESSION_AND AND BOOLEAN_EXPRESSION_AND
    """
    if params.verbose:
        print("Call to method p_booleanexpression_simple : BOOLEAN_EXPRESSION_AND : BOOLEAN_EXPRESSION_AND AND BOOLEAN_EXPRESSION_AND")
    operator = p[2]
    left = p[1]
    right = p[3]
    p[0] = BoolOperation(left, operator, right, params.current_scope_depth)


def p_boolean(p):
    """
    BOOLEAN : TRUE
            | FALSE
    """
    if params.verbose:
        print("Call to method p_boolean : BOOLEAN : TRUE    \n| FALSE")
    p[0] = p[1] == "True"


def p_integercomparison(p):
    """
    BOOLEAN_MATH_EXPRESSION : MATH_EXPRESSION INTEGER_COMPARATOR MATH_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_integercomparison : BOOLEAN_EXPRESSION : MATH_EXPRESSION INTEGER_COMPARATOR MATH_EXPRESSION")
    operator = p[2]
    left = p[1]
    right = p[3]
    if isinstance(left, str):
        left = int(left)
    elif isinstance(left, GetOperation):
        left = p[1]
    if isinstance(right, str):
        right = int(right)
    elif isinstance(right, GetOperation):
        right = p[3]
    p[0] = BoolOperation(left, operator, right, params.current_scope_depth)


def p_integercomparator(p):
    """
    INTEGER_COMPARATOR : LT
                       | GT
                       | EQ
                       | NE
    """
    if params.verbose:
        print("Call to method p_integercomparator : INTEGER_COMPARATOR : LT    \n| GT    \n| EQ    \n| NE")
    p[0] = p[1]
