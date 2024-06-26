from enum import Enum


class TokenType(Enum):
    GREETING = "GREETING"
    FAREWELL = "FAREWELL"
    GOOD = "GOOD"
    BAD = "BAD"
    NEUTRAL = "NEUTRAL"

    @property
    def title(self):
        if self == TokenType.GREETING:
            return "SALUDO"
        elif self == TokenType.FAREWELL:
            return "DESPEDIDA"
        elif self == TokenType.GOOD:
            return "BUENO"
        elif self == TokenType.BAD:
            return "MALO"
        else:
            return "NEUTRAL"

    @property
    def message(self):
        if self == TokenType.GREETING:
            return "Hello! How can I help you?"
        elif self == TokenType.FAREWELL:
            return "Goodbye! Have a great day!"
        elif self == TokenType.GOOD:
            return "Thank you!"
        elif self == TokenType.BAD:
            return "I'm sorry to hear that."
        else:
            return "Unknown token type."

    @property
    def weight(self):
        if self == TokenType.GREETING:
            return 2
        if self == TokenType.FAREWELL:
            return 2
        if self == TokenType.GOOD:
            return 1
        if self == TokenType.BAD:
            return 5
        if self == TokenType.NEUTRAL:
            return 0
