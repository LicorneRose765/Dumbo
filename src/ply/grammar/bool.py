verbose = True


def p_IN_booleanexpression(p):
    """
    BOOLEAN_EXPRESSION : BOOLEAN BOOLEAN_OPERATOR BOOLEAN
    """
    operator = p[2]
    left = p[1]
    right = p[3]
    if operator == "and":
        p[0] = left and right
    else:
        p[0] = left or right


def p_IN_booleanexpression_simple(p):
    """
    BOOLEAN_EXPRESSION : BOOLEAN
    """
    p[0] = p[1]


def p_IN_boolean(p):
    """
    BOOLEAN : TRUE
            | FALSE
    """
    p[0] = bool(p[1])


def p_IN_booleanoperator_and(p):
    """
    BOOLEAN_OPERATOR : AND
    """
    p[0] = p[1]


def p_IN_booleanoperator_or(p):
    """
    BOOLEAN_OPERATOR : OR
    """
    p[0] = p[1]


def p_IN_integercomparison(p):
    """
    BOOLEAN_EXPRESSION : MATH_EXPRESSION INTEGER_COMPARATOR MATH_EXPRESSION
    """
    operator = p[2]
    left = int(p[1])
    right = int(p[3])
    if operator == "<":
        p[0] = left < right
    elif operator == ">":
        p[0] = left > right
    elif operator == "=":
        p[0] = left == right
    elif operator == "!=":
        p[0] = left != right


def p_IN_integercomparator(p):
    """
    INTEGER_COMPARATOR : LT
                       | GT
                       | EQ
                       | NE
    """
    p[0] = p[1]