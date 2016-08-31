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



from ngSkinTools.utils import Utils
from os import path
import webbrowser

class DocLink:
    def __init__(self):
        self.title = None
        self.path = None
        self.anchor = None
        self.baseUrl = None
        
    def open(self):
        url = self.baseUrl+self.path
        if self.anchor:
            url+="#"+self.anchor
        
        webbrowser.open_new(url)
        
        
class Documentation:
    def __init__(self):
        self.base = None
        
    def makeLink(self,title,path,anchor=None):
        result = DocLink()
        result.title = title
        result.path = path
        result.anchor = anchor
        result.baseUrl = self.base
        return result
    
    def openLink(self,link):
        link.open()
    
        
SkinToolsDocs = Documentation()
SkinToolsDocs.base = "http://www.ngskintools.com/documentation/userguide/"   


# new documentation links
SkinToolsDocs.UI_TAB_PAINT = SkinToolsDocs.makeLink('Paint tab','ui','paint-tab')
SkinToolsDocs.UI_TAB_MIRROR = SkinToolsDocs.makeLink('Mirror tab','ui','mirror-tab')
SkinToolsDocs.UI_TAB_RELAX = SkinToolsDocs.makeLink('Relax tab','ui','relax-tab')

# prev links - for source compatibility, to be fixed:
SkinToolsDocs.WEIGHTSRELAX_INTERFACE = SkinToolsDocs.makeLink('skin weights relax','ui')
SkinToolsDocs.ASSIGNWEIGHTS_CLOSESTJOINT_INTERFACE = SkinToolsDocs.makeLink('assign weights by closest joint','ui','closest-joint')
SkinToolsDocs.ASSIGNWEIGHTS_MAKERIGID_INTERFACE = SkinToolsDocs.makeLink('unify weights','ui','unify-weights')
SkinToolsDocs.ASSIGNWEIGHTS_LIMITWEIGHTS_INTERFACE = SkinToolsDocs.makeLink('assign weights: limit weights','ui','limit-weights')


SkinToolsDocs.MIRRORWEIGHTS_INTERFACE = SkinToolsDocs.makeLink('mirror weights','mirroring')

SkinToolsDocs.INITWEIGHTTRANSFER_INTERFACE = SkinToolsDocs.makeLink('Init Weight Transfer','ui','init-weights-mirror')

SkinToolsDocs.CURRENTSKINSETTINGS_INTERFACE = SkinToolsDocs.makeLink('Current skin settings','ui','settings')

SkinToolsDocs.DOCUMENTATION_ROOT = SkinToolsDocs.makeLink("Current documentation",'')

