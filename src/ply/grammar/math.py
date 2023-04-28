verbose = True


def p_IN_mathexpression_plus(p):
    """
    MATH_EXPRESSION : MATH_EXPRESSION ADD TERM
    """
    p[0] = str(int(p[1]) + int(p[3]))


def p_IN_mathexpression_minus(p):
    """
    MATH_EXPRESSION : MATH_EXPRESSION SUB TERM
    """
    p[0] = str(int(p[1]) - int(p[3]))


def p_IN_mathexpression_TERM(p):
    """
    MATH_EXPRESSION : TERM
    """
    p[0] = str(int(p[1]))


def p_IN_term_times(p):
    """
    TERM : TERM MUL FACTOR
    """
    p[0] = str(int(p[1]) * int(p[3]))


def p_IN_term_div(p):
    """
    TERM : TERM DIV FACTOR
    """
    p[0] = str(int(int(p[1]) / int(p[3])))


def p_IN_term_factor(p):
    """
    TERM : FACTOR
    """
    p[0] = p[1]


def p_IN_factor_num(p):
    """
    FACTOR : INTEGER
    """
    p[0] = p[1]