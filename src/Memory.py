class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.memory = {}

    def has_key(self, name):  # variable name
        return name in self.memory.keys()

    def get(self, name):  # gets from memory current value of variable <name>
        if self.has_key(name):
            return self.memory[name]
        return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memoryStack = [memory]

    def get(self, name):  # gets from memory stack current value of variable <name>
        for memory in reversed(self.memoryStack):
            if memory.has_key(name):
                return memory[name]
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.memoryStack[-1][name] = value

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.memoryStack):
            if memory.has_key(name):
                memory[name] = value
                return

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.memoryStack.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.memoryStack.pop()
