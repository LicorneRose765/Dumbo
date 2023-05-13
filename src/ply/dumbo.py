import ply.lex as lex
import ply.yacc as yacc
import os
import sys
from pathlib import Path

import grammar.params

# *-------------------------------------------------------------------------------------------------------------------*
#     VARS
# *-------------------------------------------------------------------------------------------------------------------*

start = "PROGRAM"

# *-------------------------------------------------------------------------------------------------------------------*
#     METHODS
# *-------------------------------------------------------------------------------------------------------------------*


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
        if params.verbose:
            print("===== SYMBOLS TABLE =====")
            print(symbols_table)
            print("===== ======= ===== =====")


def dfs_result(lst):
    _res = ''
    for element in lst:
        if isinstance(element, list):
            _res += dfs_result(element)
        elif isinstance(element, Operation):
            if isinstance(element, MathOperation):
                _res += str(element.execute(1))
            else:
                _res += element.execute(1)
    return _res


def parse_data_template(data_path, template_path):
    data_content = open(Path(os.getcwd()) / data_path, "r").readlines()
    data_content_as_str = "".join(data_content)
    template_content = open(Path(os.getcwd()) / template_path, "r").readlines()
    template_content_as_str = "".join(template_content)
    content = data_content_as_str + "\n" + template_content_as_str

    result = parser.parse(content)
    interpreted = dfs_result(result)
    print(interpreted)


# *-------------------------------------------------------------------------------------------------------------------*
#     TOKENS
# *-------------------------------------------------------------------------------------------------------------------*

from grammar.tokens import *

# *-------------------------------------------------------------------------------------------------------------------*
#     GRAMMAR METHODS
# *-------------------------------------------------------------------------------------------------------------------*

from grammar.base import *
from grammar.math import *
from grammar.bool import *


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
        data_path = sys.argv[1]
        template_path = sys.argv[2]
        lexer = lex.lex()
        parser = yacc.yacc(start=start, debug=True)
        parse_data_template(data_path, template_path)
