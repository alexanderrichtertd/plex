import maya.cmds as cmds
import maya.mel as mel

import mtoa.utils as utils
import mtoa.ui.ae.utils as aeUtils
from mtoa.ui.ae.utils import aeCallback

def aiSwatchLabel(nodeName) :
    type = cmds.nodeType(nodeName)
    classificationsList = cmds.getClassification(type)
    for classification in classificationsList :
        allClassList = classification.split(':')
        for allClass in allClassList :
            classList = allClass.split('/')
            if 'swatch' == classList[0] :
                continue
            else :
                if classList :
                    if 'shader' != classList[-1] :
                        classList = filter(lambda x:x!='shader', classList)
                    return "\n".join(map(lambda x:x.capitalize(), classList))
                else :
                    return "Sample"
                
def aiSwatchDisplayNew(plugName) :
    nodeAndAttrs = plugName.split(".")
    node = nodeAndAttrs[0]
        
    cmds.formLayout('swatchDisplayForm')
    cmds.text('swatchLabel', label=aiSwatchLabel(node))
    cmds.swatchDisplayPort('swatchDisplay',
                           wh=(64, 64), rs=64)
    cmds.popupMenu('swatchPopup', button=3)
    cmds.menuItem( 'swatchSmall', label='Small' )
    cmds.menuItem( 'swatchMedium', label='Medium' )
    cmds.menuItem( 'swatchLarge', label='Large' )
    cmds.setParent(upLevel=True)
    gTextColumnWidthIndex = mel.eval("$tempVar=$gTextColumnWidthIndex;")
    cmds.formLayout('swatchDisplayForm',
                    edit=True,
                    af=[('swatchLabel',"top", 0),
                        ('swatchLabel', "bottom", 0),
                        ('swatchDisplay',"top", 0),
                        ('swatchDisplay', "bottom", 0),],
                    aof=[('swatchLabel', "right", -gTextColumnWidthIndex)],
                    an=[('swatchLabel', "left"),
                        ('swatchDisplay', "right")],
                    ac=[('swatchDisplay', "left", 5, 'swatchLabel')]
                    )

    aiSwatchDisplayReplace(plugName)

def aiSwatchDisplayReplace(plugName) :
    nodeAndAttrs = plugName.split(".")
    node = nodeAndAttrs[0]
    
    cmds.swatchDisplayPort('swatchDisplay',
                      edit=True,
                      shadingNode=node,
                      annotation='Refresh Swatch',
                      pressCommand=lambda *args: mel.eval("updateFileNodeSwatch "+node)) 
    cmds.popupMenu('swatchPopup', edit=True, button=3)
    cmds.menuItem( 'swatchSmall', edit=True,
                   command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(64, 64), rs=64))
    cmds.menuItem( 'swatchMedium', edit=True,
                   command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(96, 96), rs=96))
    cmds.menuItem( 'swatchLarge', edit=True,
                   command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(128, 128), rs=128))
    cmds.text('swatchLabel', edit=True, label=aiSwatchLabel(node))


def aiSwatchDisplay(nodeName) :
    cmds.editorTemplate(aeCallback(aiSwatchDisplayNew), aeCallback(aiSwatchDisplayReplace), "message", callCustom=True)

