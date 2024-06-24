from enum import Enum


class TokenType(Enum):
    GREETING = "GREETING"
    FAREWELL = "FAREWELL"
    GOOD = "GOOD"
    BAD = "BAD"
    NEUTRAL = "NEUTRAL"

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
