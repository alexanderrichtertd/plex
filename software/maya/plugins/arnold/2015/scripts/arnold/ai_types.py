
from ctypes import *
from .arnold_common import ai

import sys

# Arnold basic data types

AtInt8   = c_int8
AtInt16  = c_int16
AtInt32  = c_int32
AtInt64  = c_int64
AtByte   = c_ubyte
AtUInt8  = c_uint8
AtUInt16 = c_uint16
AtUInt32 = c_uint32
AtUInt64 = c_uint64

# for python 3, strings need to be converted to char pointers. we
# assume arnold takes utf-8 encoded strings 
if sys.version_info[0] >= 3:
    class AtString(c_char_p):
        @classmethod
        def from_param(cls, obj):
            if (obj is not None) and (not isinstance(obj, cls)):
                if isinstance(obj, str):
                    obj = obj.encode('utf-8')
            return c_char_p.from_param(obj)

        def __str__(self):
            if self.value is None:
                    return ""
            return self.decode()
      
        def decode(self):
            if self.value is None:
                return None
            return self.value.decode('utf-8')
     
    def AtStringToStr(astring):
        return str(astring)
else:
    AtString = c_char_p

    def AtStringToStr(string):
        return string

