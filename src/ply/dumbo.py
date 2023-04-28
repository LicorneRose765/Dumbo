import ply.lex as lex
import ply.yacc as yacc
import os
import sys
from pathlib import Path
from symbols_table import SymbolsTable

# *-------------------------------------------------------------------------------------------------------------------*
#     VARS
# *-------------------------------------------------------------------------------------------------------------------*

verbose = False

states = (
    ("IN", "exclusive"),  # state 'IN'  : when inside dumbo code
)

start = "PROGRAM"

symbols_table = SymbolsTable()

current_scope_depth = 0

# *-------------------------------------------------------------------------------------------------------------------*
#     METHODS
# *-------------------------------------------------------------------------------------------------------------------*


def assign(variable_name, value, scope_depth):
    """Assigns the value 'value' to the variable named 'variable_name' at the scope depth 'scope_depth' via the symbols table."""
    symbols_table.assign(variable_name, value, scope_depth)


def get(variable_name, scope_depth):
    return symbols_table.get(variable_name, scope_depth)


def infinite_yacc():
    while True:
        try:
            s = input('doombo > ')
        except EOFError:
            break
        if s == "":
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
        if verbose:
            print("===== SYMBOLS TABLE =====")
            print(symbols_table)
            print("===== ======= ===== =====")


# *-------------------------------------------------------------------------------------------------------------------*
#     TOKENS
# *-------------------------------------------------------------------------------------------------------------------*

reserved = {
    "PRINT": "print",
    "FOR": "for",
    "IN": "in",
    "DO": "do",
    "ENDFOR": "endfor",
    "TRUE": "true",
    "FALSE": "false",
    "IF": "if",
    "ENDIF": "endif"
}

specials = {
    "SEMICOLON": ";",
    "COMMA": ",",
    "LPAREN": "(",
    "RPAREN": ")",
    "DOT": ".",
    "ASSIGN": ":="
}

ops = {
    "ADD": "+",
    "SUB": "-",
    "MUL": "*",
    "DIV": "/",
    "LT": "<",
    "GT": ">",
    "EQ": "=",
    "NE": "!=",
    "AND": "and",
    "OR": "or"
}

tokens = tuple(reserved.keys()) + tuple(specials.keys()) + tuple(ops.keys()) + (
    "OPENING",
    "CLOSING",
    "TXT",
    "STRING",
    "INTEGER",
    "VARIABLE"
)

# *-------------------------------------------------------------------------------------------------------------------*
#     TOKEN REGEX
# *-------------------------------------------------------------------------------------------------------------------*

# t_TXT = r"(?!.*\{\{).+"
# t_STRING = r"'[^']*'"
t_ignore = ' \t'
t_IN_ignore = ' \t'


# *-------------------------------------------------------------------------------------------------------------------*
#     TOKEN METHODS
# *-------------------------------------------------------------------------------------------------------------------*


# I have to define these two as methods so I can give string the priority
def t_OPENING(t):
    """{{"""
    global current_scope_depth
    # INITIAL -> IN
    t.lexer.level = 1
    current_scope_depth = 1
    if verbose:
        print(f"Current scope depth changed to {current_scope_depth=:} because of first opening {'{{'}")
    symbols_table.init_depth_entry(current_scope_depth)
    t.lexer.begin('IN')
    return t


def t_IN_OPENING(t):
    """{{"""
    global current_scope_depth
    t.lexer.level += 1
    current_scope_depth += 1
    if verbose:
        print(f"Current scope depth changed to {current_scope_depth=:} because of new opening {'{{'}")
    symbols_table.init_depth_entry(current_scope_depth)
    return t


def t_IN_CLOSING(t):
    """}}"""
    global current_scope_depth
    t.lexer.level -= 1
    symbols_table.delete(current_scope_depth)
    current_scope_depth -= 1
    if verbose:
        print(f"Current scope depth changed to {current_scope_depth=:} because of closing {'}}'}")
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')
    return t


def t_CLOSING(t):
    """}}"""
    if verbose:
        print(f"Unexpected '{t.value[0]*2}' at line {lexer.lineno}")


def t_IN_SEMICOLON(t):
    """;"""
    return t


def t_IN_COMMA(t):
    ""","""
    return t


def t_IN_LPAREN(t):
    """\("""
    return t


def t_IN_RPAREN(t):
    """\)"""
    return t


def t_IN_DOT(t):
    """\."""
    return t


def t_IN_STRING(t):
    """'[^']*'"""
    return t


def t_IN_PRINT(t):
    """print"""
    return t


def t_IN_FOR(t):
    """for"""
    return t


def t_IN_IN(t):
    """in"""
    return t


def t_IN_DO(t):
    """do"""
    return t


def t_IN_ENDFOR(t):
    """endfor"""
    return t


def t_IN_TRUE(t):
    """true"""
    return t


def t_IN_FALSE(t):
    """false"""
    return t


def t_IN_IF(t):
    """if"""
    return t


def t_IN_ENDIF(t):
    """endif"""
    return t


def t_IN_ASSIGN(t):
    """:="""
    return t


def t_IN_ADD(t):
    """\+"""
    return t


def t_IN_SUB(t):
    """\-"""
    return t


def t_IN_MUL(t):
    """\*"""
    return t


def t_IN_DIV(t):
    """\/"""
    return t


def t_IN_LT(t):
    """\<"""
    return t


def t_IN_GT(t):
    """\>"""
    return t


def t_IN_EQ(t):
    """\="""
    return t


def t_IN_NE(t):
    """\!\="""
    return t


def t_IN_AND(t):
    """and"""
    return t


def t_IN_OR(t):
    """or"""
    return t


def t_IN_INTEGER(t):
    """\d+"""
    return t


def t_IN_VARIABLE(t):
    """[a-zA-Z_]\w*"""
    return t


def t_TXT(t):
    """[^{]+"""  # """(?!.*{{).+"""
    return t


def t_ANY_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_IN_error(t):
    print(f"Illegal character in dumbo code : {t.value[0]}")
    t.lexer.skip(1)


def t_error(t):
    print(f"Illegal character in initial state : {t.value[0]}")
    t.lexer.skip(1)


# *-------------------------------------------------------------------------------------------------------------------*
#     GRAMMAR METHODS
# *-------------------------------------------------------------------------------------------------------------------*


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


def p_expression_varfor(p):
    """
    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR
    """
    if verbose:
        print("Call to method p_expression_varfor : EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR")


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
    BOOLEAN_EXPRESSION : INTEGER INTEGER_COMPARATOR INTEGER
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


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} (value='{p.value}')")
        while True:
            tok = parser.token()  # Get the next token
            if not tok or tok.type == 'CLOSING':
                break
        parser.errok()

        # Return CLOSING to the parser as the next lookahead token
        return tok
    else:
        print("Syntax error at EOF")


# *-------------------------------------------------------------------------------------------------------------------*
#     MAIN
# *-------------------------------------------------------------------------------------------------------------------*


if __name__ == "__main__":
    if len(sys.argv) != 1:
        if len(sys.argv) != 3:
            print('Usage: python3 dumbo.py <data> <template>')
            exit(1)
        data_content = open(Path(os.getcwd()) / sys.argv[1], "r").readlines()
        data_content_as_str = "".join(data_content)
        template_content = open(Path(os.getcwd()) / sys.argv[2], "r").readlines()
        template_content_as_str = "".join(template_content)

        print("=========")
        print("   LEX   ")
        print("=========")
        print()
        print("Content that will be lexed :")
        print()
        print(data_content_as_str)
        print()

        lexer = lex.lex()
        lexer.input(data_content_as_str)
        for token in lexer:
            print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")

        print()
        print()
        print("=========")
        print("  YACC   ")
        print("=========")
        print()
        print("Content that will be yacced :")
        print()
        print(data_content_as_str)
        print()

        parser = yacc.yacc(start=start, debug=True)
        result = parser.parse(data_content_as_str)
        print(result)

        infinite_yacc()
    else:
        lexer = lex.lex()
        """lexer.input(input())
        for token in lexer:
            print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")
        """
        parser = yacc.yacc(start=start, debug=True)
        # expression = "{{ a := '2'; b := '4'; {{ c := '6'; print a; print b; print c; }} print c; }}"
        expression = "{{ if true do print 'true'; endif }}"
        print(f"{expression} = {parser.parse(expression)}")
