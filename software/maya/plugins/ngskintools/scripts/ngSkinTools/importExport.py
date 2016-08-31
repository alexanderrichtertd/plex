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

'''
Example export:

.. code-block:: python

    layerData = LayerData()
    layerData.loadFrom('skinnedMesh')
    exporter = JsonExporter()
    jsonContents = exporter.process(layerData)
    # string "jsonContents" can now be saved to an external file
    

Example import:

.. code-block:: python

    # assume that jsonContents is already loaded from file
    importer = JsonImporter()
    layerData = importer.process(jsonContents)
    layerData.saveTo('skinnedMesh')

'''
from __future__ import with_statement
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.utils import Utils, MessageException
from maya import cmds
from ngSkinTools.skinClusterFn import SkinClusterFn
from ngSkinTools.meshDataExporter import MeshDataExporter

class Influence(object):
    '''
    Single influence in a layer
    
    .. py:attribute:: weights
    
        vertex weights for this influence. Set to float list, containing 
        as many values as there are vertices in a target mesh.

    .. py:attribute:: influenceName
    
        Full path of the influence in the scene. Required value when importing
        data back into skin cluster, as influences are associated by name in 
        current implementation. 
        
    .. py:attribute:: logicalIndex
    
        Logical index for this influence in a skin cluster. Not required for
        import and only provided in export as a reference.
    '''
    
    def __init__(self):
        
        # influence logical index in a skin cluster
        self.logicalIndex = -1
        
        # full path of the influence in the scene
        self.influenceName = None
        
        # influence weights for each vertex (list of double)
        self.weights = []
        
    def __repr__(self):
        return "[Infl %r]" % (self.influenceName)
        

class Layer(object):
    '''
    Represents single layer; can contain any amount of influences.
    
    .. py:attribute:: name
    
        layer name. Default value: None; set/use as any python string.
        
    .. py:attribute:: opacity
    
        layer opacity. Defaults to 0.0. Set to float value between 0.0 and 1.0
        
    .. py:attribute:: enabled
    
        layer on/off flag. Default value is False. Set to True or False.
        
    .. py:attribute:: influences
    
        list of :class:`Influence` objects.
        
    .. py:attribute:: mask
    
        layer mask: list of floats. Set to None for uninitialized mask,
        or to float list, containing as many values as there are vertices
        in a target mesh.    
        
    .. py:attribute:: dqWeights

        dual quaternion blend weights. None if not defined for this layer,
        or float list, one value per vertex in the target mesh.
        
    '''
    
    def __init__(self):
        # layer name
        self.name = None
        
        # layer opacity
        self.opacity = 0.0
        
        # layer on/off flag
        self.enabled = False
        
        # list of influences in this layer with their weights (list of Influence)
        self.influences = []
        
        # layer mask (could be None or list of double)
        self.mask = None
        
        self.dqWeights = None
        
    def addInfluence(self, influence):
        '''
        Add an influence in this layer.
        
        :param Influence influence: influence to be added 
        '''
        
        assert isinstance(influence, Influence)
        self.influences.append(influence)
        
    def __repr__(self):
        return "[Layer %r %r %r %r]" % (self.name, self.opacity, self.enabled, self.influences)
    
class MeshInfo(object):
    def __init__(self):
        # vertex positions for each vertex, listing x y z for first vertex, then second, etc.
        # total 3*(number of vertices) values
        self.verts = []
        
        # vertex IDs for each triangle, listing three vertex indexes for first triangle, then second, etc
        # total 3*(number of triangles) values
        self.triangles = []
        

class InfluenceInfo(object):
    '''
    Metadata about an influence in a skin cluster
    
    .. py:attribute:: pivot
        
        influence pivot in world-space coordinates

    .. py:attribute:: path
        
        influence node path

    .. py:attribute:: logicalIndex
        
        influence logical index in the skin cluster.
    '''
    
    def __init__(self,pivot=None,path=None,logicalIndex=None):
        self.pivot = pivot
        self.path = path
        self.logicalIndex = logicalIndex
        
    def __repr__(self):
        return "[InflInfo %r %r %r]" % (self.logicalIndex,self.path,self.pivot)
         

class LayerData(object):
    '''
    Intermediate data object between ngSkinTools core and importers/exporters,
    representing all layers info in one skin cluster.
    
    .. py:attribute:: layers
        
        a list of :py:class:`Layer` objects.
        
    .. py:attribute:: influences
        
        a list of :py:class:`InfluenceInfo` objects. Provides information about influences
        that were found on exported skin data, and used for influence matching when importing.

    '''
    
    def __init__(self):
        self.layers = []
        self.mll = MllInterface()

        self.meshInfo = MeshInfo()
        
        self.influences = []
        
        # a map [sourceInfluenceName] -> [destinationInfluenceName]
        self.mirrorInfluenceAssociationOverrides = None
        
        self.skinClusterFn = None
        
    def addMirrorInfluenceAssociationOverride(self,sourceInfluence,destinationInfluence=None,selfReference=False,bidirectional=True):
        '''
        Adds mirror influence association override, similar to UI of "Add influences association".
        Self reference creates a source<->source association, bidirectional means that destination->source 
        link is added as well
        '''
        
        if self.mirrorInfluenceAssociationOverrides is None:
            self.mirrorInfluenceAssociationOverrides = {}
        
        if selfReference:
            self.mirrorInfluenceAssociationOverrides[sourceInfluence] = sourceInfluence
            return
        
        if destinationInfluence is None:
            raise MessageException("destination influence must be specified")
        
        self.mirrorInfluenceAssociationOverrides[sourceInfluence] = destinationInfluence
        
        if bidirectional:
            self.mirrorInfluenceAssociationOverrides[destinationInfluence] = sourceInfluence 
        

    def addLayer(self, layer):
        '''
        register new layer into this data object
        
        :param Layer layer: layer object to add.
        '''
        assert isinstance(layer, Layer)
        self.layers.append(layer)
       
    @staticmethod 
    def getFullNodePath(nodeName):
        result = cmds.ls(nodeName,l=True)
        if result is None or len(result)==0:
            raise MessageException("node %s was not found" % nodeName)
        
        return result[0]
    
    def loadInfluenceInfo(self):    
        self.influences = self.mll.listInfluenceInfo()
    
    def loadFrom(self, mesh):
        '''
        loads data from actual skin cluster and prepares it for exporting.
        supply skin cluster or skinned mesh as an argument
        '''
        
        self.mll.setCurrentMesh(mesh)
        
        meshExporter = MeshDataExporter()
        self.meshInfo = MeshInfo()
        if mesh!=MllInterface.TARGET_REFERENCE_MESH:
            mesh,skinCluster = self.mll.getTargetInfo()
            meshExporter.setTransformMatrixFromNode(mesh)
            meshExporter.useSkinClusterInputMesh(skinCluster)
            self.meshInfo.verts,self.meshInfo.triangles = meshExporter.export()
        else:
            self.meshInfo.verts = self.mll.getReferenceMeshVerts()
            self.meshInfo.triangles = self.mll.getReferenceMeshTriangles()

        self.loadInfluenceInfo()
        
        for layerID, layerName in self.mll.listLayers():
            self.mirrorInfluenceAssociationOverrides = self.mll.getManualMirrorInfluences()
            if len(self.mirrorInfluenceAssociationOverrides)==0:
                self.mirrorInfluenceAssociationOverrides = None
            
            layer = Layer()
            layer.name = layerName
            self.addLayer(layer)
            
            
            layer.opacity = self.mll.getLayerOpacity(layerID)
            layer.enabled = self.mll.isLayerEnabled(layerID)
            
            layer.mask = self.mll.getLayerMask(layerID)
            layer.dqWeights = self.mll.getDualQuaternionWeights(layerID)
            
            for inflName, logicalIndex in self.mll.listLayerInfluences(layerID,activeInfluences=True):
                if inflName=='':
                    inflName = None
                influence = Influence()
                if inflName is not None:
                    influence.influenceName = self.getFullNodePath(inflName)
                influence.logicalIndex = logicalIndex
                layer.addInfluence(influence)
                
                influence.weights = self.mll.getInfluenceWeights(layerID, logicalIndex)
                
    def __validate(self):
        
        numVerts = self.mll.getVertCount()
        
        def validateVertCount(count,message):
                if count!=numVerts:
                    raise Exception(message) 
        
        for layer in self.layers:
            maskLen = len(layer.mask)
            if maskLen != 0:
                validateVertCount(maskLen, "Invalid vertex count for mask in layer '%s': expected size is %d" % (layer.name, numVerts))
            
            for influence in layer.influences:
                validateVertCount(len(influence.weights), "Invalid weights count for influence '%s' in layer '%s': expected size is %d" % (influence.influenceName, layer.name, numVerts))
                
                if self.skinClusterFn:
                    influence.logicalIndex = self.skinClusterFn.getLogicalInfluenceIndex(influence.influenceName)
                
        
    @Utils.undoable        
    def saveTo(self, mesh):
        '''
        saveTo(self,mesh)
        
        saves data to actual skin cluster
        '''
        
        # set target to whatever was provided
        self.mll.setCurrentMesh(mesh)

        if mesh==MllInterface.TARGET_REFERENCE_MESH:
            self.mll.setWeightsReferenceMesh(self.meshInfo.verts, self.meshInfo.triangles)
            
        
        if not self.mll.getLayersAvailable():
            self.mll.initLayers()
            
        if not self.mll.getLayersAvailable():
            raise Exception("could not initialize layers")
        

        # is skin cluster available?
        if mesh!=MllInterface.TARGET_REFERENCE_MESH:
            mesh, self.skinCluster = self.mll.getTargetInfo()
            self.skinClusterFn = SkinClusterFn()
            self.skinClusterFn.setSkinCluster(self.skinCluster)
        
        self.__validate()
        
        # set target to actual mesh
        self.mll.setCurrentMesh(mesh)
            
        with self.mll.batchUpdateContext():
            if self.mirrorInfluenceAssociationOverrides:
                self.mll.setManualMirrorInfluences(self.mirrorInfluenceAssociationOverrides)
            
            for layer in reversed(self.layers):
                layerId = self.mll.createLayer(name=layer.name, forceEmpty=True)
                self.mll.setCurrentLayer(layerId)
                if layerId is None:
                    raise Exception("import failed: could not create layer '%s'" % (layer.name))
                
                self.mll.setLayerOpacity(layerId, layer.opacity)
                self.mll.setLayerEnabled(layerId, layer.enabled)
                self.mll.setLayerMask(layerId, layer.mask)
                self.mll.setDualQuaternionWeights(layerId, layer.dqWeights)
                
                for influence in layer.influences:
                    self.mll.setInfluenceWeights(layerId, influence.logicalIndex, influence.weights)
        
                
    def __repr__(self):
        return "[LayerDataModel(%r)]" % self.layers
    
    def getAllInfluences(self):
        '''
        a convenience method to retrieve a list of names of all influences used in this layer data object
        '''
        
        result = set()
        
        for layer in self.layers:
            for influence in layer.influences:
                result.add(influence.influenceName)
                
        return tuple(result)
    
    
class JsonExporter:
    def __influenceToDictionary(self, influence):
        result = {}
        result['name'] = influence.influenceName
        result['index'] = influence.logicalIndex
        result['weights'] = influence.weights
        return result
    
    def __layerToDictionary(self, layer):
        '''
        :type layer: Layer
        '''
        result = {}
        result['name'] = layer.name
        result['opacity'] = layer.opacity
        result['enabled'] = layer.enabled
        result['mask'] = layer.mask
        result['dqWeights'] = layer.dqWeights
        result['influences'] = []
        for infl in layer.influences:
            result['influences'].append(self.__influenceToDictionary(infl))
            
        return result

    def __meshInfoToDictionary(self,meshInfo):
        result = {}
        result['verts'] = meshInfo.verts
        result['triangles'] = meshInfo.triangles
        return result
    
    def __modelToDictionary(self, model):
        result = {}
        result['meshInfo'] = self.__meshInfoToDictionary(model.meshInfo)
        if model.mirrorInfluenceAssociationOverrides:
            result['manualInfluenceOverrides'] = dict(model.mirrorInfluenceAssociationOverrides.items())
        result['layers'] = []
        for layer in model.layers:
            result['layers'].append(self.__layerToDictionary(layer))
            
        if model.influences:
            result['influences'] = self.__serializeInfluences(model.influences)
            
        return result
    
    def __serializeInfluences(self, influences):
        result = {}
        for i in influences:
            result[i.logicalIndex] = {'path':i.path,'index':i.logicalIndex,'pivot': i.pivot}
        return result
    
    def process(self, layerDataModel):
        '''
        transforms LayerDataModel to JSON
        
        :param LayerData layerDataModel: layers information as object;
        :return: string containing a json document
        '''
        modelDictionary = self.__modelToDictionary(layerDataModel);
        import json    
        import re
        exportOutput = json.dumps(modelDictionary,indent=2)
        # remove line break if next line is "whitespace + closing bracket or positive/negative number"
        exportOutput = re.sub(r'\n\s+(\]|\-?\d)',r"\1",exportOutput)
        return exportOutput    
    
    
class JsonImporter:
    
    def process(self, jsonDocument):
        '''
        transform JSON document () into layerDataModel
        
        :param str jsonDocument: layers info, previously serialized as json string
        :rtype: LayerData
        '''
        import json
        self.document = json.loads(jsonDocument)
        
        model = LayerData()
        
        meshInfo = self.document.get('meshInfo')
        if meshInfo:
            model.meshInfo.verts = meshInfo['verts']
            model.meshInfo.triangles = meshInfo['triangles']
        
        model.mirrorInfluenceAssociationOverrides = self.document.get("manualInfluenceOverrides")
        
        influences = self.document.get('influences')
        if influences:
            model.influences = []
            for i in influences.values():
                model.influences.append(InfluenceInfo(pivot=i['pivot'], path=i['path'], logicalIndex=i['index'])) 
        
        for layerData in self.document["layers"]:
            layer = Layer()
            model.addLayer(layer)        
            layer.enabled = layerData['enabled']
            layer.mask = layerData.get('mask')
            layer.dqWeights = layerData.get('dqWeights')
            layer.name = layerData['name']
            layer.opacity = layerData['opacity']
            layer.influences = []

            for influenceData in layerData['influences']:
                influence = Influence()
                layer.addInfluence(influence)
                influence.weights = influenceData['weights']
                influence.logicalIndex = influenceData['index']
                influence.influenceName = influenceData['name']

        return model
    
class Format:
    def __init__(self):
        self.title = ""
        self.exporterClass = None
        self.importerClass = None
        
        # recommended file extensions for UI, e.g. file dialog
        self.recommendedExtensions = ()    
        
    def export(self,mesh):
        '''
        returns file contents that was produced with 
        '''
        model = LayerData()
        model.loadFrom(mesh)
        return self.exporterClass().process(model)
    
    def import_(self,fileContents,mesh):
        '''
        parses fileContents with importerClass and loads data onto given mesh
        '''
        model = self.importerClass().process(fileContents)
        model.saveTo(mesh)
    
class Formats:
    
    @staticmethod
    def getJsonFormat():
        f = Format()
        f.title = "JSON"
        f.exporterClass = JsonExporter
        f.importerClass = JsonImporter
        f.recommendedExtensions = ("json", "txt")
        return f
    
        
    
        
        

