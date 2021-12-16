class Node:
    def __init__(self, left, right, lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno


class Scope:
    def __init__(self, instructions, lineno=None):
        self.instructions = instructions
        self.lineno = lineno


class IntNum:
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno


class FloatNum:
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno


class String:
    def __init__(self, string, lineno=None):
        self.string = string
        self.lineno = lineno


class Variable:
    def __init__(self, name, lineno=None):
        self.name = name
        self.lineno = lineno


class BinaryExpr:
    def __init__(self, op, left, right, lineno=None):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class Range:
    def __init__(self, _from, to, lineno=None):
        self._from = _from
        self.to = to
        self.lineno = lineno


class Ref:
    def __init__(self, var, x, y, lineno=None):
        self.var = var
        self.x = x
        self.y = y
        self.lineno = lineno


class UnaryMinus:
    def __init__(self, expr, lineno=None):
        self.expr = expr
        self.lineno = lineno


class UnaryTranspose:
    def __init__(self, expr, lineno=None):
        self.expr = expr
        self.lineno = lineno


class IfStatement:
    def __init__(self, condition, ifBlock, elseBlock=None, lineno=None):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.lineno = lineno


class ForLoop:
    def __init__(self, var, _range, block, lineno=None):
        self.var = var
        self._range = _range
        self.block = block
        self.lineno = lineno


class WhileLoop:
    def __init__(self, condition, block, lineno=None):
        self.condition = condition
        self.block = block
        self.lineno = lineno


class BreakInstruction:
    def __init__(self, lineno=None):
        self.lineno = lineno


class ContinueInstruction:
    def __init__(self, lineno=None):
        self.lineno = lineno


class ReturnStatement:
    def __init__(self, value=None, lineno=None):
        self.value = value
        self.lineno = lineno


class Printable:
    def __init__(self, printable, lineno=None):
        self.printable = printable
        self.lineno = lineno


class PrintStatement:
    def __init__(self, content, lineno=None):
        self.content = content
        self.lineno = lineno


class MatrixSpecialWord:
    def __init__(self, word, value, lineno=None):
        self.word = word
        self.value = value
        self.lineno = lineno


class Vector:
    def __init__(self, inside, lineno=None):
        self.inside = inside
        self.lineno = lineno


class Matrix:
    def __init__(self, inside, lineno=None):
        self.inside = inside
        self.lineno = lineno


class Error:
    def __init__(self, lineno=None):
        self.lineno = lineno
