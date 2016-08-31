import hiero.core
import hiero.ui
from PySide import QtGui
print

class GrowClipDuration(QtGui.QAction):
    def __init__(self):
        QtGui.QAction.__init__(self, 'Grow Duration', None)
        self.triggered.connect(self.doIt)

    def doIt(self):
        print
        print 'Grow Duration'

        verbose = True

        stepSize = hiero.ui.currentViewer().frameIncrement()
        
        view = hiero.ui.activeView()
        print view

        if isinstance(view, hiero.ui.TimelineEditor):
            if view.selection() is not None and len( view.selection() ) != 0:
                
                #view.selection()[0].project().beginUndo('Grow Duration') ####################################### UNDO PROBLEM

                print 'initial selection: ', view.selection()

                for i in view.selection():                    
                    
                    if verbose:
                        print i.name()
                        print 'timeline   ', i.timelineIn(), i.timelineOut()
                        print 'source     ', i.sourceIn(), i.sourceOut()
                        print 'handles IN ', i.handleInLength(), i.handleInTime()
                        print 'handels OUT', i.handleOutLength(), i.handleOutTime()                        
                    
                    nothingRight = True
                    nothingLeft = True

                    customStepSizeR = stepSize
                    customStepSizeL = stepSize

                    for x in i.parent().items():
                        if not x == i:
                            for z in range(stepSize):
                                if x.timelineIn() == i.timelineOut() + z:
                                    print 'FOUND RIGHT at ', z, x
                                    #nothingRight = False
                                    customStepSizeR = z-1
                                    #print 'customStepSizeR', customStepSizeR               

                        if not x == i:
                            for z in range(stepSize):
                                if x.timelineOut() == i.timelineIn() - z:
                                    print 'FOUND LEFT at ', z, x
                                    #nothingLeft = False                            
                                    customStepSizeL = z-1
                                    #print 'customStepSizeL', customStepSizeL

                    if nothingRight:
                        #print 'right'
                        iniTimelineOut = i.timelineOut()
                        if customStepSizeR <= i.handleOutLength():
                            i.trimOut(-customStepSizeR)
                        else:
                            print i.name(), 'no more OUT handels'
                            i.trimOut(-i.handleOutLength())

                    if nothingLeft:
                        #print 'left'
                        iniTimelineIn = i.timelineIn()
                        if customStepSizeL <= i.handleInLength():
                            i.trimIn(-customStepSizeL)
                        else:
                            print i.name(), 'no more IN handels'
                            i.trimIn(-i.handleInLength())
            
                    if verbose:
                        #print i.name()
                        print 'timeline   ', i.timelineIn(), i.timelineOut()
                        print 'source     ', i.sourceIn(), i.sourceOut()
                        print 'handles IN ', i.handleInLength(), i.handleInTime()
                        print 'handels OUT', i.handleOutLength(), i.handleOutTime() 
                #view.selection()[0].project().endUndo() ####################################### UNDO PROBLEM

class ShrinkClipDuration(QtGui.QAction):
    def __init__(self):
        QtGui.QAction.__init__(self, 'Shrink Duration', None)
        self.triggered.connect(self.doIt)

    def doIt(self):
        print
        print 'Shrink Duration'

        verbose = True

        stepSize = hiero.ui.currentViewer().frameIncrement()
        
        view = hiero.ui.activeView()

        if isinstance(view, hiero.ui.TimelineEditor):
            if view.selection() is not None and len( view.selection() ) != 0:
                
                #view.selection()[0].project().beginUndo('Grow Duration') ####################################### UNDO PROBLEM

                print 'initial selection: ', view.selection()

                for i in view.selection():                    
                    
                    if verbose:
                        print i.name()
                        print 'timeline   ', i.timelineIn(), i.timelineOut()
                        print 'source     ', i.sourceIn(), i.sourceOut()
                        print 'handles IN ', i.handleInLength(), i.handleInTime()
                        print 'handels OUT', i.handleOutLength(), i.handleOutTime()                        
                    
                    nothingRight = True
                    nothingLeft = True

                    customStepSizeR = stepSize
                    customStepSizeL = stepSize

                    for x in i.parent().items():
                        if not x == i:
                            if x.timelineIn() == i.timelineOut() + 1:
                                print 'FOUND RIGHT'
                                nothingRight = False                            
              
                        if not x == i:         
                            if x.timelineOut() == i.timelineIn() - 1:
                                print 'FOUND LEFT'
                                nothingLeft = False                            

                    if len(view.selection()) == 1:
                        nothingRight = True
                        nothingLeft = True

                    if nothingRight:
                        #print 'right'                        
                        if i.duration() > stepSize:
                            i.trimOut(stepSize)
                        
                    if nothingLeft:
                        #print 'left'                        
                        if i.duration() > stepSize:                            
                            i.trimIn(stepSize)
            
                    if verbose:
                        print i.name()
                        print 'timeline   ', i.timelineIn(), i.timelineOut()
                        print 'source     ', i.sourceIn(), i.sourceOut()
                        print 'handles IN ', i.handleInLength(), i.handleInTime()
                        print 'handels OUT', i.handleOutLength(), i.handleOutTime() 
                #view.selection()[0].project().endUndo() ####################################### UNDO PROBLEM

GrowClipDuration = GrowClipDuration()
ShrinkClipDuration = ShrinkClipDuration()

# add to timeline-menu
TLMenu = hiero.ui.findMenuAction("Clip")
TLMenu.menu().addSeparator()
TLMenu.menu().addAction(GrowClipDuration)
TLMenu.menu().addAction(ShrinkClipDuration)

x = hiero.ui.findMenuAction('Grow Duration')
x.setShortcut(QtGui.QKeySequence('F2'))
y = hiero.ui.findMenuAction('Shrink Duration')
y.setShortcut(QtGui.QKeySequence('F1'))
