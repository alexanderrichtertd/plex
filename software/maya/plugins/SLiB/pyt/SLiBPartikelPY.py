#########################################################################
#
#  SLiB | Partikel v.01 by DGDM
#
#########################################################################
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaFX as omfx

def partikel():
    try:
        if cmds.window('PartikelUI', query = True, exists = True):
            cmds.deleteUI('PartikelUI')
    except:
        pass
        
    cmds.window('PartikelUI', tlb=0, w=450, h=450, sizeable=1, t="SLiB | Partikel")
    cmds.columnLayout("main", adj=1, p='PartikelUI' )
    cmds.button('start', label='Create Emitter', h=40, bgc=[0,0.75,0.99], c=lambda *args: (createParticles(),setAttributes(), setRateTime()), p='main')
    cmds.separator(style='none', h=10, p='main' )
    cmds.rowLayout('ratetime', nc=5, adj=5, bgc=[0.21,0.21,0.21], p='main')
    cmds.text('Emission Rate:', w=100, p="ratetime")
    cmds.intField('rate1', w=50, h=20, value=5, minValue=1, changeCommand=lambda *args: setRateTime(), p="ratetime")
    cmds.text('Emission Stop:', w=100,  h=20, p="ratetime")
    cmds.intField('stop1', w=50, h=20, value=50, minValue=1, changeCommand=lambda *args: setRateTime(), p="ratetime")
    cmds.button('set', l='Set Keyframe',en=0, bgc=[0.31,0.31,0.31], h=20, c=lambda *args: setRateTime(), p='ratetime')
    cmds.separator(style='none', h=10, p='main')
    
    cmds.frameLayout("emmitter1", w=300, cll=1, l="Primary Emitter Settings (Main)", cl=1, p='main')
    cmds.rowLayout('coll1', nc=3, adj=3, bgc=[0.21,0.21,0.21], p='emmitter1')
    cmds.checkBox('collision1', label='Collision:', w=100, v=1, cc=lambda *args: setAttributes(), p='coll1')
    cmds.checkBox('selfcollision1', label='Self Collision:', w=100, v=1,  cc=lambda *args: setAttributes(), p='coll1')
    cmds.separator(style='none', h=10, p='main' )
    
    cmds.floatSliderGrp('size1', fieldMinValue=0, label="Particle Radius : ", h=20, cw3=(100, 60, 110), value=0.2, minValue=0, maxValue=5, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('bounce1', fieldMinValue=0, label="Bounce : ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('friction1', fieldMinValue=0, label="Friction : ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('stick1', fieldMinValue=0, label="Stickiness : ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('minDistance1', fieldMinValue=0, label="Min Distance : ", h=20, cw3=(100, 60, 110), value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('maxDistance1', fieldMinValue=0, label="Max Distance : ", h=20, cw3=(100, 60, 110), value=1, minValue=0, fieldMaxValue=10, maxValue=10, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('speed1', fieldMinValue=0, label="Speed : ", h=20, cw3=(100, 60, 110), value=1, fieldMaxValue=20, maxValue=20, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('speedR1', fieldMinValue=0, label="Speed Rand: ", h=20, cw3=(100, 60, 110), value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('drag1', fieldMinValue=0, label="Drag: ", h=20, cw3=(100, 60, 110), fieldMaxValue=0.5, maxValue=0.5, value=0.01, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")
    cmds.floatSliderGrp('mass1', fieldMinValue=0, label="Mass: ", h=20, cw3=(100, 60, 110), fieldMaxValue=10, maxValue=10, value=1, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter1")

    cmds.frameLayout("emmitter2", w=300, cll=1, l="Secondary Emitter Settings (Trail)", cl=1, p='main')
    cmds.rowLayout('coll2', nc=3, adj=3, bgc=[0.21,0.21,0.21], p='emmitter2')
    cmds.checkBox('collision2', label='Collision:', w=100, v=1, cc=lambda *args: setAttributes(), p='coll2')
    cmds.checkBox('selfcollision2', label='Self Collision:', w=100, v=0,  cc=lambda *args: setAttributes(), p='coll2')
    
    cmds.floatSliderGrp('size2', fieldMinValue=0, label="Particle Radius : ", h=20, cw3=(100, 60, 110), value=0.2, minValue=0, maxValue=5, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('rate2', fieldMinValue=0, label="Emission Rate : ", h=20, cw3=(100, 60, 110), value=15, minValue=1, sliderStep=1, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('bounce2', fieldMinValue=0, label="Bounce : ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('friction2', fieldMinValue=0, label="Friction : ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('stick2', fieldMinValue=0, label="Stickiness : ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0.02, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('minDistance2', fieldMinValue=0, label="Min Distance : ", h=20, cw3=(100, 60, 110), value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('maxDistance2', fieldMinValue=0, label="Max Distance : ", h=20, cw3=(100, 60, 110), fieldMaxValue=0.1, maxValue=0.1, value=0.001, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('speed2', fieldMinValue=0, label="Speed : ", h=20, cw3=(100, 60, 110), value=0, fieldMaxValue=20, maxValue=20, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('speedR2', fieldMinValue=0, label="Speed Rand: ", h=20, cw3=(100, 60, 110), value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('conserve2', fieldMinValue=0, label="Conserve: ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=1, minValue=0.9, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('drag2', fieldMinValue=0, label="Drag: ", h=20, cw3=(100, 60, 110), fieldMaxValue=2, maxValue=2, value=0.5, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('damp2', fieldMinValue=0, label="Damp: ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.floatSliderGrp('mass2', fieldMinValue=0, label="Mass: ", h=20, cw3=(100, 60, 110), fieldMaxValue=10, maxValue=10, value=1, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="emmitter2")
    cmds.button('editPC_ramp', l='Edit Particle Color Ramp',h=20, c=lambda *args: mel.eval('editRampAttribute secondaryParticlesShape.color;'), p='emmitter2')
    cmds.separator(style='none', h=10, p='main' )
    
    cmds.frameLayout("global", w=300, cll=1, l="Global Settings", cl=1, bgc=[0.31,0.31,0.31], p='main')
    cmds.floatSliderGrp('gravity', fieldMinValue=0, label="Gravity: ", h=20, cw3=(100, 60, 110), fieldMaxValue=100, maxValue=100, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="global")
    cmds.floatSliderGrp('timescale', fieldMinValue=0, label="Time Scale: ", h=20, cw3=(100, 60, 110), fieldMaxValue=10, maxValue=10, value=1, minValue=0.010, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="global")
    cmds.floatSliderGrp('spacescale', fieldMinValue=0, label="Space Scale: ", h=20, cw3=(100, 60, 110), fieldMaxValue=10, maxValue=10, value=1, minValue=0.010, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="global")
 
    cmds.frameLayout("turbulence", w=300, cll=1, l="Turbulence Field", cl=0, bgc=[0.31,0.31,0.31], p='global')
    cmds.floatSliderGrp('mag', fieldMinValue=0, label="Magnitude: ", h=20, cw3=(100, 60, 110), fieldMaxValue=100, maxValue=100, value=0, minValue=-100, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="turbulence")
    cmds.floatSliderGrp('atten', fieldMinValue=0, label="Attenuation: ", h=20, cw3=(100, 60, 110), fieldMaxValue=2, maxValue=2, value=1, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="turbulence")
    cmds.floatSliderGrp('frequ', fieldMinValue=0, label="Frequency: ", h=20, cw3=(100, 60, 110), fieldMaxValue=100, maxValue=100, value=1, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="turbulence")
    cmds.floatSliderGrp('noiselevel', fieldMinValue=0, label="Noise Level: ", h=20, cw3=(100, 60, 110), fieldMaxValue=8, maxValue=8, value=0, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="turbulence")
    cmds.floatSliderGrp('noiseratio', fieldMinValue=0, label="Noise Ratio: ", h=20, cw3=(100, 60, 110), fieldMaxValue=1, maxValue=1, value=0.5, minValue=0, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setAttributes(), p="turbulence")
    cmds.separator(style='none', h=10, p='main' )
    
    cmds.frameLayout("trailToCurveSettings", w=300, cll=1, l="Convert Particle To Curve", cl=1, bgc=[0.31,0.31,0.31], p='main')
    cmds.rowLayout('trailToCurve', nc=5, adj=5, bgc=[0.21,0.21,0.21], p='trailToCurveSettings')
    cmds.text('Curve Start:', w=100, p="trailToCurve")
    cmds.intField('startFrame',  w=50, h=20, value=1, p='trailToCurve')
    cmds.text('Curve Stop:', w=100,  h=20, p="trailToCurve")
    cmds.intField('endFrame',  w=50, h=20, value=250, p='trailToCurve')
    cmds.button('trailToCurveButton', en=0, align="center", command=lambda x: trailToCurve(), bgc=[0,0.75,0.99], label="Particles to Curves", p='trailToCurve')
    cmds.popupMenu('pop1', p="trailToCurveButton", ctl=False, button=3)
    cmds.menuItem('deletecurve', l='Delete Curves', command=lambda *args: (cmds.delete('ParticleCurves_grp'), cmds.delete('CurveShader')))
    
    cmds.floatSliderGrp('sampledensity', fieldMinValue=0, label="Sample Density: ", h=20, cw3=(100, 60, 110), fieldMaxValue=0.5, maxValue=.5, value=0.1, minValue=0.01, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setCurve(), p="trailToCurveSettings")
    cmds.floatSliderGrp('curvewidth', fieldMinValue=0, label="Curve Width: ", h=20, cw3=(100, 60, 110), fieldMaxValue=0.5, maxValue=0.5, value=0.025, minValue=0.01, sliderStep=0.001, field=True, w=300, changeCommand=lambda *args: setCurve(), p="trailToCurveSettings")
    cmds.rowLayout('curvecheckboxes', nc=3, adj=1, bgc=[0.21,0.21,0.21], p='trailToCurveSettings' )
    cmds.checkBox('curvevisibility', label='Curve Visible:', v=0, changeCommand=lambda *args: setCurve(), p='curvecheckboxes')
    cmds.checkBox('curve1', label='Make renderable:', v=1, p='curvecheckboxes')
    cmds.separator(style='none', h=10, p='main' )
    
    cmds.frameLayout("trailToMeshSettings", w=300, cll=1, l="Convert Particle To Mesh", cl=1, bgc=[0.31,0.31,0.31], p='main')
    cmds.rowLayout('trailToMesh', nc=5, adj=5, bgc=[0.21,0.21,0.21], p='trailToMeshSettings')
    cmds.text('Treshold:', w=100, p="trailToMesh")
    cmds.floatField('treshold',  w=50, h=20, value=0.01, changeCommand=lambda *args: setAttributes(), p='trailToMesh')
    cmds.text('Radius:', w=100,  h=20, p="trailToMesh")
    cmds.floatField('radius',  w=50, h=20, changeCommand=lambda *args: setAttributes(), value=1, p='trailToMesh')
    cmds.button('trailToMeshButton', en=0 ,align="center", command=lambda x: trailToMesh(), bgc=[0,0.75,0.99], label="Particles to Mesh", p='trailToMesh')
    cmds.popupMenu('pop2', p="trailToMeshButton", ctl=False, button=3)
    cmds.menuItem('deletemesh', l='Delete Mesh', command=lambda *args: (cmds.delete('partikelMesh'),cmds.delete('MeshShader'), cmds.setAttr("secondaryParticlesShape.intermediateObject", 0)))
    cmds.separator(style='none', h=10, p='main' )
    
    cmds.frameLayout("fluidframe", w=300, cll=1, l="Emitt into Fluid", cl=1, bgc=[0.31,0.31,0.31], p='main')
    cmds.rowLayout('fluid', adj=1, bgc=[0.11,0.11,0.11], p='fluidframe')
    cmds.button('fluidButton', en=0 ,align="center", bgc=[0.31,0.31,0.31], command=lambda x: fluidEmission(), label="Fluid Emission", p='fluid')
    cmds.separator(style='none', h=10, p='main' )

    cmds.frameLayout("instaceframe", w=300, cll=1, l="Instancing", cl=1, bgc=[0.31,0.31,0.31], p='main')
    cmds.rowLayout('instance', nc=4, adj=4, bgc=[0.11,0.11,0.11], p='instaceframe')
    cmds.button('instanceButton', w=150, en=0 ,align="center", bgc=[0.31,0.31,0.31], command=lambda x: instance(), label="Instance", p='instance')
    cmds.popupMenu('removeinstance', p="instanceButton", ctl=False, button=3)
    cmds.menuItem('remove', l='Uninstance', command=lambda *args: removeInstance())
    cmds.button('randomRotButton', w=150, en=0 ,align="center", bgc=[0.31,0.31,0.31], command=lambda x: randommInstanceRotation(), label="Random Rotation", p='instance')
    cmds.button('uninstanceButton', w=150, en=0 ,align="center", bgc=[0.31,0.31,0.31], command=lambda x: uninstance(), label="Bake", p='instance')
    cmds.iconTextScrollList('instancelist', h=100, allowMultiSelection=False, p='instaceframe')
    

    
    randommInstanceRotation()
    cmds.showWindow('PartikelUI')
    try:
        cmds.window('PartikelUI', edit = True, titleBar = True, topEdge = True)
    except:
        pass
    
def setCurve():
    sampledensity = cmds.floatSliderGrp('sampledensity', q=1, v=1)
    curvewidth = cmds.floatSliderGrp('curvewidth', q=1, v=1)
    curvevisibility = cmds.checkBox('curvevisibility', q=1, v=1)
    if curvevisibility == 0:
        cmds.hide(curves)
    else:
        cmds.showHidden(curves)
    try:
        for s in strokeShapes:
            s = ', '.join(s)
            cmds.setAttr(s+".sampleDensity", sampledensity)
        for m in strokemeshs:
            name = str(m).replace('MainShape', '')
            name = name.replace("u'","").replace("'","").replace("[","").replace("]","")
            cmds.setAttr(name+".brushWidth", curvewidth)
    except:
        pass
    try:
        setCurve()
    except:
        pass

def setAttributes():
    size1 = cmds.floatSliderGrp('size1', q=1, v=1)
    size2 = cmds.floatSliderGrp('size2', q=1, v=1)
    bounce1 = cmds.floatSliderGrp('bounce1', q=1, v=1)
    friction1 = cmds.floatSliderGrp('friction1', q=1, v=1)
    stick1 = cmds.floatSliderGrp('stick1', q=1, v=1)
    minDistance1 = cmds.floatSliderGrp('minDistance1', q=1, v=1)
    maxDistance1 = cmds.floatSliderGrp('maxDistance1', q=1, v=1)
    speed1 = cmds.floatSliderGrp('speed1', q=1, v=1)
    speedR1 = cmds.floatSliderGrp('speedR1', q=1, v=1)
    drag1 = cmds.floatSliderGrp('drag1', q=1, v=1)
    mass1 = cmds.floatSliderGrp('mass1', q=1, v=1)
    rate2 = cmds.floatSliderGrp('rate2', q=1, v=1)
    bounce2 = cmds.floatSliderGrp('bounce2', q=1, v=1)
    friction2 = cmds.floatSliderGrp('friction2', q=1, v=1)
    stick2 = cmds.floatSliderGrp('stick2', q=1, v=1)
    minDistance2 = cmds.floatSliderGrp('minDistance2', q=1, v=1)
    maxDistance2 = cmds.floatSliderGrp('maxDistance2', q=1, v=1)
    speed2 = cmds.floatSliderGrp('speed2', q=1, v=1)
    speedR2 = cmds.floatSliderGrp('speedR2', q=1, v=1)
    conserve2 = cmds.floatSliderGrp('conserve2', q=1, v=1)
    drag2 = cmds.floatSliderGrp('drag2', q=1, v=1)
    damp2 = cmds.floatSliderGrp('damp2', q=1, v=1)
    mass2 = cmds.floatSliderGrp('mass2', q=1, v=1)
    ngravity = cmds.floatSliderGrp('gravity', q=1, v=1)
    mag= cmds.floatSliderGrp('mag', q=1, v=1)
    atten = cmds.floatSliderGrp('atten', q=1, v=1)
    frequ = cmds.floatSliderGrp('frequ', q=1, v=1)
    noiselevel = cmds.floatSliderGrp('noiselevel', q=1, v=1)
    noiseratio = cmds.floatSliderGrp('noiseratio', q=1, v=1)
    timescale = cmds.floatSliderGrp('timescale', q=1, v=1)
    spacescale = cmds.floatSliderGrp('spacescale', q=1, v=1)
    collision1 = cmds.checkBox('collision1', q=1, v=1)
    selfcollision1 = cmds.checkBox('selfcollision1', q=1, v=1)
    collision2 = cmds.checkBox('collision2', q=1, v=1)
    selfcollision2 = cmds.checkBox('selfcollision2', q=1, v=1)
    treshold = cmds.floatField('treshold', q=1, v=1)
    radius = cmds.floatField('radius', q=1, v=1)
    cmds.setAttr('primaryParticlesShape.radius', size1)
    cmds.setAttr('secondaryParticlesShape.radius', size2)
    cmds.setAttr('primaryParticlesShape.collide', collision1)
    cmds.setAttr('primaryParticlesShape.selfCollide', selfcollision1)
    cmds.setAttr('secondaryParticlesShape.collide', collision2)
    cmds.setAttr('secondaryParticlesShape.selfCollide', selfcollision2)
    cmds.setAttr('secondaryParticlesShape.threshold', treshold)
    cmds.setAttr('secondaryParticlesShape.blobbyRadiusScale', radius)
    cmds.setAttr('primaryParticlesShape.bounce', bounce1)
    cmds.setAttr('primaryParticlesShape.friction', friction1)
    cmds.setAttr('primaryParticlesShape.stickiness', stick1)
    cmds.setAttr('primaryEmitter.minDistance', minDistance1)
    cmds.setAttr('primaryEmitter.maxDistance', maxDistance1)
    cmds.setAttr('primaryEmitter.speed', speed1)
    cmds.setAttr('primaryEmitter.speedRandom', speedR1)
    cmds.setAttr('primaryParticlesShape.drag', drag1)
    cmds.setAttr('primaryParticlesShape.pointMass', mass1)
    cmds.setAttr('secondaryEmitter.rate', rate2)
    cmds.setAttr('secondaryParticlesShape.bounce', bounce2)
    cmds.setAttr('secondaryParticlesShape.friction', friction2)
    cmds.setAttr('secondaryParticlesShape.stickiness', stick2)
    cmds.setAttr('secondaryEmitter.minDistance', minDistance2)
    cmds.setAttr('secondaryEmitter.maxDistance', maxDistance2)
    cmds.setAttr('secondaryEmitter.speed', speed2)
    cmds.setAttr('secondaryEmitter.speedRandom', speedR2)
    cmds.setAttr('secondaryParticlesShape.conserve', conserve2)
    cmds.setAttr('secondaryParticlesShape.drag', drag2)
    cmds.setAttr('secondaryParticlesShape.damp', damp2)
    cmds.setAttr('secondaryParticlesShape.pointMass', mass2)
    cmds.setAttr('nucleus1.gravity', ngravity)
    cmds.setAttr('turbulenceF.magnitude', mag)
    cmds.setAttr('turbulenceF.attenuation', atten)
    cmds.setAttr('turbulenceF.frequency', frequ)
    cmds.setAttr('turbulenceF.noiseLevel', noiselevel)
    cmds.setAttr('turbulenceF.noiseRatio', noiseratio)
    cmds.setAttr("nucleus1.timeScale", timescale)
    cmds.setAttr("nucleus1.spaceScale", spacescale)
        
def setRateTime():
    mel.eval('performClearKeyArgList 1 {"0", "primaryEmitter.rate", "0", "0"};')
    rate1 = cmds.intField('rate1', q=1, v=1 )
    stop1 = cmds.intField('stop1', q=1, v=1  )
    cmds.currentTime(0, u=0)
    cmds.setAttr('primaryEmitter.rate', rate1)
    cmds.setKeyframe('primaryEmitter.rate')
    cmds.currentTime(stop1, u=0)
    cmds.setAttr('primaryEmitter.rate', rate1)
    cmds.setKeyframe('primaryEmitter.rate')
    cmds.currentTime(stop1+1, u=0)
    cmds.setAttr('primaryEmitter.rate', 0)
    cmds.setKeyframe('primaryEmitter.rate')
    cmds.currentTime(0, u=0) 

        
def createParticles():
    cmds.emitter( dx=1, dy=0, dz=0, sp=0.33, pos=(1, 1, 1), n='primaryEmitter')
    cmds.nParticle( n='primaryParticles')
    cmds.emitter(r=100, sro=0, nuv=0, cye='none', cyi=1, spd=1, srn=0, nsp=1, tsp=0, mxd=0, mnd=0, dx=1, dy=0, dz=0, sp=0 , n='secondaryEmitter')
    cmds.nParticle( n='secondaryParticles')
    cmds.select( clear=True )
    cmds.connectDynamic( 'primaryParticles', em='primaryEmitter' )
    cmds.connectDynamic( 'secondaryParticles', em='secondaryEmitter' )
    cmds.turbulence(n='turbulenceF', pv=1)
    cmds.group(em=1, n='Partikel_grp')
    cmds.parent('primaryEmitter', 'Partikel_grp')
    cmds.parent('primaryParticles', 'Partikel_grp')
    cmds.parent('secondaryParticles', 'Partikel_grp')
    cmds.parent('nucleus1', 'Partikel_grp')
    cmds.parent('turbulenceF', 'Partikel_grp')
    cmds.connectDynamic( 'primaryParticles', f='turbulenceF')
    cmds.connectDynamic( 'secondaryParticles', f='turbulenceF')
    cmds.setAttr("primaryParticlesShape.selfCollide", 1)
    cmds.setAttr("secondaryParticlesShape.selfCollide", 1)
    cmds.setAttr("secondaryParticlesShape.color[0].color_Position", 0)
    cmds.setAttr("secondaryParticlesShape.color[0].color_Color",  0.685, 1, 1, type='double3')
    cmds.setAttr("secondaryParticlesShape.color[1].color_Position", 0.5)
    cmds.setAttr("secondaryParticlesShape.color[1].color_Color",  0, 0, 1, type='double3')
    cmds.setAttr("secondaryParticlesShape.color[2].color_Position", 1)
    cmds.setAttr("secondaryParticlesShape.color[2].color_Color",  0, 0, 0.16, type='double3')
    cmds.setAttr("secondaryParticlesShape.colorInput", 1)
    cmds.setAttr("secondaryParticlesShape.colorInputMax", 5)
    cmds.setAttr("secondaryParticlesShape.color[0].color_Interp", 2)
    cmds.setAttr("secondaryParticlesShape.color[1].color_Interp", 2)
    cmds.setAttr("secondaryParticlesShape.color[2].color_Interp", 2)
    cmds.hide('turbulenceF')
    cmds.hide('nucleus1')
    cmds.setAttr("primaryEmitter.translateY", 0.1)
    cmds.select('secondaryParticles')
    cmds.parent(mel.eval('createNConstraint pointToPoint 0;'), 'Partikel_grp')
    cmds.button('set',e=1, en=1, bgc=[0,0.75,0.99])
    cmds.button('trailToCurveButton', e=1, en=1)
    cmds.button('trailToMeshButton', e=1, en=1)
    cmds.button('instanceButton', e=1, en=1, bgc=[0,0.75,0.99])
    cmds.button('randomRotButton', e=1, en=1, bgc=[0,0.75,0.99])
    cmds.button('uninstanceButton', e=1, en=1, bgc=[0,0.75,0.99])
    cmds.button('start', e=1, en=0, bgc=[0.31,0.31,0.31])
    cmds.button('fluidButton', e=1, en=1, bgc=[0,0.75,0.99])
    
def pPosListDict(particleName, startFrm, endFrm):
    pPosDict = {}   
    for eachFrm in range(startFrm, (endFrm + 1)):
        cmds.currentTime(eachFrm)
        pCount = cmds.particle( particleName, query=True, count=True)
        for pId in range(pCount):
            eachPartPos = cmds.particle(particleName, query=True, id=pId, attribute='position')
            try:
                pPosDict[pId].append(eachPartPos)
            except KeyError:
                pPosDict[pId] = [eachPartPos]
    return pPosDict
    
def trailToCurve():
    if cmds.objExists('ParticleCurves_grp'):
        cmds.delete('ParticleCurves_grp')
        cmds.group(em=1, n='ParticleCurves_grp')
    else:
        cmds.group(em=1, n='ParticleCurves_grp')
    
    startFrm = cmds.intField('startFrame', q=1, v=1)
    endFrm = cmds.intField('endFrame', q=1, v=1)
    
    pList = cmds.ls('primaryParticles')
    
    for pName in pList:
        pPosDict = pPosListDict(pName, startFrm, endFrm)
        for each in pPosDict.values():
             createCurve(each)
    if cmds.checkBox('curve1', q=1, v=1) == 1:
        renderCurve()
    setCurve()

def createCurve(singParPosList):
    faultlist = 4
    if len(singParPosList) >= faultlist:
        curve = cmds.curve(d=3, p=singParPosList)
        cmds.parent(curve, 'ParticleCurves_grp')
        cmds.setAttr(curve +".overrideEnabled", 1)
        cmds.setAttr(curve +".overrideColor", 17)
    else:
        print "nothing"

def renderCurve():
    global curves
    curves = cmds.listRelatives('ParticleCurves_grp')
    strokes = []
    global strokeShapes
    strokeShapes = []
    global strokemeshs
    strokemeshs = []
    
    for c in curves:
        cmds.select(c)
        mel.eval('AttachBrushToCurves;')
        strokes.append(str(cmds.ls(sl=1)))
        strokeShapes.append(cmds.listRelatives(cmds.ls(sl=1)))
        cmds.parent(cmds.ls(sl=1), 'ParticleCurves_grp')
        
        mel.eval('doPaintEffectsToPoly( 1,0,1,1,100000);')
        strokemeshs.append(str(cmds.ls(sl=1)))
        cmds.parent(cmds.ls(sl=1), 'ParticleCurves_grp')
        
        deleteme = cmds.ls('brush*'+'*MeshGroup')
        cmds.delete(deleteme)
    
    for s in strokeShapes:
        s = ', '.join(s)
        cmds.setAttr(s+".sampleDensity", 0.1)
        cmds.setAttr(s+".smoothing", 10)

    for m in strokemeshs:
        name = str(m).replace('MainShape', '')
        name = name.replace("u'","").replace("'","").replace("[","").replace("]","")
        cmds.delete(name+'Shader')
        cmds.delete(name+'ShaderSG')

    curveShader = cmds.createNode('blinn', skipSelect=True, n='CurveShader')
    cmds.select('ParticleCurves_grp')
    cmds.hyperShade(a=curveShader)
    cmds.setAttr("CurveShader.color", 0, 1, 1, type='double3')
    cmds.setAttr("CurveShader.diffuse", 1)
    cmds.setAttr("CurveShader.ambientColor", 0.3, 0.15, 0, type='double3')
    cmds.select(cl=1)
    
def interconnect():
    AllSelect = cmds.ls ( sl = True)
    ObjCount = len (AllSelect) - 1
    CurrentNum = 0
    while CurrentNum < ObjCount :
        ForNum = CurrentNum +1
        while ForNum <= ObjCount :
            print str(CurrentNum)+str(ForNum)
            CurveName = cmds.curve ( degree = 1 , point = [(0,0,0),(5,0,0)])
            cmds.connectAttr ( AllSelect[CurrentNum]+".translate" , CurveName+".cv[0]" )
            cmds.connectAttr (  AllSelect[ForNum]+".translate" , CurveName+".cv[1]" )
            PointA = cmds.pointPosition ( CurveName+".cv[0]")
            PointB = cmds.pointPosition ( CurveName+".cv[1]")
            print(  (PointA[0]-PointB[0])**2 + (PointA[1]-PointB[1])**2 + (PointA[2]-PointB[2])**2  )**0.5
            cmds.select(CurveName)
            mel.eval("AttachBrushToCurves;")
            strokeName= cmds.ls(sl = True)
            strokeShape= cmds.listRelatives(strokeName[0],  s = True)
            strokeBrush= cmds.listConnections(strokeShape[0], type= "brush")
            cmds.setAttr (strokeBrush[0]+".color1R", 1)
            cmds.setAttr (strokeBrush[0]+".color1G", 1)
            cmds.setAttr (strokeBrush[0]+".color1B", 1)
            cmds.expression(strokeBrush[0]+".transparency1", s = "vector $pointA = `pointPosition "+CurveName+".cv[1]`;\n\
    vector $pointB = `pointPosition "+CurveName+".cv[0]`;\n\
    vector $distV = $pointA - $pointB;\n\
    float $TransValue = (mag($distV)/25)-1;\n\
    if ($TransValue > 1) $TransValue = 1;\n\
    if ($TransValue < 0) $TransValue = 0;\n\
    "+strokeBrush[0]+".transparency1R = $TransValue;\n\
    "+strokeBrush[0]+".transparency1G = $TransValue;\n\
    "+strokeBrush[0]+".transparency1B = $TransValue;")
            ForNum += 1
        CurrentNum += 1

def instance():
    instanceMe = cmds.ls(sl=1)
    if len(instanceMe) == 1:
       if cmds.objExists('particleInstancer'):
            cmds.particleInstancer('secondaryParticles', e=1, a=1, obj=instanceMe)
            cmds.iconTextScrollList('instancelist', e=1, append=(instanceMe) )
       else:
            cmds.particleInstancer('secondaryParticles', a=1, obj=instanceMe, c='None', cs=1, csu='Frames', lod='Geometry', ru='Degrees', ro='XYZ', p='worldPosition', r='position', ad='worldPosition', age='age', n='particleInstancer')
            cmds.parent('particleInstancer', 'Partikel_grp')
            cmds.iconTextScrollList('instancelist', e=1, append=(instanceMe) )
    else:
        cmds.confirmDialog(m="Please select Object you want to instance!")

def removeInstance():
    instanceMe = cmds.iconTextScrollList('instancelist', si=True, q = True)
    if len(instanceMe) == 1:
        cmds.particleInstancer('secondaryParticles', e=1, rm=1, obj=instanceMe)
        cmds.iconTextScrollList('instancelist', e=1, ra=1 )
    else:
        cmds.confirmDialog(m="Please select Object you want to uninstance from list below!")
    
        
def uninstance():
    li = []
    l = cmds.ls(sl=True) or []
    for n in l:
        if cmds.nodeType(n) != "instancer": continue
        li.append(n)
    if len(li) == 0: cmds.confirmDialog(m="Please select Instancer you want to bake!")
    l = []
    m = om.MMatrix()
    dp = om.MDagPath()
    dpa = om.MDagPathArray()
    sa = om.MScriptUtil()
    sa.createFromList([0.0, 0.0, 0.0], 3)
    sp = sa.asDoublePtr()
    sf = int(cmds.playbackOptions(q=True, min=True))-1
    ef = int(cmds.playbackOptions(q=True, max=True))+2
    for i in range(sf, ef):
        cmds.currentTime(i)
        for inst in li:
            g = inst+"_baked"
            if i == sf:
                if cmds.objExists(g) == True: cmds.delete(g)
                cmds.createNode("transform", n=g)
                l.append(g)
            sl = om.MSelectionList()
            sl.add(inst)
            sl.getDagPath(0, dp)
            fni = omfx.MFnInstancer(dp)
            for j in range(fni.particleCount()):
                fni.instancesForParticle(j, dpa, m)
                for k in range(dpa.length()):
                    n = inst+"_"+str(j)+"_"+dpa[k].partialPathName()
                    if cmds.objExists(n) == False:
                        n2 = cmds.duplicate(dpa[k].partialPathName())[0]
                        n = cmds.rename(n2, n)
                        if cmds.listRelatives(n, p=True) != g:
                            n = cmds.parent(n, g)[0]
                        cmds.setKeyframe(n+".v", t=i-1, v=False)
                    tm = om.MTransformationMatrix(m)
                    t = tm.getTranslation(om.MSpace.kWorld)
                    cmds.setAttr(n+".t", t[0], t[1], t[2])
                    cmds.setKeyframe(n+".t")
                    r = tm.eulerRotation().asVector()
                    cmds.setAttr(n+".r", r[0]*57.2957795, r[1]*57.2957795, r[2]*57.2957795)
                    cmds.setKeyframe(n+".r")
                    tm.getScale(sp, om.MSpace.kWorld)
                    sx = om.MScriptUtil().getDoubleArrayItem(sp, 0)
                    sy = om.MScriptUtil().getDoubleArrayItem(sp, 1)
                    sz = om.MScriptUtil().getDoubleArrayItem(sp, 2)
                    s = om.MTransformationMatrix(dpa[k].inclusiveMatrix()).getScale(sp, om.MSpace.kWorld)
                    sx2 = om.MScriptUtil().getDoubleArrayItem(sp, 0)
                    sy2 = om.MScriptUtil().getDoubleArrayItem(sp, 1)
                    sz2 = om.MScriptUtil().getDoubleArrayItem(sp, 2)
                    cmds.setAttr(n+".s", sx*sx2, sy*sy2, sz*sz2)
                    cmds.setKeyframe(n+".s")
                    cmds.setAttr(n+".v", True)
                    cmds.setKeyframe(n+".v")
                    cmds.setKeyframe(n+".v", t=i+1, v=False)
    return l
    
def randommInstanceRotation():
    try: 
        particleObject='secondaryParticles'
        particleShape=cmds.listRelatives(particleObject, shapes=1, fullPath=1)
        instancer='particleInstancer'
        cmds.addAttr(particleShape, ln='maxRot', at='double')
        cmds.setAttr((particleShape[0] + ".maxRot"), 
            e=1, keyable=True)
        cmds.addAttr(particleShape, ln='axisPP', dt='doubleArray')
        cmds.setAttr((particleShape[0] + ".axisPP"), 
            e=1, keyable=True)
        cmds.addAttr(particleShape, ln='rotPP', dt='vectorArray')
        cmds.setAttr((particleShape[0] + ".rotPP"), 
            e=1, keyable=True)
        cmds.addAttr(particleShape, ln='maxRotRandPP', dt='doubleArray')
        cmds.setAttr((particleShape[0] + ".maxRotRandPP"), 
            e=1, keyable=True)
        expressionC = ""
        expressionC=(particleShape[0] + ".axisPP = floor(rand(3)); \n")
        expressionC+=(particleShape[0] + ".rotPP = <<rand(360),rand(360),rand(360)>>;\n")
        expressionC+=(particleShape[0] + ".maxRotRandPP = rand( 0 - " + particleShape[0] + ".maxRot," + particleShape[0] + ".maxRot)/1000;\n")
        cmds.dynExpression(particleShape[0], s=expressionC, c=1)
        expressionR = ""
        expressionR=("if (" + particleShape[0] + ".axisPP == 0)\n")
        expressionR+=(particleShape[0] + ".rotPP = " + particleShape[0] + ".rotPP + <<" + particleShape[0] + ".maxRotRandPP,0,0>>;\n")
        expressionR+=("else if (" + particleShape[0] + ".axisPP == 1)\n")
        expressionR+=(particleShape[0] + ".rotPP = " + particleShape[0] + ".rotPP + << 0, " + particleShape[0] + ".maxRotRandPP, 0 >>;\n")
        expressionR+=("else\n")
        expressionR+=(particleShape[0] + ".rotPP = " + particleShape[0] + ".rotPP + << 0, 0, " + particleShape[0] + ".maxRotRandPP >>;")
        cmds.dynExpression(particleShape[0], s=expressionR, rbd=1)
        cmds.particleInstancer(particleShape[0], rotation='rotPP', e=1, name=instancer)
    
        cmds.addAttr(particleShape, ln='scalePP', dt='vectorArray')
        mel.eval('arrayMapper -target secondaryParticlesShape -destAttr scalePP -inputV ageNormalized -type ramp;')
        cmds.setAttr("secondaryParticlesShape.lifespanMode", 0)
    
    except:
        pass

        
def trailToMesh():
    cmds.select('secondaryParticles')
    mel.eval('particleToPoly;')
    mesh = ', '.join(cmds.ls(sl=1))
    cmds.rename(mesh, 'partikelMesh')
    cmds.parent('partikelMesh', 'Partikel_grp')
    
    MeshShader = cmds.createNode('blinn', skipSelect=True, n='MeshShader')
    cmds.select('partikelMesh')
    cmds.hyperShade(a=MeshShader)
    cmds.setAttr("MeshShader.color", 0, 1, 1, type='double3')
    cmds.setAttr("MeshShader.diffuse", 1)
    cmds.setAttr("MeshShader.ambientColor", 0.3, 0.15, 0, type='double3')

    cmds.setAttr("secondaryParticlesShape.colorPerVertex", 1)
    cmds.setAttr("secondaryParticlesShape.velocityPerVertex", 0)
    cmds.setAttr("secondaryParticlesShape.meshMethod", 3)
    cmds.setAttr("secondaryParticlesShape.meshSmoothingIterations", 5)

def fluidEmission():
    fluid = mel.eval('create3DFluid 10 10 10 10 10 10;')
    fluid = cmds.listRelatives(fluid, parent=1)
    cmds.rename(fluid, 'partikelFluid')
    cmds.select('secondaryParticles')
    cmds.select('partikelFluid', add=1)
    mel.eval('EmitFluidFromObject')
    cmds.setAttr("fluidEmitter1.fluidDensityEmission", 2)
    cmds.setAttr("partikelFluidShape.temperatureMethod", 2)
    cmds.setAttr("partikelFluidShape.autoResize", 1)
    cmds.setAttr("partikelFluidShape.baseResolution", 30)
    cmds.setAttr("partikelFluidShape.densityBuoyancy", 0)
    cmds.setAttr("partikelFluidShape.densityScale", 1)
    cmds.setAttr("partikelFluidShape.velocitySwirl", 2)
    cmds.setAttr("partikelFluidShape.velocityNoise", 0.2)
    cmds.setAttr("partikelFluidShape.incandescence[0].incandescence_Color", 0, 1, 1, type='double3')
    cmds.setAttr("partikelFluidShape.incandescence[1].incandescence_Color", 0, 0, 0.6, type='double3')
    cmds.setAttr("partikelFluidShape.incandescence[1].incandescence_Position", 0.5)
    cmds.setAttr("partikelFluidShape.incandescence[2].incandescence_Color", 0.01, 0.015, 0.1, type='double3')
    cmds.setAttr("partikelFluidShape.incandescenceInputBias", 0.05)
    cmds.setAttr("partikelFluidShape.buoyancy", 0)
    cmds.setAttr("partikelFluidShape.color[0].color_Color", 0,0,0, type='double3')
