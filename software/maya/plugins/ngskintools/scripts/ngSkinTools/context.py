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

from ngSkinTools.versioncheck import VersionChecker, HttpPostTransport
from ngSkinTools.version import Version
from ngSkinTools.utils import Utils



class ApplicationSetup:
    def __init__(self):
        self.updateCheckHost = 'ngskintools.com'
        self.updateCheckPath = '/ngskintools-version-check-1'
        
        
class ApplicationContext:
    def __init__(self):
        self.setup = ApplicationSetup()
    
    def createVersionChecker(self):
        checker = VersionChecker()
        checker.currentId = Version.buildWatermark()
        checker.uniqueClientId = Version.uniqueClientId() 
        
        checker.transport = HttpPostTransport()
        checker.transport.host = self.setup.updateCheckHost
        checker.transport.path = self.setup.updateCheckPath
        
        return checker



applicationContext = ApplicationContext()