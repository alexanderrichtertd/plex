

'''
wavePanel v1.4 by falk Hofmann 2013
Falk@Kombinat-13b.de
www.kombinat-13b.de

import wavePanel
menu=nuke.menu("Nuke")
mb=menu.addMenu( "Custom Menu" )
mb.addCommand ( "wavePanel v1.4", 'wavePanel.go()', icon="wavePanel.png" )
'''

import nuke 
import nukescripts
import os

class wavePanel ( nukescripts.PythonPanel ):

    def __init__  ( self ):
     
        newPanel = nukescripts.PythonPanel.__init__ ( self , 'wavePanel' , 'wavePanel' )
        self.setMinimumSize(700, 700)
        
        self.cb = nuke.Boolean_Knob
        self.tab = nuke.Tab_Knob
        button = nuke.PyScript_Knob
        self.txt = nuke.Text_Knob
        self.pos = nuke.XY_Knob
        self.scale = nuke.WH_Knob
        self.slider = nuke.Double_Knob
        self.integer = nuke.Int_Knob
        add = self.addKnob

        
        
### build Wave Tab ### 

        curves = self.tab ('waves')
        self.waveList = ['sine' , 
                   'square' ,
                   'triangle' ,
                   'random' , 
                   'noise' , 
                   'bounce' , 
                   'sawtooth' ,  
                   'sawtoothParabolic' ,
                   'sawtoothParabolicReversed' , 
                   'sawtoothExponential'  ]
        add(curves)
        
        for i in self.waveList:
            path = 'w_' + i + ".png"
            iconPath =  '<img src="%s">' % path
            temp = button (i,  iconPath  )
            descr = self.txt (i, 'add %s tab' % i)
            sep = self.txt ('')
            add (descr)
            add (temp)
            add (sep) 
            

            
### build Blip Tab ###

        blip = self.tab ('blip')
        add(blip)
        self.blipList = [
                        'singlePulse'
                         ]

        for i in self.blipList:
            path = 'b_' + i + ".png"
            iconPath =  '<img src="%s">' % path
            temp = button (i,  iconPath  )
            descr = self.txt (i, 'add %s tab' % i)
            sep = self.txt ('')
            add (descr)
            add (temp)
            add (sep) 
            
            
### build Graphics Tab ###
            
        graphics = self.tab ('graphics')
        add(graphics)
        self.graphList = ['Circle' ,
                            'Hypocycloid' ,
                            'Lemniscate' ,
                            'Lissajous' ,
                            'Rose' , 
                            'Spiral' ]

        for i in self.graphList:
        
            path = 'g_' + i + ".png"
            iconPath =  '<img src="%s">' % path
            temp = button (i,  iconPath  )
            descr = self.txt (i, 'add %s tab' % i)
            sep = self.txt ('')
            add (descr)
            add (temp)
            add (sep) 
            

### build Info Tab ###
           
        info = self.tab ('info')
        add ( info )
        
        info = self.txt ( '@b;wave Panel v1.4' )
        infoA = self.txt ( 'suggestions,  critique or similar are very welcome.')
        infoA.setFlag(nuke.STARTLINE)
        infoB = self.txt ( 'Falk Hofmann  05_2013' )
        infoB.setFlag(nuke.STARTLINE)
        infoC = self.txt ( 'Falk@Kombinat-13b.de')
        infoC.setFlag(nuke.STARTLINE)
        
        add ( info )
        add ( infoA )
        add ( infoB )
        add ( infoC )
                        


    def knobChanged ( self,  k ):

        if k.name() in self.waveList:
            self.createWaveTab (k.name())
            
        if k.name() in self.blipList:
            self.createBlipTab (k.name())
            
        if k.name() == 'Circle':
            self.createCircleTab ()

        if k.name() == 'Spiral':
            self.createSpiralTab ()

        elif k.name() == 'Rose':
            self.createRoseTab ()        

        elif k.name() == 'Hypocycloid':
            self.createhypoTab ()
        
        elif k.name() == 'Lemniscate':
            self.createLemniTab ()

        elif k.name() == 'Lissajous':
            self.createLissaTab ()

            

    def createWaveTab ( self, wave):

        math = {'sine' : '(((sin(((frame*(pi*2/(this.frequency_%s)/2))/2)+this.offset_%s))+1)/2) * (this.max_%s-this.min_%s)  + this.min_%s' %(wave, wave, wave, wave, wave),
                      'square' : '((((sin(((frame*(pi*2/(this.frequency_%s/2))/2)+this.offset_%s))+1)/2) *(this.max_%s-this.min_%s) ) + this.min_%s) > ((this.max_%s/2)+(this.min_%s/2)) ? this.max_%s : this.min_%s' %(wave, wave, wave, wave, wave, wave, wave, wave, wave),
                      'triangle' : '(((((2*asin(sin(2*pi*(frame/this.frequency_%s)+this.offset_%s)))/pi) / 2)+0.5) * (this.max_%s-this.min_%s) ) + this.min_%s' %(wave, wave, wave, wave, wave),
                      'random' : '((random(((frame)/this.frequency_%s)+this.offset_%s)) * (this.max_%s-this.min_%s) ) + this.min_%s' %(wave, wave, wave, wave, wave),
                      'noise' : '(((1*(noise((frame/this.frequency_%s)+this.offset_%s))+1 ) /2 ) * (this.max_%s-this.min_%s) ) + this.min_%s' %(wave, wave, wave, wave, wave),
                      'bounce' :  '((sin(((frame/this.frequency_%s)*pi)+this.offset_%s)>0?sin(((frame/this.frequency_%s)*pi)+this.offset_%s):cos((((frame/this.frequency_%s)*pi)+this.offset_%s)+(pi/2))) * (this.max_%s-this.min_%s) ) + this.min_%s' %(wave, wave, wave, wave, wave, wave, wave, wave, wave),
                      'sawtooth' : '((1/this.frequency_'+wave+')*(((frame-1)+this.offset_' + wave + ') % this.frequency_' + wave + ') *(this.max_' + wave + '-this.min_' + wave + ') ) + this.min_' + wave,
                      'sawtoothParabolic' : '((sin((1/(pi/2))*(((frame-1)+this.offset_' + wave + ')/(this.frequency_' + wave + '/2.46666666)) % (pi/2)))>0.99999? 1 : (sin((1/(pi/2))*(((frame-1)+this.offset_' + wave + ')/(this.frequency_' + wave + '/2.46666666)) % (pi/2))) * (this.max_' + wave + '-this.min_' + wave + ') ) + this.min_' + wave,
                      'sawtoothParabolicReversed' : '((cos((1/(pi/2))*(((frame-1)+this.offset_' + wave + ')/(this.frequency_' + wave + '/2.46666666)) % (pi/2)))>0.99999? 1 : (cos((1/(pi/2))*(((frame-1)+this.offset_' + wave + ')/(this.frequency_' + wave + '/2.46666666)) % (pi/2))) * (this.max_' + wave + '-this.min_' + wave + ') ) + this.min_' + wave,
                      'sawtoothExponential' :'((((((exp((1/(pi/2))*(((frame-1)+this.offset_' + wave + ')/(this.frequency_' + wave + '/4.934802)) % pi*2)))/534.5)) - 0.00186741)>0.999987? 1 : (((((exp((1/(pi/2))*(((frame-1)+this.offset_' + wave + ')/(this.frequency_' + wave + '/4.934802)) % pi*2)))/534.5)) - 0.00186741) * (this.max_' + wave + '-this.min_' + wave + ') ) + this.min_' + wave
                      }

        n = nuke.selectedNode()

        sep = self.txt('')
        tabName = wave +'_wave'
        waveTab = self.tab (tabName, tabName)

        waveEx = math [str(wave)]

        min = self.slider ( 'min_' + wave, 'min' ) 
        max = self.slider ( 'max_' + wave , 'max' ) 
        max.setValue ( 1 )

        frequency = self.slider ( 'frequency_' + wave , 'frequency' )
        frequency.setRange(1,100)
        frequency.setValue ( 5 )

        offset = self.slider ( 'offset_' + wave , 'Horizontal offset')
        offset.setRange(1,100)

        result = self.slider (str(wave)+ 'Wave', str(wave) + 'Wave')
        result.setExpression (waveEx)
             
        n.addKnob(waveTab)
        n.addKnob(min)
        n.addKnob(max)
        n.addKnob(frequency)
        n.addKnob(offset)
        n.addKnob(sep)
        n.addKnob(result)
        n['label'].setValue(wave)

    
    def createBlipTab ( self, blip ):
        math = { 'singlePulse' : 'frame % (abs(every_' + blip + ')) ==  blipAt_' + blip + '? on_' + blip + ':off_' + blip 
                }
        n = nuke.selectedNode()
        
        sep = self.txt('')
        tabName = blip + '_blip'
        blipTab = self.tab (tabName, tabName)

        blipEx = math [str(blip)]

        blink = self.integer ( 'blipAt_' + blip , 'blip at frame' )
        blink.setValue ( 1 )
        
        every = self.integer ( 'every_' + blip , 'every...frames' )
        every.setValue( 10 )
 
        off = self.slider ( 'off_' + blip, 'off value' )
        on = self.slider ( 'on_' + blip , 'on value' )
        off.setValue ( 0 )        
        on.setValue ( 1 )
        
        result = self.slider (str(blip)+ 'blip', str(blip) + 'blip')
        result.setExpression (blipEx)
             
        n.addKnob(blipTab)
        n.addKnob(blink)
        n.addKnob(every)      
        n.addKnob(off)
        n.addKnob(on)
        n.addKnob(sep)
        n.addKnob(result)
        n['label'].setValue(blip)   
        
        
    def createCircleTab ( self ):
    
        n = nuke.selectedNode()
        CircleTab = self.tab ( 'CircleTab' , 'Circle Tab' )
        scale = self.scale ( 'scale_circle' , 'scale' )
        offset = self.pos ( 'offset_circle' , 'Offset') 
        fc = self.slider ( 'fc_circle' , 'Frame Cycle' )
        velo = self.slider ( 'velo_circle' , 'Velocity' )
        sep = self.txt ('' )
        result = self.pos ( 'circle' , 'circle' )

        n.addKnob( CircleTab )
        n.addKnob ( scale )
        n.addKnob ( offset )
        n.addKnob ( fc )
        n.addKnob ( velo )
        n.addKnob ( sep )
        n.addKnob ( result )

        scale.setValue ( 300 )
        offset.setValue ( 800 )
        fc.setValue ( 90 )
        velo.setValue ( 2 )
        result.setExpression ( 'offset_circle.x+scale_circle.h*sin((frame*velo_circle*acos(-1))/fc_circle)' , 0 )
        result.setExpression ( 'offset_circle.y+scale_circle.w*cos((frame*velo_circle*acos(-1))/fc_circle)' , 1 )
        n['label'].setValue('CircleTab')



    def createSpiralTab ( self ) :

        n = nuke.selectedNode()
        SpiralTab = self.tab ( 'SpiralTab' , 'Spiral Tab' )
        scale = self.scale ( 'scale_spiral' , 'scale' )
        offset = self.pos ( 'offset_spiral' , 'Offset') 
        spiral = self.slider ( 'spiral_spiral' , 'Spiral' )
        velo = self.slider ( 'velo_spiral' , 'Velocity' )
        sep = self.txt ('' )
        result = self.pos ( 'spiral' , 'spiral' )

        n.addKnob( SpiralTab )
        n.addKnob ( scale )
        n.addKnob ( offset )
        n.addKnob ( spiral )
        n.addKnob ( velo )
        n.addKnob ( sep )
        n.addKnob ( result )

        scale.setValue ( 3 )
        offset.setValue ( 800 )
        spiral.setValue ( 60 )
        velo.setValue ( 10 )
        result.setExpression ( '(scale_spiral.w*frame*cos(frame*acos(-1)*velo_spiral/spiral_spiral))+offset_spiral.x' , 0 )
        result.setExpression ( '(scale_spiral.h*frame*sin(frame*acos(-1)*velo_spiral/spiral_spiral))+offset_spiral.y' , 1 )
        n['label'].setValue('SpiralTab')
            
            
            
    def createRoseTab ( self ) :

        n = nuke.selectedNode()
        RoseTab = self.tab ( 'RoseTab' , 'Rose Tab' )
        loops = self.slider ( 'loops_rose' , 'Loops' )
        scale = self.scale ( 'scale_rose' , 'scale' )
        offset = self.pos ( 'offset_rose' , 'Offset') 
        fc = self.slider ( 'fc_rose' , 'Frame Cycle' )
        velo = self.slider ( 'velo_rose' , 'Velocity' )
        sep = self.txt ('' )
        result = self.pos ( 'rose' , 'rose' )

        n.addKnob( RoseTab )
        n.addKnob ( loops )
        n.addKnob ( scale )
        n.addKnob ( offset )
        n.addKnob ( fc )
        n.addKnob ( velo )
        n.addKnob ( sep )
        n.addKnob ( result )

        loops.setValue ( 5 )
        scale.setValue ( 300 )
        offset.setValue ( 800 )
        fc.setValue ( 90 )
        velo.setValue ( 2 )
        result.setExpression ( '(cos((frame*velo_rose*acos(-1)/fc_rose))-cos((loops_rose-1)*(frame*velo_rose*acos(-1)/fc_rose)))*scale_rose.w+offset_rose.x' , 0 )
        result.setExpression ( '(sin((frame*velo_rose*acos(-1)/fc_rose))+sin((loops_rose-1)*(frame*velo_rose*acos(-1)/fc_rose)))*scale_rose.h+offset_rose.y' , 1 )
        n['label'].setValue('RoseTab')

            
    def createLissaTab ( self ):

        n = nuke.selectedNode()
        LissaTab = self.tab ( 'LissaTab' , 'Lissajous Tab' )
        freq = self.pos ( 'freq_lissa' , 'Frequency' )
        scale = self.scale ( 'scale_lissa' , 'scale' )
        offset = self.pos ( 'offset_lissa' , 'Offset') 
        fc = self.slider ( 'fc_lissa' , 'Frame Cycle' )
        velo = self.slider ( 'velo_lissa' , 'Velocity' )
        sep = self.txt ('' )
        result = self.pos ( 'lissa' , 'lissa' )

        n.addKnob( LissaTab )
        n.addKnob ( freq )
        n.addKnob ( scale )
        n.addKnob ( offset )
        n.addKnob ( fc )
        n.addKnob ( velo )
        n.addKnob ( sep )
        n.addKnob ( result )

        freq.setValue ( 7 , 0 )
        freq.setValue ( 5 , 1 )
        scale.setValue ( 300 )
        offset.setValue ( 800 )
        fc.setValue ( 90 )
        velo.setValue ( 2 )
        result.setExpression ( 'scale_lissa.w*cos(freq_lissa.x*frame*velo_lissa*acos(-1)/fc_lissa)+offset_lissa.x' , 0 )
        result.setExpression ( 'scale_lissa.h*sin(freq_lissa.y*frame*velo_lissa*acos(-1)/fc_lissa)+offset_lissa.y' , 1 )
        n['label'].setValue('LissaTab')



    def createhypoTab ( self ):
    
        n = nuke.selectedNode()
        hypoTab = self.tab ( 'HypoTab' , 'Hypocycloid Tab' )
        points = self.slider ( 'points_hypo' , 'Points' )
        scale = self.scale ( 'scale_hypo' , 'scale' )
        offset = self.pos ( 'offset_hypo' , 'Offset') 
        fc = self.slider ( 'fc_hypo' , 'Frame Cycle' )
        velo = self.slider ( 'velo_hypo' , 'Velocity' )
        sep = self.txt ('' )
        result = self.pos ( 'hypo' , 'hypo' )  

        n.addKnob( hypoTab )
        n.addKnob ( points )
        n.addKnob ( scale )
        n.addKnob ( offset )
        n.addKnob ( fc )
        n.addKnob ( velo )
        n.addKnob ( sep )
        n.addKnob ( result )

        points.setValue ( 10 )
        scale.setValue ( 300 )
        offset.setValue ( 800 )
        fc.setValue ( 90 )
        velo.setValue ( 2 )
        result.setExpression ( '((scale_hypo.w/points_hypo)*((points_hypo -1)*cos((frame*velo_hypo*acos(-1)/fc_hypo))+cos((points_hypo-1)*(frame*velo_hypo*acos(-1)/fc_hypo)))+offset_hypo.x)' , 0 )
        result.setExpression ( '((scale_hypo.h/points_hypo)*((points_hypo-1)*sin((frame*velo_hypo*acos(-1)/fc_hypo))+sin((points_hypo-1)*(frame*velo_hypo*acos(-1)/fc_hypo)))+offset_hypo.y)' , 1 )      
        n['label'].setValue('hypoTab')


    def createLemniTab ( self ):
    
        n = nuke.selectedNode()
        LemniTab = self.tab ( 'LemniTab' , 'Lemniscate Tab' )
        scale = self.scale ( 'scale_lemni' , 'scale' )
        offset = self.pos ( 'offset_lemni' , 'Offset')    
        fc = self.slider ( 'fc_lemni' , 'Frame Cycle' )
        velo = self.slider ( 'velo_lemni' , 'Velocity' )
        sep = self.txt ('' )
        result = self.pos ( 'lemni' , 'lemni' )  

        n.addKnob( LemniTab )
        n.addKnob ( scale )
        n.addKnob ( offset )
        n.addKnob ( fc )
        n.addKnob ( velo )
        n.addKnob ( sep )
        n.addKnob ( result )  

        scale.setValue ( 300 )
        offset.setValue ( 800 )
        fc.setValue ( 60 )
        velo.setValue ( 1.2 )
        result.setExpression ('scale_lemni.w*cos((frame*velo_lemni*acos(-1)/fc_lemni))/(1+sin((frame*velo_lemni*acos(-1)/fc_lemni))*sin((frame*velo_lemni*acos(-1)/fc_lemni)))+offset_lemni.x' , 0 )
        result.setExpression ( '(scale_lemni.h*sin((frame*velo_lemni*acos(-1)/fc_lemni))*2*cos((frame*velo_lemni*acos(-1)/fc_lemni)))/(1+sin((frame*velo_lemni*acos(-1)/fc_lemni))*sin((frame*velo_lemni*acos(-1)/fc_lemni)))+offset_lemni.y ' , 1 )        
        n['label'].setValue('LemniTab')
		
		
def go():
    wP = wavePanel()
    wP.showModalDialog()

