import os

from lark import Lark, Transformer, Token, Tree
import sys
from pathlib import Path

# TODO : vérifier que la grammaire fonctionne comme ça, faudra peut-être ajouter des noms aux règles
# TODO : compléter la grammaire


class DumboTransformer(Transformer):
    def print_variable(self, args):
        return self.print(args)

    def print_string(self, args):
        return self.print(args)

    def print(self, args):
        return args[0].value

    def for_string(self, args):
        strings = ""
        for arg in args[1].children:
            while type(arg) == Tree:
                arg = arg.children
            if type(arg) == Token:
                strings += arg.value[1:-1]
                strings += ", "
            elif type(arg) == list:
                for token in arg:
                    strings += token.value[1:-1]
                    strings += ", "
            else:
                strings += str(arg)[1:-1]
                strings += ", "
        strings = strings[:-2]
        return f"for {args[0].value} in {strings} do"

    def for_variable(self, args):
        pass

    def assign(self, args):
        pass

    def assign_list(self, args):
        pass

    def concat(self, args):
        pass


def parse_data(data, data_filename):
    """
    Parse the data file and initialise the variables
    :param data: The data file
    :param data_filename The name of the data file
    """
    with open(data_filename, 'r') as f:
        data = f.read()

    # TODO : Parse the data file and initialise the variables


if __name__ == '__main__':


    if len(sys.argv) == 1:
        texts = ["i 4m s0m€ b4s!¢ ŧ€xŧ w!ŧħ CAPS 4nd $ymb0l$",
                 "{{ print abc; }}",
                 "{{ for var in ('a', 'b', 'c') do print var; endfor; }}"]
        parser = Lark(open(Path(__file__).parent.absolute() / "resources" / "dumbo_progress.lark"), start="programme", parser="lalr", transformer=DumboTransformer())
        for text in texts:
            parsed = parser.parse(text)
            print(f"   o  parsing '{text}'")
            print(repr(parsed))
            if type(parsed) == Tree:
                print(parsed.pretty()[:-1])
            print()
        exit(0)



    elif len(sys.argv) != 3:
        print('Usage: python3 main.py <data> <template>')
        exit(1)

    data_content = open(Path(os.getcwd()) / sys.argv[1], "r").readlines()
    template_content = open(Path(os.getcwd()) / sys.argv[2], "r").readlines()
