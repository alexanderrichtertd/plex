"""
    Hive Ftrack integration
    hive_ftrack.py

    version: v0.0.1
    date:    20150929
    by:      Carl Schroter

    2Do:
"""

import sys
import os
import re
import json
import errno
from PySide import QtCore, QtGui, QtUiTools
from subprocess import Popen, PIPE, STDOUT
import nuke
import nukescripts
import threading
import hive_functions
import hive_mp4convert


#sys.path.append('\\'.join(os.path.realpath(__file__).split('\\')[:-2]) + ('\\ftrack_API'))
sys.path.append('/'.join(os.path.realpath(__file__).split(os.sep)[:-2]) + ('/ftrack_API'))




os.environ['FTRACK_SERVER'] = 'https://carl-schroeter.ftrackapp.com'
os.environ['FTRACK_PROXY'] = 'https://quake.medianet.animationsinstitut.de:3128'
os.environ['FTRACK_APIKEY'] = 'd53446ae-2a27-11e5-9295-f23c91df2148'
os.environ['LOGNAME'] = 'Carl'

import ftrack

HIVE = os.getenv('HIVE')
with open(HIVE + '/HIVE_cfg.json') as data_file:
  HIVE_cfg = json.load(data_file)


def HIVE_ftrackVersionUp(projectid, seqid, shotid):

  shot = ftrack.getShot([projectid, seqid, shotid])
  comptask = shot.getTasks(taskTypes=['Compositing'])[0]
  asset = shot.createAsset(name='comp', assetType='comp', task=comptask)
  version = asset.createVersion(comment='')

  print 'created ftrack version:', version.getVersion()

def HIVE_ftrackFindVersion(projectid, seqid, shotid, version):

  shot = ftrack.getShot([projectid, seqid, shotid])
  comptask = shot.getTasks(taskTypes=['Compositing'])[0]

  finds = []

  for compversion in comptask.getAssetVersions():
    if compversion.get('version') == int(version):
      finds.append(compversion)

  return finds

def sendToFFmpeg_ftrackpublish():
  n = nuke.thisNode()
  args = hive_mp4convert.buildCommand()

  if hive_functions.HIVE_pipelineConform(n['file'].value()):

    try:
      os.makedirs('/'.join(args[-1].split('/')[:-1]))
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise

    barpercent = (n['endf'].value()-n['startf'].value()+1)/100.0
    pbar = nuke.ProgressTask('ftrack mp4')
    p = Popen(args, stdout = PIPE, stderr = STDOUT)
    while p.poll() is None:
      line = p.stdout.readline()
      if line.startswith('frame='):
        if not line: break
        currf = re.search(r"\d*(?= fps)", line)
        pbar.setProgress(int(int(currf.group())/barpercent))
        pbar.setMessage("frame: " + str(currf.group()) + "/" + str(n['endf'].value()-n['startf'].value()+1))

    parts = hive_functions.HIVE_splitBasename(args[-1])

    versions = HIVE_ftrackFindVersion(HIVE_cfg['project_id'], HIVE_cfg['sequence_id'], parts[1], int(parts[3][1:]))
    if len(versions):
      ftrack.Review.makeReviewable(versions[0], args[-1])
      versions[0].publish()

    print 'triggert ftrack file-upload to comp ' + str(parts[1]) + str(parts[3])
    nuke.message('triggert ftrack file-upload to comp ' + str(parts[1]) + str(parts[3]))

  else:
    nuke.message('It seems like this is not pipeline-conform... I\'m watching you...')