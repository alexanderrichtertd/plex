
# TODO: Implement all driver functions

from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_node_entry import AtNodeEntry
from .ai_types import *

AtDisplayCallBack = CFUNCTYPE(None, c_uint, c_uint, c_uint, c_uint, POINTER(c_byte), c_void_p)

_AiFindDriverType = ai.AiFindDriverType
_AiFindDriverType.argtypes = [AtString]
_AiFindDriverType.restype = c_void_p

def AiFindDriverType(extension):
    return NullToNone(_AiFindDriverType(extension), POINTER(AtNodeEntry))

_AiDriverExtension = ai.AiDriverExtension
_AiDriverExtension.argtypes = [POINTER(AtNodeEntry)]
_AiDriverExtension.restype = c_void_p

def AiDriverExtension(nentry):
    return NullToNone(_AiDriverExtension(nentry), POINTER(AtString))
