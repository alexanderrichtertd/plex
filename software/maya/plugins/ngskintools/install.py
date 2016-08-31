#!/usr/bin/env python
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
Simplified maya plugin module installer.

* Installs module into maya module path
* Installs shelves

'''

import sys
import os
import logging
import shutil
import glob

INSTALL_PLUGIN_NAME = "ngSkinTools"
INSTALL_PLUGIN_VERSION = "1.0.960"
INSTALL_MAYA_VERSION = '2015'
INSTALL_MAYA_PLATFORM = 64

class Installer:
    REQUIRED_PYTHON_HEX = 0x02050000
    REQUIRED_PYTHON_STR = "2.5"
    
    
    def getUserMayaFolder(self):
        '''
        returns maya settings folder in user's home dir
        '''
        homedir = os.getenv('USERPROFILE') or os.getenv('HOME')
        platformnames = {64:'x64',32:'win32'}
        if int(INSTALL_MAYA_VERSION)<2016:
            mayaFolder = "%s-%s" % (INSTALL_MAYA_VERSION,platformnames[INSTALL_MAYA_PLATFORM])
        else:
            mayaFolder = INSTALL_MAYA_VERSION
        return os.path.join(homedir,"maya",mayaFolder)
    
    def getMayaName(self):
        return "Maya %s %dbit" % (INSTALL_MAYA_VERSION,INSTALL_MAYA_PLATFORM)
    
    def checkversion(self):
        '''
        checks if required minimal python version requirements are met
        '''
        if sys.hexversion < Installer.REQUIRED_PYTHON_HEX:
            self.log.error("invalid python version: at least %s is required\n" % Installer.REQUIRED_PYTHON_STR)
            sys.exit(1)
    

    def __init__(self,debug=False):
        self.debug = False

        self.log = logging.getLogger("Installer")
        self.configureLogger()

        self.moduleBasePath =  None
        self.mayaPrefPath = None
        self.shelvesDestDir = None
        self.mayaModulesDir = None
        self.shelvesSourceMask = None
        
        
    def parseArgs(self):
        '''
        parse command line arguments
        '''
        self.log.info("Parsing command line arguments...")
        import getopt
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "d", ["debug"])
            
            for i in opts:
                if ("--debug" in i):
                    self.debug = True
            
            
            if (self.debug):
                self.log.info("**DEBUG MODE ACTIVATED**")
            
                
        except getopt.GetoptError, err:
            self.log.error(str(err))
            sys.exit(2)
        
        
    def configureLogger(self):
        '''
        configure stdout logger
        '''
        self.log.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',"%H:%M:%S")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self.log.addHandler(ch)


    def resolvePaths(self):
        self.moduleBasePath =  os.path.dirname(os.path.abspath(__file__))
        self.log.info("detected module base path: %s" % self.moduleBasePath)
        self.mayaPrefPath = self.getUserMayaFolder()
        self.log.info("detected maya settings path: %s" % self.mayaPrefPath)
        
        if not os.path.exists(self.mayaPrefPath):
            raise Exception("maya settings path '%s' does not exist; please check if you have correct maya version (%s) installed." %
                           (self.mayaPrefPath,self.getMayaName()))
            
            
    def createModuleFile(self):
        self.log.info("Installing module...")

        self.mayaModulesDir = os.path.join(self.mayaPrefPath,'modules')
        if not os.path.exists(self.mayaModulesDir):
            self.log.info("modules folder '%s' not found, creating..." % self.mayaModulesDir)
            os.mkdir(self.mayaModulesDir)
            
        self.moduleDescriptionFileName = os.path.join(self.mayaModulesDir,'%s-module.txt' % INSTALL_PLUGIN_NAME)
            
        # delete as a separate step, just to check permissions
        if (os.path.exists(self.moduleDescriptionFileName)):
            self.log.info("deleting old module description file '%s'" % self.moduleDescriptionFileName)
            os.remove(self.moduleDescriptionFileName)
            
            
        self.log.info("creating new module description file at '%s'" % self.moduleDescriptionFileName)
        f = open(self.moduleDescriptionFileName,'w')
        try:
            f.write("+ %s %s " % (INSTALL_PLUGIN_NAME,INSTALL_PLUGIN_VERSION))
            f.write(self.moduleBasePath)
            f.write(os.linesep)
        finally:
            f.close()
            
    def installShelf(self):
        self.log.info("Installing maya shelf buttons...")
        
        self.shelvesDestDir =os.path.join(self.mayaPrefPath,'prefs','shelves')
        if not os.path.exists(self.shelvesDestDir):
            self.log.info("maya shelves preference path '%s' does not exist, creating... " % self.shelvesDestDir)
            os.makedirs(self.shelvesDestDir)

        self.shelvesSourceMask = os.path.join(self.moduleBasePath,'shelves','*.mel') \
                            if not self.debug else \
                            os.path.join(os.path.dirname(__file__),'..','mel','*.mel')
                            
        for file in glob.glob(self.shelvesSourceMask):
            shutil.copy(file, self.shelvesDestDir)
            
        
    def run(self):
        '''
        main installer method
        '''
        try:
            self.log.info("Running %s %s installer for %s ..." % (INSTALL_PLUGIN_NAME,INSTALL_PLUGIN_VERSION, self.getMayaName()))
            self.parseArgs()

            self.checkversion()
            
            self.resolvePaths()
            
            self.createModuleFile()
            
            self.installShelf()
            
            if self.debug:    
                self.uninstall()

            self.log.info("Done.")
        except Exception,e:
            self.log.error("There was an unexpected error: %s",e.message)
        raw_input("Press any key to exit.")
            
            
    def uninstall(self):
        '''
        mainly just a  debug method to cleanup everything
        '''
        self.log.info("uninstalling...")
        
        if not self.debug:
            return;
        
        if self.debug:
            if self.mayaModulesDir is not None:
                shutil.rmtree(self.mayaModulesDir)
        
        # delete every shell mentioned in source shell folder
        if self.moduleBasePath is not None:
            for file in glob.glob(self.shelvesSourceMask):
                os.remove(os.path.join(self.shelvesDestDir,os.path.basename(file)))
            


if __name__ == '__main__':
    Installer().run()