verbose = False


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

    def assign(self, name, value, scope_depth):
        """Assigns the value 'value' to the variable named 'name' at the scope depth 'scope_depth'"""
        try:
            self.table[scope_depth]
        except KeyError:
            self.table[scope_depth] = {}
        self.table[scope_depth][name] = value
        if verbose:
            print(f"Assigned {value=:} to {name=:} in scope {scope_depth=:}")

    def get(self, name, scope_depth):
        if verbose:
            print(f"Trying to get the variable {name=:} at {scope_depth=:}")
        try:
            value = self.table[scope_depth][name]
        except KeyError:
            if scope_depth > 0:
                value = self.get(name, scope_depth - 1)
            else:
                print(f"SyntaxError : Cannot find variable {name}. ")
                if verbose:
                    print(f"    Searched at {scope_depth=:} for in the following table :")
                    print(f"    {self.table}")
                # raise SyntaxError(f"Cannot find variable {name}.")
                return None
        return value

    def delete(self, scope_depth):
        if verbose:
            print(f"Call to delete variables entry in {scope_depth=:}")
        if verbose:
            print(f"Table before deletion of {scope_depth=:} :")
            print(f"    {self.table}")
        try:
            del self.table[scope_depth]
        except KeyError as ignored:
            pass
        if verbose:
            print(f"Table after deletion of {scope_depth=:} :")
            print(f"    {self.table}")

    def init_depth_entry(self, scope_depth):
        if verbose:
            print(f"Created a new entry for variables in {scope_depth=:}")
        self.table[scope_depth] = {}


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
