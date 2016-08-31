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

class XmlRule:
    def parentEntering(self):
        pass
    def parentExiting(self):
        pass
    def visit(self,node):
        pass
    def isMatch(self,node):
        return True;
    
class ContainerNodeRule(XmlRule):
    def __init__(self):
        self.selfRules = [] # rules that apply to current node
        self.childRules = [] # rules that apply to child rules
        
    def isMatch(self,node):
        for r in self.selfRules:
            if r.isMatch(node):
                return True
        return False
        
    def addSelfRule(self,rule):
        self.selfRules.append(rule)
        return rule
        
    def addRule(self,rule):
        self.childRules.append(rule)
        return rule
      
    def visitNode(self,rule,node):
        if rule.isMatch(node):
            rule.visit(node)

    def visit(self,node):
        allRules = self.childRules+self.selfRules 
        
        for i in allRules:
            i.parentEntering()

        for i in self.selfRules:
            self.visitNode(i, node)
        
                
        for n in node.childNodes:
            for i in self.childRules:
                self.visitNode(i, n)

        for i in allRules:
            i.parentExiting()
            
class Required(XmlRule):
    def __init__(self,rule):
        self.rule=rule

    def isMatch(self,node):
        return self.rule.isMatch(node);
        
    def visit(self,node):
        self.found=True
        self.rule.visit(node)
    
    def parentEntering(self):
        self.found=False
        self.rule.parentEntering()
    
    def parentExiting(self):
        self.rule.parentExiting()
        if not self.found:
            raise RequiredNodeNotFoundException('Rule was not found',self.rule)
            
    def __repr__(self):
        return "%s[%r]" % (self.__class__.__name__,self.rule)

class NodeRule(ContainerNodeRule):
    def __init__(self,nodeName,action=None):
        ContainerNodeRule.__init__(self)
        self.action=action
        self.nodeName=nodeName
        
    def isMatch(self,node):
        return self.nodeName==node.nodeName

    def doAction(self,node):
        self.action(node)

    def visit(self,node):
        if self.action is not None:
            self.doAction(node)
        
        ContainerNodeRule.visit(self, node)

    def __repr__(self):
        return "%s[%s]" % (self.__class__.__name__,self.nodeName)
    
class NodeAttributeRule(XmlRule):
    def __init__(self,attributeName,action=None):
        self.attributeName=attributeName
        self.action=action
        
    def isMatch(self,node):
        return node.hasAttribute(self.attributeName)
    
    def visit(self,node):
        if self.action is not None:
            self.action(node.attributes[self.attributeName].value);
    def __repr__(self):
        return "%s[%s]" % (self.__class__.__name__,self.attributeName)
    
class TextNodeRule(NodeRule):
    def isMatch(self,node):
        return NodeRule.isMatch(self, node) and node.firstChild is not None and node.firstChild.nodeType==Node.TEXT_NODE

    def visit(self,node):
        if self.action is not None:
            self.action(node.firstChild.data);

            
           
class RequiredNodeNotFoundException(Exception):
    def __init__(self,message,rule):
        Exception.__init__(self,message)
        self.rule = rule
            
  
    

class Digester:
    @staticmethod
    def walkXml(node,ruleList):
        for rule in ruleList:
            if not rule.isMatch(node):
                continue
            
            rule.beforeNode(node)

            for r in rule.getChildRules():
                r.parentEntering()


            for n in node.childNodes:
                Digester.walkXml(n,rule.getChildRules())
                    
            for r in rule.getChildRules():
                r.parentExiting()
                
            rule.afterNode(node)
        
        