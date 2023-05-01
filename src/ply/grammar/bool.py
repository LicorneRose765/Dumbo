from .operation import BoolOperation, GetOperation
from . import params


def p_booleanexpression(p):
    """
    BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION BOOLEAN_OPERATOR BOOLEAN_EXPRESSION
    """
    if params.verbose:
        print("Call to method p_booleanexpression : BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION BOOLEAN_OPERATOR BOOLEAN_EXPRESSION")
    operator = p[2]
    left = p[1]
    right = p[3]
    p[0] = BoolOperation(left, operator, right, params.current_scope_depth)


def p_booleanexpression_simple(p):
    """
    BOOLEAN_EXPRESSION : BOOLEAN
    """
    if params.verbose:
        print("Call to method p_booleanexpression_simple : BOOLEAN_EXPRESSION : BOOLEANpression_simple : ")
    p[0] = p[1]


def p_boolean(p):
    """
    BOOLEAN : TRUE
            | FALSE
    """
    if params.verbose:
        print("Call to method p_boolean : BOOLEAN : TRUE    \n| FALSE")
    p[0] = bool(p[1])


def p_booleanoperator_and(p):
    """
    BOOLEAN_OPERATOR : AND
    """
    if params.verbose:
        print("Call to method p_booBOOLEAN_OPERATOR : ANDleanoperator_and : ")
    p[0] = p[1]


def p_booleanoperator_or(p):
    """
    BOOLEAN_OPERATOR : OR
    """
    if params.verbose:
        print("Call to method p_boBOOLEAN_OPERATOR : ORoleanoperator_or : ")
    p[0] = p[1]


def p_integercomparison(p):
    """
    BOOLEAN_EXPRESSION : MATH_EXPRESSION INTEGER_COMPARATOR MATH_EXPRESSION
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
        left = p[1]
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
