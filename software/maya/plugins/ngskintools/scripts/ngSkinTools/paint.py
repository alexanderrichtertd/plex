#
#    ngSkinTools
#    Copyright (c) 2009-2015 Viktoras Makauskas. 
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by
#    Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License:
#        http://creativecommons.org/licenses/by-nc-nd/3.0/
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode.txt
#         
#    A copy of the license can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

from maya import cmds

pySideAvailable = False
try:
    from PySide.QtGui import QApplication
    from PySide.QtCore import Qt
    pySideAvailable = True
except:
    pass # no PySide yet? ok, we'll deal with it.
    

def ngLayerPaintCtxInitialize(shape):
    '''
    a wrapper for paint stroke start, feeding in the CTRL/Shift keyboard modifiers 
    for the next brush
    '''
    kargs = {}
    if pySideAvailable:
        keyboardState = QApplication.keyboardModifiers()
        kargs['shift'] = bool(keyboardState & Qt.ShiftModifier)
        kargs['control'] = bool(keyboardState & Qt.ControlModifier)
        
    return cmds.ngLayerPaintCtxInitialize(shape,**kargs)