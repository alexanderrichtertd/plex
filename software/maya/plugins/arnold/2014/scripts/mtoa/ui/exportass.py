import maya.cmds as cmds
import maya.mel as mel
from mtoa.callbacks import *

def pushOptionsUITemplate():
    if (not cmds.uiTemplate('oa_optionsTemplate', exists=True)):
        cmds.uiTemplate('oa_optionsTemplate')

        cmds.frameLayout(defineTemplate='oa_optionsTemplate',
                         collapsable=True, collapse=False,
                         labelVisible=True, borderVisible=False)
        cmds.columnLayout(defineTemplate='oa_optionsTemplate',
                          adjustableColumn=True)
        
        cmds.checkBoxGrp(defineTemplate='oa_optionsTemplate',
                         columnWidth=[2,240], numberOfCheckBoxes=1,
                         label='')
        
        cmds.optionMenuGrp(defineTemplate='oa_optionsTemplate',
                           columnAlign=[1, "right"],
                           columnWidth=[2,160])

    cmds.setUITemplate('oa_optionsTemplate', pushTemplate=True)

def popOptionsUITemplate():
    cmds.setUITemplate(popTemplate=True)

def getMaskValues():
    mask = 0

    if cmds.checkBoxGrp('oa_export_options', q=True, value1=True):
        mask += 1
    if cmds.checkBoxGrp('oa_export_cameras', q=True, value1=True):
        mask += 2
    if cmds.checkBoxGrp('oa_export_lights', q=True, value1=True):
        mask += 4
    if cmds.checkBoxGrp('oa_export_shapes', q=True, value1=True):
        mask += 8
    if cmds.checkBoxGrp('oa_export_shaders', q=True, value1=True):
        mask += 16
    if cmds.checkBoxGrp('oa_export_override', q=True, value1=True):
        mask += 32
    if cmds.checkBoxGrp('oa_export_drivers', q=True, value1=True):
        mask += 64
    if cmds.checkBoxGrp('oa_export_filters', q=True, value1=True):
        mask += 128

    return mask

def setMaskValues(mask):
    cmds.checkBoxGrp('oa_export_filters', edit=True, value1=(mask / 128))
    mask = mask % 128
    cmds.checkBoxGrp('oa_export_drivers', edit=True, value1=(mask / 64))
    mask = mask % 64
    cmds.checkBoxGrp('oa_export_override', edit=True, value1=(mask / 32))
    mask = mask % 32
    cmds.checkBoxGrp('oa_export_shaders', edit=True, value1=(mask / 16))
    mask = mask % 16
    cmds.checkBoxGrp('oa_export_shapes', edit=True, value1=(mask / 8))
    mask = mask % 8
    cmds.checkBoxGrp('oa_export_lights', edit=True, value1=(mask / 4))
    mask = mask % 4
    cmds.checkBoxGrp('oa_export_cameras', edit=True, value1=(mask / 2))
    mask = mask % 2
    cmds.checkBoxGrp('oa_export_options', edit=True, value1=mask)

def SequenceToggleOn(*arg):
   ToggleSequenceLine(True)
   
def SequenceToggleOff(*arg):
   ToggleSequenceLine(False)

def ToggleSequenceLine(flag):
   cmds.text("oa_exportStartLabel",edit=True,enable=flag)
   cmds.floatField("oa_exportStart",edit=True,enable=flag)
   cmds.text("oa_exportEndLabel",edit=True,enable=flag)
   cmds.floatField("oa_exportEnd",edit=True,enable=flag)
   cmds.text("oa_exportStepLabel",edit=True,enable=flag)
   cmds.floatField("oa_exportStep",edit=True,enable=flag)

def LightToggleOn(*arg):
   ToggleLightLinking(True)
   
def LightToggleOff(*arg):
   ToggleLightLinking(False)

def ToggleLightLinking(flag):
   cmds.optionMenuGrp('oa_export_light_links',edit=True,enable=flag)
   cmds.optionMenuGrp('oa_export_shadow_links',edit=True,enable=flag)
   
def parseSettingsString(settingsString):
    settings = {}
    if settingsString :
        # parse settings
        settingsDecs = settingsString.split(";")
        for dec in settingsDecs :
            flag, space, value = dec.partition(' ')
            flag = flag.lstrip('-')
            if value == '' :
                settings[flag] = True
            else :
                try:
                    settings[flag] = int(value)
                except ValueError:
                    try:
                        settings[flag] = float(value)
                    except:
                        settings[flag] = value

    # get default settings from options node
    optionsNode = 'defaultArnoldRenderOptions'
    if cmds.ls(optionsNode):    
        settings.setdefault('compressed', cmds.getAttr('%s.output_ass_compressed' % optionsNode))
        settings.setdefault('boundingBox', cmds.getAttr('%s.outputAssBoundingBox' % optionsNode))
        settings.setdefault('asciiAss', not cmds.getAttr('%s.binaryAss' % optionsNode))
        settings.setdefault('mask', cmds.getAttr('%s.output_ass_mask' % optionsNode))
        settings.setdefault('lightLinks', cmds.getAttr('%s.lightLinking' % optionsNode))
        settings.setdefault('shadowLinks', cmds.getAttr('%s.shadowLinking' % optionsNode))
        settings.setdefault('expandProcedurals', cmds.getAttr('%s.expandProcedurals' % optionsNode))
        settings.setdefault('forceTranslateShadingEngines', cmds.getAttr('%s.forceTranslateShadingEngines' % optionsNode))
        
    return settings

def buildSettingsString(settings):
    def flagSyntaxItems(items):
        for key, value in items :
            if value is True:
                yield '-%s' % key
            elif value is not False:
                yield '-%s %r' % (key, value)
        
    settingsString = ';'.join(flagSyntaxItems(settings.items()))
    return settingsString 

def arnoldAssOpts(parent = '', action = '', initialSettings = '', resultCallback = ''):
    
    # print 'parent: %(p)s, action: %(a)s, initialSettings: %(s)s, resultCallback: %(c)s\n' % \
    #  {"p": parent, "a": action, "s": initialSettings, "c": resultCallback}

    retval = 0
    currentOptions = ''
        
    if action == 'post':
        settings = parseSettingsString(initialSettings)
        
        cmds.setParent(parent)

        pushOptionsUITemplate()
        
        cmds.columnLayout()
        cmds.checkBoxGrp('oa_compressed',
                         label1='Use gzip Compression (.ass.gz)',
                         value1=settings.get('compressed', False))
        cmds.checkBoxGrp('oa_write_bbox',
                         label1='Export Bounding Box',
                         value1=settings.get('boundingBox', False))
        cmds.checkBoxGrp('oa_binary_ass',
                         label1='Use Binary Encoding',
                         value1=not settings.get('asciiAss', False))

        cmds.setParent('..')
        cmds.separator(style='none')
        cmds.frameLayout(label='Export', collapsable=True)
        cmds.columnLayout()
        
        cmds.checkBoxGrp('oa_export_options', label1='Options', value1=True)
        cmds.checkBoxGrp('oa_export_cameras', label1='Cameras', value1=True)
        cmds.checkBoxGrp('oa_export_lights', label1='Lights', value1=True,
                         onCommand1=LightToggleOn,
                         offCommand1=LightToggleOff)
        cmds.checkBoxGrp('oa_export_shapes', label1='Shapes', value1=True)
        cmds.checkBoxGrp('oa_export_shaders', label1='Shaders', value1=True)
        cmds.checkBoxGrp('oa_export_override', label1='Override Nodes', value1=True)
        cmds.checkBoxGrp('oa_export_drivers', label1='Drivers', value1=True)
        cmds.checkBoxGrp('oa_export_filters', label1='Filters', value1=True)
        setMaskValues(settings.get('mask', 255))
        
        cmds.text("oa_exportSeparator",label="")        
        cmds.checkBoxGrp('oa_expandProcedurals',
                         label1='Expand Procedurals',
                         value1=settings.get('expandProcedurals', False))
        cmds.checkBoxGrp('oa_forceTranslateShadingEngines',
                         label1='Force Translate Shading Engines',
                         value1=settings.get('forceTranslateShadingEngines', False))
        cmds.text("oa_exportSeparatorOther",label="")
        lightsOn = cmds.checkBoxGrp('oa_export_lights', query=True, value1=True)
        
        cmds.optionMenuGrp('oa_export_light_links', label='Light Linking')
        entries = cmds.attributeQuery('lightLinking', typ='aiOptions', listEnum=True)[0].split(':')
        for entry in entries :
            cmds.menuItem(label=entry)
        cmds.optionMenuGrp('oa_export_light_links', edit=True, select=1+settings.get('lightLinks', 0))
        cmds.optionMenuGrp('oa_export_light_links', edit=True, enable=lightsOn)
        
        cmds.optionMenuGrp('oa_export_shadow_links', label='Shadow Linking')
        entries = cmds.attributeQuery('shadowLinking', typ='aiOptions', listEnum=True)[0].split(':')
        for entry in entries :
            cmds.menuItem(label=entry)
        cmds.optionMenuGrp('oa_export_shadow_links', edit=True, select=1+settings.get('shadowLinks', 0)) 
        cmds.optionMenuGrp('oa_export_shadow_links', edit=True, enable=lightsOn)
        
        cmds.setParent('..')      
        cmds.setParent('..')
        cmds.separator(style='none')    
        cmds.frameLayout(label='Sequence', collapsable=True)
        cmds.columnLayout()
        
        if settings.get('startFrame', None) is not None and settings.get('endFrame', None) is not None:
            sequence = True;
        else:
            sequence = False;
        cmds.checkBoxGrp("oa_exportSequence",
                         label1="Sequence",
                         onCommand1=SequenceToggleOn,
                         offCommand1=SequenceToggleOff,
                         value1=sequence)

        cmds.setParent( '..' ) 
        cmds.rowColumnLayout(numberOfColumns=6,
                             columnAttach=[(1, "left", 140), (2, "both", 0), (3, "both", 0),
                                           (4, "both", 0), (5, "both", 0), (6, "right", 0)])
        cmds.text("oa_exportStartLabel",label="Start ")
        cmds.floatField("oa_exportStart")
        start = cmds.playbackOptions(query=True, animationStartTime=True)
        cmds.floatField("oa_exportStart", edit=True,
                        value=settings.get('startFrame', start), enable=sequence)
        cmds.text("oa_exportEndLabel",label="End   ")
        cmds.floatField("oa_exportEnd")
        end = cmds.playbackOptions(query=True, animationEndTime=True)
        cmds.floatField("oa_exportEnd", edit=True,
                        value=settings.get('endFrame', end), enable=sequence)
        cmds.text("oa_exportStepLabel",label="Step  ")
        cmds.floatField("oa_exportStep")
        step = cmds.playbackOptions(query=True, by=True)
        cmds.floatField("oa_exportStep", edit=True,
                        value=settings.get('frameStep', step), enable=sequence)

        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        popOptionsUITemplate()
        
        retval = 1

    elif action == 'query':
        settings = {}
        
        # output ass format
        settings['compressed'] = cmds.checkBoxGrp('oa_compressed', query=True, value1=True)
        settings['boundingBox'] = cmds.checkBoxGrp('oa_write_bbox', query=True, value1=True)
        settings['asciiAss'] = not cmds.checkBoxGrp('oa_binary_ass', query=True, value1=True)      
        
        # export mask and options
        settings['mask'] = getMaskValues()
        
        if (cmds.optionMenuGrp('oa_export_light_links', query=True, enable=True)):
            settings['lightLinks'] = cmds.optionMenuGrp('oa_export_light_links', query=True, select=True) - 1
        else:
            settings['lightLinks'] = 0
        if (cmds.optionMenuGrp('oa_export_shadow_links', query=True, enable=True)):    
            settings['shadowLinks'] = cmds.optionMenuGrp('oa_export_shadow_links', query=True, select=True) - 1
        else:
            settings['shadowLinks'] = 0
                    
        # sequence
        sequence = cmds.checkBoxGrp("oa_exportSequence", query=True, value1=True)
        if sequence :
            settings['startFrame'] = cmds.floatField("oa_exportStart", query=True, value=True)
            settings['endFrame']   = cmds.floatField("oa_exportEnd", query=True, value=True)
            settings['frameStep']  = cmds.floatField("oa_exportStep", query=True, value=True)        
         
        settings['expandProcedurals'] = cmds.checkBoxGrp('oa_expandProcedurals', query=True, value1=True)
        settings['forceTranslateShadingEngines'] = cmds.checkBoxGrp('oa_forceTranslateShadingEngines', query=True, value1=True)
        
        currentOptions = buildSettingsString(settings)
        # print 'callback: %(c)s, options: %(o)s\n' % {"c": resultCallback, "o": currentOptions}
        mel.eval(resultCallback+'("'+currentOptions+'")')
        retval = 1
    else:
        retval = 0

    return retval




