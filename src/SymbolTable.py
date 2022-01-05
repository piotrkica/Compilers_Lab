class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):  # put variable symbol under <name> entry
        self.symbols[name] = symbol

    def get(self, name):  # get variable symbol from <name> entry
        def _parent_get():
            return self.parent.get(name) if self.parent else None
        return self.symbols.get(name, None) or _parent_get()

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent
