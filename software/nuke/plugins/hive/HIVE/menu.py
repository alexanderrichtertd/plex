"""
    Hive Nuke environment
    menu.py

    version: 0.0v3
    date:    20150728
    by:      Carl Schroter

    2Do:
"""

# Hive imports


# other imports
import rvflipbook
import IconPanel
import wavePanel
import hive_functions

# Hive menu structure
HIVEmenu = nuke.toolbar("Nodes").addMenu('HIVE', icon='hive_menu.png')
x = HIVEmenu.addCommand('HIVEMIND v0.1.31')
x.setEnabled(False)

HIVEmenu.addSeparator()

HIVEmenu.addCommand('version up', 'hive_functions.HIVE_versionUp()', icon='ParticleDirectionalForce.png')

HIVEmenu.addSeparator()

HIVEmenu.addMenu('Nodes')
HIVEmenu.addMenu('Toolsets')
HIVEmenu.addMenu('Tools')
HIVEmenu.addMenu('Commands')

HIVEmenu.addCommand('Tools/bundle comp', "nuke.load('collectFiles'), collectFiles()")
HIVEmenu.addCommand('Tools/clean up comp', "nuke.load('cleanUpComp'), cleanUpComp()")
HIVEmenu.addCommand('Tools/wavePanel v1.4', 'wavePanel.go()', icon="wavePanel.png" )
HIVEmenu.addCommand('Tools/vuRenderThreads', 'vuRenderThreadsNuke.showPopup()', '#F7')

HIVEmenu.addCommand('Toolsets/flock of birds', 'nuke.tcl(\'flockOfBirds.nk\')')
HIVEmenu.addCommand('Toolsets/despill library', 'nuke.tcl(\'despillLibrary.nk\')')
HIVEmenu.addCommand('Toolsets/cs flare', 'nuke.tcl(\'cs_flare.nk\')')

hive_functions.HIVE_buildGizmoMenu(HIVEmenu)

HIVEmenu.addCommand('Commands/hide inputs', 'hive_functions.HIVE_hideInputs()', '+h')
HIVEmenu.addCommand('Commands/extract selected', 'nuke.extractSelected()', 'e')

# set Favorites
hive_functions.HIVE_buildFavorites()

# Knob Defaults
nuke.knobDefault('Write.mov.colorspace', 'sRGB')
nuke.knobDefault("Remove.channels", "rgba")
nuke.knobDefault("Remove.operation", "keep")
nuke.knobDefault("BackdropNode.note_font_color", "0xffffffff")
nuke.knobDefault("BackdropNode.note_font_size", "150")
nuke.knobDefault("BackdropNode.note_font", "bold")
nuke.knobDefault("Blur.channels","rgba")

nuke.knobDefault('Write.beforeRender',
'''try:
  hive_functions.HIVE_beforeRender()
except:
  pass''')
nuke.knobDefault('Write.afterRender',
'''try:
  hive_functions.HIVE_afterRender()
except:
  pass''')

#Franks IconPanel
def addIconPanel():
    global iconPanel
    iconPanel = IconPanel.IconPanel()
    return iconPanel.addToPane()

paneMenu = nuke.menu('Pane')
paneMenu.addCommand('Universal Icons', 'addIconPanel()')
nukescripts.registerPanel('com.ohufx.iconPanel', 'addIconPanel()')