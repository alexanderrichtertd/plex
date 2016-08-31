import maya.cmds as cmds
import maya.mel as mel
import mtoa.core as core
import platform, os

def arnoldRender(width, height, doShadows, doGlowPass, camera, options):
    # Make sure the aiOptions node exists
    core.createOptions()
    cmds.arnoldRender(cam=camera, w=width, h=height) 
    
def arnoldBatchRenderOptionsString():    
    origFileName = cmds.file(q=True, sn=True)
    
    if not cmds.about(batch=True):
        silentMode = 0
        try:
            silentMode = int(os.environ['MTOA_SILENT_MODE'])
        except:
            pass
        if silentMode != 1:
            dialogMessage = 'Are you sure you want to start a potentially long task?'
            if platform.system().lower() == 'linux':
                dialogMessage += ' (batch render on linux cannot be stopped)'
            ret = cmds.confirmDialog(title='Confirm', message=dialogMessage,
                                        button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
            if ret != 'Yes':
                raise Exception('Stopping batch render.')
    try:
        port = core.MTOA_GLOBALS['COMMAND_PORT']
        return ' -r arnold -ai:ofn \\"' + origFileName + '\\" -ai:port %i ' % port
    except:
        return ' -r arnold -ai:ofn \\"' + origFileName + '\\" '

def arnoldBatchRender(option):
    # Make sure the aiOptions node exists
    core.createOptions()
    # Parse option string
    kwargs = {}
    options = option.split(" ")
    i, n = 0, len(options)
    if cmds.objExists('defaultResolution.mtoaCommandPort'):
        kwargs['port'] = cmds.getAttr('defaultResolution.mtoaCommandPort')
    if cmds.objExists('defaultArnoldRenderOptions.mtoaOrigFileName'):
        kwargs['ofn'] = cmds.getAttr('defaultArnoldRenderOptions.mtoaOrigFileName')
    while i < n:
        if options[i] in ["-w", "-width"]:
            i += 1
            if i >= n:
                break
            kwargs["width"] = int(options[i])

        elif options[i] in ["-h", "-height"]:
            i += 1
            if i >= n:
                break
            kwargs["height"] = int(options[i])

        elif options[i] in ["-cam", "-camera"]:
            i += 1
            if i >= n:
                break
            kwargs["camera"] = options[i]
        i += 1
    try:
        cmds.arnoldRender(batch=True, **kwargs)
    except RuntimeError, err:
        print err
        
def arnoldBatchStop():
    import pymel.core as pm
    pm.mel.eval('batchRender')

def arnoldIprStart(editor, resolutionX, resolutionY, camera):
    # Make sure the aiOptions node exists
    core.createOptions()
    cmds.arnoldIpr(cam=camera, w=resolutionX, h=resolutionY, mode='start')

def arnoldIprStop():
    cmds.arnoldIpr(mode='stop')

def arnoldIprIsRunning():
    return cmds.arnoldIpr()

def arnoldIprRender(width, height, doShadows, doGlowPass, camera):
    cmds.arnoldIpr(cam=camera, w=width, h=height, mode=render)

def arnoldIprRefresh():
    cmds.arnoldIpr(mode='refresh')

def arnoldIprPause(editor, pause):
    if pause:
        cmds.arnoldIpr(mode='pause')
    else:
        cmds.arnoldIpr(mode='unpause')

def arnoldIprChangeRegion(renderPanel):
    cmds.arnoldIpr(mode='region')
