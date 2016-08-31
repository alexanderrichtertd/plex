## NEW COMMS module

import maya.cmds as m
import sfTools.utils as sfu
import sfMayaTools.utils as sfmu

def attach_shaders(verbose=False, shadingNodeType="aiStandard", forceNameSpace=False):
    """ Finds all geometry (polygons and nurbs) under the selected group
    and finds and attaches the appropriate shader based on the shaderType
    tags on the transform node
    """
    sel = m.ls(sl=1)
    if not sel: 
        m.inViewMessage(amg='Please select a GRP!', pos='midCenter', dk=True)
        return
        
    if verbose: print "shadingNodeType:", shadingNodeType

    newShaders = []
    # newShaderSGs = []
    shaderAssignmentList = {}

    print '\nFinding Shaders....\n======================'

    for item in sel:
        # if not item.endswith("_GRP"):
        #     m.inViewMessage(amg='Please select a GRP!', pos='midCenter', dk=True)
        #     return
        geometry = _get_geometry(item)

        for geo in geometry:
            if verbose: print "\n%s" % geo

            # add to new namespace if one provided
            if forceNameSpace:
                namespace = forceNameSpace
            else:
                # get deepest namespace to ensure collection leaf nodes are correctly
                namespace = geo.split("|")[-1].split(":")[-2] if ":" in geo else None

            if verbose: print "namespace: %s" % namespace
            shaderType = m.getAttr("%s.shaderType" % geo) if m.objExists("%s.shaderType" % geo) else None
            if not shaderType: continue

            if verbose: print "shaderType: %s" % shaderType
            shaderName = "%s_SHD" % (shaderType)
            shaderSGName = "%s_SHDSG" % (shaderType)

            # check if shader exists in the same namespace as the geometry
            if namespace and m.objExists("%s:%s" % (namespace,shaderSGName)):
                shaderSG = "%s:%s" % (namespace,shaderSGName)
                if verbose: print "assigning existing namespaced shader %s" % shaderSG

            # check if shader exists in the first numerical iteration of the geometry namespace
            elif namespace and not forceNameSpace and m.objExists("%s:%s" % (_get_first_namespace(namespace),shaderSGName)):
                shaderSG = "%s:%s" % (_get_first_namespace(namespace),shaderSGName)
                if verbose: print "assigning existing first namespaced shader %s" % shaderSG

            # check if shader exists in the equivalent "shader pack" namespace 
            elif namespace and not forceNameSpace and m.objExists("%s:%s" % (_get_shader_namespace(namespace),shaderSGName)):
                shaderSG = "%s:%s" % (_get_shader_namespace(namespace),shaderSGName)
                if verbose: print "assigning shader namespaced shader %s" % shaderSG

            # check if shader exists in the root namespace
            elif m.objExists("%s" % shaderSGName):
                shaderSG = shaderSGName
                if verbose: print "assigning shader %s" % shaderSG

            # else create the shader
            else:
                shader = shaderName

                if namespace:
                    shader = "%s:%s" % (namespace,shader)

                if verbose: print "creating shader %s" % shader
                shader = create_shader(shadingNodeType, shader)
                shaderSG = "%sSG" % shader
                sfmu.addToSet(shader, "%s:shader_SEL" % namespace) if namespace else sfmu.addToSet(shader, "shader_SEL")
                newShaders.append(shader)

            # if shader: shaderSG = "%sSG" % shader
            # if shader: shaderSG = shader

            if not shaderSG in shaderAssignmentList.keys(): shaderAssignmentList[shaderSG] = []
            shaderAssignmentList[shaderSG].append(geo)

    if len(newShaders) > 0:
        print '\nNew Shaders created:\n======================\n\t%s' % sfu.prettyPrint(newShaders, divider = '\n\t')
    print '\nAssigning Shaders.....\n======================'
    for shaderSG in sorted(shaderAssignmentList.keys()):
        print ('\t%s'%shaderSG).ljust(40), 'to:  ', shaderAssignmentList[shaderSG]
        m.sets(shaderAssignmentList[shaderSG], forceElement=shaderSG, edit=1) #ASSIGN SHADER - this way works in batch mode

    m.select(sel,r=1)

def _get_first_namespace(namespace):
    num = namespace.split('_')[-2]
    return namespace.replace(num,"01")

def _get_shader_namespace(namespace):
    num = namespace.split('_')[-2]
    return namespace.replace("_%s_" % num,"_shaders_")

def _get_geometry(item):
    return [m.listRelatives(item, fullPath=1, parent=1)[0] for item in 
                m.listRelatives(item, fullPath=1, children=1, allDescendents=1,
                type=["mesh", "nurbsSurface", "aiStandIn"])
                if len(m.listRelatives(item, parent=1)) > 0]

def create_shader(shadingNodeType, shaderName, meshes=None):
    
    shaderSG = shaderName + 'SG'
    shader = shaderName
    if not m.objExists (shader):
        shader = m.shadingNode (shadingNodeType, n=shaderName, asShader=1, skipSelect=1)
        #m.select(cl=1) # added to remove selection
    if not m.objExists (shaderSG):
        #shaderSG = m.createNode ('shadingEngine', n=shaderSG, skipSelect=True)
        shaderSG = m.sets(renderable=True, noSurfaceShader=True, empty=True, name=shaderSG)
    # tryConnect(shader+'.outColor', shaderSG+'.surfaceShader')
    try:
        connect_shader_to_SG(shader, shaderSG)
    except:pass
    
    if meshes:
        print '\t', 'assigning'.ljust(15), shader.ljust(40), 'to'.ljust(10), meshes
        m.sets(meshes,forceElement=shaderSG, edit=1)
    
    return str(shaderName)

def connect_shader_to_SG(shader, shaderSG):

    if m.nodeType(shader).startswith(('mi_','mia_','miss_')):
        m.connectAttr(shader+'.message', shaderSG+'.miMaterialShader', f=1)
        m.connectAttr(shader+'.message', shaderSG+'.miShadowShader', f=1)
        m.connectAttr(shader+'.message', shaderSG+'.miPhotonShader', f=1)

    elif m.nodeType(shader).startswith(('ai','al')):
        m.connectAttr(shader+'.outColor', shaderSG+'.aiSurfaceShader', f=1)

    else:
        m.connectAttr(shader+'.message', shaderSG+'.surfaceShader', f=1)


def create_shader_holders(shaders=None):
    '''
    Please select shaders for which you want to create shader holders
    Shader Holders will force translation of attached shaders into the Arnold scene
    and override any shaders assigned in the aiStandin
    '''
    if not shaders:shaders = m.ls(sl=1)

    for shader in shaders:
        if not shader.endswith('_SHD'): continue
        print shader
        name = shader.split('_SHD')[0]
        if not m.objExists("%s_HLD"%name):
            holder = m.polyCube(n="%s_HLD"%name, ch=0)
            holderShape = sfmu.getShapeNode(holder)
            m.setAttr("%s.castsShadows"%holderShape, 0)
            m.setAttr("%s.receiveShadows"%holderShape, 0)
            m.setAttr("%s.motionBlur"%holderShape, 0)
            m.setAttr("%s.primaryVisibility"%holderShape, 0)
            m.setAttr("%s.smoothShading"%holderShape, 0)
            m.setAttr("%s.visibleInReflections"%holderShape, 0)
            m.setAttr("%s.visibleInRefractions"%holderShape, 0)
            m.setAttr("%s.doubleSided"%holderShape, 0)
            m.setAttr("%s.aiVisibleInDiffuse"%holderShape, 0)
            m.setAttr("%s.aiVisibleInGlossy"%holderShape, 0)

            # prevents viewport slowdown when switching to textured mode
            m.setAttr("%s.overrideEnabled"%holderShape, 1) 
            m.setAttr("%s.overrideLevelOfDetail"%holderShape, 1)

            m.sets(holder, forceElement=sfmu.getSG(shader), e=1)
            sfmu.addToGroup(holder, "shader_HLD_GRP")

    sfmu.addToGroup("shader_HLD_GRP", "RENDER_GEO_GRP")
