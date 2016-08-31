# This example adds a right-click Menu to the Timeline, Spreadsheet and Bin View for getting the current Selection
# After running this action, 'hiero.selectedItems' will store the selected items for use in the Script Editor.
# An Action is also added to the Edit Menu, with a keyboard shortcut of Ctrl/Cmd+Alt+C.
# v1.0.1 - Antony Nasce, May 14th, 2013
# Note: Ctrl/Cmd+Alt+C shortcut does not currently work in the Spreadsheet due to Bug 35887 - hiero.ui.activeView does not return a SpreadsheeView

import hiero.core
import hiero.ui
from PySide.QtGui import QAction

class SelectedShotAction(QAction):
  kAlwaysReturnActiveItem = True
  def __init__(self):
    QAction.__init__(self, "Get Python Selection", None)
    self.triggered.connect(self.getPythonSelection)
    hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.eventHandler)
    hiero.core.events.registerInterest("kShowContextMenu/kBin", self.eventHandler)
    hiero.core.events.registerInterest("kShowContextMenu/kSpreadsheet", self.eventHandler)
    self.setShortcut("Ctrl+Alt+C")
    self._selection = None

  def getPythonSelection(self):
    """Get the Python selection and stuff it in: hiero.selectedItems"""
    self.updateActiveViewSelection()
    
    print "Python selection stored in: hiero.selectedItems:\n", self._selection
    hiero.selectedItems = self._selection
  
  def updateActiveViewSelection(self):
    view = hiero.ui.activeView()

    if hasattr(view, 'selection'):
      selection = view.selection()

      # If we're in the BinView, we pretty much always want the activeItem, so whack that in...
      if isinstance(view,hiero.ui.BinView):
        if self.kAlwaysReturnActiveItem:
          self._selection = [(item.activeItem() if hasattr(item,'activeItem') else item) for item in selection]
          print 'Bin View found.. selection is:' + str(self._selection)
      else:
        self._selection = selection

  def eventHandler(self, event):
    view = event.sender
    self._selection = None
    if isinstance(view, hiero.ui.SpreadsheetView):
      self._selection = view.selection()

    # Add the Menu to the right-click menu
    event.menu.addAction( self )

# The act of initialising the action adds it to the right-click menu...
SelectedShotAction = SelectedShotAction()

# And to enable the Ctrl/Cmd+Alt+C, add it to the Menu bar Edit menu...
editMenu = hiero.ui.findMenuAction("Edit")
editMenu.menu().addAction(SelectedShotAction)
