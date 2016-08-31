import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiAOVTemplate(ShaderAETemplate):

    def defaultValueNew(self, nodeAttr):
        pm.attrNavigationControlGrp('aiAOVDefaultValue',
                                    label='Default Shader',
                                    at=nodeAttr)

    def defaultValueReplace(self, nodeAttr):
        pm.attrNavigationControlGrp('aiAOVDefaultValue', edit=True, at=nodeAttr)

    def outputsNew(self, attr):
        node, plug = attr.split('.', 1)
        attr = pm.Attribute(attr)
        self.frame = pm.mel.AEnewNonNumericMulti(node,
                                                 plug,
                                                 "AOV Outputs",
                                                 "", "AEnewCompound",
                                                 attr.getArrayIndices())

    def outputsReplace(self, attr):
        node, plug = attr.split('.', 1)
        attr = pm.Attribute(attr)
        #pm.setParent(self.frame)
        pm.mel.AEreplaceNonNumericMulti(self.frame,
                                        node,
                                        plug,
                                        "", "AEreplaceCompound",
                                        attr.getArrayIndices())

    def setup(self):
        #mel.eval('AEswatchDisplay "%s"' % nodeName)

        self.beginScrollLayout()
        self.beginLayout("AOV Attributes", collapse=False)

        #self.beginLayout("Primary Controls", collapse=False)
        self.addControl('enabled')
        self.addControl('name')
        self.addControl('type', label='Data Type')
        self.addCustom('defaultValue', self.defaultValueNew, self.defaultValueReplace)

        self.endLayout()

        self.addCustom('outputs', self.outputsNew, self.outputsReplace)

        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        self.addExtraControls()

        self.endScrollLayout()
        
        # attributes left to allow easier upgrading. will be removed
        self.suppress('imageFormat')
        self.suppress('filterType')
        self.suppress('prefix')
