"""
    Hive Nuke environment
    init.py

    version: v0.0.2
    date:    20150929
    by:      Carl Schroter

    2Do:
"""

# Set plugin/gizmo sub-folders
nuke.pluginAddPath('./nuke_GIZMOS')
nuke.pluginAddPath('./nuke_ICONS')
nuke.pluginAddPath('./nuke_PLUGINS')
nuke.pluginAddPath('./nuke_PYTHON')
nuke.pluginAddPath('./nuke_TOOLSETS')

logLevel = 1

# Nuke imports

# other imports

try:
  import json
  HIVE = os.getenv('HIVE')
  with open(HIVE + '/HIVE_cfg.json') as data_file:
    HIVE_cfg = json.load(data_file)

  if logLevel: print " ", chr(254), "   OK   _ config json"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ config json"
  #raise

try:
  import hive_functions
  if logLevel: print " ", chr(254), "   OK   _ functions"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ functions"
  #raise

try:
  import hive_nodeTweaks
  if logLevel: print " ", chr(254), "   OK   _ node tweaks"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ node tweaks"
  #raise

try:
  import hive_mp4convert
  if logLevel: print " ", chr(254), "   OK   _ mp4 convert"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ mp4 convert"
  #raise

try:
  import hive_write
  if logLevel: print " ", chr(254), "   OK   _ write node"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ write node"
  #raise

try:
	import hive_beforeRender
	if logLevel: print " ", chr(254), "   OK   _ before render"
except Exception, e:
	if logLevel: print " ", chr(254), " FAILED _ before render"
	#raise

try:
  import hive_afterRender
  if logLevel: print " ", chr(254), "   OK   _ after render"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ after render"
  #raise

if HIVE_cfg['HIVE']['use_ftrack']:
  try:
    import hive_ftrack
    if logLevel: print " ", chr(254), "   OK   _ ftrack"
  except Exception, e:
    if logLevel: print " ", chr(254), " FAILED _ ftrack"
    #raise

try:
  from vuRenderThreads.plugin_nuke import plugin_nuke as vuRenderThreadsNuke
  if logLevel: print " ", chr(254), "   OK   _ vuRenderThreads"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ vuRenderThreads"
  #raise

try:
  import SendToRoyalRender
  if logLevel: print " ", chr(254), "   OK   _ RoyalRender"
except Exception, e:
  if logLevel: print " ", chr(254), " FAILED _ RoyalRender"

print "\n"