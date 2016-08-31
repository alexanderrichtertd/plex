P:/_pipeline/_sandbox/nuke/gizmos/wsdf.gizmo


# current node of the knob
nuke.thisNode()

# getting a knob's value of a specific node:
[value Read1.first]

# getting a knob's value of current node:
[value this.size]

# 01.10.2015 15:45
[date %d.%m.%Y]  [date %H:%M]

# 000_comp_v001_ar
[file rootname [file tail [value root.name] ] ]

# dont work but theoreticly
[value root.dirName]

# get parent knob value
[value parent.comment]







# set Path
[file dirname [value root.name]]/_rendering/[file rootname [file tail [value root.name]]]/[if {[value this.exr]} {return "exr"} {return "jpg"}]/[file rootname [file tail [value root.name] ] ].####.[if {[value this.exr]} {return "exr"} {return "jpg"}]

# create folder [before render]
if not os.path.isdir(os.path.dirname(nuke.thisNode()['file'].evaluate())):
  os.makedirs(os.path.dirname(nuke.thisNode()['file'].evaluate()))

# Img with Link
<a href="https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline">
<img border="0" alt="BREAKINGPOINT" src="\\bigfoot\breakingpoint\_pipeline\img\banner\bpBanner.png" width="522" height="54">
</a>

# Img
<img border="0" alt="BREAKINGPOINT" src="\\bigfoot\breakingpoint\_pipeline\img\btn\btnRender48.png" width="20" height="20">



//bigfoot/breakingpoint/_pipeline/img/btn/btnInboxF48.png




if not os.path.isdir(os.path.dirname(nuke.thisNode()['file'].getValue())):
  os.makedirs(os.path.dirname(nuke.thisNode()['file'].getValue()))



  P:\0_rnd\arichter\nuke\_rendering\gizmoWrite11\exr\gizmoWrite11.####.exr




# add linked icon into panel
# <a href="https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline">
# <img border="0" alt="banner" src="P:\_pipeline\img\banner\bpBanner.png" width="522" height="54">

# add on create
# nuke.selectedNode()["onCreate"].setValue("from scripts import write\nwrite.start()")

# <b><font size='4' color='#dc520f'> arWRITE</font></b><font size='2' align='right'><br> pipeline conform write node</font>

# <font size='2' color='#808080'>v0.4.0 | © Alexander Richter | 2016</font>




if nuke.selectedNode()["exr"].getValue() and not os.path.isdir(os.path.dirname(nuke.thisNode()['renderPath'].evaluate())):
  os.makedirs(os.path.dirname(nuke.thisNode()['renderPath'].evaluate()))

if nuke.selectedNode()["jpg"].getValue() and not os.path.isdir(os.path.dirname(nuke.thisNode()['renderPath'].evaluate()).replace("exr","jpg")):
  os.makedirs(os.path.dirname(nuke.thisNode()['renderPath'].evaluate()).replace("exr","jpg"))
