#*************************************************
# Title         Import Look Dev Water
#
# Content       Import look dev scene into current scene
#               and set up the scene for look dev
#
# Author        simon.french@framstore.com
# Modification  alexander.richter@framstore.com
#*************************************************

import os
import sys

import maya.mel  as mel
import maya.cmds as cmds


def import_neutral_lookdev_arnold_water_scene(filePath = ""):
    projectPath = "/"

    if filePath == "": 
        basePath = os.path.realpath(__file__).split("/")

        # GET project path : /job/comms/projectName
        for i in range(0,4):
            projectPath = os.path.join(projectPath, basePath[i])

        filePath = os.path.join(projectPath,"asset/GenericScene/lookdev/lookdev/work/maya/scenes/")

    arnold_template_file = os.path.join(filePath, "GenericScene_lookdev_default_v001.mb")
    mel.eval('source nyLoadArnold.mel')

    print filePath
    print arnold_template_file

    # import scene
    timeUnit = cmds.currentUnit(time=1, q=1)
    cmds.currentUnit( time='pal', updateAnimation=False)
    cmds.file(arnold_template_file, i=True, type="mayaBinary", rpr="CLASH",
              options="v=0", pr=True, loadReferenceDepth="all")
    cmds.currentUnit( time=timeUnit, updateAnimation=False)

    # setup render globals
    try:
        import sfMayaTools.aiTools as ait
        ait.setArnoldPrefs()
    except:
        sys.stdout.write("WARNING: Cannot load sfMayaTools.aiTools. Not to worry, but your render globals have not been fully setup")
        cmds.setAttr("defaultViewColorManager.imageColorProfile", 4)
        cmds.setAttr("defaultViewColorManager.displayColorProfile", 5)
    
   
    # Set timeline
    cmds.playbackOptions(ast=1001)
    cmds.playbackOptions(min=1001)
    cmds.playbackOptions(max=1110)
    cmds.playbackOptions(aet=1110)
    mel.eval('currentTime 1001 ;')




 # filenodes = [ 
    #               {"node" : "IBL_studioCyc", "filename" : "ibl_studioCyc_4k.tx"},
    #               {"node" : "IBL_studioKinoFlo", "filename" : "ibl_studioKinoFlo_4k.tx"},
    #               {"node" : "IBL_studioKinoFlo_alt_01", "filename" : "ibl_studioKinoFlo_alt_01_4k.tx"},
    #               {"node" : "IBL_studioKinoFlo_alt_02", "filename" : "ibl_studioKinoFlo_alt_02_4k.tx"},
    #               {"node" : "IBL_sunny", "filename" : "ibl_sunny_4k.tx"},
    #               {"node" : "colorChecker", "filename" : "ColorChecker_LIN_20charts_16bit.tif"}
    #             ]

    # # Attach image files
    # for node in filenodes:
    #     hdri_file = os.path.join(filePath, node["filename"])
    #     cmds.setAttr("%s.fileTextureName"%node["node"], hdri_file, type="string")

    # cmds.setAttr("studio_imagePlaneShape.imageName", 
    #                 os.path.join(filePath, "plate_studioKinoFlo_clean_2k.exr"), type="string")
    
