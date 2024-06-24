from speech_analytics.models.token_type import TokenType


class WordInfo:
    def __init__(self, token: TokenType, weight: int):
        self.token = token
        self.weight = weight
