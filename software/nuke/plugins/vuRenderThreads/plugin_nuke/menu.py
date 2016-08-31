import nuke
import plugin_nuke

menuMain = nuke.menu( 'Nodes' ).addMenu("vuRenderThreads")
menuMain.addCommand("vuRenderThreads", "plugin_nuke.showPopup()", "Alt+F7")