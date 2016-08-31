"""
    Hive Nuke environment
    beforeRender.py

    adds to the beforeRender callback

    version: 0.0v1
    date:    20140714
    by:      Carl Schroter

    2Do:
"""

import nuke, os, errno

def createWriteDir():
  if not nuke.thisNode()['disable'].value():
    file = nuke.filename(nuke.thisNode())
    dir = os.path.dirname( file )
    osdir = nuke.callbacks.filenameFilter( dir )
    # cope with the directory existing already by ignoring that exception
    try:
      os.makedirs( osdir )
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise

nuke.addBeforeRender(createWriteDir)