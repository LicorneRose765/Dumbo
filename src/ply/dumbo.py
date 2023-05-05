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

    print(content)
    lexer = lex.lex()
    parser = yacc.yacc(start=start)
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
        parse_data_template(data_path, template_path)
    else:
        lexer = lex.lex()
        """lexer.input(input())
        for token in lexer:
            print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")
        """
        parser = yacc.yacc(start=start, debug=True)
        expressions = ["{{ a := '2'; b := '4'; }} {{ c := '6'; print a; print b; print c; }} {{ print c; }}",
         "{{ if 2 < 3 do print 'true'; print 'i am veri smart'; endif; }} {{ a := 17; b := '11'; }}",
         "{{ list := ('1', '2', '3'); for var in list do print var; endfor; }}",
         "{{ 2 + 2 * 2 - 2; }} abcd",
         "{{ for myvar in ('a', 'b', 'c') do print myvar; endfor; }}",
         "{{ i := 2; if i < 1 do print 'yes'; endif; }}",
         "{{ nom := 'oui'; print '<a_href=\"'.nom.'\">'.nom.'</a>'; }}",
         "{{ i := 0; print i.'\n'; i := i + 1; print i.'\n'; i := i + 1; print i.'\n'; }}",
         "{{ liste_photo := ('a', 'b', 'c'); print liste_photo; }}",
        # baby_chad_expression =
                     "{{ i := 0;" \
                     "   for nom in ('a', 'b', 'c') do" \
                     "       print nom.', i = '.i;" \
                     "       if i > 0 do print 'i > 0'; endif;" \
                     "       print '\n';" \
                     "       i := i + 1;" \
                     "   endfor; }}",
        #chad_expression =
                          "{{" \
                          "nom := 'Brouette';" \
                          "prenom := 'Quentin';" \
                          "cours := ('Logique 1', 'Logique 2', 'Algebre 1', 'Math elem');" \
                          "}}" \
                          "{{ print nom; }}<--- ce nom est ridicule\n" \
                          "{{" \
                          "i := 0;" \
                          "for nom in ('name', 'NAME', 'NAAAAME') do" \
                          "    if i > 0 do print ', '; endif;" \
                          "    print '<a_href=\"'.nom.'\">'.nom.'</a>';" \
                          "    i := i + 1;" \
                          "endfor;" \
                          "}}",
        # giga_chad_expression =
                               "{{ liste_photo := ('holiday.png', 'flower.jpg', 'dog.png', 'house.png'); nom := 'my album'; }}" \
                               "<html>\n" \
                               "  <head>" \
                               "    <title>{{ print nom; }}</title>" \
                               "  </head>\n" \
                               "  <body>\n" \
                               "  <h1>{{ print nom; }}</h1>\n" \
                               "{{" \
                               "i := 0;" \
                               "for nom in liste_photo do" \
                               "    if i > 0 do print ', '; endif ;" \
                               "    print '<a href=\"'.nom.'\">'.nom.'</a>';" \
                               "    i := i + 1;" \
                               "endfor;" \
                               "}}\n" \
                               "Il y a {{ print i.' images '; }} dans l album {{ print nom; }}.\n" \
                               "  </body>\n" \
                               "</html>"]
        # expression = giga_chad_expression
        for expression in expressions:
            result = parser.parse(expression)
            s = ""
            for op in result:
                s += str(op)
                s += "\n"
            print()
            print(f"{expression} =\n")
            print(s)
            print("RESULT\n"
                  "======")
            print(dfs_result(result))
