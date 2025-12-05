from enum import Enum


class ColorCode:
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return self.code

    def __add__(self, other):
        return self.code + str(other)

    def __radd__(self, other):
        return str(other) + self.code


class Color(Enum):
    RED = ColorCode("\033[31m")
    GREEN = ColorCode("\033[32m")
    YELLOW = ColorCode("\033[33m")
    BLUE = ColorCode("\033[34m")
    MAGENTA = ColorCode("\033[35m")
    CYAN = ColorCode("\033[36m")
    WHITE = ColorCode("\033[37m")
    RESET = ColorCode("\033[0m")
    NONE = ColorCode("")

    BOLD = ColorCode("\033[1m")
    UNDERLINE = ColorCode("\033[4m")
    REVERSE = ColorCode("\033[07m")
    STRIKETHROUGH = ColorCode("\033[09m")
    BLINK = ColorCode("\033[5m")
    ITALIC = ColorCode("\033[3m")

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return str(self.value) + str(other)

    def __radd__(self, other):
        return str(other) + str(self.value)