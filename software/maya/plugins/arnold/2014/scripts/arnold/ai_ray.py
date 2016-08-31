
from ctypes import *

AI_RAY_UNDEFINED =  0x00         # undefined type
AI_RAY_CAMERA =     0x01         # ray originating at the camera
AI_RAY_SHADOW =     0x02         # shadow ray towards a light source
AI_RAY_REFLECTED =  0x04         # mirror reflection ray
AI_RAY_REFRACTED =  0x08         # mirror refraction ray
AI_RAY_SUBSURFACE = 0x10         # subsurface scattering probe ray
AI_RAY_DIFFUSE =    0x20         # indirect diffuse (also known as diffuse GI) ray
AI_RAY_GLOSSY =     0x40         # glossy/blurred reflection ray
AI_RAY_ALL =        0xFF         # mask for all ray types
AI_RAY_GENERIC =    AI_RAY_ALL   # mask for all ray types
