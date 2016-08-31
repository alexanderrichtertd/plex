#Aton
===
The Aton project is a Arnold Interface-compatible display driver
and Nuke plugin for direct rendering into the Nuke interface.

##How to install
-
1. Copy **aton.dll**(.dylib, .so) from ~/Bin to your **$NUKE_PATH**
  * In your init.py
  
     ```import aton```

  * In your menu.py 

     ```
     import nuke
     toolbar = nuke.menu("Nodes")
     mainToolBar=nuke.toolbar("Nodes")
     m = mainToolBar.addMenu("Menu")
     m.addCommand("Aton", "nuke.createNode(\"Aton\")")
     ```

2. Copy **driver_aton.dll**(.dylib, .so) from ~/Bin to your **$ARNOLD_PLUGIN_PATH**

3. Copy **aton_maya.py** from ~/Scripts to your Maya's scripts folder
 
##How to Use

1. Open Nuke and create an Aton node  
2. Open Maya, make sure Arnold is set as default renderer
3. Run this line bellow in script editor to open Aton UI or put it on the shelf

     ```
    from aton_maya import *
    aton = Aton()
    aton.show()
    ```


===
##How to Build

To build it yourself you will need to have

* Nuke 9.0+ SDK
* Arnold 4.2+ SDK
* Boost 1.54+

It's based on: 

*Dan Bethelli's Rmanconnect which is freely available at.*
http://github.com/danbethell/rmanconnect

*Chad Dombrova's driver for arnold, freely available at.*
https://github.com/chadrik/renderconnect.

Arnold® is a registered trademark of Solid Angle.

Nuke® is a registered trademark of The Foundry.
