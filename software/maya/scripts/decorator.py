
from functools import wraps

import maya.mel as mel


#************************
# Decorators
def viewport_off(func):

    @wraps(func)
    def viewport(*args, **kwargs):

        try:
            # viewport OFF
            mel.eval("paneLayout -e -manage false $gMainPane")
            return func(*args, **kwargs)
        except Exception:
            raise
        finally:
            # viewport ON
            mel.eval("paneLayout -e -manage true $gMainPane")

    return viewport
