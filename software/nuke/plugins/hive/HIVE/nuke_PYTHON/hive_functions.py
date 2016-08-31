"""
    Hive Nuke environment
    hive_functions.py

    version: 0.0v1
    date:    20150709
    by:      Carl Schroter

    2Do:
"""
#Nuke Imports
import nuke, nukescripts

#other imports
import os, json

#Hive imports
import hive_beforeRender
import hive_afterRender
import hive_ftrack

HIVE = os.getenv('HIVE')
with open(HIVE + '/HIVE_cfg.json') as data_file:
  HIVE_cfg = json.load(data_file)

def HIVE_beforeRender():
  #print "HIVE_beforeRender"
  hive_beforeRender.createWriteDir()

def HIVE_afterRender():
  #print "HIVE_afterRender"
  #hive_afterRender.sendToFFmpeg()
  pass

def HIVE_hideInputs():
  for i in nuke.selectedNodes():
    if i['hide_input'].value():
      i['hide_input'].setValue(False)
    else:
      i['hide_input'].setValue(True)

def HIVE_buildGizmoMenu(menu):
  # add old Bezier node
  menu.addCommand('Nodes/Bezier (old)', 'nuke.tcl(\'Bezier\')')
  # add all other gizmos
  for file in os.listdir(HIVE + '/nuke_GIZMOS'):
    if file.endswith('.gizmo'):
      gizmo = file.replace('.gizmo', '')
      menu.addCommand('Nodes/' + gizmo, 'nuke.tcl(\'' + str(gizmo) + '\')')

def HIVE_buildFavorites():
  # remove default favs
  nuke.removeFavoriteDir("Home")
  nuke.removeFavoriteDir("Root")
  nuke.removeFavoriteDir("Nuke")
  nuke.removeFavoriteDir("Current")

  # shot specific favs
  if HIVE_pipelineConform():

    favlist = [i for i in HIVE_cfg['nuke_shot_favs']]

    shotid = hive_functions.HIVE_splitBasename()[0]

    for i in reversed(favlist):
      nuke.addFavoriteDir(i.replace('#shot', shotid), '/'.join([HIVE_cfg['basedir'], HIVE_cfg['folder_structure']['shots_dir'], shotid, HIVE_cfg['nuke_shot_favs'][i].replace('#shot', shotid)]))

  # HIVE_cfg favs
  favlist = [i for i in HIVE_cfg['nuke_favs']]

  for i in reversed(favlist):
    favparts = HIVE_cfg['nuke_favs'][i].split(':')

    # inside folder_structure
    if len(favparts) > 1:
      if favparts[0] == 'folder_structure':
        # reference folder_structure folder
        if not favparts[1][0] == '#':
          # add fav
          nuke.addFavoriteDir(i, '/'.join([HIVE_cfg['basedir'], HIVE_cfg['folder_structure'][favparts[1]]]))
        # predefined shortcut in folder_structure
        else:
          if favparts[1][1:] == 'userdir':
            # add fav
            nuke.addFavoriteDir(i, '/'.join([HIVE_cfg['basedir'], HIVE_cfg['folder_structure']['user_dir'], os.environ.get('USERNAME')]))

    else:
      if not favparts[0][0] == '#': #hardcoded path
        nuke.addFavoriteDir(i, favparts[0])
      else: #predefined shortcut
        if favparts[0][1:] == 'userdesktop':
          # add fav
          nuke.addFavoriteDir(i, '/'.join(['C:/Users', os.environ.get('USERNAME'), 'Desktop']))
        elif favparts[0][1:] == 'basedir':
          nuke.addFavoriteDir(i, HIVE_cfg['basedir']+'/')

def HIVE_pipelineConform(filepath=''):
  ''' lets try to find out if this is pipeline conform '''

  if filepath == '':
    if not nuke.root().name() == 'Root':
      filepath = nuke.root().name()
    else:
      print 'Please save your script first!'
      return False

  filenameparts = filepath.split('/')
  #print filenameparts

  if not filenameparts[0] == HIVE_cfg['basedir']:
    print 'wrong basedir'
    return False

  if not filenameparts[1] == HIVE_cfg['folder_structure']['shots_dir']:
    print 'not in', HIVE_cfg['folder_structure']['shots_dir']
    return False

  #shot consistency
  shot_level = filenameparts[2].split('_')[0]
  task_level = filenameparts[3].split('_')[1]
  work_level = filenameparts[4].split('_')[0]
  file_level = filenameparts[-1].split('_')[0]

  #print shot_level,task_level,work_level,file_level

  ext = HIVE_splitBasename(filepath)[-1]

  if ext in ['nk']:
    #print 'this is a nuke script'
    if shot_level == task_level == work_level == file_level:
      # all shotids same
      return True
    else:
      print 'shot numbers differ in path'
      return False

  elif ext in ['jpg', 'jpeg', 'exr', 'tif', 'tiff', 'png', 'dpx']:
    #print 'this is an img or imgseq'
    version_level = filenameparts[5].split('_')[1]
    #print version_level
    if shot_level == task_level == work_level == version_level == file_level:
      # all shotids same
      return True
    else:
      #print 'shot numbers differ in path'
      return False

  else:
    #print 'don\'t know what this is...'
    print 'not a nuke-script or img/imgseq'
    return False

def HIVE_splitBasename(filepath=''):

  if filepath == '':
    if not nuke.root().name() == 'Root':
      filepath = nuke.root().name()

  basename = os.path.basename(nukescripts.replaceHashes(filepath))
  parts = []

  for i in basename.split('_')[:-1] : parts.append(i)
  parts.append(basename.split('_')[-1].split('.')[0])
  for i in basename.split('.')[1:] : parts.append(i)

  return parts

def HIVE_versionUp():
  if HIVE_pipelineConform():
    parts = HIVE_splitBasename(nuke.root().name())

    # version up script
    cur_version = int(parts[3][1:]) # 1
    new_version = cur_version+1 #2
    new_verstionstring = 'v{0:03d}'.format(new_version) #v002
    newfilename = '_'.join(parts[:3]) + '_' + new_verstionstring + '_' + os.environ['USERNAME'][:2] + '.' + '.'.join(parts[5:])

    scriptpath = '/'.join(nuke.root().name().split('/')[:5])
    existingScripts =  os.listdir(scriptpath)

    #print existingScripts

    for existingfile in existingScripts:
      if not existingfile.endswith('~'):
        if '_'.join(HIVE_splitBasename(existingfile)[:4]) == '_'.join(parts[:3]) + '_' + new_verstionstring:    #DM_020_comp_v001 DM_020_comp_v002
          if nuke.ask('version "' + '_'.join(HIVE_splitBasename(existingfile)[:4]) + '" exists. Overwrite?'):
            nuke.scriptSaveAs( scriptpath + '/' + newfilename, 1)

            # version up ftrack
            if HIVE_cfg['HIVE']['use_ftrack']:
              #print HIVE_cfg['project_id'], HIVE_cfg['sequence_id'], parts[1]
              if not len(hive_ftrack.HIVE_ftrackFindVersion(HIVE_cfg['project_id'], HIVE_cfg['sequence_id'], parts[1], new_version)):
                hive_ftrack.HIVE_ftrackVersionUp(HIVE_cfg['project_id'], HIVE_cfg['sequence_id'], parts[1]) #projectid, seqid, shotid

            # version up write node