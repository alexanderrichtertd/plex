
# TODO: Add callback handling

from ctypes import *
from .arnold_common import ai
from .ai_types import *

# Severity levels (for callback function)
#
AI_SEVERITY_INFO =      0x00  ## regular information message
AI_SEVERITY_WARNING =   0x01  ## warning message
AI_SEVERITY_ERROR =     0x02  ## error message
AI_SEVERITY_FATAL =     0x03  ## fatal error message

# Logging flags
#
AI_LOG_NONE =          0x0000  ## don't show any messages
AI_LOG_INFO =          0x0001  ## show all regular information messages
AI_LOG_WARNINGS =      0x0002  ## show warning messages
AI_LOG_ERRORS =        0x0004  ## show error messages
AI_LOG_DEBUG =         0x0008  ## show debug messages
AI_LOG_STATS =         0x0010  ## show detailed render statistics
AI_LOG_ASS_PARSE =     0x0020  ## show .ass-file parsing details
AI_LOG_PLUGINS =       0x0040  ## show details about plugins loaded
AI_LOG_PROGRESS =      0x0080  ## show a progress message at 5% increments while rendering
AI_LOG_NAN =           0x0100  ## show warnings for pixels with NaN's
AI_LOG_TIMESTAMP =     0x0200  ## prefix messages with a timestamp (elapsed time)
AI_LOG_BACKTRACE =     0x0400  ## show the stack contents after abnormal program termination (\c SIGSEGV, etc)
AI_LOG_MEMORY =        0x0800  ## prefix messages with current memory usage
AI_LOG_COLOR =         0x1000  ## add colors to log messages based on severity
AI_LOG_SSS =           0x2000  ## show messages about sub-surface scattering pointclouds
AI_LOG_ALL = AI_LOG_INFO      | AI_LOG_WARNINGS  | AI_LOG_ERRORS    | \
             AI_LOG_DEBUG     | AI_LOG_STATS     | AI_LOG_PLUGINS   | \
             AI_LOG_PROGRESS  | AI_LOG_NAN       | AI_LOG_ASS_PARSE | \
             AI_LOG_TIMESTAMP | AI_LOG_BACKTRACE | AI_LOG_MEMORY    | \
             AI_LOG_COLOR     | AI_LOG_SSS

AiMsgSetLogFileName = ai.AiMsgSetLogFileName
AiMsgSetLogFileName.argtypes = [AtString]

AiMsgSetLogFileFlags = ai.AiMsgSetLogFileFlags
AiMsgSetLogFileFlags.argtypes = [c_int]

AiMsgSetConsoleFlags = ai.AiMsgSetConsoleFlags
AiMsgSetConsoleFlags.argtypes = [c_int]

AiMsgSetMaxWarnings = ai.AiMsgSetMaxWarnings
AiMsgSetMaxWarnings.argtypes = [c_int]

# Callback function receives the following parameters:
#     int    --> log mask
#     int    --> message severity level
#     string --> message string
#     int    --> tabs
AtMsgCallBack = CFUNCTYPE(None, c_int, c_int, AtString, c_int)

_AiMsgSetCallback = ai.AiMsgSetCallback
_AiMsgSetCallback.argtypes = [AtMsgCallBack]

def AiMsgSetCallback(cb):
    # keep a reference to avoid the callback getting garbage collected
    ai.msg_callback_reference = cb
    _AiMsgSetCallback(cb)

_AiMsgResetCallback = ai.AiMsgResetCallback

def AiMsgResetCallback():
    ai.msg_callback_reference = None
    _AiMsgResetCallback()

def AiMsgInfo(format, *params):
    ai.AiMsgInfo(format, *params)

def AiMsgDebug(format, *params):
    ai.AiMsgDebug(format, *params)

def AiMsgWarning(format, *params):
    ai.AiMsgWarning(format, *params)

def AiMsgError(format, *params):
    ai.AiMsgError(format, *params)

def AiMsgFatal(format, *params):
    ai.AiMsgFatal(format, *params)

AiMsgTab = ai.AiMsgTab
AiMsgTab.argtypes = [c_int]

AiMsgUtilGetUsedMemory = ai.AiMsgUtilGetUsedMemory
AiMsgUtilGetUsedMemory.restype = AtUInt64

AiMsgUtilGetElapsedTime = ai.AiMsgUtilGetElapsedTime
AiMsgUtilGetElapsedTime.restype = AtUInt32
