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
        def extract_strings(arg: Tree or Token):
            if type(arg) == Token:
                return arg.value
            elif type(arg) == Tree:
                l1 = extract_strings(arg.children[0])
                l2 = extract_strings(arg.children[1])
                strings = []
                strings.extend(l1)
                strings.extend(l2)
                # we get many "'" in the strings but idk why so this is the easiest method to remove them
                while "'" in strings:
                    strings.remove("'")
                return strings

        values = ""
        for s in extract_strings(args[1]):
            values += f"{s}, "
        values = values[:-2]
        return f"for {args[0].value} in ({values}) do"

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
        texts = [#"i 4m s0m€ b4s!¢ ŧ€xŧ w!ŧħ CAPS 4nd $ymb0l$",
                 #"{{ print abc; }}",
                 "{{ for var in ('a', 'b', 'c', 'd') do print var; endfor; }}"]
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
        print('Usage: python3 dumbo.py <data> <template>')
        exit(1)

    data_content = open(Path(os.getcwd()) / sys.argv[1], "r").readlines()
    template_content = open(Path(os.getcwd()) / sys.argv[2], "r").readlines()
