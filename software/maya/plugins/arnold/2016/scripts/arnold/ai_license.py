
from ctypes import *
from .arnold_common import ai
from .ai_types import *

AiLicenseSetServer = ai.AiLicenseSetServer
AiLicenseSetServer.argtypes = [AtString, c_uint]
AiLicenseSetServer.restype = c_bool

ai.AiLicenseGetServer.argtypes = [AtString, POINTER(c_uint)]
ai.AiLicenseGetServer.restype = c_bool

def AiLicenseGetServer(host, port):
    return ai.AiLicenseGetServer(host, byref(port))

AiLicenseSetAttempts = ai.AiLicenseSetAttempts
AiLicenseSetAttempts.argtypes = [c_int]

AiLicenseGetAttempts = ai.AiLicenseGetAttempts
AiLicenseGetAttempts.argtypes = []
AiLicenseGetAttempts.restype = c_uint

AiLicenseSetAttemptDelay = ai.AiLicenseSetAttemptDelay
AiLicenseSetAttemptDelay.argtypes = [c_int]

AiLicenseGetAttemptDelay = ai.AiLicenseGetAttemptDelay
AiLicenseGetAttemptDelay.argtypes = []
AiLicenseGetAttemptDelay.restype = c_uint

class AtLicenseInfo(Structure):
    _fields_ = [("used", c_bool),
                ("name", c_char * 64),
                ("ver", c_char * 64),
                ("exp", c_char * 64),
                ("options", c_char * 64),
                ("count", c_int),
                ("current_inuse", c_int),
                ("current_resuse", c_int),
                ("hbased", c_int),
                ("hold", c_int),
                ("max_roam", c_int),
                ("max_share", c_int),
                ("min_remove", c_int),
                ("min_checkout", c_int),
                ("min_timeout", c_int),
                ("nres", c_int),
                ("num_roam_allowed", c_int),
                ("roaming", c_int),
                ("share", c_int),
                ("soft_limit", c_int),
                ("thisroam", c_int),
                ("timeout", c_int),
                ("tz", c_int),
                ("tokens", c_int),
                ("type", c_int),
                ("ubased", c_int)]

AI_LIC_SUCCESS            =  0 # no error
AI_LIC_ERROR_CANTCONNECT  =  1 # can't connect to any rlm server
AI_LIC_ERROR_INIT         =  2 # error on initialization
AI_LIC_ERROR_NOTFOUND     =  3 # no licenses found (expired or not loaded)
AI_LIC_ERROR_NOTAVAILABLE =  4 # no licenses available (all in use)
AI_LIC_ERROR              = -1 # generic license error

ai.AiLicenseGetInfo.argtypes = [POINTER(POINTER(AtLicenseInfo)), POINTER(c_uint)]
ai.AiLicenseGetInfo.restype = c_int

def AiLicenseGetInfo(licenses, n):
    return ai.AiLicenseGetInfo(byref(licenses), byref(n))
