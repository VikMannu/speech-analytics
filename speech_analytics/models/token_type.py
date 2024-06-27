from enum import Enum


class TokenType(Enum):
    GREETING = "GREETING"
    FAREWELL = "FAREWELL"
    IDENTIFICATION = "IDENTIFICATION"
    GOOD = "GOOD"
    BAD = "BAD"
    NEUTRAL = "NEUTRAL"

    @property
    def title(self):
        if self == TokenType.GREETING:
            return "SALUDO"
        elif self == TokenType.FAREWELL:
            return "DESPEDIDA"
        elif self == TokenType.IDENTIFICATION:
            return "IDENTIFICACIÓN"
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
        elif self == TokenType.IDENTIFICATION:
            return "Please provide your document or ID."
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
        elif self == TokenType.FAREWELL:
            return 2
        elif self == TokenType.IDENTIFICATION:
            return 3
        elif self == TokenType.GOOD:
            return 1
        elif self == TokenType.BAD:
            return 5
        else:
            return 0
