
class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Block(Node):
    def  __init__(self, content):
        self.content = content

class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, string):
        self.string = string

class Printable(Node):
    def __init__(self, printable, nxt=None):
        self.printable = printable
        self.nxt = nxt  # plaska lista

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class MatWord(Node):
    def __init__(self, word, value):
        self.word = word
        self.value = value

class ReturnStatement(Node):
    def __init__(self, word, value=None):
        self.word = word
        self.value = value

class PrintStatement(Node):
    def __init__(self, content):
        self.content = content

class UnaryMinus(Node):
    def __init__(self, expr):
        self.expr = expr

class UnaryTranspose(Node):
    def __init__(self, expr):
        self.expr = expr

class ForLoop(Node):
    def __init__(self, var, _range, block):
        self.var = var
        self._range = _range
        self.block = block

class WhileLoop(Node):
    def __init__(self, condition, operations):
        self.condition = condition
        self.operations = operations

class IfElse(Node):
    def __init__(self, condition, ifBlock, elseBlock=None):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

class Matrix(Node):
    def __init__(self, inside, deepInside):
        self.inside = inside
        self.deepInside = deepInside

class Vector(Node):
    def __init__(self, inside):
        self.inside = inside


class BreakInstruction(Node):
    def __init__(self):
        pass

class ContinueInstruction(Node):
    def __init__(self):
        pass

class Error(Node):
    def __init__(self):
        pass
