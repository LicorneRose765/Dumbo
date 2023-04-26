import ply.lex as lex
import ply.yacc as yacc
import os
from lark import Lark, Transformer, Token, Tree
import sys
from pathlib import Path

# *-------------------------------------------------------------------------------------------------------------------*
#     VARS
# *-------------------------------------------------------------------------------------------------------------------*

verbose = True

states = (
    ("IN", "exclusive"),  # state 'IN'  : when inside dumbo code
)

start = "PROGRAM"

variables_table = {}

# *-------------------------------------------------------------------------------------------------------------------*
#     METHODS
# *-------------------------------------------------------------------------------------------------------------------*


def assign(variable_name, value):
    """Assigns the value 'value' to the variable named 'variable_name'."""
    print(f"Assigning {value:} to {variable_name:}")
    variables_table[variable_name] = value


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
        print(variables_table)


# *-------------------------------------------------------------------------------------------------------------------*
#     TOKENS
# *-------------------------------------------------------------------------------------------------------------------*

reserved = {
    "PRINT": "print",
    "FOR": "for",
    "IN": "in",
    "DO": "do",
    "ENDFOR": "endfor",
    "SEMICOLON": ";",
    "COMMA": ",",
    "LPAREN": "(",
    "RPAREN": ")",
    "DOT": ".",
    "ASSIGN": ":="
}

tokens = tuple(reserved.keys()) + (
    "OPENING",
    "CLOSING",
    "TXT",
    "STRING",
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
    # INITIAL -> IN
    t.lexer.level = 1
    t.lexer.begin('IN')
    return t


def t_IN_OPENING(t):
    """{{"""
    t.lexer.level += 1
    return t


def t_IN_CLOSING(t):
    """}}"""
    t.lexer.level -= 1

    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')

    return t


def t_CLOSING(t):
    """}}"""
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


def t_IN_ASSIGN(t):
    """:="""
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
        print("Call to method p_stringlistinterior_double")
    print(f"{p[1]:}")
    print(f"{p[3]:}")
    p[0] = [p[1][1:-1]] + p[3]


def p_stringlistinterior_single(p):
    """
    STRING_LIST_INTERIOR : STRING
    """
    if verbose:
        print("Call to method p_stringlistinterior_single")
    p[0] = [p[1][1:-1]]


def p_stringlist(p):
    """
    STRING_LIST : LPAREN STRING_LIST_INTERIOR RPAREN
    """
    if verbose:
        print("Call to method p_stringlist")
    p[0] = p[2]


def p_expression_assignments(p):
    """
    EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION
               | VARIABLE ASSIGN STRING_LIST
    """
    if verbose:
        print("Call to method p_expression_assignments")
    value = p[3]
    variable_name = p[1]
    assign(variable_name, value)
    p[0] = ''


def p_stringexpression_double(p):
    """
    STRING_EXPRESSION : STRING_EXPRESSION DOT STRING_EXPRESSION
    """
    if verbose:
        print("Call to method p_stringexpression_double")
    p[0] = p[1] + p[3]


def p_string_expression_string(p):
    """
    STRING_EXPRESSION : STRING
    """
    if verbose:
        print("Call to method p_stringexpression_string")
    p[0] = p[1][1:-1]


def p_string_expression_variable(p):
    """
    STRING_EXPRESSION : VARIABLE
    """
    if verbose:
        print("Call to method p_stringexpression_variable")
    try:
        value = variables_table[p[1]]
    except KeyError:
        raise SyntaxError(f"Cannot find variable {p[1]} in the scope.")
    p[0] = value


def p_expression_strlistfor(p):
    """
    EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR
    """
    if verbose:
        print("Call to method p_expression_strlistfor")


def p_expression_varfor(p):
    """
    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR
    """
    if verbose:
        print("Call to method p_expression_varfor")


def p_expression_print(p):
    """
    EXPRESSION : PRINT STRING_EXPRESSION
    """
    if verbose:
        print("Call to method p_expression_print")
    p[0] = p[2]


def p_dumboblock(p):
    """
    DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING
    """
    if verbose:
        print("Call to method p_dumboblock")
    p[0] = "".join(p[2])


def p_expression_list_single(p):
    """
    EXPRESSION_LIST : EXPRESSION SEMICOLON
    """
    if verbose:
        print("Call to method p_expression_list_single")
    p[0] = [p[1]]


def p_expression_list_multiple(p):
    """
    EXPRESSION_LIST : EXPRESSION SEMICOLON EXPRESSION_LIST
    """
    if verbose:
        print("Call to method p_expression_list_multiple")
    p[0] = [p[1]] + p[3]


def p_program_double(p):
    """
    PROGRAM : DUMBO_BLOCK PROGRAM
            | TXT PROGRAM
    """
    if verbose:
        print("Call to method p_program_double")
    p[0] = p[1] + p[2]


def p_program_single(p):
    """
    PROGRAM : DUMBO_BLOCK
            | TXT
    """
    if verbose:
        print("Call to method p_program_single")
    p[0] = p[1]


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
        lexer.input(input())
        for token in lexer:
            print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")

        parser = yacc.yacc(start=start, debug=True)
        infinite_yacc()