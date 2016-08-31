
from ctypes import *
from .arnold_common import ai, NullToNone
from .ai_nodes import *
from .ai_bbox import *
from .ai_types import *

# Cache types
#
AI_CACHE_TEXTURE      = 0x0001  ## Flushes all texturemaps
AI_CACHE_SSS          = 0x0002  ## Flushes all irradiance pointclouds for sub-surface scattering
AI_CACHE_HAIR_DIFFUSE = 0x0004  ## Flushes hair diffuse cache
AI_CACHE_BACKGROUND   = 0x0008  ## Flushes all skydome importance tables for background
AI_CACHE_QUAD         = 0x0010  ## Flushes all quad lights importance tables
AI_CACHE_ALL          = 0xFFFF  ## Flushes all cache types simultaneously

class AtNodeIterator(Structure):
    pass

class AtNodeEntryIterator(Structure):
    pass

class AtAOVIterator(Structure):
    pass

class AtAOVEntry(Structure):
    _fields_ = [("name", AtString),
                ("type", AtByte),
                ("blend_mode", c_int)]

AiUniverseIsActive = ai.AiUniverseIsActive
AiUniverseIsActive.restype = c_bool

AiUniverseCacheFlush = ai.AiUniverseCacheFlush
AiUniverseCacheFlush.argtypes = [c_int]

_AiUniverseGetOptions = ai.AiUniverseGetOptions
_AiUniverseGetOptions.restype = c_void_p

def AiUniverseGetOptions():
    return NullToNone(_AiUniverseGetOptions(), POINTER(AtNode))

_AiUniverseGetCamera = ai.AiUniverseGetCamera
_AiUniverseGetCamera.restype = c_void_p

def AiUniverseGetCamera():
    return NullToNone(_AiUniverseGetCamera(), POINTER(AtNode))

AiUniverseGetSceneBounds = ai.AiUniverseGetSceneBounds
AiUniverseGetSceneBounds.restype = AtBBox

_AiUniverseGetNodeIterator = ai.AiUniverseGetNodeIterator
_AiUniverseGetNodeIterator.argtypes = [c_uint]
_AiUniverseGetNodeIterator.restype = c_void_p

def AiUniverseGetNodeIterator(mask):
    return NullToNone(_AiUniverseGetNodeIterator(mask), POINTER(AtNodeIterator))

_AiUniverseGetNodeEntryIterator = ai.AiUniverseGetNodeEntryIterator
_AiUniverseGetNodeEntryIterator.argtypes = [c_uint]
_AiUniverseGetNodeEntryIterator.restype = c_void_p

def AiUniverseGetNodeEntryIterator(mask):
    return NullToNone(_AiUniverseGetNodeEntryIterator(mask), POINTER(AtNodeEntryIterator))

_AiUniverseGetAOVIterator = ai.AiUniverseGetAOVIterator
_AiUniverseGetAOVIterator.argtypes = []
_AiUniverseGetAOVIterator.restype = c_void_p

def AiUniverseGetAOVIterator():
    return NullToNone(_AiUniverseGetAOVIterator(), POINTER(AtAOVIterator))

AiNodeIteratorDestroy = ai.AiNodeIteratorDestroy
AiNodeIteratorDestroy.argtypes = [POINTER(AtNodeIterator)]

_AiNodeIteratorGetNext = ai.AiNodeIteratorGetNext
_AiNodeIteratorGetNext.argtypes = [POINTER(AtNodeIterator)]
_AiNodeIteratorGetNext.restype = c_void_p

def AiNodeIteratorGetNext(iter):
    return NullToNone(_AiNodeIteratorGetNext(iter), POINTER(AtNode))

AiNodeIteratorFinished = ai.AiNodeIteratorFinished
AiNodeIteratorFinished.argtypes = [POINTER(AtNodeIterator)]
AiNodeIteratorFinished.restype = c_bool

AiNodeEntryIteratorDestroy = ai.AiNodeEntryIteratorDestroy
AiNodeEntryIteratorDestroy.argtypes = [POINTER(AtNodeEntryIterator)]

_AiNodeEntryIteratorGetNext = ai.AiNodeEntryIteratorGetNext
_AiNodeEntryIteratorGetNext.argtypes = [POINTER(AtNodeEntryIterator)]
_AiNodeEntryIteratorGetNext.restype = c_void_p

def AiNodeEntryIteratorGetNext(iter):
    return NullToNone(_AiNodeEntryIteratorGetNext(iter), POINTER(AtNodeEntry))

AiNodeEntryIteratorFinished = ai.AiNodeEntryIteratorFinished
AiNodeEntryIteratorFinished.argtypes = [POINTER(AtNodeEntryIterator)]
AiNodeEntryIteratorFinished.restype = c_bool

AiAOVIteratorDestroy = ai.AiAOVIteratorDestroy
AiAOVIteratorDestroy.argtypes = [POINTER(AtAOVIterator)]

_AiAOVIteratorGetNext = ai.AiAOVIteratorGetNext
_AiAOVIteratorGetNext.argtypes = [POINTER(AtAOVIterator)]
_AiAOVIteratorGetNext.restype = c_void_p

def AiAOVIteratorGetNext(iter):
    return NullToNone(_AiAOVIteratorGetNext(iter), POINTER(AtAOVEntry))

AiAOVIteratorFinished = ai.AiAOVIteratorFinished
AiAOVIteratorFinished.argtypes = [POINTER(AtAOVIterator)]
AiAOVIteratorFinished.restype = c_bool

AiTextureInvalidate = ai.AiTextureInvalidate
AiTextureInvalidate.argtypes = [AtString]
