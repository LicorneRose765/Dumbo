from .symbols_table import symbols_table
from . import params


def assign(variable_name, value, scope_depth, lookup=True):
    """See symbols_table.assign for more information."""
    symbols_table.assign(variable_name, value, scope_depth, lookup=lookup)


def get(variable_name, scope_depth):
    return symbols_table.get(variable_name, scope_depth)


def delete_scope(scope_depth):
    """Removes variables defines at the scope 'scope_depth'"""
    symbols_table.delete(scope_depth)


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
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        assign(self.variable_name, self.variable_value, body_scope_depth)
        return ""


class IfOperation(Operation):
    def __init__(self, condition, then_body: list[Operation], body_scope_depth):
        """
        :param condition: The condition to meet (BoolOperation)
        :param then_body: Operations to execute if the condition is True
        :param body_scope_depth: The scope depth of the body of the if statement
        """
        self.condition = condition
        self.then_body = then_body
        self.body_scope_depth = body_scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   IF {self.condition} DO\n    " + "\n    ".join(str(op) for op in self.then_body) + ">"

    def execute(self, body_scope_depth):
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        res = ""
        condition_is_met = False
        if isinstance(self.condition, BoolOperation):
            condition_is_met = self.condition.execute(self.body_scope_depth)
        elif isinstance(self.condition, str):
            condition_is_met = bool(self.condition)
        if condition_is_met:
            for op in self.then_body:
                res += op.execute(self.body_scope_depth)
        return res


class PrintOperation(Operation):
    def __init__(self, string_expression):
        """
        :param identifier: If printing a variable, the name of the variable, if printing a string, the conent of the string
        :param isVar: whether we are printing a var or not
        """
        self.string_expression = string_expression

    def __str__(self):
        return f"<{self.__class__.__name__}   PRINT {self.string_expression}>"

    def execute(self, body_scope_depth):
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        return self.string_expression.execute()


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

    def __sanity_check__(self, required_types: list[type]):
        right_is_ok = [isinstance(self.rhs, type) for type in required_types]
        left_is_ok = [isinstance(self.lhs, type) for type in required_types]
        valid = any(left_is_ok) and any(right_is_ok)
        if not valid:
            print(f"Invalid operands for {self.__str__()}")
        return valid

    def __get_left_right__(self, types_to_simplify: list[type]):
        left = self.lhs
        right = self.rhs
        if any([isinstance(self.lhs, _type) for _type in types_to_simplify]):
            left = self.lhs.execute(self.scope_depth)
        if any([isinstance(self.rhs, _type) for _type in types_to_simplify]):
            right = self.rhs.execute(self.scope_depth)
        return left, right

    def execute(self, body_scope_depth):
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        valid_types_1 = [bool, BoolOperation, GetOperation]
        valid_types_2 = [int, MathOperation, GetOperation]
        if self.operator == "and":
            if not self.__sanity_check__(valid_types_1):
                return False
            left, right = self.__get_left_right__([BoolOperation, GetOperation])
            return left and right
        elif self.operator == "or":
            if not self.__sanity_check__(valid_types_1):
                return False
            left, right = self.__get_left_right__([BoolOperation, GetOperation])
            return left or right
        elif self.operator == "<":
            if not self.__sanity_check__(valid_types_2):
                return False
            left, right = self.__get_left_right__([MathOperation, GetOperation])
            return left < right
        elif self.operator == ">":
            if not self.__sanity_check__(valid_types_2):
                return False
            left, right = self.__get_left_right__([MathOperation, GetOperation])
            return left > right
        elif self.operator == "=":
            if not self.__sanity_check__(valid_types_2):
                return False
            left, right = self.__get_left_right__([MathOperation, GetOperation])
            return left == right
        elif self.operator == "!=":
            if not self.__sanity_check__(valid_types_2):
                return False
            left, right = self.__get_left_right__([MathOperation, GetOperation])
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

    def __sanity_check__(self, required_types: list[type]):
        right_is_ok = [isinstance(self.rhs, _type) for _type in required_types]
        left_is_ok = [isinstance(self.lhs, _type) for _type in required_types]
        valid = any(left_is_ok) and any(right_is_ok)
        if not valid:
            print(f"Invalid operands for {self.__str__()}")
        return valid

    def __get_left_right__(self, types_to_simplify: list[type]):
        left = self.lhs
        right = self.rhs
        if any([isinstance(self.lhs, _type) for _type in types_to_simplify]):
            left = self.lhs.execute(self.scope_depth)
        if any([isinstance(self.rhs, _type) for _type in types_to_simplify]):
            right = self.rhs.execute(self.scope_depth)
        return left, right

    def execute(self, body_scope_depth):
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        valid_types = [int, MathOperation, GetOperation]
        if self.operator == "+":
            if not self.__sanity_check__(valid_types):
                return 0
            left, right = self.__get_left_right__([MathOperation, GetOperation])
            return left + right
        elif self.operator == "-":
            if not self.__sanity_check__(valid_types):
                return 0
            left, right = self.__get_left_right__([MathOperation, GetOperation])
            return left - right
        elif self.operator == "*":
            if not self.__sanity_check__(valid_types):
                return 0
            left, right = self.__get_left_right__([MathOperation, GetOperation])
            return left * right
        elif self.operator == "/":
            if not self.__sanity_check__(valid_types):
                return 0
            left, right = self.__get_left_right__([MathOperation, GetOperation])
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
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        res = ""
        assign(self.temporary_variable_name, "", self.body_scope_depth, lookup=False)
        if isinstance(self.string_list, GetOperation):
            string_list = self.string_list.execute(self.body_scope_depth)
        else:
            string_list = self.string_list
        for var in string_list:
            assign(self.temporary_variable_name, var, self.body_scope_depth, lookup=False)
            for op in self.body:
                res += op.execute(self.body_scope_depth)
        delete_scope(self.body_scope_depth)
        return res


class StringExpressionNode:
    def __init__(self, value, isVar, scope_depth, lhs, rhs):
        if params.verbose:
            print(f"Creating a {self.__class__.__name__}")
        self.value = value
        self.isVar = isVar
        self.lhs = lhs
        self.rhs = rhs
        self.scope_depth = scope_depth

    def __str__(self):
        return f"{self.value}" if self.isVar else f"'{self.value}'"

    def __repr__(self):
        return self.__str__()

    def __get_true_value__(self):
        if self.isVar:
            return get(self.value, self.scope_depth)
        return self.value

    def execute(self):
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        stack = [self]
        result = []
        while stack:
            node = stack.pop()
            left, right = node.lhs, node.rhs
            if node.value:
                result.append(str(node.__get_true_value__()))
            if right:
                stack.append(right)
            if left:
                stack.append(left)
        return "".join(result)


class GetOperation(Operation):
    def __init__(self, var_name, scope_depth):
        self.var_name = var_name
        self.scope_depth = scope_depth

    def __str__(self):
        return f"<{self.__class__.__name__}   {self.var_name}>"

    def execute(self, body_scope_depth):
        if params.verbose:
            print(f"Executing {self.__class__.__name__}")
        return get(self.var_name, self.scope_depth)


class TextBlock(Operation):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def execute(self, body_scope_depth):
        return self.text
