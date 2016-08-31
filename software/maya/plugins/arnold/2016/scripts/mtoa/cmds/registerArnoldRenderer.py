import glob
import os
import sys
import inspect
import mtoa.utils
import arnoldShelf

def mtoaPackageRoot():
    '''return the path to the mtoa python package directory'''
    return os.path.dirname(os.path.dirname(inspect.getfile(inspect.currentframe())))

if 'pymel' not in globals():
    import pymel
    import pymel.versions as versions
    maya_version = versions.shortName()
    print "Maya %s importing module pymel %s (%s)" % (maya_version, pymel.__version__, pymel.__file__)
else :
    print "Maya %s had already imported module pymel %s (%s)" % (maya_version, pymel.__version__, pymel.__file__)
    
import pymel.core as pm

try:
    import mtoa.utils as utils
    import mtoa.ui.exportass as exportass
    import mtoa.ui.nodeTreeLister as nodeTreeLister
    import mtoa.ui.globals.common
    from mtoa.ui.globals.common import createArnoldRendererCommonGlobalsTab, updateArnoldRendererCommonGlobalsTab
    from mtoa.ui.globals.settings import createArnoldRendererGlobalsTab, updateArnoldRendererGlobalsTab, updateBackgroundSettings, updateAtmosphereSettings, createArnoldRendererOverrideTab, updateArnoldRendererOverrideTab
    from mtoa.ui.globals.settings import createArnoldRendererDiagnosticsTab, updateArnoldRendererDiagnosticsTab, createArnoldRendererSystemTab, updateArnoldRendererSystemTab
    from mtoa.ui.aoveditor import createArnoldAOVTab, updateArnoldAOVTab
    import mtoa.ui.ae.utils as aeUtils
    from mtoa.ui.arnoldmenu import createArnoldMenu
    import mtoa.cmds.arnoldRender as arnoldRender
except:
    import traceback
    traceback.print_exc(file=sys.__stderr__) # goes to the console
    raise

if not pm.about(batch=True):
    for nodeType in pm.pluginInfo('mtoa', q=1, dependNode=1):
        pm._factories.addMayaType(nodeType, 'kPluginDependNode')

def _overrideMelScripts():
    # for those procedures that we could not simply define overrides interactively, we keep edited files
    # per version of maya
    root = mtoaPackageRoot()
    maya_version = versions.shortName()
    meldir = os.path.join(root, maya_version, 'mel')
    meldir = mtoa.utils.convertToUnicode(meldir)
    pathsep = mtoa.utils.convertToUnicode(os.pathsep)
    maya_script_path = mtoa.utils.convertToUnicode(mtoa.utils.getEnvironmentVariable(u'MAYA_SCRIPT_PATH'))
    mtoa.utils.setEnvironmentVariable(u'MAYA_SCRIPT_PATH', meldir + pathsep + maya_script_path)
    for f in glob.glob(os.path.join(meldir, '*.mel')):
        print>>sys.__stdout__, "Maya %s sourcing MEL override %s" % (maya_version, f)
        print "Maya %s sourcing MEL override %s" % (maya_version, f)
        pm.mel.source(pm.mel.encodeString(f))
        test = pm.mel.whatIs(os.path.split(f)[1]).split(': ', 1)
        if len(test) == 2 and test[1].replace('\\', '/') != f.replace('\\', '/'):
            pm.warning("Overriding failed: Maya is still using %s" % test[1])

def _overridePythonScripts():
    root = mtoaPackageRoot()
    maya_version = versions.shortName()
    path = os.path.join(root, maya_version)
    if not os.path.isdir(path):
        return
    sys.path.insert(0, path)
    # for root, dirnames, filenames in os.walk('path'): 
    for f in os.listdir(path):
        if f.endswith('.py'):
            print>>sys.__stdout__, "Maya %s importing * from Python override %s from %s" % (maya_version, f, path)
            print "Maya %s importing * from Python override %s from %s" % (maya_version, f, path)
            import_string = "from %s import *" % os.path.splitext(f)[0]
            exec import_string
            # module = __import__(os.path.splitext(f)[0])

def _addAEHooks():
    """
    in versions of Maya prior to 2013 there is no way to override built-in AE templates.
    """
    # Realflow uses the AEshapeHooks global variable as a convention for sharing AEshapeTemplate overrides,
    # so we will too, unless a more popular convention is found.
    pm.melGlobals.initVar('string[]', 'AEshapeHooks')
    hooks = list(pm.melGlobals['AEshapeHooks'])
    import mtoa.ui.ae.templates
    procName = utils.pyToMelProc(mtoa.ui.ae.templates.loadArnoldTemplate, [('string', 'nodeName')], useName=True)
    hooks.append(procName)
    pm.melGlobals['AEshapeHooks'] = hooks

# We need to override this two proc to avoid
# errors because of the hardcoded code.
def updateMayaImageFormatControl():
    #pm.mel.source("createMayaSoftwareCommonGlobalsTab.mel")
    currentRenderer = utils.currentRenderer()
    if currentRenderer == 'mentalRay':
        pm.mel.updateMentalRayImageFormatControl()
    elif currentRenderer == 'arnold':
        mtoa.ui.globals.common.updateArnoldImageFormatControl()
    else:
        pm.mel.updateMayaSoftwareImageFormatControl();

    if currentRenderer != 'arnold' and pm.mel.getApplicationVersionAsFloat() >= 2009:
        pm.mel.updateMultiCameraBufferNamingMenu();

def renderSettingsTabLabel_melToUI(smel):

    # The arguments passed inside this procedure should not
    # be localized. This procedure uses the first string
    # argument that is passed with the "-addGlobalsTab"
    # flag in the "renderer" command.

    try:
        result = pm.mel.uiRes({
            'Common'             : "m_unifiedRenderGlobalsWindow.kCommon",
            'Passes'             : "m_unifiedRenderGlobalsWindow.kPassesTab",
            'Maya Software'      : "m_unifiedRenderGlobalsWindow.kMayaSoftware",
            'Maya Hardware'      : "m_unifiedRenderGlobalsWindow.kMayaHardware",
            'Maya Vector'        : "m_unifiedRenderGlobalsWindow.kMayaVector",
            'Features'           : "m_unifiedRenderGlobalsWindow.kFeatures",
            'Quality'            : "m_unifiedRenderGlobalsWindow.kQuality",
            'Indirect Lighting'  : "m_unifiedRenderGlobalsWindow.kIndirectLighting",
            'Options'            : "m_unifiedRenderGlobalsWindow.kOptions"
            }[smel])
    except:
        result = smel
        pm.mel.uiToMelMsg("renderSettingsTabLabel_melToUI", smel, 0)

    return result

def addOneTabToGlobalsWindow(renderer, tabLabel, createProc):
    # Check to see if the unified render globals window existed.
    # If it does not exist, then we don't need to add any tab yet.
    if not pm.window('unifiedRenderGlobalsWindow', exists=True):
        try:
            pm.error(pm.mel.uiRes("m_unifiedRenderGlobalsWindow.kCannotAddTabs"))
        except:
            pass
        return
    
    displayAllTabs = pm.mel.isDisplayingAllRendererTabs()

    # If the current renderer the renderer is not this
    # renderer, then don't add the tab yet.
    if not displayAllTabs and utils.currentRenderer() != renderer:
        return

    pm.setParent('unifiedRenderGlobalsWindow')

    # Hide the tabForm while updating.
    tabFormManagedStatus = pm.formLayout('tabForm', q=True, manage=True)
    pm.formLayout('tabForm', edit=True, manage=False)
    pm.setParent('tabForm')

    # Set the correct tabLayout parent.
    if displayAllTabs:
        tabLayoutName = pm.mel.getRendererTabLayout(pm.melGlobals['gMasterLayerRendererName'])
    else:
        tabLayoutName = pm.mel.getRendererTabLayout(renderer)

    pm.setParent(tabLayoutName)

    # The tabName is the tabLabel with the white space removed
    # and the word "Tab" added to the end.
    # "masterLayer" will act as the renderer name if the tab
    # is in the master layer.
    tabName = pm.mel.rendererTabName(renderer, tabLabel)

    # if the tab-control does not exist, define it and add it
    # to the tabLayout
    if not pm.layout(tabName, exists=True):
        pm.setUITemplate('renderGlobalsTemplate', pushTemplate=True)
        pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

        # Define the tab
        pm.formLayout(tabName)

        # get the content of the tab from the createTabProc

        # Most create procs are now deferred till the tab is selected
        # These two are the default tabs, so we don't defer them
        createProcs = ['createMayaSoftwareCommonGlobalsTab',
                          'createMayaSoftwareGlobalsTab',
                          'createArnoldRendererCommonGlobalsTab',
                          'createArnoldRendererGlobalsTab',
                          'createArnoldRendererSystemTab',
                          'createArnoldRendererOverrideTab',
                          'createArnoldRendererDiagnosticsTab']

        if createProc in createProcs:
            pm.mel.eval(createProc)

        # These end off the layouts of the information in the Tab
        pm.setParent('..')

        pm.setUITemplate(popTemplate=True)
        pm.setUITemplate(popTemplate=True)

        # Add the tab to the tabLayout
        pm.tabLayout(tabLayoutName,
                       edit=True,
                       tabLabel=(tabName, renderSettingsTabLabel_melToUI(tabLabel)))

    # Restore the old manage status for the tabForm.
    pm.formLayout('tabForm', edit=True, manage=tabFormManagedStatus)

def _register():
    args = {}
    args['renderProcedure'] = utils.pyToMelProc(arnoldRender.arnoldRender,
                                          [('int', 'width'), ('int', 'height'),
                                           ('int', 'doShadows'), ('int', 'doGlowPass'),
                                           ('string', 'camera'), ('string', 'options')])
    args['renderRegionProcedure'] = 'mayaRenderRegion'
    args['commandRenderProcedure']    = utils.pyToMelProc(arnoldRender.arnoldBatchRender,
                                                    [('string', 'option')])
    args['batchRenderProcedure']        = utils.pyToMelProc(arnoldRender.arnoldBatchRender,
                                                    [('string', 'option')])
    args['batchRenderOptionsStringProcedure'] = utils.pyToMelProc(arnoldRender.arnoldBatchRenderOptionsString, returnType='string')
    args['cancelBatchRenderProcedure']  = utils.pyToMelProc(arnoldRender.arnoldBatchStop)
    args['iprRenderProcedure']          = utils.pyToMelProc(arnoldRender.arnoldIprRender,
                                                    [('int', 'width'), ('int', 'height'),
                                                     ('int', 'doShadows'), ('int', 'doGlowPass'),
                                                     ('string', 'camera')])
    args['isRunningIprProcedure']       = utils.pyToMelProc(arnoldRender.arnoldIprIsRunning, returnType='int')
    args['startIprRenderProcedure']     = utils.pyToMelProc(arnoldRender.arnoldIprStart,
                                                    [('string', 'editor'), ('int', 'resolutionX'),
                                                     ('int', 'resolutionY'), ('string', 'camera')])
    args['stopIprRenderProcedure']      = utils.pyToMelProc(arnoldRender.arnoldIprStop)
    args['refreshIprRenderProcedure']   = utils.pyToMelProc(arnoldRender.arnoldIprRefresh)
    args['pauseIprRenderProcedure']     =   utils.pyToMelProc(arnoldRender.arnoldIprPause,
                                                    [('string', 'editor'), ('int', 'pause')])
    args['changeIprRegionProcedure']    = utils.pyToMelProc(arnoldRender.arnoldIprChangeRegion,
                                                    [('string', 'renderPanel')])
    pm.renderer('arnold', rendererUIName='Arnold Renderer', **args)
        
    pm.renderer('arnold', edit=True, addGlobalsTab=('Common',
                                                      utils.pyToMelProc(createArnoldRendererCommonGlobalsTab, useName=True),
                                                      utils.pyToMelProc(updateArnoldRendererCommonGlobalsTab, useName=True)))
    pm.renderer('arnold', edit=True, addGlobalsTab=('Arnold Renderer',
                                                      utils.pyToMelProc(createArnoldRendererGlobalsTab, useName=True),
                                                      utils.pyToMelProc(updateArnoldRendererGlobalsTab, useName=True)))
    pm.renderer('arnold', edit=True, addGlobalsTab=('System', 
                                                      utils.pyToMelProc(createArnoldRendererSystemTab, useName=True), 
                                                      utils.pyToMelProc(updateArnoldRendererSystemTab, useName=True)))
    pm.renderer('arnold', edit=True, addGlobalsTab=('AOVs', 
                                                      utils.pyToMelProc(createArnoldAOVTab, useName=True), 
                                                      utils.pyToMelProc(updateArnoldAOVTab, useName=True)))
    pm.renderer('arnold', edit=True, addGlobalsTab=('Diagnostics', 
                                                      utils.pyToMelProc(createArnoldRendererDiagnosticsTab, useName=True), 
                                                      utils.pyToMelProc(updateArnoldRendererDiagnosticsTab, useName=True)))
    pm.renderer('arnold', edit=True, addGlobalsTab=('Override', 
                                                      utils.pyToMelProc(createArnoldRendererOverrideTab, useName=True), 
                                                      utils.pyToMelProc(updateArnoldRendererOverrideTab, useName=True)))
    pm.renderer('arnold', edit=True, addGlobalsNode='defaultArnoldRenderOptions')
    utils.pyToMelProc(updateBackgroundSettings, useName=True)
    utils.pyToMelProc(updateAtmosphereSettings, useName=True)
    #We have to source this file otherwise maya will override
    #our mel proc overrides below.
    #
    pm.mel.source('createMayaSoftwareCommonGlobalsTab.mel')
    
    utils.pyToMelProc(addOneTabToGlobalsWindow,
                      [('string', 'renderer'), ('string', 'tabLabel'), ('string', 'createProc')],
                      useName=True)
    utils.pyToMelProc(renderSettingsTabLabel_melToUI,
                      [('string', 'mel')],
                      useName=True)
    utils.pyToMelProc(updateMayaImageFormatControl,
                      useName=True)

def registerArnoldRenderer():
    try:
        alreadyRegistered = pm.renderer('arnold', exists=True)
        if not alreadyRegistered:

            pm.evalDeferred(_register)

            # AE Templates
            # the following must occur even in batch mode because they contain calls to registerDefaultTranslator
            pm.evalDeferred(aeUtils.loadAETemplates)
            import rendererCallbacks
            rendererCallbacks.registerCallbacks()
            import mtoa.ui.ae.customShapeAttributes
            import mtoa.ui.ae.customShaderTemplates
            if not pm.about(batch=True):
                # Reload the AE Window if it has already been opened
                pm.evalDeferred(aeUtils.rebuildAE)
                # create the Arnold menu
                createArnoldMenu()

            # version specific overrides or additions
            _overridePythonScripts()
            _overrideMelScripts()

            # Add option box for file translator
            utils.pyToMelProc(exportass.arnoldAssOpts,
                              [('string', 'parent'), ('string', 'action'),
                               ('string', 'initialSettings'), ('string', 'resultCallback')],
                               useName=True)
            
            # callbacks
            import mtoa.core as core
            core.installCallbacks()
            core.MTOA_GLOBALS['COMMAND_PORT'] = None

            import maya.cmds as cmds
            if not pm.about(batch=True):
                commandPortBase = 4700
                try:
                    commandPortBase = int(os.environ['MTOA_COMMAND_PORT'])
                except:
                    commandPortBase = 4700
                # opening a command port for different tools and maya batch progress messages
                for port in range(commandPortBase, commandPortBase + 100):
                    commandPortName = ':%i' % port
                    try:
                        cmds.commandPort(name=commandPortName)
                        core.MTOA_GLOBALS['COMMAND_PORT'] = port
                        break
                    except:
                        pass
            if not pm.about(batch=True):
                pm.evalDeferred(arnoldShelf.createArnoldShelf)
    except:
        import traceback
        traceback.print_exc(file=sys.__stderr__)
        raise

