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

from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.utils import MessageException, Utils
from ngSkinTools.log import LoggerFactory
from maya import OpenMayaAnim as oma
from maya import OpenMaya as om
from maya import cmds
from ngSkinTools.skinClusterFn import SkinClusterFn

log = LoggerFactory.getLogger("ImportInfluences")

class ImportInfluences(object):

    def __init__(self):
        self.sourceSkinCluster = None
        self.destinationSkinCluster = None
        
        
    def __detectSkinCluster(self,mesh):
        mll = MllInterface()
        mll.setCurrentMesh(mesh)
        try:
            _,skinCluster = mll.getTargetInfo()
        except TypeError:
            raise MessageException("cannot find skin cluster attached to %s" % mesh)
        
        log.info("detected skin cluster %s on mesh %s" % (skinCluster, mesh))
        return skinCluster
        
        
    def setSourceFromMesh(self,sourceMesh):
        '''
        detect source skin cluster from given mesh
        '''
        self.sourceSkinCluster = self.__detectSkinCluster(sourceMesh)
        
    def setDestinationFromMesh(self,destinationMesh):
        '''
        detect destination skin cluster from given mesh
        '''
        self.destinationSkinCluster = self.__detectSkinCluster(destinationMesh)
        
    def initFromSelection(self):
        items = cmds.ls(sl=True)
        if items==None or len(items)!=2:
            raise MessageException("select two skinned meshes to perform this operation")
        
        self.setSourceFromMesh(items[0])
        self.setDestinationFromMesh(items[1])
        
        
    def listInfluences(self,skinCluster):
        '''
        lists full dag paths of all influences in given skin cluster 
        '''
        return SkinClusterFn().setSkinCluster(skinCluster).listInfluences()
    
    
    def addInfluence(self,influenceName):
        '''
        adds influence to destination skin cluster
        '''
        cmds.skinCluster(self.destinationSkinCluster, edit=True,ai=influenceName,lw=True,wt=0.0)
        cmds.setAttr(influenceName+".liw",0)
    
    
    def listInfluencesDiff(self):
        '''
        returns a list of influences that are in source skin cluster, but not in destination skin cluster
        '''
        sourceInfluences = self.listInfluences(self.sourceSkinCluster)
        destinationInfluences = self.listInfluences(self.destinationSkinCluster)
        
        for i in destinationInfluences:
            try:
                sourceInfluences.remove(i)
            except ValueError:
                pass
            
            
        return sourceInfluences