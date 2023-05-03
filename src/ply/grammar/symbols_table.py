from . import params


class SymbolsTable:
    def __init__(self, table=None):
        self.table = table if table is not None else {}

    def __str__(self):
        def pretty_print_dict(d, indent=0):
            _s = ""
            for key, value in d.items():
                if isinstance(value, dict):
                    _s += ' ' * (4 * key - 4 if key != 1 else 0) + "{ \n"
                    _s += pretty_print_dict(value, key * 4)
                    # _s += ' ' * (indent + 3 * key if key != 1 else 0) + "} \n"
                else:
                    _s += ' ' * indent + f"{key}: {value}\n"
            return _s

        ss = pretty_print_dict(self.table)
        return ss

    def assign(self, name, value, scope_depth, lookup=True):
        """Assigns the value 'value' to the variable named 'name' at the scope depth 'scope_depth'. If lookup is True,
        we check if the value is already defined at a higher scope, and if so, we overwrite it. This is the default
        behavior but the argument can be set to False so we simply define a new variable at the given scope."""
        # TODO : if we do assign operations in a for loop and the variable already exists, it musts temporarily
        #  overwrite it
        #  -> 1. look for it
        #     2. if it exists, set the value at the scope of the already existing variable
        try:
            self.table[scope_depth]
        except KeyError:
            self.table[scope_depth] = {}
        final_scope_to_assign = scope_depth
        if lookup:
            found_value_and_scope = self.get(name, scope_depth, get_scope=True)
            if found_value_and_scope:
                final_scope_to_assign = found_value_and_scope[1]
        # I just wanted to do if isinstance(value, Operation) but I got circular imported so I had to work around it
        try:
            self.table[final_scope_to_assign][name] = value.execute(scope_depth)
        except AttributeError:
            self.table[final_scope_to_assign][name] = value
        if params.verbose:
            print(f"Assigned {value=:} to {name=:} in scope {final_scope_to_assign=:}")

    def get(self, name, scope_depth, get_scope=False):
        if params.verbose:
            print(f"Trying to get the variable {name=:} at {scope_depth=:}")

        while scope_depth >= 1:
            inner_dict = self.table.get(scope_depth)
            if inner_dict:
                value = inner_dict.get(name)
                if value is not None:
                    if get_scope:
                        return value, scope_depth
                    return value
            scope_depth -= 1
        return None

        try:
            value = self.table[scope_depth][name]
        except KeyError:
            if scope_depth > 0:
                value_scope = self.get(name, scope_depth - 1, get_scope=True)
                if value_scope is not None:
                    value, scope = value_scope
            else:
                print(f"SyntaxError : Cannot find variable {name}. ")
                if params.verbose:
                    print(f"    Searched at {scope_depth=:} for in the following table :")
                    print(f"    {self.table}")
                # raise SyntaxError(f"Cannot find variable {name}.")
                return None
        if get_scope:
            return value, scope
        else:
            return value

    def delete(self, scope_depth):
        if params.verbose:
            print(f"Call to delete variables entry in {scope_depth=:}")
        if params.verbose:
            print(f"Table before deletion of {scope_depth=:} :")
            print(f"    {self.table}")
        try:
            del self.table[scope_depth]
        except KeyError as ignored:
            pass
        if params.verbose:
            print(f"Table after deletion of {scope_depth=:} :")
            print(f"    {self.table}")

    def init_depth_entry(self, scope_depth):
        if params.verbose:
            print(f"Created a new entry for variables in {scope_depth=:}")
        self.table[scope_depth] = {}


symbols_table = SymbolsTable()


if __name__ == "__main__":
    """
    st =
    {
        "a" = "a"
        "b" = "b"
        {
            {
                "4" = "4"
                "555555" = "5"
                {
                    "7" = "7"
                    "88888" = "8"
                    "9999999" = "9"
                }
            }
        }
    }
    """
    st = SymbolsTable({1: {"a": "a", "b": "b"}, 2: {}, 3: {"4": "4", "555555": "5"}, 4: {"7": "7", "88888": "8", "9999999": "9"}})
    print(st)
    print(st.get("b", 4))
