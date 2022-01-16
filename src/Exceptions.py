class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass


class ReturnValueException(Exception):
    def __init__(self, value):
        self.value = value


class ReturnException(Exception):
    pass
