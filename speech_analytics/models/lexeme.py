from speech_analytics.models.token_type import TokenType


class Lexeme:
    def __init__(self, lexemes: [str], token: TokenType, weight: int):
        self.lexemes = lexemes
        self.token = token
        self.weight = weight
        self.length = len(lexemes)
