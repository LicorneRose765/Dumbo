import ply.lex as lex
import ply.yacc as yacc
import os
from lark import Lark, Transformer, Token, Tree
import sys
from pathlib import Path

# *-------------------------------------------------------------------------------------------------------------------*
#     VARS
# *-------------------------------------------------------------------------------------------------------------------*

start = "PROGRAM"

# *-------------------------------------------------------------------------------------------------------------------*
#     TOKENS
# *-------------------------------------------------------------------------------------------------------------------*

reserved = {
    "PRINT": "print",
    "FOR": "for",
    "IN": "in",
    "DO": "do",
    "ENDFOR": "endfor",
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
t_VARIABLE = r"[a-zA-Z_]\w*"
t_ignore = ' \t'

# *-------------------------------------------------------------------------------------------------------------------*
#     TOKEN METHODS
# *-------------------------------------------------------------------------------------------------------------------*


# I have to define these two as methods so I can give string the priority
def t_OPENING(t):
    """\{\{"""
    return t


def t_CLOSING(t):
    """\}\}"""
    return t


def t_STRING(t):
    """'[^']*'"""
    return t


def t_PRINT(t):
    """print"""
    return t


def t_FOR(t):
    """for"""
    return t


def t_IN(t):
    """in"""
    return t


def t_DO(t):
    """do"""
    return t


def t_ENDFOR(t):
    """endfor"""
    return t


def t_ASSIGN(t):
    """assign"""
    return t


def t_TXT(t):
    """(?!.*\{\{).+"""
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character : {t.value[0]}")
    t.lexer.skip(1)

# *-------------------------------------------------------------------------------------------------------------------*
#     GRAMMAR METHODS
# *-------------------------------------------------------------------------------------------------------------------*


def p_stringlistinterior_double(p):
    """
    STRING_LIST_INTERIOR : STRING ',' STRING_LIST_INTERIOR
    """
    return p


def p_stringlistinterior_single(p):
    """
    STRING_LIST_INTERIOR : STRING
    """
    return p


def p_stringlist(p):
    """
    STRING_LIST : '(' STRING_LIST_INTERIOR ')'
    """
    return p


def p_expression_assignments(p):
    """
    EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION
               | VARIABLE ASSIGN STRING_LIST
    """
    return p


def p_stringexpression_double(p):
    """
    STRING_EXPRESSION : STRING_EXPRESSION '.' STRING_EXPRESSION
    """
    return p


def p_stringexpression_single(p):
    """
    STRING_EXPRESSION : STRING
                      | VARIABLE
    """
    return p


def p_expression_strlistfor(p):
    """
    EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR
    """
    return p


def p_expression_varfor(p):
    """
    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR
    """
    return p


def p_expression_print(p):
    """
    EXPRESSION : PRINT STRING_EXPRESSION
    """
    return p


def p_dumboblock(p):
    """
    DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING
    """
    return p


def p_expressionlist(p):
    """
    EXPRESSION_LIST : EXPRESSION ';'
                    | EXPRESSION ';' EXPRESSION_LIST
    """
    print("Encountered EXPRESSION_LIST : EXPRESSION | EXPRESSION ; EXPRESSION_LIST")
    return p


def p_program_double(p):
    """
    PROGRAM : TXT PROGRAM
            | DUMBO_BLOCK PROGRAM
    """
    print("Encountered PROGRAM : TXT PROGRAM | DUMBO_BLOCK PROGRAM")
    p[0] = p[1] + p[2]  # TODO : pas sûr
    return p


def p_program_single_dumboblock(p):
    """
    PROGRAM : DUMBO_BLOCK
    """
    print("Encountered PROGRAM : DUMBO_BLOCK")
    p[0] = p[1]  # TODO : pas sûr
    return p


def p_program_single_txt(p):
    """
    PROGRAM : TXT
    """
    print("Encountered PROGRAM : TXT")
    p[0] = p[1]  # TODO : pas sûr
    return p


# *-------------------------------------------------------------------------------------------------------------------*
#     MAIN
# *-------------------------------------------------------------------------------------------------------------------*


if __name__ == "__main__":
    """
    if len(sys.argv) != 3:
        print('Usage: python3 dumbo.py <data> <template>')
        exit(1)
    data_content = open(Path(os.getcwd()) / sys.argv[1], "r").readlines()
    template_content = open(Path(os.getcwd()) / sys.argv[2], "r").readlines()
    """

    import sys

    lexer = lex.lex()
    lexer.input(input())
    for token in lexer:
        print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")

    parser = yacc.yacc(start=start, debug=True)
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if s == "":
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
