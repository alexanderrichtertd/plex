
from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_node_entry import *

AiASSWriteFunc = ai.AiASSWrite
AiASSWriteFunc.argtypes = [AtString, c_int, c_bool, c_bool]
AiASSWriteFunc.restype = c_int

def AiASSWrite(filename, mask = AI_NODE_ALL, open_procs = False, binary = True):
    return AiASSWriteFunc(filename, mask, open_procs, binary)

AiASSLoadFunc = ai.AiASSLoad
AiASSLoadFunc.argtypes = [AtString, c_int]
AiASSLoadFunc.restype = c_int

def AiASSLoad(filename, mask = AI_NODE_ALL):
    return AiASSLoadFunc(filename, mask)
