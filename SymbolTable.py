#!/usr/bin/python


class VariableSymbol:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return f'{self.name} : {self.type}'


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.scopes = [({}, "global")]
        self.current_scope = 0

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.scopes[self.current_scope][0][name] = VariableSymbol(name, symbol)

    def get(self, name):  # get variable symbol or fundef from <name> entry
        iScope = self.current_scope
        while iScope >= 0:
            if name in self.scopes[iScope][0]:
                return self.scopes[iScope][0][name]
            iScope -= 1
        return None

    def getParentScope(self):
        return self.parent

    def getScope(self, name):
        iScope = self.current_scope
        while iScope >= 0:
            if self.scopes[iScope][1] == name:
                return self.scopes[iScope]
            iScope -= 1
        return None

    def pushScope(self, name):
        self.scopes.append(({}, name))
        self.current_scope += 1

    def popScope(self):
        self.scopes.pop()
        self.current_scope -= 1
