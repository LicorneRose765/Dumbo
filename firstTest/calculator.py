from lark import Lark, Transformer, UnexpectedInput

cal_grammar = r"""
    ?start: expr
    ?expr: expr "+" term -> add
            | expr "-" term -> sub
            | term
    
    ?term: term "*" factor -> mul
            | term "/" factor -> div
            | factor
            
    ?factor: NUMBER -> number
            | "-" factor -> neg
            | "(" expr ")"
    
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""


# Le ? devant les règles indique que si la règle ne contient qu'un membre, alors elle sera "inlined" ?


class CalcTransformer(Transformer):
    def add(self, args):
        return args[0] + args[1]

    def sub(self, args):
        return args[0] - args[1]

    def mul(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]

    def neg(self, args):
        return -args[0]

    def number(self, args):
        return float(args[0])


cal_parser = Lark(cal_grammar, parser='lalr', transformer=CalcTransformer())


# Parser='lal' est le parser le plus rapide, mais la grammaire doit être LALR(1). Sinon, le parser par défaut est
# Earley. transformer=CalcTransformer() permet d'appliquer les transformations définies dans la classe
# CalcTransformer directement Sans créer l'arbre. C'est plus rapide.


if __name__ == '__main__':
    print(cal_parser.parse('(1+2)*3'))
