
# TODO: Implement all color functions

from ctypes import *
from .arnold_common import ai
from .ai_constants import *
from .ai_types import *

# RGB color
class AtRGB(Structure):
    _fields_ = [("r", c_float),
                ("g", c_float),
                ("b", c_float)]

    def __init__(self, *args):
        if len(args) == 3:
            self.r = float(args[0])
            self.g = float(args[1])
            self.b = float(args[2])
        elif len(args) == 1:
            self.r = float(args[0])
            self.g = float(args[0])
            self.b = float(args[0])

    def clamp(self, lo, hi):
        out = AtRGB()
        out.r = lo if self.r < lo else hi if self.r > hi else self.r
        out.g = lo if self.g < lo else hi if self.g > hi else self.g
        out.b = lo if self.b < lo else hi if self.b > hi else self.b
        return out

    def isSmall(self, epsilon = AI_EPSILON):
        return abs(self.r) < epsilon and abs(self.g) < epsilon and abs(self.b) < epsilon

    ## Arithmetic operators

    def __add__(self, other):
        if isinstance(other, AtRGB):
            return AtRGB(self.r + other.r, self.g + other.g, self.b + other.b)
        else:
            return AtRGB(self.r + float(other), self.g + float(other), self.b + float(other))

    def __sub__(self, other):
        if isinstance(other, AtRGB):
            return AtRGB(self.r - other.r, self.g - other.g, self.b - other.b)
        else:
            return AtRGB(self.r - float(other), self.g - float(other), self.b - float(other))

    def __mul__(self, other):
        if isinstance(other, AtRGB):
            return AtRGB(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            return AtRGB(self.r * float(other), self.g * float(other), self.b * float(other))

    def __div__(self, other):
        if isinstance(other, AtRGB):
            return AtRGB(self.r / other.r, self.g / other.g, self.b / other.b)
        else:
            return AtRGB(self.r / float(other), self.g / float(other), self.b / float(other))

    def __neg__(self):
        return AtRGB(-self.r, -self.g, -self.b)

    ## Comparison operators

    def __eq__(self, other):
        if isinstance(other, AtRGB):
            return (self.r == other.r and self.g == other.g and self.b == other.b)
        else:
            return (self.r == float(other) and self.g == float(other) and self.b == float(other))

    def __ne__(self, other):
        if isinstance(other, AtRGB):
            return (self.r != other.r or self.g != other.g or self.b != other.b)
        else:
            return (self.r != float(other) or self.g != float(other) or self.b != float(other))

AtColor = AtRGB

# RGB color + alpha
class AtRGBA(Structure):
    _fields_ = [("r", c_float),
                ("g", c_float),
                ("b", c_float),
                ("a", c_float)]

    def __init__(self, *args):
        if len(args) == 4:
            self.r = float(args[0])
            self.g = float(args[1])
            self.b = float(args[2])
            self.a = float(args[3])
        elif len(args) == 1:
            self.r = float(args[0])
            self.g = float(args[0])
            self.b = float(args[0])
            self.a = 1

    def rgb(self):
        return AtRGB(self.r, self.g, self.b)

    def clamp(self, lo, hi):
        out = AtRGBA()
        out.r = lo if self.r < lo else hi if self.r > hi else self.r
        out.g = lo if self.g < lo else hi if self.g > hi else self.g
        out.b = lo if self.b < lo else hi if self.b > hi else self.b
        out.a = lo if self.a < lo else hi if self.a > hi else self.a
        return out

    ## Arithmetic operators

    def __add__(self, other):
        if isinstance(other, AtRGBA):
            return AtRGBA(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)
        else:
            return AtRGBA(self.r + float(other), self.g + float(other), self.b + float(other), self.a + float(other))

    def __sub__(self, other):
        if isinstance(other, AtRGBA):
            return AtRGBA(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)
        else:
            return AtRGBA(self.r - float(other), self.g - float(other), self.b - float(other), self.a - float(other))

    def __mul__(self, other):
        if isinstance(other, AtRGBA):
            return AtRGBA(self.r * other.r, self.g * other.g, self.b * other.b, self.a * other.a)
        else:
            return AtRGBA(self.r * float(other), self.g * float(other), self.b * float(other), self.a * float(other))

    def __div__(self, other):
        if isinstance(other, AtRGBA):
            return AtRGBA(self.r / other.r, self.g / other.g, self.b / other.b, self.a / other.a)
        else:
            return AtRGBA(self.r / float(other), self.g / float(other), self.b / float(other), self.a / float(other))

    def __neg__(self):
        return AtRGBA(-self.r, -self.g, -self.b, -self.a)

    ## Comparison operators

    def __eq__(self, other):
        if isinstance(other, AtRGBA):
            return (self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a)
        else:
            return (self.r == float(other) and self.g == float(other) and self.b == float(other) and self.a == float(other))

    def __ne__(self, other):
        if isinstance(other, AtRGBA):
            return (self.r != other.r or self.g != other.g or self.b != other.b or self.a != other.a)
        else:
            return (self.r != float(other) or self.g != float(other) or self.b != float(other) or self.a != float(other))


AI_RGB_BLACK  = AtColor(0, 0, 0)         ## Black color declaration
AI_RGB_RED    = AtColor(1, 0, 0)         ## Red color declaration
AI_RGB_GREEN  = AtColor(0, 1, 0)         ## Green color declaration
AI_RGB_BLUE   = AtColor(0, 0, 1)         ## Blue color declaration
AI_RGB_50GREY = AtColor(0.5, 0.5, 0.5)   ## 50%-grey color declaration
AI_RGB_WHITE  = AtColor(1, 1, 1)         ## White color declaration

AI_RGBA_BLACK  = AtRGBA(0, 0, 0, 0)         ## Black color declaration
AI_RGBA_RED    = AtRGBA(1, 0, 0, 1)         ## Red color declaration
AI_RGBA_GREEN  = AtRGBA(0, 1, 0, 1)         ## Green color declaration
AI_RGBA_BLUE   = AtRGBA(0, 0, 1, 1)         ## Blue color declaration
AI_RGBA_50GREY = AtRGBA(0.5, 0.5, 0.5, 1)   ## 50%-grey color declaration
AI_RGBA_WHITE  = AtRGBA(1, 1, 1, 1)         ## White color declaration
