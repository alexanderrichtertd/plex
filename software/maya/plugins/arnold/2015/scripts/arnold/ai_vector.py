
import math
from ctypes import *
from .arnold_common import ai
from .ai_constants import *
from .ai_types import *

# 3D point
class AtPoint(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]

    def __init__(self, *args):
        if len(args) == 3:
            self.x = float(args[0])
            self.y = float(args[1])
            self.z = float(args[2])
        elif len(args) == 1:
            self.x = float(args[0])
            self.y = float(args[0])
            self.z = float(args[0])

    def clamp(self, lo, hi):
        out = AtPoint()
        out.x = lo if self.x < lo else hi if self.x > hi else self.x
        out.y = lo if self.y < lo else hi if self.y > hi else self.y
        out.z = lo if self.z < lo else hi if self.z > hi else self.z
        return out

    def isSmall(self, epsilon = AI_EPSILON):
        return abs(self.x) < epsilon and abs(self.y) < epsilon and abs(self.z) < epsilon

    ## Arithmetic operators

    def __add__(self, other):
        if isinstance(other, AtPoint):
            return AtPoint(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return AtPoint(self.x + float(other), self.y + float(other), self.z + float(other))

    def __sub__(self, other):
        if isinstance(other, AtPoint):
            return AtPoint(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return AtPoint(self.x - float(other), self.y - float(other), self.z - float(other))

    def __mul__(self, other):
        if isinstance(other, AtPoint):
            return AtPoint(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return AtPoint(self.x * float(other), self.y * float(other), self.z * float(other))

    def __div__(self, other):
        if isinstance(other, AtPoint):
            return AtPoint(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return AtPoint(self.x / float(other), self.y / float(other), self.z / float(other))

    def __neg__(self):
        return AtPoint(-self.x, -self.y, -self.z)

    ## Comparison operators

    def __eq__(self, other):
        if isinstance(other, AtPoint):
            return (self.x == other.x and self.y == other.y and self.z == other.z)
        else:
            return (self.x == float(other) and self.y == float(other) and self.z == float(other))

    def __ne__(self, other):
        if isinstance(other, AtPoint):
            return (self.x != other.x or self.y != other.y or self.z != other.z)
        else:
            return (self.x != float(other) or self.y != float(other) or self.z != float(other))

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        temp = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if temp != 0:
            temp = 1.0 / temp
        return AtPoint(self.x * temp, self.y * temp, self.z * temp)

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def cross(v1, v2):
    return AtPoint(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)

def distance(p1, p2):
    v = p2 - p1
    return v.length()

def distance2(p1, p2):
    v = p2 - p1
    return v.x * v.x + v.y * v.y + v.z * v.z

def distanceToPlane(x, n, p):
    return dot(x, n) - dot(p, n)

# 2D point
class AtPoint2(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]

    def __init__(self, *args):
        if len(args) == 2:
            self.x = float(args[0])
            self.y = float(args[1])
        elif len(args) == 1:
            self.x = float(args[0])
            self.y = float(args[0])

    def clamp(self, lo, hi):
        out = AtPoint2()
        out.x = lo if self.x < lo else hi if self.x > hi else self.x
        out.y = lo if self.y < lo else hi if self.y > hi else self.y
        return out

    def isSmall(self, epsilon = AI_EPSILON):
        return abs(self.x) < epsilon and abs(self.y) < epsilon

    ## Arithmetic operators

    def __add__(self, other):
        if isinstance(other, AtPoint2):
            return AtPoint2(self.x + other.x, self.y + other.y)
        else:
            return AtPoint2(self.x + float(other), self.y + float(other))

    def __sub__(self, other):
        if isinstance(other, AtPoint2):
            return AtPoint2(self.x - other.x, self.y - other.y)
        else:
            return AtPoint2(self.x - float(other), self.y - float(other))

    def __mul__(self, other):
        if isinstance(other, AtPoint2):
            return AtPoint2(self.x * other.x, self.y * other.y)
        else:
            return AtPoint2(self.x * float(other), self.y * float(other))

    def __div__(self, other):
        if isinstance(other, AtPoint2):
            return AtPoint2(self.x / other.x, self.y / other.y)
        else:
            return AtPoint2(self.x / float(other), self.y / float(other))

    def __neg__(self):
        return AtPoint2(-self.x, -self.y)

    ## Comparison operators

    def __eq__(self, other):
        if isinstance(other, AtPoint2):
            return (self.x == other.x and self.y == other.y)
        else:
            return (self.x == float(other) and self.y == float(other))

    def __ne__(self, other):
        if isinstance(other, AtPoint2):
            return (self.x != other.x or self.y != other.y)
        else:
            return (self.x != float(other) or self.y != float(other))

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y

def distance(p1, p2):
    v = p2 - p1
    return v.length()

def distance2(p1, p2):
    v = p2 - p1
    return v.x * v.x + v.y * v.y

# Homogeneous point
#
class AtHPoint(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float),
                ("w", c_float)]

AtVector = AtPoint
AtVector2 = AtPoint2

# Vector components
#
AI_X = 0
AI_Y = 1
AI_Z = 2

# Constants
#
AI_P3_ZERO = AtPoint(0, 0, 0)
AI_V3_ZERO = AtVector(0, 0, 0)
AI_V3_HALF = AtVector(0.5, 0.5, 0.5)
AI_V3_ONE  = AtVector(1, 1, 1)
AI_V3_X    = AtVector(1, 0, 0)
AI_V3_Y    = AtVector(0, 1, 0)
AI_V3_Z    = AtVector(0, 0, 1)
AI_V3_NEGX = AtVector(-1, 0, 0)
AI_V3_NEGY = AtVector(0, -1, 0)
AI_V3_NEGZ = AtVector(0, 0, -1)
AI_P2_ZERO = AtPoint2(0, 0)
AI_P2_ONE  = AtPoint2(1, 1)
