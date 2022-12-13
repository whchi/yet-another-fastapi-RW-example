class BadArgsException(ValueError):
    ...


class ModelNotFoundException(ValueError):

    def __init__(self, message: str = ''):
        self.message = message
