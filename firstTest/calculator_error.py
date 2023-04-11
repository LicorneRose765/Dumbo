from lark import Lark, Transformer, UnexpectedInput

from calculator import cal_grammar

cal_parser = Lark(cal_grammar, parser='lalr', transformer=Transformer())


class CalcSyntaxError(SyntaxError):
    def __str__(self):
        context, line, column = self.args
        return f"{self.label} at line {line}, column {column}.\n{context}"


class CalcMissingValue(CalcSyntaxError):
    label = 'Missing Value'


class CalcMissingOpening(CalcSyntaxError):
    label = 'Missing Opening'


class CalcMissingClosing(CalcSyntaxError):
    label = 'Missing Closing'


class CalcUnknownChar(CalcSyntaxError):
    label = 'Unknown Character'


class CalcUnknownError(CalcSyntaxError):
    label = 'Unknown Error'


def parse(text):
    try:
        j = cal_parser.parse(text)
    except UnexpectedInput as u:
        # On récupère la classe de l'exception qui correspond à l'exemple donné
        exc_class = u.match_examples(cal_parser.parse, {
            CalcUnknownChar: ['a'],
            CalcMissingOpening: ['1+2)', ')'],
            CalcMissingClosing: ['(', '(1+2'],
            CalcMissingValue: ['1++2', '1+2*', '1+2/', '1+2-', '1+2+', '()', '']
        }, use_accepts=True)
        if not exc_class:
            print("oui")
            raise CalcUnknownError(u.get_context(text), u.line, u.column)
        raise exc_class(u.get_context(text), u.line, u.column)


def test():
    try:
        parse('(1+2*3')
    except CalcMissingClosing as e:
        print(e)

    try:
        parse('1+2*42)')
    except CalcMissingOpening as e:
        print(e)

    try:
        parse('1+2*')
    except CalcMissingValue as e:
        print(e)

    try:
        parse('')
    except CalcMissingValue as e:
        print(e)

    try:
        parse('1+')
    except CalcMissingValue as e:
        print(e)

    try:
        parse('a')
    except CalcUnknownChar as e:
        print(e)


if __name__ == '__main__':
    test()
