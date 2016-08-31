import pymel.core as pm
import mtoa.aovs as aovs
import mtoa.ui.ae.templates as templates
import mtoa.ui.ae.shaderTemplate as shaderTemplate
import mtoa.ui.aoveditor as aoveditor
from collections import defaultdict

class DisplacementShaderTemplate(templates.AttributeTemplate):
    def setup(self):
        self.addControl('aiDisplacementPadding', label='Bounds Padding')
        self.addControl('aiDisplacementZeroValue', label='Scalar Zero Value')
        self.addControl('aiDisplacementAutoBump', label='Auto Bump')

templates.registerAETemplate(DisplacementShaderTemplate, 'displacementShader')

class FileTemplate(templates.AttributeTemplate):
    def setup(self):
        self.addControl('aiFilter', label='Filter Type')
        self.addControl('aiMipBias', label='Mip-map Bias')
        self.addControl('aiUseDefaultColor', label='Use Default Color')

templates.registerAETemplate(FileTemplate, 'file')
        
class Bump2dTemplate(templates.AttributeTemplate):
    def setup(self):
        self.addControl('aiFlipR', label='Flip R Channel')
        self.addControl('aiFlipG', label='Flip G Channel')
        self.addControl('aiSwapTangents', label='Swap Tangents')
        self.addControl('aiUseDerivatives', label='Use Derivatives')
        self.addControl('aiGammaCorrect', label='Gamma Correct')

templates.registerAETemplate(Bump2dTemplate, 'bump2d')

class ProjectionTemplate(templates.AttributeTemplate):
    def setup(self):
        self.addControl('aiUseReferenceObject', label='Use Texture Reference Object')
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")

templates.registerAETemplate(ProjectionTemplate, 'projection')
