import ply.lex as lex

tokens = (
    "PROGRAMME",
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
    import sys

    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    for token in lexer:
        print(f"line {token.lineno} : token '{token.value}' (type '{token.type}')")
