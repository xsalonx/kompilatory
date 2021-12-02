from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator

padder = "| "

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        if self.left:
            self.left.printTree(indent)
        if self.right:
            self.right.printTree(indent)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(padder * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(padder * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(padder * indent + self.string)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(padder * indent + self.name)

    @addToClass(AST.BinaryExpr)
    def printTree(self, indent=0):
        print(padder * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(padder * indent + "RANGE")
        self._from.printTree(indent + 1)
        self.to.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        print(padder * indent + "REF")
        self.var.printTree(indent + 1)
        self.x.printTree(indent + 1)
        self.y.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print(padder * indent + '-')
        self.expr.printTree(indent + 1)

    @addToClass(AST.UnaryTranspose)
    def printTree(self, indent=0):
        print(padder * indent + "TRANSPOSE")
        self.expr.printTree(indent + 1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print(padder * indent + "IF")
        self.condition.printTree(indent + 1)
        print(padder * indent + "THEN")
        self.ifBlock.printTree(indent + 1)
        if self.elseBlock is not None:
            print(padder * indent + "ELSE")
            self.elseBlock.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print(padder * indent + "FOR")
        self.var.printTree(indent + 1)
        self._range.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print(padder * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent=0):
        print(padder * indent + 'BREAK')

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent=0):
        print(padder * indent + 'CONTINUE')

    @addToClass(AST.ReturnStatement)
    def printTree(self, indent=0):
        print(padder * indent + "RETURN")
        if self.value is not None:
            self.value.printTree(indent + 1)

    @addToClass(AST.Printable)
    def printTree(self, indent=0):
        self.printable.printTree(indent)

    @addToClass(AST.PrintStatement)
    def printTree(self, indent=0):
        print(padder * indent + "PRINT")
        self.content.printTree(indent + 1)

    @addToClass(AST.MatrixSpecialWord)
    def printTree(self, indent=0):
        print(padder * indent + self.word)
        self.value.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(padder * indent + 'VECTOR')
        self.inside.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
