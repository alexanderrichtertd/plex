Arnold DNA render kit 2.0

*** Description.
- aiCreateAttr - add attributes mtoa_constant_<name> of different data types to an jbject shapes
- aiSetAttr - set attributes mtoa_constant_<name>
- aiIDmanager - create OJECT or SHADER IDs
- aiSetSubdiv - set sobdivition attributes and turn maya smooth off
- aiShaderManager - read and set custom attributes to operate with materials
- aiSaveVersion - save next version of current scene. Scene should has name like <scene_Name_001.mb>



*** How to install.
Put scripts to \Documents\maya\201X-x64\scripts
Put icons to \Documents\maya\201X-x64\prefs\icons

*** How to run.
In Python tab of Maya script editor execute code

For aiCreateAttr.py:
import aiCreateAttr
aiCreateAttr.windowADD()

For aiSetAttr.py:
import aiSetAttr
aiSetAttr.windowSET()

For iIDmanager.py:
import aiIDmanager
aiIDmanager.windowID()

For aiSetSubdiv.py:
from aiSetSubdiv import *
windowSBD()


For aiShaderManager.py:
import aiShaderManager
aiShaderManager.windowSHM()

For aiSaveVersion.py:
import aiSaveVersion
aiSaveVersion.SNV()


Detail descriotion www.kiryha.blogspot.com/2014/02/render-notes.html
