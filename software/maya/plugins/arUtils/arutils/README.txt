At this stage we have developed a practical toolset which increases our productivity
in day to day and productions tasks.

With that in mind we want to share our developments
with you and are more than happy to make them publicly available.


We started this as a total spare time project and it was aimed to get a better python
& qt programming knowledge as well as sharing experiences and ideas.

The toolset focuses
on workflows within Autodesk's Maya and the Solidangle'S MtoA (MayaToArnold plugin) and
is associated with shading, lighting and rendering workflows.

If you want to use it, we would be honored to get your feedback, suggestions, requests
and bug reports.



Just drop us a line at ardevutils@gmail.com

Though it seems like a complete toolset, our code and development is far from being
complete or bug-free, but nevertheless we hope that you will benefit from our tools.


If you like what we do and want to support us with developing further tools and workflow
enhancements we would be more than happy to receive a donation.
We still have a lot of ideas in mind and we want to spend some time developing them.


INSTALLATION:

To install the arUtils package you have two options:

If you want to use arUtils with Maya 2013 and below, please ensure that you have installed
PyQt correctly. 
You can use arUtils with Maya 2014 and newer without installing anything
else.

Additional infos about installing you can find here:
http://nathanhorne.com/?p=451

Option 1 


(recommended):
-------------------------------------------------------------------------------------------
- 
unzip the the archive file and copy the filepath

- open the maya.env file within your Maya application directory

- if you are not sure where this is on your OS please take a look into this Maya File
  Variables Help
  
(http://help.autodesk.com/view/MAYAUL/2015/ENU/?guid=Environment_Variables_Setting_environment_variables_using_Maya)

- add the following two lines in your maya.env file and overwrite it. 

Replace "path to
  arutils main directory" with your previously copied filepath


MAYA_MODULE_PATH = path to arutils main directory

PYTHONPATH = path to arutils main directory



in case you are on windows it could look like this:

MAYA_MODULE_PATH = C:\tools\arutils-0.1.0

PYTHONPATH = C:\tools\arutils-0.1.0

When you start maya the next time you should see the maya menu arutils. Thats it! You can use it now :)

-----------------------------------------------------------------------------------------------------------------------------------------------------

Option 2:
-----------------------------------------------------------------------------------------------------------------------------------------------------
- unzip the the archive file
- from the arutils-versionr (root folder) copy the arutils folder into your Maya script
  directory

- If you are not sure where this is on your OS please take a look into this Maya File Variables Help
  (http://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2015/ENU/Maya/files/Environment-Variables-File-path-variables-htm.html)

- within the arutils/scripts folder you can find a userSetup.py file

- copy this file into the same maya scripts directory as you did before with the arutils folder

When you start maya the next time you should see the maya menu arutils. Thats it. You can use it now :)

------------------------------------------------------------------------------------------------------------------------------------------------------


------------------------------------------------------------------------------------------------------------------------------------------------------
Disclaimer:

We, Arvid Schneider and Rico Koschmitzky (arUtils) are not responsible in any way, if the tools made
available by us are causing any broken or damaged scenes. The arUtils package is only genuine if it
is downloaded from the official download page here. If you have downloaded it elsewhere, we too take
no responsibility at all.

Copyright 2015
Rico Koschmitzky & Arvid Schneider