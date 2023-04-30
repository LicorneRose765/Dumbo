from .symbols_table import symbols_table


def assign(variable_name, value, scope_depth):
    """Assigns the value 'value' to the variable named 'variable_name' at the scope depth 'scope_depth' via the symbols.py table."""
    symbols_table.assign(variable_name, value, scope_depth)


class Operation:
    def execute(self, body_scope_depth):
        raise NotImplementedError("Subclass should override this method.")

    def __repr__(self):
        return self.__str__()


class AssignOperation(Operation):
    def __init__(self, variable_name, variable_value, scope_depth):
        """
        :param variable_name: The name of the variable
        :param variable_value: The value of the variable
        :param scope_depth: The scope depth of the variable
        """
        self.variable_name = variable_name
        self.variable_value = variable_value
        self.scope_depth = scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   ASSIGN {self.variable_value} TO {self.variable_name} AT DEPTH {self.scope_depth}>"

    def execute(self, body_scope_depth):
        assign(self.variable_name, self.variable_value, self.scope_depth)


class IfOperation(Operation):
    def __init__(self, condition_result, then_body: list[Operation], body_scope_depth):
        """
        :param condition_result: True or False (result of the condition that was parsed)
        :param then_body: Operations to execute if the condition_result is True
        :param body_scope_depth: The scope depth of the body of the if statement
        """
        self.condition_result = condition_result
        self.then_body = then_body
        self.body_scope_depth = body_scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   IF {self.condition_result} DO\n    " + "\n    ".join(str(op) for op in self.then_body) + ">"

    def execute(self, body_scope_depth):
        if self.condition_result:
            for op in self.then_body:
                op.execute(self.body_scope_depth)


class PrintOperation(Operation):
    def __init__(self, content):
        """
        :param content: The string to print
        """
        self.content = content

    def __str__(self):
        return f"<{self.__class__.__name__}   PRINT {self.content}>"

    def execute(self, body_scope_depth):
        return self.content


class BoolOperation(Operation):
    def __init__(self, lhs, operator, rhs, scope_depth):
        """
        :param lhs: Left hand side of the operation
        :param operator: Operator of the operation
        :param rhs: Right hand side of the operation
        :param scope_depth: The scope depth at which the operation happens
        """
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs
        self.scope_depth = scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   [{self.lhs} {self.operator} {self.rhs}]>"

    def __sanity_check__(self, required_type: type):
        valid = isinstance(self.lhs, required_type) and isinstance(self.rhs, required_type)
        if not valid:
            print(f"Invalid operands for {self.__str__()}")
        return valid

    def __get_left_right__(self, type_to_simplify):
        left = self.lhs, right = self.rhs
        if isinstance(self.lhs, type_to_simplify):
            left = self.lhs.execute(self.scope_depth)
        if isinstance(self.rhs, type_to_simplify):
            right = self.rhs.execute(self.scope_depth)
        return left, right

    def execute(self, body_scope_depth):
        if self.operator == "and":
            if not self.__sanity_check__(bool or BoolOperation):
                return False
            left, right = self.__get_left_right__(BoolOperation)
            return left and right
        elif self.operator == "or":
            if not self.__sanity_check__(bool or BoolOperation):
                return False
            left, right = self.__get_left_right__(BoolOperation)
            return left or right
        elif self.operator == "<":
            if not self.__sanity_check__(int or MathOperation):
                return False
            left, right = self.__get_left_right__(MathOperation)
            return left < right
        elif self.operator == ">":
            if not self.__sanity_check__(int or MathOperation):
                return False
            left, right = self.__get_left_right__(MathOperation)
            return left > right
        elif self.operator == "=":
            if not self.__sanity_check__(int or MathOperation):
                return False
            left, right = self.__get_left_right__(MathOperation)
            return left == right
        elif self.operator == "!=":
            if not self.__sanity_check__(int or MathOperation):
                return False
            left, right = self.__get_left_right__(MathOperation)
            return left != right


class MathOperation(Operation):
    def __init__(self, lhs, operator, rhs, scope_depth):
        """
        :param lhs: Left hand side of the operation
        :param operator: Operator of the operation
        :param rhs: Right hand side of the operation
        :param scope_depth: The scope depth at which the operation happens
        """
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs
        self.scope_depth = scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   [{self.lhs} {self.operator} {self.rhs}]>"

    def __sanity_check__(self, required_type: type):
        valid = isinstance(self.lhs, required_type) and isinstance(self.rhs, required_type)
        if not valid:
            print(f"Invalid operands for {self.__str__()}")
        return valid

    def __get_left_right__(self, type_to_simplify):
        left = self.lhs, right = self.rhs
        if isinstance(self.lhs, type_to_simplify):
            left = self.lhs.execute(self.scope_depth)
        if isinstance(self.rhs, type_to_simplify):
            right = self.rhs.execute(self.scope_depth)
        return left, right

    def execute(self, body_scope_depth):
        if self.operator == "+":
            if not self.__sanity_check__(int or MathOperation):
                return 0
            left, right = self.__get_left_right__(BoolOperation)
            return left + right
        elif self.operator == "-":
            if not self.__sanity_check__(int or MathOperation):
                return 0
            left, right = self.__get_left_right__(BoolOperation)
            return left - right
        elif self.operator == "*":
            if not self.__sanity_check__(int or MathOperation):
                return 0
            left, right = self.__get_left_right__(BoolOperation)
            return left * right
        elif self.operator == "/":
            if not self.__sanity_check__(int or MathOperation):
                return 0
            left, right = self.__get_left_right__(BoolOperation)
            return int(left / right)


class ForOperation(Operation):
    def __init__(self, temporary_variable_name, string_list, body: list[Operation], body_scope_depth):
        """
        :param temporary_variable_name: The name of the temporary variable
        :param string_list: The list of strings to iterate over
        :param body: The list of operations to execute in the body
        :param body_scope_depth: The scope depth of the body of the if statement
        """
        self.temporary_variable_name = temporary_variable_name
        self.string_list = string_list
        self.body = body
        self.body_scope_depth = body_scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   FOR {self.temporary_variable_name} in {self.string_list} DO\n    " + "\n    ".join(str(op) for op in self.body) + ">"

    def execute(self, body_scope_depth):
        assign(self.temporary_variable_name, "", self.body_scope_depth)
        for var in self.string_list:
            assign(self.temporary_variable_name, var, self.body_scope_depth)
            for op in self.body:
                op.execute(self.body_scope_depth)
