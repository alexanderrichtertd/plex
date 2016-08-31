"""
    cleanUpComp.py

    version: 0.0v3
    update:    20140516
    by:      Carl Schroter
    
    2Do:
        switch between node selection and all nodes
        delete unconnectes writes
        progressbar!!!
"""

import nuke

def cleanUpComp(nodes='all'):
 
    def cleanUpPanel():
        p = nuke.Panel("CleanUpComp by Carl Schroter")    
            
        p.addBooleanCheckBox("exclude read nodes", True)
        p.addBooleanCheckBox("exclude backdrops", True)
        p.addBooleanCheckBox("exclude viewer nodes", True)
        p.addBooleanCheckBox("include disabled nodes", True)
        
        
        p.addButton("Cancel")
        p.addButton("OK")
        
        retVar = p.show()

        return (retVar, p.value('exclude read nodes'), p.value('exclude backdrops'), p.value('exclude viewer nodes'), p.value('include disabled nodes'))
 
    def doCleanUp(excludeNodeClasses, includeDisabled):

        for i in nuke.allNodes():
            
            #delete disabled nodes
            if includeDisabled:
                if i.knobs().has_key('disable'):
                    if i['disable'].value() == True:
                        nuke.delete(i)
                        continue
                
            #no downstream connection
            if i.dependent() == [] and i.Class() not in excludeNodeClasses:

                #no upstream connection
                if i.dependencies() == []:
                    print "deleting unconnected node", i.name()
                else:
                    print "deleting dead end", i.name()
                
                #nodelist.remove(i)
                nuke.delete(i)

        for i in nuke.allNodes():            
            if i.dependent() == [] and i.Class() not in excludeNodeClasses:
                return 0 #still dead ends in script
        return 1 #no dead ends
    
    nuke.Undo.name("clean up script")
    nuke.Undo.begin()

    print "\nCLEAN UP COMP"
    print "-------------"
    
    initialNodeCount = nuke.allNodes().__len__()
    nodelist = []
    if nodes == 'all':
        nodelist = nuke.allNodes()
        print "iterating over all nodes"
    elif nodes == 'selected':        
        nodelist = nuke.selectedNodes()
        print "iterating over selected nodes"
        
    print "-------------"
                
    stop = False
    ret = cleanUpPanel()
    
    #print ret
    
    excludeNodeClasses = ['Write']
    if ret[1] == True:
        excludeNodeClasses.append('Read')
    if ret[2] == True:
        excludeNodeClasses.append('BackdropNode')
    if ret[3] == True:
        excludeNodeClasses.append('Viewer')
    
    #print excludeNodeClasses
    
    if ret[0] != 1:
        print "cleanUpComp canceled"
        return
        
    while not stop:  
        print "crawling again"
        if doCleanUp(excludeNodeClasses, ret[4]) == 1:
            stop = True
                  
    print "-------------"    
    print "clean up done!"
    print "reduced nodecount from {} to {}".format(initialNodeCount, nuke.allNodes().__len__())
    nuke.Undo.end()


