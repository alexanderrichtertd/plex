
# TODO: Implement all matrix functions

from ctypes import *
from .arnold_common import ai
from .ai_types import *
from .ai_vector import *

class AtMatrix(Structure):
    _fields_ = [("a00", c_float),
                ("a01", c_float),
                ("a02", c_float),
                ("a03", c_float),
                ("a10", c_float),
                ("a11", c_float),
                ("a12", c_float),
                ("a13", c_float),
                ("a20", c_float),
                ("a21", c_float),
                ("a22", c_float),
                ("a23", c_float),
                ("a30", c_float),
                ("a31", c_float),
                ("a32", c_float),
                ("a33", c_float)]

AiM4Identity = ai.AiM4Identity
AiM4Identity.argtypes = [POINTER(AtMatrix)]

AiM4IsIdentity = ai.AiM4IsIdentity
AiM4IsIdentity.argtypes = [POINTER(AtMatrix)]
AiM4IsIdentity.restype = c_bool

AiM4IsSingular = ai.AiM4IsSingular
AiM4IsSingular.argtypes = [POINTER(AtMatrix)]
AiM4IsSingular.restype = c_bool

AiM4PointByMatrixMult = ai.AiM4PointByMatrixMult
AiM4PointByMatrixMult.argtypes = [POINTER(AtPoint), POINTER(AtMatrix), POINTER(AtPoint)]

AiM4VectorByMatrixMult = ai.AiM4VectorByMatrixMult
AiM4VectorByMatrixMult.argtypes = [POINTER(AtVector), POINTER(AtMatrix), POINTER(AtVector)]

AiM4Translation = ai.AiM4Translation
AiM4Translation.argtypes = [POINTER(AtMatrix), POINTER(AtVector)]

AiM4RotationX = ai.AiM4RotationX
AiM4RotationX.argtypes = [POINTER(AtMatrix), c_float]

AiM4RotationY = ai.AiM4RotationY
AiM4RotationY.argtypes = [POINTER(AtMatrix), c_float]

AiM4RotationZ = ai.AiM4RotationZ
AiM4RotationZ.argtypes = [POINTER(AtMatrix), c_float]

AiM4Scaling = ai.AiM4Scaling
AiM4Scaling.argtypes = [POINTER(AtMatrix), POINTER(AtVector)]

AiM4Frame = ai.AiM4Frame
AiM4Frame.argtypes = [POINTER(AtMatrix), POINTER(AtVector), POINTER(AtVector), POINTER(AtVector), POINTER(AtVector)]

AiM4HPointByMatrixMult = ai.AiM4HPointByMatrixMult
AiM4HPointByMatrixMult.argtypes = [POINTER(AtHPoint), POINTER(AtMatrix), POINTER(AtHPoint)]

AiM4VectorByMatrixTMult = ai.AiM4VectorByMatrixTMult
AiM4VectorByMatrixTMult.argtypes = [POINTER(AtVector), POINTER(AtMatrix), POINTER(AtVector)]

AiM4Mult = ai.AiM4Mult
AiM4Mult.argtypes = [POINTER(AtMatrix), POINTER(AtMatrix), POINTER(AtMatrix)]

AiM4Copy = ai.AiM4Copy
AiM4Copy.argtypes = [POINTER(AtMatrix), POINTER(AtMatrix)]

AiM4Transpose = ai.AiM4Transpose
AiM4Transpose.argtypes = [POINTER(AtMatrix), POINTER(AtMatrix)]

AiM4Invert = ai.AiM4Invert
AiM4Invert.argtypes = [POINTER(AtMatrix), POINTER(AtMatrix)]

AiM4Determinant = ai.AiM4Determinant
AiM4Determinant.argtypes = [POINTER(AtMatrix)]
AiM4Determinant.restype = c_double

AiM4Lerp = ai.AiM4Lerp
AiM4Lerp.argtypes = [POINTER(AtMatrix), c_float, POINTER(AtMatrix), POINTER(AtMatrix)]

AiM4Berp = ai.AiM4Berp
AiM4Berp.argtypes = [c_float, c_float, POINTER(AtMatrix), POINTER(AtMatrix), POINTER(AtMatrix), POINTER(AtMatrix)]
