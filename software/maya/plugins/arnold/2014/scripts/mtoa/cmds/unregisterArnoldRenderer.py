import maya.cmds as cmds
import arnoldShelf
import rendererCallbacks

def unregisterArnoldRenderer():
    cmds.deleteUI('ArnoldMenu', menu=True)
    cmds.renderer('arnold', unregisterRenderer=True)
    arnoldShelf.removeArnoldShelf()
    rendererCallbacks.clearCallbacks()
