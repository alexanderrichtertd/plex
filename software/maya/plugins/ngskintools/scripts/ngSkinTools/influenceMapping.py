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
Influence mapping process creates a "source->destination" list for two influence lists,
describing how based on influence metadata (name, position) and mapping requirements
(mirror mode, left/right side name prefixes, etc) a mapping is created, 
where "source->destination" in, say, weight transfer/mirror situation, describes that weights
currently associated with source influence, should be transfered  to destination influence.

for mirror mode, same influence can map to itself, which would generally mean "copy influence weights
on one side to be the same on the other side".

mapping is returned as "logical index"->"logical index" map.

For usage details, see unit test examples.
'''

import re
from itertools import izip
import math
from maya import OpenMaya as om

class NameMatchingRule:
    def __init__(self):
        self.prefixRegexp = None
        self.mirrorMode = False
        self.prefixes = None
        self.ignoreNamespaces = True
    
    def reversePath(self,path):
        result = path.split("|")
        result.reverse()
        if self.ignoreNamespaces:
            result = [i.split(":")[-1] for i in result]
        return result
    
    def startMatching(self,source):
        self.source = source
        self.sourcePath = source.path
        self.sourceNameParts = self.reversePath(source.path)
        self.match = None
        self.bestMatchScore = [0]*len(self.sourceNameParts)
        
    def regexpMatchAny(self,fragments):
        return '('+'|'.join(fragments)+')'
    
    def setPrefixes(self,*prefixes):
        self.prefixes = prefixes
        self.prefixRegexp = re.compile(self.regexpMatchAny(prefixes)+'(.*)')
        self.matchGroup = 2
        
    def setSuffixes(self,*suffixes):
        self.suffixes = suffixes
        self.prefixRegexp = re.compile('(.*)'+self.regexpMatchAny(suffixes))
        self.matchGroup = 1
        
    def isMirrorName(self,source,destination):
        if self.prefixRegexp is None:
            return False
        
        def dropPrefix(shortName):
            match = self.prefixRegexp.match(shortName)
            if match:
                return match.group(self.matchGroup)
            
            # no side prefix found, return None as standin
            return None
        
        # if short names mismatch, both have prefixes and common part (without prefixes) match,
        # they're probably mirrors of themselves
        return source!=destination and dropPrefix(source)==dropPrefix(destination)!=None        
        
        
    def testCandidate(self,destination):
        def isChildOf(a,b):
            return b.startswith(a+"|")
        
        if isChildOf(self.sourcePath, destination.path) or isChildOf(destination.path, self.sourcePath):
            # parent-child relationship between the two
            return
        
        candidatePath = self.reversePath(destination.path)
        
        for source,dest,(scoreIndex,scoreValue) in izip(self.sourceNameParts,candidatePath,enumerate(self.bestMatchScore[:])):
            # calculate match score for each name portion;
            # only move further
            currentScore = 0
            if source==dest:
                currentScore += 1
                
            if self.mirrorMode and self.isMirrorName(source, dest):
                currentScore += 2
            
            # if current candidate matched already,just contiue filling in it's score
            if self.match == destination:
                self.bestMatchScore[scoreIndex] = currentScore
                continue    
            
            if currentScore==0:
                # curent step not matched?
                return
            
            if scoreValue<currentScore:
                # a better score was found
                self.bestMatchScore[scoreIndex] = currentScore
                self.match = destination
                
            if scoreValue>currentScore:
                return
                
                
class DistanceMatchRule:
    def __init__(self):
        self.mirrorMode = False
        self.mirrorAxis = 0
        self.maxThreshold = 0.01

    
    def startMatching(self,source):
        if source.pivot is None:
            raise Exception("source influence should have a pivot")

        self.source = source
        
        self.matchPosition = list(source.pivot)
        if self.mirrorMode:
            self.matchPosition[self.mirrorAxis] = -self.matchPosition[self.mirrorAxis]  
        self.match = None
        self.bestMatchDistance = None

    def vectorLength(self,vector):
        return math.sqrt(sum(i*i for i in vector))
    
    def vectorDiff(self,vFrom,vTo):
        return (vTo[0]-vFrom[0],vTo[1]-vFrom[1],vTo[2]-vFrom[2])

    def testCandidate(self,destination):
        if destination.pivot is None:
            raise Exception("candidate destination influence should have a pivot")
        
        # mirror mode and not on the opposite side? discard candidate; does not apply to self
        if self.mirrorMode and (self.matchPosition[self.mirrorAxis]>0)!=(destination.pivot[self.mirrorAxis]>0):
            if destination.path!=self.source.path:
               return
            
        distance = self.vectorLength(self.vectorDiff(self.matchPosition, destination.pivot))
        
        # will be more readable than a long "if" statement
        def isBetterMatch():
            if abs(distance)>self.maxThreshold:
                return False
            
            if self.bestMatchDistance is None:
                return True
            
            distanceDiff = self.bestMatchDistance-distance
            
            
            if abs(distanceDiff)<0.01:
                # under close call situations, matching paths win
                if self.source.path==self.match.path:
                    return False
                if self.source.path==destination.path:
                    return True
                
            
            return distanceDiff>0
        
        if isBetterMatch():
            self.match = destination
            self.bestMatchDistance = distance

class InfluenceMapping:
    '''
    Calculates influence-to-influence mapping for weights mirroring
    and transfer
    '''
    
    def __init__(self):
        self.sourceInfluences = []
        self.destinationInfluences = None
        self.manualOverrides = {}
        self.mirrorMode = True

        self.nameMatchRule = NameMatchingRule()
        self.distanceMatchRule = DistanceMatchRule()
        
        self.rules = [self.nameMatchRule,self.distanceMatchRule]
        
    def convertManualOverridesToIndexes(self):
        def convert(influence,influenceList):
            if not isinstance(influence,basestring):
                return influence
            
            selection = om.MSelectionList();
            selection.add(influence)
            path = om.MDagPath()
            selection.getDagPath(0,path)
            influence = path.fullPathName()
            
            for i in influenceList:
                if i.path==influence:
                    return i.logicalIndex
            raise Exception("Failed to convert influence path to logical index: "+influence)
         
        conversion = {}
        for source,destination in self.manualOverrides.items():
            conversion[convert(source,self.sourceInfluences)] = convert(destination,self.destinationInfluences)      

        self.manualOverrides = conversion
        
    def validateManualOverrides(self):
        '''
        only keep those manual overrides that have valid indexes 
        in source and destination lists
        '''
        sourceIndexes = [i.logicalIndex for i in self.sourceInfluences]
        destIndexes = [i.logicalIndex for i in self.destinationInfluences]
        
        self.manualOverrides = dict([
            item for item 
            in self.manualOverrides.items()
            if item[0] in sourceIndexes and ((item[1] in destIndexes) or (item[1] is None))
        ])
        
        
    def calculate(self):
        
        for rule in self.rules:
            rule.mirrorMode = self.mirrorMode

        if self.destinationInfluences is None:
            self.destinationInfluences = self.sourceInfluences
        
        self.convertManualOverridesToIndexes()
        self.validateManualOverrides()

        self.mapping = dict(self.manualOverrides)
            
        for i in self.sourceInfluences:
            if i.logicalIndex in self.manualOverrides:
                # should already be mapped
                continue
            
            matchedSelf = False
            for rule in self.rules:
                rule.startMatching(i)
                
                for j in self.destinationInfluences:
                    rule.testCandidate(j)
                
                # if matched self, just try another rule
                if rule.match==i:
                    matchedSelf = True
                    continue
                
                
                if rule.match is not None:
                    matchedSelf = False
                    self.mapping[i.logicalIndex] = rule.match.logicalIndex
                    break
                
            # no better match than self was found; just use it.
            if matchedSelf:
                self.mapping[i.logicalIndex] = i.logicalIndex