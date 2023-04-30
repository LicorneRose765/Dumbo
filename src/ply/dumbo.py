import ply.lex as lex
import ply.yacc as yacc
import os
import sys
from pathlib import Path

# *-------------------------------------------------------------------------------------------------------------------*
#     VARS
# *-------------------------------------------------------------------------------------------------------------------*

verbose = True

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
        if verbose:
            print("===== SYMBOLS TABLE =====")
            print(symbols_table)
            print("===== ======= ===== =====")


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
        # expression = "{{ if 2 < 3 do print 'true'; print 'i am veri smart'; endif; }} {{ a := 17; b := '11'; }}"
        # expression = "{{ list := ('1', '2', '3'); for var in list do print var; endfor; }}"
        # expression = "{{ 2 + 2 * 2 - 2; }} abcd"
        expression = "{{ for myvar in ('a', 'b', 'c') do print myvar; endfor; }}"
        result = parser.parse(expression)
        s = ""
        for op in result:
            s += str(op)
            s += "\n"
        print()
        print(f"{expression} =")
        print(s)
