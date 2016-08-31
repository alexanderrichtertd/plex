import pymel.core as pm
import maya.cmds as cmds
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate
import arnold as ai

def aiUtilityCreateColorMode(attr):
    cmds.setUITemplate('attributeEditorPresetsTemplate', pushTemplate=True)
    cmds.attrEnumOptionMenuGrp('AIUtilityColorMode', attribute=attr, label="Color Mode", 
                               enumeratedItem=[(0, 'Color'), (3, 'Normal'), (1, 'Geometric Normal'), (2, 'Un-bumped Normal'), (22, 'Bump Difference'),
                                                (4, 'Barycentric Coords'), (5, 'UV Coords'), (6, 'U Coords'), (7, 'V Coords'),
                                                (8, 'U Surface Derivative (dPdu)'), (9, 'V Surface Derivative (dPdv)'),
                                                (10, 'Shading Point (Relative to BBox)'), (11, 'Primitive ID'), (12, 'Uniform ID'),
                                                (13, 'Triangle Wireframe'), (14, 'Polygon Wireframe'), (15, 'Object'),
                                                (16, 'Edge Length'), (17, 'Floatgrid'), (18, 'Reflection Lines'),
                                                (19, 'Bad UVs'), (20, 'Number of Lights'), (21, 'Object ID')])    
    cmds.setUITemplate(popTemplate=True)

def aiUtilitySetColorMode(attr):
    cmds.attrEnumOptionMenuGrp('AIUtilityColorMode', edit=True, attribute=attr)

class AEaiUtilityTemplate(ShaderAETemplate):
    def checkShadeMode(self, nodeName):
        fullAttr = '%s.%s' % (nodeName, 'shade_mode')
        shadeModeValue = pm.getAttr(fullAttr)
        if shadeModeValue == 3:
            pm.editorTemplate(dimControl=(nodeName, 'aoDistance', False))
        else:
            pm.editorTemplate(dimControl=(nodeName, 'aoDistance', True))

    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.beginLayout('Utility Attributes', collapse=False)
        self.addControl('shade_mode', changeCommand=self.checkShadeMode, label='Shade Mode')
        self.addCustom('color_mode', aiUtilityCreateColorMode, aiUtilitySetColorMode)
        if int(ai.AiGetVersion()[2]) > 2:
            self.addControl('overlay_mode', label='Overlay Mode')
        self.addControl('color', label='Color')
        self.addControl('opacity', label='Opacity')
        self.addControl('ao_distance', label='AO Distance')
        self.endLayout()

        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        self.addExtraControls()
        
        self.endScrollLayout()        

