import nuke
import hive_mp4convert

nukeOriginalCreateNode = nuke.createNode

#==========================================================
#  NODE definition
#==========================================================
def createMyCustomNodes(node, knobs = "", inpanel = True):
	n = nukeOriginalCreateNode(node = node, knobs = knobs, inpanel = inpanel)

	# FreameHold with <this frame> button
	#------------------------------------------------------
	if n.Class() == "FrameHold":
		b1 = nuke.Tab_Knob('FrameHold++')
		b2 = nuke.Int_Knob('new_first_frame','first frame')
		b3 = nuke.PyScript_Knob('thisFrame', 'this frame', "nuke.thisNode()['new_first_frame'].setValue(nuke.frame())")
		b4 = nuke.Int_Knob('new_increment','increment')

		n.addKnob(b1)
		n.addKnob(b2)
		n.addKnob(b3)
		n.addKnob(b4)

		n['first_frame'].setExpression('new_first_frame')
		n['increment'].setExpression('new_increment')
		n['new_first_frame'].setValue(nuke.frame())
	
	# GridWarp with <copy Source to Destination> btn in UserTab
	#------------------------------------------------------
	elif n.Class() == "GridWarp3":
		b1 = nuke.PyScript_Knob('Src2Dest','copy Source to Destination', "nuke.thisNode()['destination_grid_col'].fromScript(nuke.thisNode()['source_grid_col'].toScript())")
		b2 = nuke.PyScript_Knob('Dest2Src','copy Destination to Source', "nuke.thisNode()['source_grid_col'].fromScript(nuke.thisNode()['destination_grid_col'].toScript())")
		b3 = nuke.PyScript_Knob('swapSrcDst','Swap Src and Dst', "dst = nuke.thisNode()['destination_grid_col'].toScript()\nsrc = nuke.thisNode()['source_grid_col'].toScript()\nnuke.thisNode()['destination_grid_col'].fromScript(src)\nnuke.thisNode()['source_grid_col'].fromScript(dst)")

		n.addKnob(b1)
		n.addKnob(b2)
		n.addKnob(b3)

		n['Dest2Src'].setFlag(nuke.STARTLINE)
		n['swapSrcDst'].setFlag(nuke.STARTLINE)
		n['channels'].setFlag(0)

	# SplineWarp with <copy Source to Destination> btn in UserTab
	#------------------------------------------------------
	elif n.Class() == "SplineWarp3":
		b1 = nuke.Text_Knob('t','', 'The current version of this script works only with exactly 2 splines present\nand the same number of controlpoints on the src and dst spline.')
		b2 = nuke.Text_Knob('','')
		b2.setFlag(nuke.STARTLINE)
		b3 = nuke.PyScript_Knob('resetbtn','copy selected to non-selected spline','import splinewarp_reset_v001\nsplinewarp_reset_v001.splinewarp_reset()')
		
		n.addKnob(b1)
		n.addKnob(b2)
		n.addKnob(b3)

		n['channels'].setFlag(0)
		
	# Read node with versions tab
	#------------------------------------------------------
	elif n.Class() == "Read":
		hive_mp4convert.buildTab(n)
		n['file'].setFlag(0)

	return n

nuke.createNode = createMyCustomNodes
