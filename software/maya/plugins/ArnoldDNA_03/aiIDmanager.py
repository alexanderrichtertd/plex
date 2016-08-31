# 256 create objet and shader based IDs
# For OBJECT IDS: select objects, push "create Object ID button"
# For SHADER IDS: select shading groups and push "create shader ID button".
# If ino SG selected IDs will be created for all shading groups.
# creation shader ID require clean scene without existing AOVs, othervise it may work wrong.
# Put script to \Documents\maya\201X-x64\scripts 
# In Python tab of Maya script editor execute code:
# import aiIDmanager
# aiIDmanager.windowID()


import pymel.core as pm
import mtoa.aovs as aovs
import sys

#define RGB colors
R = ( 1, 0, 0 )
G = ( 0, 1, 0 )
B = ( 0, 0, 1 )
def checkArnold(*args):
    #check if current render is Arnold
    if( pm.getAttr( 'defaultRenderGlobals.currentRenderer' ) != 'arnold' ):
       pm.confirmDialog( t="Warning", message= "Set current render to Arnold!", icon='critical' )
       sys.exit( "Please use Arnold render!" )


def checkObjID(*args):#check existing ids to create proper nubers for next ids
    if pm.objExists('aiAOV_objectID_*'): 
        pm.select('aiAOV_objectID_*')
        exist = pm.ls(sl = True)[-1]
        exist = float(exist.split('_')[2]) +1
        pm.select (d = True)
    else: 
        exist = 0
    return exist

def checkShdrID(*args):#check existing ids to create proper nubers for next ids
    if pm.objExists('aiAOV_shaderID_*'): 
        pm.select('aiAOV_shaderID_*')
               
        exist = pm.ls(sl = True)[-1]
        exist = float(exist.split('_')[2]) + 1 
        
    else:
        if pm.objExists('aiAOV_*'): 
            pm.select('aiAOV_*')
            exist = pm.ls(sl = 1)
            exist = len(exist)
            
        else:
            exist = 0
    return exist


def iterBy( iterable, count ):#Hamish McKenzie procedure to process list in blocks of N elrmrnts
 	cur = 0
 	i = iter( iterable )
 	while True:
 		try:
 			toYield = []
 			for n in range( count ): toYield.append( i.next() )
 			yield toYield
 		except StopIteration:
 			if toYield: yield toYield
 			break
 			
def addObjAOV( index ): # Creates AOV render pass for object ID
    aovName = 'objectID_' + str(index)
    aovs.AOVInterface().addAOV( aovName )
    return aovName
    
def addShdrAOV(index): # Creates AOV render pass
    aovName = 'shaderID_' + str(index)
    aovs.AOVInterface().addAOV( aovName )
    return aovName
    
def createShaderR(index): # create RGB shaders  
    shdrIDMatR = pm.shadingNode('aiUtility', asShader=True, name = 'id_R_' + str(index))
    shdrIDMatR.shadeMode.set(2)
    shdrIDMatR.color.set(R)
def createShaderG(index):   
    shdrIDMatR = pm.shadingNode('aiUtility', asShader=True, name = 'id_G_' + str(index))
    shdrIDMatR.shadeMode.set(2)
    shdrIDMatR.color.set(G)
def createShaderB(index):   
    shdrIDMatR = pm.shadingNode('aiUtility', asShader=True, name = 'id_B_' + str(index))
    shdrIDMatR.shadeMode.set(2)
    shdrIDMatR.color.set(B)

def deleteObjAOV(*args):# delete object AOVs and aiUserDataColor shaders
    pm.delete('aiAOV_objectID_*')
    pm.delete('catchMask_*')
def deleteShdrAOV(*args):# delete shader AOVs and shaders
    pm.delete('aiAOV_objectID_*')
    pm.delete('id_R_*')
    pm.delete('id_G_*')
    pm.delete('id_B_*')
    
def addColor(index): #create color attribute
    colorAttrName = 'maskOBJ_' +  str(index)
    colorAttrNameLong = 'mtoa_constant_' + str(colorAttrName)
    pm.addAttr( longName= colorAttrNameLong , niceName = colorAttrName , usedAsColor=True, attributeType='float3' )
    pm.addAttr( longName='R' +  str(colorAttrName), attributeType='float', parent=colorAttrNameLong )
    pm.addAttr( longName='G' +  str(colorAttrName), attributeType='float', parent=colorAttrNameLong )
    pm.addAttr( longName='B' +  str(colorAttrName), attributeType='float', parent=colorAttrNameLong )
    return colorAttrNameLong

def setupObjID(index):
    # create AOV and plug aiUserDatacolor
    mskObjectMat = pm.shadingNode('aiUserDataColor', asShader=True, name = 'catchMask_' + str('%02d' % index) )
    mskObjectMat.colorAttrName.set('maskOBJ_' + str('%02d' % index))
    objectID  = addObjAOV ('%02d' % index)
    objectIDFull = 'aiAOV_' + str(objectID)
    ID = pm.PyNode(objectIDFull)
    mskObjectMat.outColor >> ID.defaultValue    

def createObjID(*agrs):
    checkArnold()
       
    sel = pm.ls(sl = 1) #select jbject for object IDs
    
    index = checkObjID()
    for i in iterBy(sel,3):
        #Create AOV and mask color to RED
        setupObjID(index)
        pm.select(i[0]) 
        pm.runtime.SelectHierarchy()
        selShapes = pm.ls(sl = 1, shapes = True)
        pm.select(selShapes)
        msk = addColor('%02d' %index)
        
        for e in selShapes: #set mask color to R
            attr = str(e) + '.mtoa_constant_maskOBJ_' + str('%02d' % index)
            pm.setAttr(attr, R)
        
        pm.select(i[1])  
        pm.runtime.SelectHierarchy()
        selShapes = pm.ls(sl = 1, shapes = True)
        pm.select(selShapes)
        msk = addColor('%02d' %index)
        
        for e in selShapes: #set mask color to G
            attr = str(e) + '.mtoa_constant_maskOBJ_' + str('%02d' % index)
            pm.setAttr(attr, G)   
            
        pm.select(i[2])  
        pm.runtime.SelectHierarchy()
        selShapes = pm.ls(sl = 1, shapes = True)
        pm.select(selShapes)
        msk = addColor('%02d' %index)
        
        for e in selShapes: #set mask color to B
            attr = str(e) + '.mtoa_constant_maskOBJ_' + str('%02d' % index)
            pm.setAttr(attr, B)    
        
        index += 1

def createShdrID(*agrs):
    checkArnold()
    # check if any Shading Group selected or not
    shdrs = pm.ls(sl = 1, type='shadingEngine')
    if shdrs:
        print 'Shading groups selected manualy'
    else:
        confirm = pm.confirmDialog ( title='WARNING', message='No shading group selected, create IDs for all shades in scene?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirm == 'Yes':
            shdrs = pm.ls(type='shadingEngine')
            shdrs.remove('initialParticleSE')
            shdrs.remove('initialShadingGroup')
        else:
            sys.exit()
    
        
        
    index = checkShdrID()    
    for i in iterBy(shdrs,3):
        addShdrAOV('%02d' %index) #create AOV
        
        #create and plug R
        createShaderR('%02d' %index)
        shader = 'id_R_%02d' %index
        SHD = pm.PyNode(shader)
        SHD.outColor >> i[0].aiCustomAOVs[index].aovInput;
        #create and plug G
        if i[1]:
            createShaderG('%02d' %index)
            shader = 'id_G_%02d' %index
            SHD = pm.PyNode(shader)
            SHD.outColor >> i[1].aiCustomAOVs[index].aovInput;
        
        #create and plug B
        if i[2]:
            createShaderB('%02d' %index)
            shader = 'id_B_%02d' %index
            SHD = pm.PyNode(shader)
            SHD.outColor >> i[2].aiCustomAOVs[index].aovInput;    
        
        index +=1    

def windowID(*args):
    
    if pm.window('manager', q = 1, ex = 1):
        pm.deleteUI('manager')
    win = pm.window('manager', t= 'ID manager', rtf=True, w = 300, h = 100, s = 0)
    with win:
        mainLayout = pm.columnLayout()
        with mainLayout:
            createOBJ = pm.button(l = 'Create OBJECT IDs', w = 300, h = 50)
            createSHD = pm.button(l = 'Create SHADER IDs', w = 300, h = 50)
    createOBJ.setCommand(createObjID)
    createSHD.setCommand(createShdrID)
    win.show()



