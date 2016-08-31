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

from xml.dom.minidom import Node
from xml.parsers.expat import ExpatError
from ngSkinTools.xmldigester import RequiredNodeNotFoundException, NodeRule,\
    XmlRule, Required, TextNodeRule, NodeAttributeRule, ContainerNodeRule
from traceback import print_exc
from ngSkinTools.log import LoggerFactory

log = LoggerFactory.getLogger("version checker")

class CheckerTransport:
    '''
    the way version checker sends requests and retrieves
    response for that is separated from version checker,
    so that it's easy to switch.
    '''
    def getResponseFor(self,request):
        '''
        sends XML in one or the other way and returns response 
        '''
        
class ListenerTransport(CheckerTransport):
    def __init__(self,transport):
        self.transport = transport
        
    def getResponseFor(self, request):
        response = self.transport.getResponseFor(request)
        return response
        
        
class HttpPostTransport(CheckerTransport):
    
    def __init__(self):
        self.host=''
        self.path=''
    
    def getResponseFor(self, request):
        import httplib, urllib
        from socket import gaierror 
        try:
            headers = {"Content-type": "text/xml",
                        "Accept": "text/plain"}
            conn = httplib.HTTPConnection(self.host)
            conn.request("POST", self.path, request, headers)
            response = conn.getresponse()
            return response.read()
        except Exception,err:
            log.debug(err)
            raise VersionCheckException("could not read response from server")
            

class VersionCheckerLink:
    def __init__(self):
        self.title = None
        self.url = None    
    
class VersionCheckException(Exception):
    '''
    a generic exception that happened while performing a version check
    '''
    
    
    
class VersionChecker:
    '''
    Implements communication with a remote service in order to find out
    if current installation is up to date
    '''
    
    def __init__(self):
        self.currentId=None
        self.uniqueClientId=None
        
        self.transport = None
        
        self.links = []
        
        self.updateAvailable = None
        self.updateTitle = None
        self.updateDate = None
        
        
    def createRequest(self):
        '''
        creates request XML
        '''
        
        return """<?xml version="1.0" encoding="UTF-8" ?>
                    <version-check>
                        <current-install>
                            <uuid>%s</uuid>
                            <unique-client-id>%s</unique-client-id>
                        </current-install>
                    </version-check>        
        """ % (self.currentId,self.uniqueClientId)
    
    def execute(self):
        try:
            log.info("version check started")
            response = self.transport.getResponseFor(self.createRequest())
            log.info("response: "+response)
            self.parseResponse(response)
            log.info("response parse was successfull")
            
        except VersionCheckException,err:
            raise;
            
        except ExpatError,err:
            raise VersionCheckException, "Version check failed: invalid response from server."
            
        except Exception, err:
            import traceback;traceback.print_exc()
            raise VersionCheckException("Version check failed: "+repr(err))
        
    def isUpdateAvailable(self):
        return self.updateAvailable
        
    def parseResponse(self,response):
        from xml.dom import minidom
        xml = minidom.parseString(response)
        
        
        def validateNotEmpty(value,message):
            if len(value)==0:
                raise VersionCheckException(message)
        
        def addLink(node):
            self.currentLink = VersionCheckerLink()
            self.links.append(self.currentLink)
            
        def setLinkUrl(value):
            self.currentLink.url=value.strip()
            validateNotEmpty(self.currentLink.url, "empty link url")
            
        def setLinkTitle(value):
            self.currentLink.title=value.strip()
            validateNotEmpty(self.currentLink.title, "empty link title")
            
            
        class Optional:
            def __init__(self,ruleList):
                self.ruleList=ruleList
        
            
        def setUpdateTitle(value):
            self.updateTitle=value
            validateNotEmpty(self.updateTitle, "update title is empty")
        
        def setReleaseDate(value):
            self.updateDate=value
            validateNotEmpty(self.updateDate, "release date was empty")
            
        def setErrorMessage(value):
            validateNotEmpty(value, "error value was empty")
            raise VersionCheckException(value)
        
        def setUpdateAvailabe(value):
            validateNotEmpty(value.strip(), "update value was empty")
            self.updateAvailable=value=='yes'

        
        class RootElementChoice(ContainerNodeRule):
            def __repr__(self):
                return "(version-check,error)"
        
        rootRule = ContainerNodeRule()
        choice = RootElementChoice()
        rootRule.addSelfRule(Required(choice))
        versionInfo = NodeRule('version-information')
        choice.addSelfRule(versionInfo)
        versionInfo.addSelfRule(Required(NodeAttributeRule('updateAvailable',setUpdateAvailabe)))
        
        cv = NodeRule('current-version')
        versionInfo.addRule(Required(cv))
        cv.addRule(Required(TextNodeRule('release-date',setReleaseDate)))
        cv.addRule(Required(TextNodeRule('title',setUpdateTitle)))

        links =NodeRule('links')
        versionInfo.addRule(links)
        link=NodeRule('link',addLink)
        links.addRule(Required(link))
        link.addSelfRule(Required(NodeAttributeRule('url',setLinkUrl)))
        links.addRule(Required(TextNodeRule('link',setLinkTitle)))
        
        
        errorRule = choice.addSelfRule(NodeRule('error'))
        errorRule.addRule(Required(TextNodeRule('message',setErrorMessage)))
        
        
        try:
            rootRule.visit(xml.documentElement)
        except RequiredNodeNotFoundException,err:
            raise VersionCheckException('Invalid response from server,required elements not found: %r'%err.rule)
        
    def getLinks(self):
        return self.links
    
    
