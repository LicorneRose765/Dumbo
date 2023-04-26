import ply.lex as lex
import ply.yacc as yacc
import os
from lark import Lark, Transformer, Token, Tree
import sys
from pathlib import Path

# *-------------------------------------------------------------------------------------------------------------------*
#     VARS
# *-------------------------------------------------------------------------------------------------------------------*

states = (
    ("IN", "exclusive"),  # state 'IN'  : when inside dumbo code
)

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
    t.lexel.level += 1
    return t


def t_IN_CLOSING(t):
    """}}"""
    t.lexer.level -= 1

    if t.lexer.level == 0:
         t.lexer.begin('INITIAL')

    return t


def t_CLOSING(t):
    """}}"""
    print(f"Unexpected '{t.value[0]}' at line {lexer.lineno}")


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
    """assign"""
    return t


def t_TXT(t):
    """(?!.*\{\{).+"""
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
    STRING_LIST_INTERIOR : STRING ',' STRING_LIST_INTERIOR
    """
    print("Call to method p_stringlistinterior_double")
    return p


def p_stringlistinterior_single(p):
    """
    STRING_LIST_INTERIOR : STRING
    """
    print("Call to method p_stringlistinterior_single")
    return p


def p_stringlist(p):
    """
    STRING_LIST : '(' STRING_LIST_INTERIOR ')'
    """
    print("Call to method p_stringlist")
    return p


def p_expression_assignments(p):
    """
    EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION
               | VARIABLE ASSIGN STRING_LIST
    """
    print("Call to method p_expression_assignments")
    return p


def p_stringexpression_double(p):
    """
    STRING_EXPRESSION : STRING_EXPRESSION '.' STRING_EXPRESSION
    """
    print("Call to method p_stringexpression_double")
    return p


def p_stringexpression_single(p):
    """
    STRING_EXPRESSION : STRING
                      | VARIABLE
    """
    print("Call to method p_stringexpression_single")
    return p


def p_expression_strlistfor(p):
    """
    EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR
    """
    print("Call to method p_expression_strlistfor")
    return p


def p_expression_varfor(p):
    """
    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR
    """
    print("Call to method p_expression_varfor")
    return p


def p_expression_print(p):
    """
    EXPRESSION : PRINT STRING_EXPRESSION
    """
    print("Call to method p_expression_print")
    return p


def p_dumboblock(p):
    """
    DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING
    """
    print("Call to method p_dumboblock")
    return p


def p_expressionlist(p):
    """
    EXPRESSION_LIST : EXPRESSION ';'
                    | EXPRESSION ';' EXPRESSION_LIST
    """
    print("Call to method p_expressionlist")
    return p


def p_program_double(p):
    """
    PROGRAM : TXT PROGRAM
            | DUMBO_BLOCK PROGRAM
    """
    p[0] = p[1] + p[2]  # TODO : pas sûr
    print("Call to method p_program_double")
    return p


def p_program_single_dumboblock(p):
    """
    PROGRAM : DUMBO_BLOCK
    """
    p[0] = p[1]  # TODO : pas sûr
    print("Call to method p_program_single_dumboblock")
    return p


def p_program_single_txt(p):
    """
    PROGRAM : TXT
    """
    p[0] = p[1]  # TODO : pas sûr
    print("Call to method p_program_single_txt")
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

    lexer = lex.lex()
    lexer.input(input())
    for token in lexer:
        print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")

    parser = yacc.yacc(start=start, debug=True)
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
