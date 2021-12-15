class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Scope:
    def __init__(self, _type):
        self._type = _type


class IntNum:
    def __init__(self, value):
        self.value = value


class FloatNum:
    def __init__(self, value):
        self.value = value


class String:
    def __init__(self, string):
        self.string = string


class Variable:
    def __init__(self, name):
        self.name = name


class BinaryExpr:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Range:
    def __init__(self, _from, to):
        self._from = _from
        self.to = to


class Ref:
    def __init__(self, var, x, y):
        self.var = var
        self.x = x
        self.y = y


class UnaryMinus:
    def __init__(self, expr):
        self.expr = expr


class UnaryTranspose:
    def __init__(self, expr):
        self.expr = expr


class IfStatement:
    def __init__(self, condition, ifBlock, elseBlock=None):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock


class ForLoop:
    def __init__(self, var, _range, block):
        self.var = var
        self._range = _range
        self.block = block


class WhileLoop:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class BreakInstruction:
    def __init__(self):
        pass


class ContinueInstruction:
    def __init__(self):
        pass


class ReturnStatement:
    def __init__(self, value=None):
        self.value = value


class Printable:
    def __init__(self, printable):
        self.printable = printable


class PrintStatement:
    def __init__(self, content):
        self.content = content


class MatrixSpecialWord:
    def __init__(self, word, value):
        self.word = word
        self.value = value


class Vector:
    def __init__(self, inside):
        self.inside = inside


class Error:
    def __init__(self):
        pass
