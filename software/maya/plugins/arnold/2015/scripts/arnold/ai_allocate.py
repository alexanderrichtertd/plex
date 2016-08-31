
from ctypes import *
from .arnold_common import ai
from .ai_types import *

AiMalloc_func = ai.AiMalloc_func
AiMalloc_func.argtypes = [c_ulong, AtString, c_int, AtString]
AiMalloc_func.restype = c_void_p

def AiMalloc(size):
    return AiMalloc_func(size, '', 0, '')

AiRealloc_func = ai.AiRealloc_func
AiRealloc_func.argtypes = [c_void_p, c_ulong, AtString, c_int, AtString]
AiRealloc_func.restype = c_void_p

def AiRealloc(addr, size):
    return AiRealloc_func(addr, size, '', 0, '')

AiFree_func = ai.AiFree_func
AiFree_func.argtypes = [c_void_p, AtString, c_int, AtString]

def AiFree(addr):
    AiFree_func(addr, '', 0, '')
