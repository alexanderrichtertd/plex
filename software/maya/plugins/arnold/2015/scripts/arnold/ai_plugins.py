
from ctypes import *
from .arnold_common import ai
from .ai_types import *

AiLoadPlugins = ai.AiLoadPlugins
AiLoadPlugins.argtypes = [AtString]

AiLoadPlugin = ai.AiLoadPlugin
AiLoadPlugin.argtypes = [AtString]
