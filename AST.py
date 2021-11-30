
class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Block:
    def __init__(self, inside):
        self.inside = inside

class IntNum:
    def __init__(self, value):
        self.value = value

class FloatNum:
    def __init__(self, value):
        self.value = value

class String:
    def __init__(self, string):
        self.string = string

class Printable:
    def __init__(self, printable, nxt=None):
        self.printable = printable
        self.nxt = nxt

class Variable:
    def __init__(self, name):
        self.name = name

class BinaryExpr:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class MatrixSpecialWord:
    def __init__(self, word, value):
        self.word = word
        self.value = value

class ReturnStatement:
    def __init__(self, word, value=None):
        self.word = word
        self.value = value

class PrintStatement:
    def __init__(self, content):
        self.content = content

class UnaryMinus:
    def __init__(self, expr):
        self.expr = expr

class UnaryTranspose:
    def __init__(self, expr):
        self.expr = expr

class ForLoop:
    def __init__(self, var, _range, block):
        self.var = var
        self._range = _range
        self.block = block

class WhileLoop:
    def __init__(self, condition, operations):
        self.condition = condition
        self.operations = operations

class If:
    def __init__(self, condition, ifBlock):
        self.condition = condition
        self.ifBlock = ifBlock

class IfElse:
    def __init__(self, condition, ifBlock, elseBlock):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

class Matrix:
    def __init__(self, inside):
        self.inside = inside

class Vector:
    def __init__(self, inside):
        self.inside = inside


class BreakInstruction:
    def __init__(self):
        pass

class ContinueInstruction:
    def __init__(self):
        pass

class Error:
    def __init__(self):
        pass
