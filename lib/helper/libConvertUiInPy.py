#*************************************************************
# title:        Convert UI in Py
#
# content:      Converts ui and rcc format into py
#
# dependencies: Python
#
# author:       Alexander Richter 
# email:        contact@richteralexander.com
#*************************************************************

import subprocess
subprocess.Popen("C:/Python27/lib/site-packages/pyside/pyside-rcc -o ../../software/maya/scripts/ui/img_rc.py ../../img/img.qrc", shell=True)
subprocess.Popen("C:/Python27/lib/site-packages/pyside/pyside-rcc -o ../../img/img_rc.py ../../img/img.qrc", shell=True)

# subprocess.Popen("C:/Python27/scripts/pyside-uic -o ../../utilities/ui/arSave.py ../../utilities/ui/ui/arSave.ui", shell=True)
# subprocess.Popen("C:/Python27/scripts/pyside-uic -o ../../utilities/ui/arSaveAs.py ../../utilities/ui/ui/arSaveAs.ui", shell=True)
# subprocess.Popen("C:/Python27/scripts/pyside-uic -o ../../software/maya/scripts/ui/alembicExport.py ../../software/maya/scripts/ui/qt/alembicExport.ui", shell=True)
# subprocess.Popen("C:/Python27/scripts/pyside-uic -o ../../utilities/ui/arReport.py ../../utilities/ui/ui/arReport.ui", shell=True)
# # subprocess.Popen("C:/Python27/scripts/pyside-uic -o ui/warehouse.py ../software/maya/scripts/ui/qt/warehouse.ui", shell=True)
# # subprocess.Popen("C:/Python27/scripts/pyside-uic -o ../software/maya/scripts/ui/warehouse.py ../software/maya/scripts/ui/qt/warehouse.ui", shell=True)
# # subprocess.Popen("C:/Python27/lib/site-packages/pyside/pyside-rcc -o ../software/maya/scripts/ui/software/maya_rc.py ../software/maya/scripts/ui/qt/maya.qrc", shell=True)
# subprocess.Popen("C:/Python27/lib/site-packages/pyside/pyside-rcc -o ../../utilities/ui/img_rc.py ../../img/img.qrc", shell=True)

