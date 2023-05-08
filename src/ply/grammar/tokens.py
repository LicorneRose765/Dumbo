from .symbols_table import symbols_table
from . import params

reserved = {
    "PRINT": "print",
    "FOR": "for",
    "IN": "in",
    "DO": "do",
    "ENDFOR": "endfor",
    "TRUE": "True",
    "FALSE": "False",
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


t_ANY_ignore = ' \t'


# *-------------------------------------------------------------------------------------------------------------------*
#     TOKEN METHODS
# *-------------------------------------------------------------------------------------------------------------------*


# I have to define these two as methods so I can give string the priority
def t_OPENING(t):
    """{{"""
    # INITIAL -> IN
    t.lexer.level = 1
    params.current_scope_depth = 1
    if params.verbose:
        print(f"Current scope depth changed to {params.current_scope_depth=:} because of first opening {'{{'}")
    symbols_table.init_depth_entry(params.current_scope_depth)
    t.lexer.begin('IN')
    return t


def t_IN_OPENING(t):
    """{{"""
    t.lexer.level += 1
    params.current_scope_depth += 1
    if params.verbose:
        print(f"Current scope depth changed to {params.current_scope_depth=:} because of new opening {'{{'}")
    symbols_table.init_depth_entry(params.current_scope_depth)
    return t


def t_IN_CLOSING(t):
    """}}"""
    t.lexer.level -= 1
    params.current_scope_depth -= 1
    if params.verbose:
        print(f"Current scope depth changed to {params.current_scope_depth=:} because of closing {'}}'}")
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')
    return t


def t_CLOSING(t):
    """}}"""
    if params.verbose:
        print(f"Unexpected '{t.value[0]*2}'")


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
    t.lexer.level += 1
    params.current_scope_depth += 1
    if params.verbose:
        print(f"Current scope depth changed to {params.current_scope_depth=:} because of for")
    symbols_table.init_depth_entry(params.current_scope_depth)
    return t


def t_IN_IN(t):
    """in"""
    return t


def t_IN_DO(t):
    """do"""
    return t


def t_IN_ENDFOR(t):
    """endfor"""
    t.lexer.level -= 1
    symbols_table.delete(params.current_scope_depth)
    params.current_scope_depth -= 1
    if params.verbose:
        print(f"Current scope depth changed to {params.current_scope_depth=:} because of endfor")
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')
    return t


def t_IN_TRUE(t):
    """True"""
    return t


def t_IN_FALSE(t):
    """False"""
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