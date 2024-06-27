from enum import Enum


class Role(Enum):
    AGENT = "AGENT"
    CUSTOMER = "CUSTOMER"

    @property
    def title(self):
        if self == Role.AGENT:
            return "Agente"
        elif self == Role.CUSTOMER:
            return "Cliente"
