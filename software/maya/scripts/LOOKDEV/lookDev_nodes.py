#*************************************************
# Title         LookDev Node
#
# Content       Adds nodes to create the lookDev scene
#
# Author        alexander.richter1986@gmail.com
#*************************************************


import pymel.core as pm

def addTextureNodesToShader():
    txPath     = ""
    imgNames   = ["diffuseColor_TEX", "specular1Color_TEX", "specular1Roughness_TEX", "bump_TEX", "vdm_TEX"]
    shaderNode = pm.ls(selection=True)
    aiImageList = []

    if not len(shaderNode) or len{shaderNode} > 1 or not str(shaderNode[0]).endswith("_SHD"):
    	print "Select a node!"
    	return
    
    # connect shader and shaderGroup
    
    for name in imgNames:
        aiImageList.append(pm.createNode( 'aiImage', n=name))
        # add tex path to node
        # check "ignore missing tiles" 
    
    # dif & spec
    for i in range(0,2):
        remapHsv = pm.createNode( 'remapHsv')
        pm.connectAttr( aiImageList[i] + '.outColor', remapHsv + '.color' )
        pm.connectAttr( remapHsv + '.outColor', shaderNode + '.' + imgNames[i].split("_")[0] )
    
    #specR
    remapValue = pm.createNode( 'remapValue')
    pm.connectAttr( aiImageList[2] + '.outColorR', remapValue + '.inputValue' )
    pm.connectAttr( remapValue + '.outColorR', shaderNode + '.' + imgNames[2].split("_")[0] )
    
    #bump
    bump2d = pm.createNode( 'bump2d')
    pm.connectAttr( aiImageList[3] + '.outColorR', bump2d + '.bumpValue' )
    pm.connectAttr( bump2d + '.outNormal', shaderNode + '.normalCamera' )
        
    #vdm
    displacementShader = pm.createNode( 'displacementShader')
    pm.connectAttr( aiImageList[4] + '.outColor', displacementShader + '.vectorDisplacement' )
    pm.connectAttr( displacementShader + '.displacement', shaderNode + 'SG.displacementShader') 

addTextureNodesToShader()    
