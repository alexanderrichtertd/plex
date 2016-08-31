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

import logging
import sys

class DummyLogger(object):
    def __getattr__(self,name):
        return self.doNothing
    
    def doNothing(self,*args,**kwargs):
        pass
    
    def isEnabledFor(self,*args):
        return False
    
class DummyLoggerFactory:
    def getLogger(self,name):
        return DummyLogger()
    

            

class SimpleLoggerFactory:
    ROOT_LOGGER_NAME="ngSkinTools"
    
    def __init__(self,level=logging.DEBUG):
        self.level = level
        self.log = self.configureRootLogger()
        
    def configureRootLogger(self):
        logger = logging.getLogger(self.ROOT_LOGGER_NAME)        
        logger.setLevel(self.level)
        #logger.handlers = []
        
        formatter = logging.Formatter("[%(name)s %(levelname)s %(asctime)s] %(message)s")
        formatter.datefmt = '%H:%M:%S'
        
        for i in logger.handlers[:]:
            logger.removeHandler(i)

        ch = logging.StreamHandler(sys.__stdout__)
        ch.setLevel(self.level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False
        
        
        return logger
        
    
    def getLogger(self,name):
        return self.log
    
        self.log.debug("creating logger '%s'" % name)
            
        result = logging.getLogger(self.ROOT_LOGGER_NAME+"."+name)
        result.setLevel(self.level)
        
        result.info("alive check")
        return result
    
LoggerFactory = DummyLoggerFactory()     
       
    
