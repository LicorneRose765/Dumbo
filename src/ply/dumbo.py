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
    "print": "PRINT",
    "for": "FOR",
    "in": "IN",
    "do": "DO",
    "endfor": "ENDFOR"
}

tokens = (
    "DUMBO_BLOCK",
    "EXPRESSION_LIST",
    "EXPRESSION",
    "STRING_EXPRESSION",
    "STRING_LIST",
    "STRING_LIST_INTERIOR",
    "TXT",
    "STRING",
    "VARIABLE"
) + tuple(reserved.values())

# *-------------------------------------------------------------------------------------------------------------------*
#     TOKEN REGEX
# *-------------------------------------------------------------------------------------------------------------------*

t_TXT = r"(?!.*\{\{).+"
t_STRING = r"'[^']*'"
t_VARIABLE = r"[a-zA-Z_]\w*"
t_ignore = ' \t'

# *-------------------------------------------------------------------------------------------------------------------*
#     TOKEN METHODS
# *-------------------------------------------------------------------------------------------------------------------*

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character : {t.value[0]}")
    t.lexer.skip(1)

# *-------------------------------------------------------------------------------------------------------------------*
#     GRAMMAR METHODS
# *-------------------------------------------------------------------------------------------------------------------*


def p_program_single(p):
    """
    PROGRAM : TXT
            | DUMBO_BLOCK
    """
    print("Encountered PROGRAM : TXT | DUMBO_BLOCK")
    p[0] = p[1]  # TODO : pas sûr


def p_program_double(p):
    """
    PROGRAM : TXT PROGRAM
            | DUMBO_BLOCK PROGRAM
            | STRING
    """
    print("Encountered PROGRAM : TXT PROGRAM | DUMBO_BLOCK PROGRAM")
    p[0] = p[1] + p[2]  # TODO : pas sûr


def p_error(p):
    print(f"Syntax error in input {p} !")


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
        if s == "": break
        if not s: continue
        result = parser.parse(s)
        print(result)
