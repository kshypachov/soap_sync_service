from typing import Any

# модель відповіді
class AnswerResult:
    error = -1
    success = 0

    def __init__(self, code: int, message: Any):
        self.code = code
        self.message = message
