import ply.lex as lex
import os
from lark import Lark, Transformer, Token, Tree
import sys
from pathlib import Path

tokens = (
    "PROGRAM",
    "DUMBO_BLOCK",
    "EXPRESSION_LIST",
    "EXPRESSION",
    "STRING_EXPRESSION",
    "STRING_LIST",
    "STRING_LIST_INTERIOR",
    "TXT",
    "STRING",
    "VARIABLE"
)

t_TXT = r"(?!.*\{\{).+"
t_STRING = r"'[^']*'"
t_VARIABLE = r"[a-zA-Z_]\w*"
t_ignore = ' \t'


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character : {t.value[0]}")
    t.lexer.skip(1)


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
    lexer.input(sys.stdin.read())
    for token in lexer:
        print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")
