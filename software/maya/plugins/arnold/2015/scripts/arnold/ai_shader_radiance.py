
from ctypes import *
from .arnold_common import ai
from .ai_color import *
from .ai_nodes import *
from .ai_vector import *

AiIrradiance = ai.AiIrradiance
AiIrradiance.argtypes = [POINTER(AtPoint), POINTER(AtVector), AtByte, AtUInt32]
AiIrradiance.restype = AtRGB

AiRadiance = ai.AiRadiance
AiRadiance.argtypes = [POINTER(AtPoint), POINTER(AtVector), POINTER(AtVector), POINTER(AtNode), AtUInt32, c_float, c_float, POINTER(AtNode), AtByte, AtUInt32]
AiRadiance.restype = AtRGB
