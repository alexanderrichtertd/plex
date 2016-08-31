
# TODO: Implement bounding box functions

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_vector import *

class AtBBox(Structure):
    _fields_ = [("min", AtPoint),
                ("max", AtPoint)]

    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], AtPoint) and isinstance(args[1], AtPoint):
            self.min = args[0]
            self.max = args[1]
        elif len(args) == 6:
            self.min = AtPoint(args[0], args[1], args[2])
            self.max = AtPoint(args[3], args[4], args[5])

    ## Comparison operators

    def __eq__(self, other):
        if isinstance(other, AtBBox):
            return (self.min == other.min and self.max == other.max)
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, AtBBox):
            return (self.min != other.min or self.max != other.max)
        else:
            return True

class AtBBox2(Structure):
    _fields_ = [("minx", c_int),
                ("miny", c_int),
                ("maxx", c_int),
                ("maxy", c_int)]

    def __init__(self, *args):
        if len(args) == 4:
            self.minx = int(args[0])
            self.miny = int(args[1])
            self.maxx = int(args[2])
            self.maxy = int(args[3])

    ## Comparison operators

    def __eq__(self, other):
        if isinstance(other, AtBBox2):
            return (self.minx == other.minx and self.miny == other.miny and self.maxx == other.maxx and self.maxy == other.maxy)
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, AtBBox2):
            return (self.minx != other.minx or self.miny != other.miny or self.maxx != other.maxx or self.maxy != other.maxy)
        else:
            return True

# unit bounding-box
#
AI_BBOX_UNIT = AtBBox((0, 0, 0), (1, 1, 1))

# zero-width bounding-box
#
AI_BBOX_ZERO = AtBBox((0, 0, 0), (0, 0, 0))
