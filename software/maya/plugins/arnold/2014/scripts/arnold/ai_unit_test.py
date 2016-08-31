
from ctypes import *
from .arnold_common import ai
from .ai_types import *

AiTest = ai.AiTest
AiTest.restype = c_bool
