#!/usr/bin/python
import AST
import SymbolTable
from collections import defaultdict

is_error = False

symtable = SymbolTable.SymbolTable(None, "symtable")
ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

ttype['+']["str"]["str"] = "str"
ttype['*']["str"]["int"] = "str"
ttype['*']["int"]["str"] = "str"

ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "int"
ttype[".+"]["int"]["int"] = "int"
ttype[".-"]["int"]["int"] = "int"
ttype[".*"]["int"]["int"] = "int"
ttype["./"]["int"]["int"] = "int"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype[".+"]["int"]["float"] = "float"
ttype[".-"]["int"]["float"] = "float"
ttype[".*"]["int"]["float"] = "float"
ttype["./"]["int"]["float"] = "float"
ttype['<']["int"]["float"] = "logic"
ttype['>']["int"]["float"] = "logic"
ttype["<="]["int"]["float"] = "logic"
ttype[">="]["int"]["float"] = "logic"
ttype["=="]["int"]["float"] = "logic"
ttype["!="]["int"]["float"] = "logic"

ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype[".+"]["float"]["int"] = "float"
ttype[".-"]["float"]["int"] = "float"
ttype[".*"]["float"]["int"] = "float"
ttype["./"]["float"]["int"] = "float"
ttype['<']["float"]["int"] = "logic"
ttype['>']["float"]["int"] = "logic"
ttype["<="]["float"]["int"] = "logic"
ttype[">="]["float"]["int"] = "logic"
ttype["=="]["float"]["int"] = "logic"
ttype["!="]["float"]["int"] = "logic"

ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype[".+"]["float"]["float"] = "float"
ttype[".-"]["float"]["float"] = "float"
ttype[".*"]["float"]["float"] = "float"
ttype["./"]["float"]["float"] = "float"
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

castable_operations = ['/', '+', '-', '*', '>', '<', ">=", "<=", "==", "!="]
castable_matrix_operations = [".+", ".-", ".*", "./"]
castable_types = ["int", "float"]

def ttype_contains(t):
    sub_ttype = ttype
    for e in t:
        if e not in sub_ttype:
            return False
        else:
            sub_ttype = sub_ttype[e]
    return True

class Error:
    errors = {
        "no_var": "Undeclared variable",
        "no_loop_scope_break": "Break instruction outside the loop",
        "no_loop_scope_continue": "Continue instruction outside the loop",
        "not_logic": "Not a logical statement",
        "inv_range": "Incorrect range expressions types",
        "inv_transpose": "Trying to transpose a non-matrix",
        "inv_mat_arg": "Invalid matrix size argument",
        "inv_mat_arg_types": "Invalid matrix arguments types (not ints)",
        "inv_mat_arg_values": "Invalid matrix arguments values",
        "error": "Error found by parser",
        "diff_ty": "Different types"
    }

    def __init__(self, code, lineno):
        self.code = code
        self.lineno = lineno

        global is_error
        is_error = True

    def __str__(self):
        return f'{self.errors[self.code]} in line {self.lineno}'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)

        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_Node(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Scope(self, node):
        symtable.pushScope("scope")
        self.visit(node.instructions)
        symtable.popScope()

    def visit_BinaryExpr(self, node):
        op = node.op
        type2 = self.visit(node.right)

        if op == '=':
            if isinstance(node.left, AST.Variable):
                if type2:
                    symtable.put(node.left.name, type2)
            elif isinstance(node.left, AST.Ref):
                type1 = self.visit(node.left)
                if type2 != type1 and (type2 not in castable_types or type2 not in castable_types):
                    print(Error('diff_ty', node.lineno), '141')
            return None

        type1 = self.visit(node.left)
        if op in castable_operations and type1 in castable_types and type2 in castable_types:
            return ttype[op][type1][type2]

        if isinstance(type1, tuple) and isinstance(type2, tuple):
            if len(type1) == len(type2) == 3:
                rows1, cols1, vals1 = type1[0], type1[1], type1[2]
                rows2, cols2, vals2 = type2[0], type2[1], type2[2]
                if not ((rows1 == rows2 or "VARIABLE_SIZE" in [rows1, rows2])
                        and (cols1 == cols2 or "VARIABLE_SIZE" in [cols1, cols2])):
                    print(Error('diff_ty', node.lineno))
                    return None
                if not ttype_contains((op, vals1, vals2)):
                    print(Error('diff_ty', node.lineno), '155')
                    return None
                return (rows1, cols1, ttype[op][vals1][vals2])
            else:
                print(op, type1, type2)
                print("matrices other than 2-dim nor supported, ", node.lineno)
                global is_error
                is_error = True
                return None

        if op in castable_matrix_operations:  # matrix op on non-matrix type
            print(Error('mat_op_on_non_mat', node.lineno))
            return None

        if ttype_contains((op[0], type1, type2)):
            return ttype[op][type1][type2]

        print(type1, type2)
        print(Error('diff_ty', node.lineno), '164')

    def visit_Variable(self, node):
        var = symtable.get(node.name)
        if var is None:
            print(Error("no_var", node.lineno))
            return None
        return var.type

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_Range(self, node):
        t1 = self.visit(node.from_)
        t2 = self.visit(node.to)

        return "int" if t1 == t2 == "int" else None

    def visit_Ref(self, node):
        x_type = self.visit(node.x)
        y_type = self.visit(node.y)
        tmp = symtable
        var = node.var
        varAST = symtable.get(var.name)
        var_type = varAST.type

        if not isinstance(var_type, tuple):
            print(Error("no_var", node.lineno))
            return None
        rows, cols, mat_type = var_type[0], var_type[1], var_type[2]
        if x_type == y_type == "int":
            if hasattr(node.x, "value") and (
                    node.x.value < 0 or node.x.value >= rows or node.y.value < 0 or node.y.value >= cols):
                print(Error("inv_mat_arg_values", node.lineno))
                return None
            return mat_type
        else:
            print(Error("inv_mat_arg_types", node.lineno))
            return None

    def visit_UnaryMinus(self, node):
        return self.visit(node.expr)

    def visit_UnaryTranspose(self, node):
        type1 = self.visit(node.expr)
        if not isinstance(type1, tuple):
            print(Error("inv_transpose", node.lineno))
            return None
        return type1[1], type1[0], type1[2]

    def visit_IfStatement(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            print(Error("not_logic", node.lineno))
        symtable.pushScope("if")
        self.visit(node.ifBlock)
        symtable.popScope()
        if node.elseBlock is not None:
            symtable.pushScope("else")
            self.visit(node.elseBlock)
            symtable.popScope()

    def visit_ForLoop(self, node):
        type1 = self.visit(node.range_)
        if type1 != "int":
            print(Error("inv_range", node.lineno))
        symtable.put(node.var.name, type1)
        symtable.pushScope("loop")
        self.visit(node.block)
        symtable.popScope()

    def visit_WhileLoop(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            print(Error("not_logic", node.lineno))
        symtable.pushScope("loop")
        self.visit(node.block)
        symtable.popScope()

    def visit_BreakInstruction(self, node):
        loop_scope = symtable.getScope("loop")
        if loop_scope is None:
            print(Error("no_loop_scope_break", node.lineno))

    def visit_ContinueInstruction(self, node):
        loop_scope = symtable.getScope("loop")
        if loop_scope is None:
            print(Error("no_loop_scope_continue", node.lineno))

    def visit_ReturnStatement(self, node):
        if node.value:
            self.visit(node.value)

    def visit_Printable(self, node):
        self.visit(node.printable)

    def visit_PrintStatement(self, node):
        n = node.content
        while isinstance(n, AST.Node):
            self.visit(n.right)
            n = n.left
        self.visit(n)

    def visit_MatrixSpecialWord(self, node):
        n = node.value
        sizes = []
        while isinstance(n, AST.Node):
            if self.visit(n.right) != "int":
                print(Error("inv_mat_arg", node.lineno))
            if isinstance(n.right, AST.IntNum):
                sizes = [n.right.value] + sizes
            else:
                sizes = ["VARIABLE_SIZE"] + sizes
            n = n.left
        if self.visit(n) != "int":
            print(Error("inv_mat_arg", node.lineno))
        if isinstance(n, AST.IntNum):
            sizes = [n.value] + sizes
        else:
            sizes = ["VARIABLE_SIZE"] + sizes

        if len(sizes) == 1:
            sizes = sizes * 2
        res_type = sizes + ["int"]
        return tuple(res_type)

    def visit_Vector(self, node):
        n = node.inside
        elem_type = self.visit(n.right)
        l = 0
        while isinstance(n, AST.Node):
            if elem_type != self.visit(n.right):
                print(Error("diff_ty", node.lineno))
            n = n.left
            l += 1
        if elem_type != self.visit(n):
            print(Error("diff_ty", node.lineno))
        l += 1
        return (l, elem_type)

    def visit_Matrix(self, node):
        n = node.inside
        size, elem_type = self.visit(n.right)
        rows_numb = 0
        while isinstance(n, AST.Node):
            if self.visit(n.right) != (size, elem_type):
                print(Error("diff_ty", node.lineno))
            n = n.left
            rows_numb += 1
        if (size, elem_type) != self.visit(n):
            print(Error("diff_ty", node.lineno))
        rows_numb += 1
        return rows_numb, size, elem_type

    def visit_Error(self, node):
        print(Error("error", node.lineno))
