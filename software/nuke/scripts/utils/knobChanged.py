nuke.thisNode().knob('knobChanged').setValue('''

currentNode = nuke.thisNode()

# EXR
if currentNode["chbExr"].getValue():
    currentNode["exrPath"].setEnabled(True)    
    currentNode["exrRv"].setEnabled(True)    
    currentNode["exrFolder"].setEnabled(True)
else:
    currentNode["exrPath"].setEnabled(False)    
    currentNode["exrRv"].setEnabled(False)    
    currentNode["exrFolder"].setEnabled(False) 

# JPG
if currentNode["chbJpg"].getValue():
    currentNode["jpgPath"].setEnabled(True)    
    currentNode["jpgRv"].setEnabled(True)    
    currentNode["jpgFolder"].setEnabled(True)
else:
    currentNode["jpgPath"].setEnabled(False)    
    currentNode["jpgRv"].setEnabled(False)    
    currentNode["jpgFolder"].setEnabled(False) 

# META
if currentNode["meta"].getValue():
    currentNode["status"].setEnabled(True)    
    currentNode["comment"].setEnabled(True)    
else:
    currentNode["status"].setEnabled(False)    
    currentNode["comment"].setEnabled(False)    

# THREADS
if currentNode["submit"].getValue() == 0.0:
    currentNode["threads"].setVisible(True)
    currentNode["space01"].setVisible(True)
else:
    currentNode["threads"].setVisible(False)
    currentNode["space01"].setVisible(False)

''')