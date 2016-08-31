import hiero.core
import hiero.ui
from PySide import QtGui
print

class RippleShorten(QtGui.QAction):
    def __init__(self):
        QtGui.QAction.__init__(self, 'Ripple Shorten', None)
        self.triggered.connect(self.doIt)

    def doIt(self):
        print
        print 'Ripple Shorten'

        newSel = []
        stepSize = hiero.ui.currentViewer().frameIncrement()
        
        view = hiero.ui.activeView()
        if isinstance(view, hiero.ui.TimelineEditor):
            if view.selection() is not None and len( view.selection() ) != 0:
                
                for index,i in enumerate(view.selection()):
                
                    if i.duration() > stepSize * 2:
                        i.trimIn(stepSize)
                        i.trimOut(stepSize)
                
                    i.move((-index*stepSize * 2)-stepSize)

RippleShorten = RippleShorten()

# add to timeline-menu
TLMenu = hiero.ui.findMenuAction("Clip")
TLMenu.menu().addSeparator()
TLMenu.menu().addAction(RippleShorten)

x = hiero.ui.findMenuAction('Ripple Shorten')
x.setShortcut(QtGui.QKeySequence('F3'))
