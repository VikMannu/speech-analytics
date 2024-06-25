from speech_analytics.models.token_type import TokenType


class Lexeme:
    def __init__(self, lexemes: [str], token: TokenType, weight: int):
        self.key: str = '_'.join(lexemes)
        self.lexemes = lexemes
        self.token = token
        if token == TokenType.NEUTRAL:
            self.weight = 0
        else:
            self.weight = weight
        self.length = len(lexemes)

    @property
    def root(self):
        return self.lexemes[0]

    def to_dict(self):
        return {
            'key': self.key,
            'lexemes': self.lexemes,
            'token': self.token.value,  # Use .value to get the enum value
            'weight': self.weight,
            'length': self.length
        }

    def __str__(self):
        return f"Lexema({' '.join(map(str, self.lexemes))}): {self.token.title}({self.weight})"
