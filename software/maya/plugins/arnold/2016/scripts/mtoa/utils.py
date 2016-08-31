# NOTE: this module should not import PyMEL
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import inspect
import types
import re
import os
import shlex
import sys
import ctypes
import string
from hooks import fileTokenScene, fileTokenRenderPass, fileTokenCamera, fileTokenRenderLayer, fileTokenVersion

def even(num):
    return bool(num % 2)

def odd(num):
    return not bool(num % 2)

def capitalize(s):
    return s[0].upper() + s[1:] if s else s

def prettify(s):
    "convert from '_fooBar_Spangle22poop1' to 'Foo Bar Spangle22 Poop1'"
    return ' '.join([capitalize(x) for x in re.findall('[a-zA-Z][a-z]*[0-9]*',s)])

def toMayaStyle(s):
    "convert from this_style to thisStyle"
    parts = s.split('_')
    return ''.join([parts[0]] + [capitalize(x) for x in parts[1:]])

def groupn(iterable, n):
    '''
    group a flat list into tuples of length n
    '''
    return zip(*[iter(iterable)]*n)

def createColor(node, name):
    node = str(node)
    cmds.addAttr(node, longName=name, at='float3', usedAsColor=True)
    cmds.addAttr(node, longName=name + 'R', at='float', parent=name)
    cmds.addAttr(node, longName=name + 'G', at='float', parent=name)
    cmds.addAttr(node, longName=name + 'B', at='float', parent=name)

_objectStore = {}

def pyToMelProc(pyobj, args=(), returnType=None, procName=None, useName=False, procPrefix='pyToMel_'):
    '''
    create a MEL procedure from a python callable
    
    :pyobj:
        any python callable

    :args: 
        a list of (type, name) pairs defining the arguments of the MEL procedure to create. should be
        compatible with the arguments of the passed python object. 

    :procName:
        name to use for the MEL procedure, if None, useName and procPrefix are used to control the name

    :useName:
        use the name of the python object as the MEL procedure

    :procPrefix:
        if neither procName or useName are provided, the id() function is used to generate an unique
        integer for the python object to use as the MEL procedure name. the procPrefix is prepended to this name. 
    '''
    melParams = []
    pyParams = []
    melReturn = returnType if returnType else '' 

    for type, name in args:
        melParams.append('%s $%s' % (type, name))
        #if the arguement is a string we add \\" before and after
        if type == 'string':
            pyParams.append(r"""'"+$%s+"'""" % name)
        else:
            pyParams.append(r'"+$%s+"' % name)

    # get a unique id for this object
    objId = id(pyobj)

    # fill out a dictionary for formatting the procedure definition
    d = {}

    if procName:
        d['procname'] = procName
    elif useName:
        d['procname'] = pyobj.__name__
    else:
        # prefix
        # try to add some extra info to the name for easier debugging
        if isinstance(pyobj, types.LambdaType):
            procPrefix += '_lambda'
        elif isinstance(pyobj, (types.FunctionType, types.BuiltinFunctionType)):
            try:
                procPrefix += '_' + pyobj.__name__
            except (AttributeError, TypeError):
                pass
        elif isinstance(pyobj, types.MethodType):
            try:
                procPrefix += '_' + pyobj.im_class.__name__ + '_' + pyobj.__name__
            except (AttributeError, TypeError):
                pass
        d['procname'] = '%s%s' % (procPrefix, objId)

    d['melParams'] = ', '.join(melParams)
    d['pyParams'] = ', '.join(pyParams)
    d['melReturn'] = melReturn
    d['thisModule'] = __name__
    d['id'] = objId

    contents = '''global proc %(melReturn)s %(procname)s(%(melParams)s){'''
    if melReturn:
        contents += 'return '
    contents += '''python("import %(thisModule)s;%(thisModule)s._objectStore[%(id)s](%(pyParams)s)");}'''

    mel.eval(contents % d)
    # TODO: check for error and don't add the python object if we failed
    _objectStore[objId] = pyobj
    return d['procname']

# from supportRenderers.mel
def currentRenderer():
    return cmds.getAttr('defaultRenderGlobals.currentRenderer')

def findMelScript(name):
    path = mel.eval('whatIs("%s")'%name)
    path = path.split('in:')[-1][1:]
    proc = []
    grab = 0
    go = False
    with open(path) as f:
        for line in f:
            if name in line and 'proc' in line:
                proc.append(line)
                go = True
            
            if go and ('{' in line):
                grab += 1
              
            if grab > 0 and go:
                proc.append(line)
            
            if '}' in line and go:
                grab -= 1

            if grab == 0 and len(proc) != 1 and go:
                go=False
                break
    return proc

def safeDelete(node):
    '''delete a node, or disconnect it, if it is read-only'''
    if node.isReadOnly():
        node.message.disconnect()
    else:
        cmds.delete(str(node))

def _substitute(parts, tokens, allOrNothing=False, leaveUnmatchedTokens=False):
    result = []
    for i, tok in enumerate(parts):
        if even(i):
            try:
                tokn = tokens[tok]
                if tokn is None:
                    result.append('<%s>' % tok)
                else:
                    result.append(tokn.replace(':', '_'))
            except KeyError:
                if allOrNothing:
                    if leaveUnmatchedTokens:
                        return '<%s>' % tok
                    else:
                        return ''
                elif leaveUnmatchedTokens:
                    result.append('<%s>' % tok)
                else:
                    result.append('')
        else:
            result.append(tok)
    return ''.join(result)

_tokenCallbacks = []
_tokenNames = []
def registerFileToken(func, newTokens=None):
    """
    Register a function for modifying the file path generated by getImageName.
    
    func : callable
        The callback function. It is expected to take the form:
    
        func(path, tokens, **kwargs)
        
        - path (str) : the file path with unexpanded tokens
        - tokens (dict) : a dictionary of token names to token values.
        - kwargs (dict) : additional arguments passed to getFileName()

        If the function modifies the path string, it should return the modified path as a result.
        The dictionary should be modified in place.

    newTokens : string, list of strings, or None
        The names of any new tokens defined by the function, if any
    """
    global _tokenCallbacks
    global _tokenNames
    assert callable(func), "first argument to registerFileToken must be a python callable"
    _tokenCallbacks.append(func)
    if newTokens:
        if isinstance(newTokens, str):
            _tokenNames.append(str)
        else:
            try:
                _tokenNames.extend(str)
            except:
                print "second argument to registerFileToken expects a string or a list of strings"

def registeredTokens():
    global _tokenNames
    return _tokenNames[:]

def expandFileTokens(path, tokens, leaveUnmatchedTokens=False):
    """
    path : str
        unexpanded path, containing tokens of the form <MyToken>
    
    tokens : dict or str
        dictionary of the form {'MyToken' : value} or space separated string of form 'MyToken=value'

    This is a token expansion system based on Maya's, but with several improvements.
    In addition to standard tokens of the form <MyToken>, it also supports
    conditional groups using brackets, which will only be expanded if all the
    tokens within it exist.

    for example, in the following case, the group's contents (the underscore) are
    included because the RenderPass token is filled:
    
        >>> expandFileTokens('filename[_<RenderPass>].jpg', {'RenderPass' : 'Diffuse'})
        'filename_Diffuse.jpg'

    but in this case the contents enclosed in brackets is dropped:

        >>> expandFileTokens('filename[_<RenderPass>].jpg', {})
        'filename.jpg'
    """
    if isinstance(tokens, basestring):
        tokens = dict([pair.split('=') for pair in shlex.split(tokens)])

    grp_reg = re.compile('\[([^\]]+)\]')
    tok_reg = re.compile('<([a-zA-Z]+)>')
    result = []
    for i, grp in enumerate(grp_reg.split(path)):
        parts = tok_reg.split(grp)
        if even(i):
            result.append(_substitute(parts, tokens, allOrNothing=True, leaveUnmatchedTokens=leaveUnmatchedTokens))
        else:
            result.append(_substitute(parts, tokens, allOrNothing=False, leaveUnmatchedTokens=leaveUnmatchedTokens))
    return ''.join(result)

def translatorToExtension(translatorName):
    if (translatorName == "deepexr") :
        return "exr"
    else :
        return translatorName
    
def getFileName(pathType, tokens, path='<Scene>', frame=None, fileType='images',
                 createDirectory=False, isSequence=None, leaveUnmatchedTokens=False,
                 catchErrors=True, **kwargs):
    """
    A more generic replacement for MCommonRenderSettingsData.getImageName() that also works for types other
    than images.
    
    The naming scheme defined by the `path` argument is error-checked and corrected where necessary.
    For example, if there are multiple renderable cameras in the scene but a <Camera> token does not appear
    in the passed `path` naming scheme, then a <Camera> sub-directory will be added to `path`.
    A similar check is performed for render layers and AOVs.
    
    This function largely reproduces the behavior of MCommonRenderSettingsData.getFileName() with
    several important exceptions:
    
        - If 'RenderPass' is in the passed tokens map but not in the naming scheme, a <RenderPass>
          sub-directory will be automatically added.  By default, MCommonRenderSettingsData.getImageName()
          would only perform this operation if a Maya render pass node was setup in the scene (which
          MtoA does not use)
        - Whether or not the generated path is a sequence can be overridden by the `isSequence` argument,
          a setting which MCommonRenderSettingsData.getImageName() always pulled from the globals
        - MCommonRenderSettingsData.getImageName() only works for images, adding them to the workspace directory
          set for the 'images' type.  This function can work for any registered file rule (see the MEL
          workspace command), including 'ASS'.

    pathType : 
            - MCommonRenderSettingsData.kFullPathImage or 'full'
            - MCommonRenderSettingsData.kRelativePath or 'relative'
            - MCommonRenderSettingsData.kFullPathTmp or 'temp'
    
    path : str
            unexpanded path, containing tokens surrounded by square brackets: <MyToken>
    
    tokens : dict or str
            dictionary of the form {'MyToken' : value} or space separated string of form 
            'MyToken=value Other=foo'
    
    frame : float, int, or None
            frame number. If None, current frame is used
    
    fileType : str
            a valid type to pass to workspace -fileRuleEntry
    
    createDirectory : bool
            whether or not to create the directory (ignored when pathType is 'temp')
    
    isSequence : bool or None
            specify whether the path generated should include a frame number. If None, use the render globals
    
    leaveUnmatchedTokens : bool
            whether unmatched tokens should be left unexpanded or removed
    
    catchErrors : bool
            if False, errors raised by a token will not be caught and will abort the entire function

    """
    # convert tokens to dictionary
    if isinstance(tokens, basestring):
        tokens = dict([pair.split('=') for pair in shlex.split(tokens)])

    kwargs.update(dict(frame=frame,
                       fileType=fileType,
                       createDirectory=createDirectory,
                       isSequence=isSequence,
                       leaveUnmatchedTokens=leaveUnmatchedTokens))

    # get info from globals
    # NOTE: there is a bug in the wrapper of this class that prevents us from retrieving the
    # 'namePattern' property, so that must be properly passed in via the 'path' argument
    settings = pm.api.MCommonRenderSettingsData()
    pm.api.MRenderUtil.getCommonRenderSettings(settings)
    if isSequence is None:
        isSequence = settings.isAnimated()
    if isSequence:
        schemes = ('',
                   '.<Frame>.<Extension>',
                   '.<Frame>.<Extension>',
                   '.<Extension>.<Frame>',
                   '<Frame>',
                   '<Frame>.<Extension>',
                   '_<Frame>.<Extension>')
    else:
        schemes = ('',
                   '.<Extension>',
                   '.<Extension>',
                   '.<Extension>',
                   '',
                   '.<Extension>',
                   '.<Extension>')
    path += schemes[settings.namingScheme]

    if '<Extension>' in path and 'Extension' not in tokens:
        tokens['Extension'] = translatorToExtension(pm.getAttr('defaultArnoldDriver.aiTranslator'))
    if '<Frame>' in path and 'Frame' not in tokens:
        # TODO: add handling of sub-frames
        if frame is None:
            frame = pm.currentTime()
        else:
            frame = float(frame)
        if settings.renumberFrames:
            byFrame = settings.renumberBy/settings.frameBy
            frame = frame * byFrame - (settings.frameStart.value()-settings.renumberStart) - (byFrame-1.0)
        tokens['Frame'] = frame
    if 'Frame' in tokens and isinstance(tokens['Frame'], (float, int)):
        frame = tokens['Frame']
        frame = str(int(round(frame)))
        # add padding
        frame = ((settings.framePadding -len(frame)) * '0') + frame
        tokens['Frame'] = frame

    global _tokenCallbacks
    for cb in _tokenCallbacks:
        try:
            res = cb(path, tokens, **kwargs)
        except Exception, err:
            if catchErrors:
                print "Callback %s.%s failed: %s" % (cb.__module__, cb.__name__, err)
            else:
                raise
        else:
            if res is not None:
                path = res

    #print path, tokens
    partialPath = expandFileTokens(path, tokens, leaveUnmatchedTokens=leaveUnmatchedTokens)
    if pathType in [pm.api.MCommonRenderSettingsData.kRelativePath, 'relative']:
        return partialPath

    imageDir = pm.workspace(fileRuleEntry=fileType)
    imageDir = imageDir if imageDir else 'data'
    imageDir = pm.workspace(expandName=imageDir);

    if pathType in [pm.api.MCommonRenderSettingsData.kFullPathTmp, 'temp']:
        result = os.path.join(imageDir, 'tmp', partialPath)
    elif pathType in [pm.api.MCommonRenderSettingsData.kFullPathImage, 'full']:
        result = os.path.join(imageDir, partialPath)
    else:
        raise TypeError("Invalid pathType")

    result = result.replace("\\", "/")
    if createDirectory:
        dir =  os.path.dirname(result)
        try:
            os.makedirs(dir)
        except OSError as exc:
            import errno
            # if directory already exists we ignore the exception
            # NOTE that we do not use os.path.exists to avoid potential race conditions
            # on render farms
            if exc.errno != errno.EEXIST:
                raise
    return result

registerFileToken(fileTokenScene, 'Scene')
registerFileToken(fileTokenRenderPass, 'RenderPass')
registerFileToken(fileTokenCamera, 'Camera')
registerFileToken(fileTokenRenderLayer, 'RenderLayer')
registerFileToken(fileTokenVersion, 'Version')

def convertToUnicode(s):
    try:
        s = s.encode('utf-8')
    except UnicodeDecodeError:
        pass
    return s

def getEnvironmentVariable(name):
    '''
    This function is meant to support unicode environment variables in python 2.*
    '''
    if sys.platform == 'win32':
        n= ctypes.windll.kernel32.GetEnvironmentVariableW(name, None, 0)
        if n==0:
            return None
        buf= ctypes.create_unicode_buffer(u'\0'*n)
        ctypes.windll.kernel32.GetEnvironmentVariableW(name, buf, n)
        return buf.value
    else:
        return os.environ[name]

def setEnvironmentVariable(name, value):
    '''
    This function is meant to support unicode environment variables in python 2.*
    '''
    if sys.platform == 'win32':    
        buf= ctypes.create_unicode_buffer(value)
        ctypes.windll.kernel32.SetEnvironmentVariableW(name, buf)
    else:
        os.environ[name] = value    
        
def createLocator(locatorType, asLight=False):
    lNode = pm.createNode('transform', name='%s1' % locatorType)
    lName = lNode.name()
    lId = lName[len(locatorType):]
    shapeName = '%sShape%s' % (locatorType, lId)
    pm.createNode(locatorType, name=shapeName, parent=lNode)       
    if asLight:
        cmds.connectAttr('%s.instObjGroups' % lName, 'defaultLightSet.dagSetMembers', nextAvailable=True)
    return (shapeName, lName)

def getSourceImagesDir():
    sourceImagesRule = cmds.workspace(fileRuleEntry='sourceImages')
    if sourceImagesRule != None:
        sourceImagesRule = sourceImagesRule.split(';')
        ret = []
        for rule in sourceImagesRule:
            ret.append(cmds.workspace(expandName=rule))
        return ret
    else:
        return [cmds.workspace(expandName='sourceimages')]
