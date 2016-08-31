
from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_color import *
from .ai_types import *
from .ai_vector import *
from .ai_matrix import *

class AtArray(Structure):
    _fields_ = [("data",      c_void_p),
                ("nelements", AtUInt32),
                ("nkeys",     AtByte),
                ("type",      AtByte)]

ai.AiArray.restype = POINTER(AtArray)

def AiArray(nelems, keys, type, *params):
    return ai.AiArray(nelems, keys, type, *params)

_AiArrayAllocate = ai.AiArrayAllocate
_AiArrayAllocate.argtypes = [AtUInt32, AtByte, AtByte]
_AiArrayAllocate.restype = c_void_p

def AiArrayAllocate(nelements, nkeys, type):
    return NullToNone(_AiArrayAllocate(nelements, nkeys, type), POINTER(AtArray))

AiArrayDestroy = ai.AiArrayDestroy
AiArrayDestroy.argtypes = [POINTER(AtArray)]

_AiArrayConvert = ai.AiArrayConvert
_AiArrayConvert.argtypes = [AtUInt32, AtByte, AtByte, c_void_p]
_AiArrayConvert.restype = c_void_p

def AiArrayConvert(nelements, nkeys, type, data):
    return NullToNone(_AiArrayConvert(nelements, nkeys, type, data), POINTER(AtArray))

ai.AiArrayModify.restype = c_void_p

def AiArrayModify(array, nelems, keys, type, *params):
    return NullToNone(ai.AiArrayModify(array, nelems, keys, type, *params), POINTER(AtArray))

_AiArrayCopy = ai.AiArrayCopy
_AiArrayCopy.argtypes = [POINTER(AtArray)]
_AiArrayCopy.restype = c_void_p

def AiArrayCopy(array):
    return NullToNone(_AiArrayCopy(array), POINTER(AtArray))

AiArraySetKey = ai.AiArraySetKey
AiArraySetKey.argtypes = [POINTER(AtArray), AtByte, c_void_p]
AiArraySetKey.restype = c_bool

AiArrayInterpolatePnt = ai.AiArrayInterpolatePnt
AiArrayInterpolatePnt.argtypes = [POINTER(AtArray), c_float, AtUInt32]
AiArrayInterpolatePnt.restype = AtPoint

AiArrayInterpolateVec = ai.AiArrayInterpolateVec
AiArrayInterpolateVec.argtypes = [POINTER(AtArray), c_float, AtUInt32]
AiArrayInterpolateVec.restype = AtVector

AiArrayInterpolateFlt = ai.AiArrayInterpolateFlt
AiArrayInterpolateFlt.argtypes = [POINTER(AtArray), c_float, AtUInt32]
AiArrayInterpolateFlt.restype = c_float

AiArrayInterpolateMtx = ai.AiArrayInterpolateMtx
AiArrayInterpolateMtx.argtypes = [POINTER(AtArray), c_float, AtUInt32, POINTER(AtMatrix)]

# AtArray getters
#
AiArrayGetBool = ai.AiArrayGetBoolFunc
AiArrayGetBool.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetBool.restype = c_bool

AiArrayGetByte = ai.AiArrayGetByteFunc
AiArrayGetByte.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetByte.restype = AtByte

AiArrayGetInt = ai.AiArrayGetIntFunc
AiArrayGetInt.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetInt.restype = c_int

AiArrayGetUInt = ai.AiArrayGetUIntFunc
AiArrayGetUInt.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetUInt.restype = c_uint

AiArrayGetFlt = ai.AiArrayGetFltFunc
AiArrayGetFlt.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetFlt.restype = c_float

AiArrayGetPnt = ai.AiArrayGetPntFunc
AiArrayGetPnt.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetPnt.restype = AtPoint

AiArrayGetPnt2 = ai.AiArrayGetPnt2Func
AiArrayGetPnt2.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetPnt2.restype = AtPoint2

AiArrayGetVec = ai.AiArrayGetVecFunc
AiArrayGetVec.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetVec.restype = AtVector

AiArrayGetRGB = ai.AiArrayGetRGBFunc
AiArrayGetRGB.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetRGB.restype = AtRGB

AiArrayGetRGBA = ai.AiArrayGetRGBAFunc
AiArrayGetRGBA.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetRGBA.restype = AtRGBA

AiArrayGetPtr = ai.AiArrayGetPtrFunc
AiArrayGetPtr.argtypes = [POINTER(AtArray), AtUInt32]
AiArrayGetPtr.restype = c_void_p

_AiArrayGetStr = ai.AiArrayGetStrFunc
_AiArrayGetStr.argtypes = [POINTER(AtArray), AtUInt32]
_AiArrayGetStr.restype = AtString

def AiArrayGetStr(array, index):
    return AtStringToStr(_AiArrayGetStr(array, index))

_AiArrayGetArray = ai.AiArrayGetArrayFunc
_AiArrayGetArray.argtypes = [POINTER(AtArray), AtUInt32]
_AiArrayGetArray.restype = c_void_p

def AiArrayGetArray(array, index):
    return NullToNone(_AiArrayGetArray(array, index), POINTER(AtArray))

AiArrayGetMtx = ai.AiArrayGetMtxFunc
AiArrayGetMtx.argtypes = [POINTER(AtArray), AtUInt32, POINTER(AtMatrix)]

# AtArray setters
#

AiArraySetBool = ai.AiArraySetBoolFunc
AiArraySetBool.argtypes = [POINTER(AtArray), AtUInt32, c_bool]

AiArraySetByte = ai.AiArraySetByteFunc
AiArraySetByte.argtypes = [POINTER(AtArray), AtUInt32, AtByte]

AiArraySetInt = ai.AiArraySetIntFunc
AiArraySetInt.argtypes = [POINTER(AtArray), AtUInt32, c_int]

AiArraySetUInt = ai.AiArraySetUIntFunc
AiArraySetUInt.argtypes = [POINTER(AtArray), AtUInt32, c_uint]

AiArraySetFlt = ai.AiArraySetFltFunc
AiArraySetFlt.argtypes = [POINTER(AtArray), AtUInt32, c_float]

AiArraySetRGB = ai.AiArraySetRGBFunc
AiArraySetRGB.argtypes = [POINTER(AtArray), AtUInt32, AtRGB]

AiArraySetRGBA = ai.AiArraySetRGBAFunc
AiArraySetRGBA.argtypes = [POINTER(AtArray), AtUInt32, AtRGBA]

AiArraySetPnt = ai.AiArraySetPntFunc
AiArraySetPnt.argtypes = [POINTER(AtArray), AtUInt32, AtPoint]

AiArraySetPnt2 = ai.AiArraySetPnt2Func
AiArraySetPnt2.argtypes = [POINTER(AtArray), AtUInt32, AtPoint2]

AiArraySetVec = ai.AiArraySetVecFunc
AiArraySetVec.argtypes = [POINTER(AtArray), AtUInt32, AtVector]

AiArraySetMtx = ai.AiArraySetMtxFunc
AiArraySetMtx.argtypes = [POINTER(AtArray), AtUInt32, POINTER(AtMatrix)]

AiArraySetStr = ai.AiArraySetStrFunc
AiArraySetStr.argtypes = [POINTER(AtArray), AtUInt32, AtString]

AiArraySetPtr = ai.AiArraySetPtrFunc
AiArraySetPtr.argtypes = [POINTER(AtArray), AtUInt32, c_void_p]

AiArraySetArray = ai.AiArraySetArrayFunc
AiArraySetArray.argtypes = [POINTER(AtArray), AtUInt32, POINTER(AtArray)]
