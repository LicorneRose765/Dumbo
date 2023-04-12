from lark import Lark, Transformer
import sys

dumbo_grammar = r"""
    ?programme: txt 
                | txt programme
                | dumbo_bloc 
                | dumbo_bloc programme
                
    TXT : /(?!.*\{\{).*/  // contient pas {{
    
    ?dumbo_bloc: "{{" expression_list "}}"
    
    ?expression_list: expression ";" expression_list
                      | expression ";"
    
    ?expression: "print" string_expression -> print
                | "for" variable "in" string_list 
                  "do" expression_list "endfor" -> for_string
                | "for" variable "in" variable 
                  "do" expression_list "endfor" -> for_variable
                | variable ":=" string_expression -> assign
                | variable ":=" string_list -> assign_list
    
    ?string_expression: string
                        | variable
                        | string_expression "." string_expression -> concat
                    
    ?string_list: "(" string_list_interior ")"
    
    ?string_list_interior: string 
                            | string "," string_list_interior
    
    ?VARIABLE : /[a-zA-Z_]\w*/  // lettre ou underscore + (lettre ou nombre ou underscore)*
    ?STRING : "'" /[^']*?/ "'"  // ' + ((tout sauf single quote)*)? + '
"""
# TODO : vérifier que la grammaire fonctionne comme ça, faudra peut-être ajouter des noms aux règles
# TODO : compléter la grammaire


def parse_data(data):
    """
    Parse the data file and initialise the variables
    :param data: The data file
    """
    with open(filename_data, 'r') as f:
        data = f.read()

    # TODO : Parse the data file and initialise the variables


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 main.py <data> <template>')
        exit(1)
    filename_data = sys.argv[1]
    filename_template = sys.argv[2]
    # TODO : Regarder si il vaut mieux envoyer ligne par ligne ou tout le fichier d'un coup
