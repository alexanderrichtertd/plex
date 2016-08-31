import os.path
import imp
import sys
import traceback

def loadExtensionUI(sharedLibraryPath):
    '''
    given the path to a c++ shared library, attempt to load a python module
    living in the same directory with the same name

    it is the responsibility of this module to call
    `mtoa.ui.ae.registerCustomAttrTemplate()` for each maya node translated by the
    extension.
    '''
    
    path, name = os.path.split(sharedLibraryPath)
    name = os.path.splitext(name)[0]
    pathname = os.path.join(path, name + '.py')
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass
    
    if os.path.exists(pathname):
        fp = open(pathname)
        description = ('.py', 'U', 1)
        try:
            return imp.load_module(name, fp, pathname, description)
        except RuntimeError, err:
            print "Error loading Extension UI %s" % pathname
            traceback.print_exc()
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
