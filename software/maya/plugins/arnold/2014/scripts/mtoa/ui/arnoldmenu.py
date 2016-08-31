import pymel.core as pm
import mtoa.core as core
from mtoa.core import createStandIn, createVolume
from mtoa.ui.ae.aiStandInTemplate import LoadStandInButtonPush
import mtoa.utils as mutils
import maya.cmds as cmds
import mtoa.txManager
import mtoa.lightManager
import mtoa.renderToTexture
import arnold as ai

from uuid import getnode as get_mac
import os
import shutil
import sys

def doCreateStandInFile():
    node = createStandIn()
    LoadStandInButtonPush(node.name())

def doExportStandin():
    pm.mel.eval('ExportSelection')
    pm.mel.eval('setCurrentFileTypeOption ExportActive "" "ASS Export"')

def doExportOptionsStandin():
    pm.mel.eval('ExportSelectionOptions')
    pm.mel.eval('setCurrentFileTypeOption ExportActive "" "ASS Export"')
    
def doCreateMeshLight():
    sls = cmds.ls(sl=True, et='transform')
    if len(sls) == 0:
        cmds.confirmDialog(title='Error', message='No transform is selected!', button='Ok')
        return
    shs = cmds.listRelatives(sls[0], type='mesh')
    if shs is None:
        cmds.confirmDialog(title='Error', message='The selected transform has no meshes', button='Ok')
        return
    elif len(shs) == 0:
        cmds.confirmDialog(title='Error', message='The selected transform has no meshes', button='Ok')
        return
    cmds.setAttr('%s.aiTranslator' % shs[0], 'mesh_light', type='string')

    
def arnoldAboutDialog():
    arnoldAboutText =  u"Arnold for Maya\n\n"
    arnoldAboutText += "MtoA " + cmds.pluginInfo( 'mtoa', query=True, version=True)
    arnoldMercurialID = cmds.arnoldPlugins(getMercurialID=True)
    if not '(Master)' in arnoldMercurialID:
        arnoldAboutText += " - " + arnoldMercurialID
    arnoldAboutText += "\nArnold Core "+".".join(ai.AiGetVersion())+"\n\n"
    arnoldAboutText += u"(c) 2001-2009 Marcos Fajardo and (c) 2009-2015\nSolid Angle SL\n\n"
    arnoldAboutText += u"Developed by: Ángel Jimenez, Olivier Renouard,\nYannick Puech, Borja Morales, Nicolas Dumay,\nPedro Fernando Gomez, Pál Mezei\n\n"
    arnoldAboutText += u"Acknowledgements: Javier González, Miguel González, \nLee Griggs, Chad Dombrova, Gaetan Guidet, \nGaël Honorez, Diego Garcés, Kevin Tureski, \nFrédéric Servant"

    if (cmds.window("AboutArnold", ex=True)):
        cmds.deleteUI("AboutArnold")
    w = cmds.window("AboutArnold", title="About")
    cmds.window("AboutArnold", edit=True, width=402, height=280)
    cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1,20), (2, 52), (3, 50), (4, 280)] )

    cmds.text(label="");cmds.text(label="");cmds.text(label="");cmds.text(label="")

    cmds.text(label="")
    cmds.image(image="MtoA_Logo.png")
    cmds.text(label="")
    cmds.text(align="left",label=arnoldAboutText)

    cmds.text(label="");cmds.text(label="\n");cmds.text(label="");cmds.text(label="")

    cmds.text(label="")
    cmds.text(label="")
    cmds.button( width=150,label='OK', command=('import maya.cmds as cmds;cmds.deleteUI(\"' + w + '\", window=True)') )
    cmds.setParent( '..' )
    
    cmds.showWindow(w)
    
def dotDotDotButtonPush(file):
    licenseFilter = 'License Files (*.lic)'
    ret = cmds.fileDialog2(fileFilter=licenseFilter, 
                            cap='Load License File',okc='Load',fm=1)
    if ret is not None and len(ret):
        cmds.textField(file, edit=True, text=ret[0])
        
def installButtonPush(file):
    licenseFile = cmds.textField(file, query=True, text=True)
    import maya.mel as mel
    mPath = mel.eval('getenv "MTOA_PATH"')
    destination = os.path.join(mPath,'bin')
    try:
        shutil.copy(licenseFile,destination)
        cmds.confirmDialog(title='Success', message='License Successfully Installed', button=['Ok'], defaultButton='Ok' )
    except:
        cmds.arnoldCopyAsAdmin(f=licenseFile,o=destination)
    
def arnoldLicenseDialog():
    if (cmds.window("ArnoldLicense", ex=True)):
        cmds.deleteUI("ArnoldLicense")
    w = cmds.window("ArnoldLicense", title="Arnold Node-locked License")
    cmds.window("ArnoldLicense", edit=True, width=550, height=280)
    cmds.columnLayout()
    cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1,10), (2, 64), (3, 18), (4, 450)] )

    cmds.text(label="");cmds.text(label="");cmds.text(label="");cmds.text(label="")

    arnoldAboutText =  u"A node-locked license allows you to render with Arnold on one computer only.\n"

    cmds.text(label="")
    cmds.image(image="licensing_mtoa.png")
    cmds.text(label="")
    cmds.text(align="left",label=arnoldAboutText)

    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()

    cmds.setParent( '..' )
    cmds.separator()

    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,10), (2, 500)] )
    macText =  u"To issue a node-locked license, we need the MAC address of your computer.\n"
    cmds.text(label="")
    cmds.text(align="left",label=macText)
    cmds.setParent( '..' )
    cmds.separator()

    cmds.rowColumnLayout( numberOfColumns=6, columnWidth=[(1,10),(2,90), (3, 190),(4,40),(5,80),(6,132)] )
    cmds.text(label="")
    cmds.text(align="left",label="MAC Address")
    name = cmds.textField()
    mac = get_mac()
    mactext = ("%012X" % mac)
    cmds.textField(name,  edit=True, text=mactext, editable=False )
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()

    cmds.setParent( '..' )

    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,10), (2, 500)] )
    macText =  u"To install your node-locked license, locate the license file (.lic) and click Install.\n"
    cmds.text(label="")
    cmds.text(align="left",label=macText)
    cmds.setParent( '..' )

    cmds.rowColumnLayout( numberOfColumns=8, columnWidth=[(1,10),(2,90), (3, 190),(4,7),(5,26),(6,7),(7,80),(8,132)] )
    cmds.text(label="")
    cmds.text(align="left",label="License file (.lic)")
    file = cmds.textField()
    cmds.text(label="")
    cmds.button( label='...', command=lambda *args: dotDotDotButtonPush(file) )
    cmds.text(label="")
    cmds.button( label='Install', command=lambda *args: installButtonPush(file) )
    cmds.text(label="")

    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    cmds.setParent( '..' )

    cmds.rowColumnLayout( numberOfColumns=5, columnWidth=[(1,200),(2,160), (3, 80),(4,20),(5,80)] )
    cmds.text(label="")
    cmds.text(label="")
    cmds.button( label='Close', command=('import maya.cmds as cmds;cmds.deleteUI(\"' + w + '\", window=True)'))
    cmds.text(label="")
    cmds.button( label='Help', c=lambda *args: cmds.launch(webPage='https://www.solidangle.com/support/licensing/'))

    cmds.setParent( '..' )

    cmds.showWindow(w)
    
def arnoldTxManager():
    win = mtoa.txManager.MtoATxManager()
    win.create()
    win.refreshList()
    
def arnoldLightManager():
    win = mtoa.lightManager.MtoALightManager()
    win.create()

def arnoldBakeGeo():
    objFilter = "Obj File (*.obj)"
    ret = cmds.fileDialog2(cap='Bake Selection as OBJ', fm=0, ff=objFilter)
    if ret is not None and len(ret):
        cmds.arnoldBakeGeo(f=ret[0])

def arnoldRenderToTexture():
    selList = cmds.ls(sl=1)
    if (len(selList) == 0):
        cmds.confirmDialog( title='Render To Texture', message='No Geometry Selected', button=['Ok'], defaultButton='Ok', cancelButton='Ok', dismissString='Ok' )
        return False

    win = mtoa.renderToTexture.MtoARenderToTexture()
    win.create()
    

def selectCamera(cam):
    core.ACTIVE_CAMERA=cam

def populateSelectCamera():
    # clear camera menu
    pm.menu('ArnoldSelectCamera', edit=True, deleteAllItems=True)

    coll = pm.radioMenuItemCollection(parent='ArnoldSelectCamera')

    # populate camera menu    
    cameras = cmds.ls(type='camera')
    if cameras != None:
        activeCamera = core.ACTIVE_CAMERA
        if not activeCamera in cameras:
            activeCamera = None
        if activeCamera == None:
            if 'perspShape' in cameras:
                activeCamera = 'perspShape'
            elif len(cameras):
                activeCamera = cameras[0]
            core.ACTIVE_CAMERA = activeCamera
        for cam in cameras:
            pm.menuItem('SelectCameraItem%s' % cam, label=cam, parent='ArnoldSelectCamera',
                        radioButton=cam == activeCamera, cl=coll,
                        c='from mtoa.ui.arnoldmenu import selectCamera; selectCamera("%s")' % cam)

def startRender():
    if core.ACTIVE_CAMERA != None:
        cmds.arnoldRender(cam=core.ACTIVE_CAMERA)

def startRenderView():
    # core.ACTIVE_CAMERA is not set, anything we could do here ?
    #if core.ACTIVE_CAMERA != None:
    #    cmds.arnoldRenderView(cam=core.ACTIVE_CAMERA)
    # so instead we're calling it without any argument
    core.createOptions()

    cmds.arnoldRenderView()

def startIpr():
    if core.ACTIVE_CAMERA != None:
        cmds.arnoldIpr(cam=core.ACTIVE_CAMERA, m='start')

def refreshRender():
    if core.ACTIVE_CAMERA != None:
        cmds.arnoldIpr(cam=core.ACTIVE_CAMERA, m='refresh')

def stopRender():
    if core.ACTIVE_CAMERA != None:
        cmds.arnoldIpr(cam=core.ACTIVE_CAMERA, m='stop')

def createArnoldMenu():
    # Add an Arnold menu in Maya main window
    if not pm.about(b=1):
        pm.menu('ArnoldMenu', label='Arnold', parent='MayaWindow', tearOff=True )

        pm.menuItem('ArnoldStandIn', label='StandIn', parent='ArnoldMenu', subMenu=True, tearOff=True)
        pm.menuItem('ArnoldCreateStandIn', parent='ArnoldStandIn', label="Create",
                    c=lambda *args: createStandIn())
        pm.menuItem('ArnoldCreateStandInFile', parent='ArnoldStandIn', optionBox=True,
                    c=lambda *args: doCreateStandInFile())
        pm.menuItem('ArnoldExportStandIn', parent='ArnoldStandIn', label='Export',
                    c=lambda *args: doExportStandin())
        pm.menuItem('ArnoldExportOptionsStandIn', parent='ArnoldStandIn', optionBox=True,
                    c=lambda *args: doExportOptionsStandin())

        pm.menuItem('ArnoldLights', label='Lights', parent='ArnoldMenu', subMenu=True, tearOff=True)
        
        pm.menuItem('ArnoldAreaLights', parent='ArnoldLights', label="Area Light",
                    c=lambda *args: mutils.createLocator('aiAreaLight', asLight=True))
        pm.menuItem('SkydomeLight', parent='ArnoldLights', label="Skydome Light",
                    c=lambda *args: mutils.createLocator('aiSkyDomeLight', asLight=True))
        pm.menuItem('ArnoldMeshLight', parent='ArnoldLights', label='Mesh Light',
                    c=lambda *args: doCreateMeshLight())
        pm.menuItem('PhotometricLights', parent='ArnoldLights', label="Photometric Light",
                    c=lambda *args: mutils.createLocator('aiPhotometricLight', asLight=True))

        pm.menuItem(parent='ArnoldLights', divider=True)

        pm.menuItem('MayaDirectionalLight', parent='ArnoldLights', label="Maya Directional Light",
                    c=lambda *args: cmds.CreateDirectionalLight())
        pm.menuItem('MayaPointLight', parent='ArnoldLights', label="Maya Point Light",
                    c=lambda *args: cmds.CreatePointLight())
        pm.menuItem('MayaSpotLight', parent='ArnoldLights', label="Maya Spot Light",
                    c=lambda *args: cmds.CreateSpotLight())
        pm.menuItem('MayaQuadLight', parent='ArnoldLights', label="Maya Quad Light",
                    c=lambda *args: cmds.CreateAreaLight())
                    
        pm.menuItem('ArnoldVolume', label='Volume', parent='ArnoldMenu',
                    c=lambda *args: createVolume())
                    
        pm.menuItem('ArnoldFlush', label='Flush Caches', parent='ArnoldMenu', subMenu=True, tearOff=True)
        pm.menuItem('ArnoldFlushTexture', parent='ArnoldFlush', label="Textures",
                    c=lambda *args: cmds.arnoldFlushCache(textures=True))
        pm.menuItem('ArnoldFlushBackground', parent='ArnoldFlush', label="Skydome Lights",
                    c=lambda *args: cmds.arnoldFlushCache(skydome=True))
        pm.menuItem('ArnoldFlushQuads', parent='ArnoldFlush', label="Quad Lights",
                    c=lambda *args: cmds.arnoldFlushCache(quads=True))
        pm.menuItem('ArnoldFlushAll', parent='ArnoldFlush', label="All",
                    c=lambda *args: cmds.arnoldFlushCache(flushall=True))
                    
        pm.menuItem('ArnoldUtilities', label='Utilities', parent='ArnoldMenu', subMenu=True, tearOff=True)
        pm.menuItem('ArnoldBakeGeo', label='Bake Selected Geometry', parent='ArnoldUtilities',
                    c=lambda *args: arnoldBakeGeo())
        pm.menuItem('ArnoldRenderToTexture', label='Render Selection To Texture', parent='ArnoldUtilities',
                    c=lambda *args: arnoldRenderToTexture())
        pm.menuItem('ArnoldTxManager', label='Tx Manager', parent='ArnoldUtilities',
                    c=lambda *args: arnoldTxManager())                    
        pm.menuItem('ArnoldLightManager', label='Light Manager', parent='ArnoldUtilities',
                    c=lambda *args: arnoldLightManager())

        pm.menuItem('ArnoldHelpMenu', label='Help', parent='ArnoldMenu',
                    subMenu=True, tearOff=True)

        pm.menuItem('ArnoldUserGuide', label='User Guide', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://support.solidangle.com/display/AFMUG/Arnold+for+Maya+User+Guide'))

        pm.menuItem('ArnoldTutorials', label='Common Workflows', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://support.solidangle.com/display/AFMUG/Common+Workflows'))

        pm.menuItem('ArnoldVideos', label='Videos', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://support.solidangle.com/display/AFMUG/Video+Tutorials'))

        pm.menuItem(divider=1, parent='ArnoldHelpMenu')

        pm.menuItem('ArnoldSolidAngle', label='Solid Angle', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://www.solidangle.com'))

        pm.menuItem('ArnoldMailingLists', label='Mailing Lists', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://subscribe.solidangle.com'))

        pm.menuItem('ArnoldAsk', label='Knowledge Base', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://ask.solidangle.com'))

        pm.menuItem('ArnoldSupportBlog', label='Support Blog', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://support.solidangle.com/blog/arnsupp'))

        pm.menuItem('ArnoldLicensing', label='Licensing', parent='ArnoldHelpMenu',
                    c=lambda *args: arnoldLicenseDialog())

        pm.menuItem(divider=1, parent='ArnoldHelpMenu')

        pm.menuItem('ArnoldDeveloperGuide', label='Developer Guide', parent='ArnoldHelpMenu',
                    c=lambda *args: cmds.launch(webPage='https://support.solidangle.com/display/ARP/Arnoldpedia'))

        pm.menuItem('ArnoldExperimentalMenu', label='Experimental', parent='ArnoldMenu', subMenu=True, tearOff=True)
        pm.menuItem('ArnoldRenderView', label='MtoA RenderView', parent='ArnoldExperimentalMenu',
                    c=lambda *args: startRenderView())


        pm.menuItem('ArnoldRender', label='Houdini MPlay', parent='ArnoldExperimentalMenu', subMenu=True, tearOff=True)
        pm.menuItem('ArnoldSelectCamera', label='Select Camera', parent='ArnoldRender', subMenu=True, tearOff=False, 
                    postMenuCommand=lambda *args: populateSelectCamera())
        populateSelectCamera()
        pm.menuItem('ArnoldStartRender', label='Render', parent='ArnoldRender',
                    c=lambda *args: startRender())
        pm.menuItem('ArnoldStartIPR', label='IPR', parent='ArnoldRender',
                    c=lambda *args: startIpr())
        pm.menuItem('ArnoldRefresh', label='Refresh', parent='ArnoldRender',
                    c=lambda *args: refreshRender())
        pm.menuItem('ArnoldStopRender', label='Stop Render', parent='ArnoldRender',
                    c=lambda *args: stopRender())
                    
        pm.menuItem('ArnoldAbout', label='About', parent='ArnoldMenu',
                    c=lambda *args: arnoldAboutDialog())

