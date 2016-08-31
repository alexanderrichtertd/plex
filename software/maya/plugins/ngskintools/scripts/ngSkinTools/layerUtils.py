#
#    ngSkinTools
#    Copyright (c) 2009-2015 Viktoras Makauskas. 
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by
#    Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License:
#        http://creativecommons.org/licenses/by-nc-nd/3.0/
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode.txt
#         
#    A copy of the license can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

from maya import cmds
from ngSkinTools.log import LoggerFactory


log = LoggerFactory.getLogger("LayerUtils")

class NamedPaintTarget:
    MASK = "mask"
    DUAL_QUATERNION = "dq"

class LayerUtils:
     
    @staticmethod
    def iterCustomNodes():
        for nodeType in ['ngSkinLayerData','ngSkinLayerDisplay']:
            items = cmds.ls(type=nodeType)
            if items is not None:
                for i in items:
                    yield i
    
    @staticmethod
    def deleteCustomNodes():
        log.info("removing ngSkinTools nodes from current scene")
                
        nodes = list(LayerUtils.iterCustomNodes())
        if len(nodes)>0:
            cmds.delete(nodes)
        
    @staticmethod
    def hasCustomNodes():
        for _ in LayerUtils.iterCustomNodes():
            return True
        
        return False
        

