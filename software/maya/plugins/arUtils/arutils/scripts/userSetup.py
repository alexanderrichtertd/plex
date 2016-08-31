import sys
import os
import pymel.core as pm
import maya.mel as mel
import arutils.ui.generalUI
import arutils.src.arUtilitiesMaya


ICON_LOCATION = os.path.join(os.path.dirname(arutils.ui.generalUI.__file__)[:-2] + 'icons')

global AR_MAIN
AR_MAIN = {'Options' : '',
           'ViewportRender' : '',
           'TextureSwitch' : '',
           'MaterialIdManager' : '',
           'ConsolidateTextures' : '',
           'LightGeoControl' : '',
           'AssetLibrary' : '',
           'AssetPublish' : '',
           'AssetManager' : ''}

def arMayaMenuUnique01():
    arMenu = pm.menu('arUtilsMenu', p = 'MayaWindow', l = 'arUtils',to = 1)

    pm.menuItem(p = arMenu,
                l = 'Options',
                c = 'import arutils.ui.generalUI;arOptions = arutils.ui.generalUI.Options();AR_MAIN["Options"] = arOptions;arOptions.show()')
    pm.menuItem(d = True)
    pm.menuItem(p = arMenu,
                l = 'Online Documentation',
                c = 'import arutils.doc.openDoc;arutils.doc.openDoc.openOnlineDoc()')
    pm.menuItem(d = True)
    pm.menuItem(p = arMenu,
                l = 'Viewport Render',
                c = 'import arutils.ui.generalUI;arViewportRender = arutils.ui.generalUI.drawViewportRenderRegion();AR_MAIN["ViewportRender"] = arViewportRender')
    pm.menuItem(p = arMenu,
                l = 'Texture Switch',
                c = 'import arutils.ui.generalUI;'
                    'arTextureSwitch = arutils.ui.generalUI.TextureSwitchUI();'
                    'AR_MAIN["TextureSwitch"] = arTextureSwitch;\ntry:arTextureSwitch.close();\nexcept:pass;\narTextureSwitch.dockUI(init = True);')
    pm.menuItem(p = arMenu,
                l = 'Material ID Manager',
                c = 'import arutils.ui.generalUI;arMaterialIdManager = arutils.ui.generalUI.MaterialIdManager().showUi();AR_MAIN["MaterialIdManager"] = arMaterialIdManager')
    pm.menuItem(p = arMenu,
                l = 'Light/Geo Control',
                c = 'import arutils.ui.generalUI;arLightGeoControl = arutils.ui.generalUI.LightGeoControl();AR_MAIN["LightGeoControl"] = arLightGeoControl;arLightGeoControl.showUi()')
    """
    assetsMenu = pm.menuItem(p = arMenu, l = 'Assets', to = True, sm = True)
    pm.menuItem(p = assetsMenu,
                l = 'Asset Libary',
                c = 'import arutils.ui.generalUI;reload(arutils.ui.generalUI);arutils.ui.generalUI.AssetLibrary().showUi()')
    pm.menuItem(p = assetsMenu,
                l = 'Asset Publish',
                c = 'import arutils.ui.generalUI;reload(arutils.ui.generalUI);arutils.ui.generalUI.AssetPublish().showUi()')
    pm.menuItem(p = assetsMenu,
                l = 'Asset Manager',
                c = 'import arutils.ui.generalUI;reload(arutils.ui.generalUI);arutils.ui.generalUI.AssetManager().showUi()')
    """
    toolMenu = pm.menuItem(p = arMenu, l = 'Utilities', to = True, sm = True)
    """
    pm.menuItem(p = toolMenu,
                l = 'Consolidate Scene Textures',
                c = 'import arutils.ui.generalUI;reload(arutils.ui.generalUI);'
                    'arConsolidateSceneTextures = arutils.ui.generalUI.ConsolidateTextures();'
                    'AR_MAIN["ConsolidateTextures"] = arConsolidateSceneTextures;arConsolidateSceneTextures.showUi()')
    """
    pm.menuItem(p = toolMenu,
                l = 'Dock Output Window',
                c = 'import arutils.ui.generalUI;arutils.ui.generalUI.dockableOutputWindow()')
    pm.menuItem(p = toolMenu,
                l = 'Search UI Elements',
                c = 'import arutils.ui.generalUI;arutils.ui.generalUI.SearchUI().create()')
    """
    pm.menuItem(p = toolMenu,
                l = 'Dock Script Editor',
                c = 'import arutils.ui.generalUI;reload(arutils.ui.generalUI);arutils.ui.generalUI.openCustomScriptEditor()')
    pm.menuItem(p = toolMenu,
                l = 'Light Control',
                c = 'import arutils.ui.generalUI;reload(arutils.ui.generalUI);arutils.ui.generalUI.LightControl().create(winValue = True)')
    """
    pm.menuItem(p = toolMenu,
                l = 'FPS Drop Down',
                c = 'import arutils.ui.generalUI;arutils.ui.generalUI.fpsDropDown()')
    pm.menuItem(p = arMenu,
                d = True)
    pm.menuItem(p = arMenu,
                l = 'About',
                c = pm.Callback(about))

    ''' ChannelBox CopyPaste Menu items '''
    mel.eval('generateChannelMenu "popupMenu1" 1;')
    pm.menuItem('realCopy',
                l = 'Copy',
                p = 'popupMenu1',
                ia = 'cutItem',
                bld = True,
                c = 'x = arutils.src.arUtilitiesMaya.Attributes(); pm.Callback(x.copyCmd())')
    pm.menuItem('realPaste',
                l = 'Paste',
                p = 'popupMenu1',
                ia = 'copyItem',
                bld = True,
                c = 'pm.Callback(x.pasteCmd())')

    ''' Outliner Set Menu Item'''

    try:
        Scenes = arutils.src.arUtilitiesMaya.Scenes()
        setMenu = pm.menuItem('customSetMenu',
                              l = 'Sets',
                              bld = True,
                              sm = True,
                              p = 'outlinerPanel1Popup')
        pm.menuItem('setMenuItemA',
                    l = 'Add Selection to Set',
                    c = pm.Callback(Scenes.addRemoveSetMembers,'add'), p = setMenu)
        pm.menuItem('setMenuItemB',
                    l = 'Remove Members from Set',
                    c = pm.Callback(Scenes.addRemoveSetMembers,'remove'), p = setMenu)
    except:
        pm.displayWarning('[arutils]: Could not create outliner menu')


def about():
    arutils.ui.generalUI.Generic.windowCheck('arUtilsAboutWin')
    aboutWin = pm.window('arUtilsAboutWin', t = 'arUtils', s = False, mxb = False, mnb = False)
    winLayout = pm.rowColumnLayout(nc = 2)

    text = '\n' + \
       '          arUtils 0.1.3\n\n' + \
       '\n' \
       '\n          Author: Rico Koschmitzky & Arvid Schneider' + \
       '\n          Mail: ardevutils@gmail.com' + \
       '\n          Acknowledgements: Justin Israel, Philipp Oeser' + \
       '\n\n'
    pm.text(al = 'left', l = text, p = winLayout)
    pm.image(p = winLayout, i = os.path.join(ICON_LOCATION, 'arUtilsSmallWhite.png'))
    aboutWin.show()
    
pm.evalDeferred('arMayaMenuUnique01()')