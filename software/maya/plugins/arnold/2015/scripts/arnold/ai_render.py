
from ctypes import *
from .arnold_common import ai
from .ai_types import *

# Rendering modes
#
AI_RENDER_MODE_CAMERA = 0  ## Instruct Arnold to render from a camera
AI_RENDER_MODE_FREE =   1  ## Put Arnold in a mode to process arbitrary ray requests

# Error codes
#
AI_SUCCESS =                       0x00    ## no error
AI_ABORT =                         0x01    ## render aborted
AI_ERROR_WRONG_OUTPUT =            0x02    ## can't open output file
AI_ERROR_NO_CAMERA =               0x03    ## camera not defined
AI_ERROR_BAD_CAMERA =              0x04    ## bad camera data
AI_ERROR_VALIDATION =              0x05    ## usage not validated
AI_ERROR_RENDER_REGION =           0x06    ## invalid render region
AI_ERROR_OUTPUT_EXISTS =           0x07    ## output file already exists
AI_ERROR_OPENING_FILE =            0x08    ## can't open file
AI_INTERRUPT =                     0x09    ## render interrupted by user
AI_ERROR_UNRENDERABLE_SCENEGRAPH = 0x0A    ## unrenderable scenegraph
AI_ERROR_NO_OUTPUTS =              0x0B    ## no rendering outputs
AI_ERROR =                           -1    ## generic error

AiBegin = ai.AiBegin

AiEnd = ai.AiEnd

AiRenderFunc = ai.AiRender
AiRenderFunc.argtypes = [c_int]
AiRenderFunc.restype = c_int

def AiRender(mode = AI_RENDER_MODE_CAMERA):
    return AiRenderFunc(mode)

AiRenderAbort = ai.AiRenderAbort

AiRenderInterrupt = ai.AiRenderInterrupt

AiRendering = ai.AiRendering
AiRendering.restype = c_bool
