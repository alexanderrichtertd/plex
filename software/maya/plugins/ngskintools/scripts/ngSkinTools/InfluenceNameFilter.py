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

from ngSkinTools.InfluenceNameTransforms import InfluenceNameTransform
import re
class InfluenceNameFilter:
    '''
    simple helper object to match against filter strings;
    accepts filter as a string, breaks it down into lowercase tokens, and
    matches values in non-case sensitive way
    
    e.g. filter "leg arm spines" matches "leg", "left_leg", 
    "R_arm", but does not match "spine"
    
    in a  special case of empty filter, returns true for isMatch
    '''
    
    def __init__(self):
        self.matchers = None
        
    def setFilterString(self,filterString):
        
        def createPattern(expression):
            expression = "".join([char for char in expression if char.lower() in "abcdefghijklmnopqrstuvwxyz0123456789_*"])
            expression = expression.replace("*", ".*")
            return re.compile(expression,re.I)
        
        self.matchers = [createPattern(i.strip()) for i in filterString.split() if i.strip()!='']
        return self
        
    def isMatch(self,value):
        if len(self.matchers)==0:
            return True
        
        value = InfluenceNameTransform.getShortName(str(value).lower())
        for pattern in self.matchers:
            if pattern.search(value) is not None:
                return True
            
        return False

