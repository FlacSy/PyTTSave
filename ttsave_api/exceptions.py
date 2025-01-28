class TTSaveError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ServerError(TTSaveError):
    def __init__(self, message: str = "Ошибка сервера"):
        super().__init__(message)

class ParserError(TTSaveError):
    def __init__(self, message: str = "Ошибка при парсинге"):
        super().__init__(message)