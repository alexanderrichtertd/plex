
from ctypes import *
from .arnold_common import ai
from .ai_types import *

ai.AiGetVersion.argtypes = [AtString, AtString, AtString, AtString]
ai.AiGetVersion.restype = AtString

# NOTE: The following two functions differ from Arnold API. They represent the functionality
#       of AiGetVersion() in a Python friendly way

# Returns version numbers as a 4-element list: [arch, major, minor, fix]
def AiGetVersion():
    arch = create_string_buffer(10)
    major = create_string_buffer(10)
    minor = create_string_buffer(10)
    fix = create_string_buffer(20)
    ai.AiGetVersion(arch, major, minor, fix)
    return [arch.value, major.value, minor.value, fix.value]

def AiGetVersionString():
    arch = AtString()
    major = AtString()
    minor = AtString()
    fix = AtString()
    return AtStringToStr(ai.AiGetVersion(arch, major, minor, fix))

_AiGetVersionInfo = ai.AiGetVersionInfo
_AiGetVersionInfo.restype = AtString

def AiGetVersionInfo():
    return AtStringToStr(_AiGetVersionInfo())

_AiGetCompileOptions = ai.AiGetCompileOptions
_AiGetCompileOptions.restype = AtString

def AiGetCompileOptions():
    return AtStringToStr(_AiGetCompileOptions())

AiCheckAPIVersion = ai.AiCheckAPIVersion
AiCheckAPIVersion.argtypes = [AtString, AtString, AtString]
AiCheckAPIVersion.restype = c_bool

AiSetAppString = ai.AiSetAppString
AiSetAppString.argtypes = [AtString]
