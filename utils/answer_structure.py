class AnswerResult:

    error = -1
    success = 0

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message