
from ctypes import *
from .arnold_common import ai
from .ai_types import *

AtEnum = POINTER(AtString)

AiEnumGetValue = ai.AiEnumGetValue
AiEnumGetValue.argtypes = [AtEnum, AtString]
AiEnumGetValue.restype = c_int

_AiEnumGetString = ai.AiEnumGetString
_AiEnumGetString.argtypes = [AtEnum, c_int]
_AiEnumGetString.restype = AtString

def AiEnumGetString(enum_type, index):
    return AtStringToStr(_AiEnumGetString(enum_type, index))
