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

from maya import OpenMayaAnim as oma
from maya import OpenMaya as om
from ngSkinTools.utils import Utils, MessageException

class SkinClusterFn(object):
    
    def __init__(self):
        self.fn = None
        self.skinCluster = None
        
    def setSkinCluster(self,skinClusterName):
        self.skinCluster = skinClusterName
        self.fn = oma.MFnSkinCluster(Utils.getMObjectForNode(skinClusterName))
        return self
        
    def getLogicalInfluenceIndex(self,influenceName):
        try:
            path = Utils.getDagPathForNode(influenceName)
        except:
            raise MessageException("Could not find influence '%s' in %s" % (influenceName, self.skinCluster))
            
        return self.fn.indexForInfluenceObject(path)
        
        
    def listInfluences(self):
        dagPaths = om.MDagPathArray()
        
        self.fn.influenceObjects(dagPaths)
        result = []
        for i in range(dagPaths.length()):
            result.append(dagPaths[i].fullPathName())
        
        return result
    

    