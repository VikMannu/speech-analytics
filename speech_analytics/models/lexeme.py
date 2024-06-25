from speech_analytics.models.token_type import TokenType


class Lexeme:
    def __init__(self, lexemes: [str], token: TokenType, weight: int):
        self.key: str = '_'.join(lexemes)
        self.lexemes = lexemes
        self.token = token
        self.weight = weight
        self.length = len(lexemes)

    def __str__(self):
        return f"Lexema({' '.join(map(str, self.lexemes))}): {self.token.title}"
