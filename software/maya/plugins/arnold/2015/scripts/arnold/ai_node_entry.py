
from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_deprecated import *
from .ai_types import *
from .ai_params import *

# Node types
#
AI_NODE_UNDEFINED =  0x0000  ## Undefined type
AI_NODE_OPTIONS =    0x0001  ## Options node (following the "singleton" pattern, there is only one options node)
AI_NODE_CAMERA =     0x0002  ## Camera nodes (\c persp_camera, \c fisheye_camera, etc)
AI_NODE_LIGHT =      0x0004  ## Light source nodes (\c spot_light, etc)
AI_NODE_SHAPE =      0x0008  ## Geometry nodes (\c sphere, \c polymesh, etc)
AI_NODE_SHADER =     0x0010  ## Shader nodes (\c lambert, etc)
AI_NODE_OVERRIDE =   0x0020  ## EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes
AI_NODE_DRIVER =     0x0040  ## Output driver nodes (\c driver_tiff, etc)
AI_NODE_FILTER =     0x0080  ## Pixel sample filter nodes (\c box_filter, etc
AI_NODE_ALL =        0xFFFF  ## Bitmask including all node types, used by AiASSWrite()

class AtNodeEntry(Structure):
    pass

class AtNodeMethods(Structure):
    pass

class AtParamIterator(Structure):
    pass

class AtMetaDataIterator(Structure):
    pass

class AtMetaDataEntry(Structure):
    _fields_ = [("name", AtString),
                ("param", AtString),
                ("type", AtByte),
                ("value", AtParamValue)]

_AiNodeEntryLookUp = ai.AiNodeEntryLookUp
_AiNodeEntryLookUp.argtypes = [AtString]
_AiNodeEntryLookUp.restype = c_void_p

def AiNodeEntryLookUp(name):
    return NullToNone(_AiNodeEntryLookUp(name), POINTER(AtNodeEntry))

_AiNodeEntryGetName = ai.AiNodeEntryGetName
_AiNodeEntryGetName.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetName.restype = AtString

def AiNodeEntryGetName(node_entry):
    return AtStringToStr(_AiNodeEntryGetName(node_entry))

AiNodeEntryGetType = ai.AiNodeEntryGetType
AiNodeEntryGetType.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetType.restype = c_int

_AiNodeEntryGetTypeName = ai.AiNodeEntryGetTypeName
_AiNodeEntryGetTypeName.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetTypeName.restype = AtString

def AiNodeEntryGetTypeName(node_entry):
    return AtStringToStr(_AiNodeEntryGetTypeName(node_entry))

AiNodeEntryGetOutputType = ai.AiNodeEntryGetOutputType
AiNodeEntryGetOutputType.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetOutputType.restype = c_int

_AiNodeEntryGetFilename = ai.AiNodeEntryGetFilename
_AiNodeEntryGetFilename.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetFilename.restype = c_void_p

def AiNodeEntryGetFilename(name):
    return NullToNone(_AiNodeEntryGetFilename(name), AtString)

_AiNodeEntryGetVersion = ai.AiNodeEntryGetVersion
_AiNodeEntryGetVersion.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetVersion.restype = AtString

def AiNodeEntryGetVersion(node_entry):
    return AtStringToStr(_AiNodeEntryGetVersion(node_entry))

AiNodeEntryGetCount = ai.AiNodeEntryGetCount
AiNodeEntryGetCount.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetCount.restype = c_int

AiNodeEntryGetNumParams = ai.AiNodeEntryGetNumParams
AiNodeEntryGetNumParams.argtypes = [POINTER(AtNodeEntry)]
AiNodeEntryGetNumParams.restype = c_int

_AiNodeEntryGetParameter = ai.AiNodeEntryGetParameter
_AiNodeEntryGetParameter.argtypes = [POINTER(AtNodeEntry), c_int]
_AiNodeEntryGetParameter.restype = c_void_p

def AiNodeEntryGetParameter(nentry, index):
    return NullToNone(_AiNodeEntryGetParameter(nentry, index), POINTER(AtParamEntry))

_AiNodeEntryLookUpParameter = ai.AiNodeEntryLookUpParameter
_AiNodeEntryLookUpParameter.argtypes = [POINTER(AtNodeEntry), AtString]
_AiNodeEntryLookUpParameter.restype = c_void_p

def AiNodeEntryLookUpParameter(nentry, name):
    return NullToNone(_AiNodeEntryLookUpParameter(nentry, name), POINTER(AtParamEntry))

AiNodeEntryInstall = ai.AiNodeEntryInstall
AiNodeEntryInstall.argtypes = [c_int, AtByte, AtString, AtString, POINTER(AtNodeMethods), AtString]

AiNodeEntryUninstall = ai.AiNodeEntryUninstall
AiNodeEntryUninstall.argtypes = [AtString]

@deprecated
def AiNodeInstall(type, output_type, name, filename, methods, version):
    return AiNodeEntryInstall(type, output_type, name, filename, methods, version)

@deprecated
def AiNodeUninstall(name):
    return AiNodeEntryUninstall(name)

_AiNodeEntryGetParamIterator = ai.AiNodeEntryGetParamIterator
_AiNodeEntryGetParamIterator.argtypes = [POINTER(AtNodeEntry)]
_AiNodeEntryGetParamIterator.restype = c_void_p

def AiNodeEntryGetParamIterator(nentry):
    return NullToNone(_AiNodeEntryGetParamIterator(nentry), POINTER(AtParamIterator))

_AiNodeEntryGetMetaDataIterator = ai.AiNodeEntryGetMetaDataIterator
_AiNodeEntryGetMetaDataIterator.argtypes = [POINTER(AtNodeEntry), AtString]
_AiNodeEntryGetMetaDataIterator.restype = c_void_p

def AiNodeEntryGetMetaDataIterator(nentry, param = None):
    return NullToNone(_AiNodeEntryGetMetaDataIterator(nentry, param), POINTER(AtMetaDataIterator))

AiParamIteratorDestroy = ai.AiParamIteratorDestroy
AiParamIteratorDestroy.argtypes = [POINTER(AtParamIterator)]

_AiParamIteratorGetNext = ai.AiParamIteratorGetNext
_AiParamIteratorGetNext.argtypes = [POINTER(AtParamIterator)]
_AiParamIteratorGetNext.restype = c_void_p

def AiParamIteratorGetNext(iter):
    return NullToNone(_AiParamIteratorGetNext(iter), POINTER(AtParamEntry))

AiParamIteratorFinished = ai.AiParamIteratorFinished
AiParamIteratorFinished.argtypes = [POINTER(AtParamIterator)]
AiParamIteratorFinished.restype = c_bool

AiMetaDataIteratorDestroy = ai.AiMetaDataIteratorDestroy
AiMetaDataIteratorDestroy.argtypes = [POINTER(AtMetaDataIterator)]

_AiMetaDataIteratorGetNext = ai.AiMetaDataIteratorGetNext
_AiMetaDataIteratorGetNext.argtypes = [POINTER(AtMetaDataIterator)]
_AiMetaDataIteratorGetNext.restype = c_void_p

def AiMetaDataIteratorGetNext(iter):
    return NullToNone(_AiMetaDataIteratorGetNext(iter), POINTER(AtMetaDataEntry))

AiMetaDataIteratorFinished = ai.AiMetaDataIteratorFinished
AiMetaDataIteratorFinished.argtypes = [POINTER(AtMetaDataIterator)]
AiMetaDataIteratorFinished.restype = c_bool
