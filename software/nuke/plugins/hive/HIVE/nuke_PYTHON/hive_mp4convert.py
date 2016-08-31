"""
    Hive Nuke environment
    hive_mp4convert.py

    read node extension

    version: v0.1.4
    date:    20150926
    by:      Carl Schroter

    2Do:
    - move to pyqt threading
    - stop transcode
"""

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

HIVE = os.getenv('HIVE')
with open(HIVE + '/HIVE_cfg.json') as data_file:
  HIVE_cfg = json.load(data_file)

def buildMovPath(n):
  imgSeqPath = nukescripts.replaceHashes(n['file'].value())
  base, ext = os.path.splitext(os.path.basename(imgSeqPath))

  mp4folder = '_'.join('/'.join(imgSeqPath.split('/')[:-1]).split('_')[:-1]) + '_mp4'
  filename = '_'.join(hive_functions.HIVE_splitBasename(imgSeqPath)[:-2])

  movPath =  mp4folder + '/' + filename + '.mp4'

  if imgSeqPath.lower() != movPath.lower():
    return movPath
  else:
    movPath =  mp4folder + '/' + filename + '_converted.mp4'
    return movPath

def buildCommand():
  n = nuke.thisNode()

  mp4_width = str(int(n['mp4_format'].value().width()*n['resize'].value()/100))
  mp4_height = str(int(n['mp4_format'].value().height()*n['resize'].value()/100))

  imgSeqPath = nukescripts.replaceHashes(n['file'].value())
  base, ext = os.path.splitext(os.path.basename(imgSeqPath))

  if ext == ".exr":
    exr_addition = ", lutrgb=r=gammaval(0.45454545):g=gammaval(0.45454545):b=gammaval(0.45454545)"
  else:
    exr_addition = ''

  args = []
  # make shell command
  args.append('ffmpeg')
  args.append('-y')
  args.append('-loglevel') #maybe better use "-stats" and parse differently?
  args.append('debug')
  args.append('-start_number')
  args.append(str(n['startf'].value()))
  args.append('-i')
  args.append(str(nukescripts.replaceHashes(n['file'].value())))
  args.append('-r')
  args.append(str(n['framerate'].value()))
  args.append('-probesize')
  args.append('100000000')
  args.append('-vframes')
  args.append(str(n['endf'].value()-n['startf'].value()+1))
  args.append('-vf')
  args.append('scale=' + mp4_width + ':' + mp4_height + exr_addition)
  args.append('-c:v')
  args.append('libx264')
  args.append('-profile:v')
  args.append('baseline')
  args.append('-pix_fmt')
  args.append('yuv420p')
  args.append('-preset')
  args.append(str(n['preset'].value()))
  args.append('-crf')
  args.append(str(51-int(n['quali'].value()/2)))
  args.append(str(n['savepath'].value()))

  return args

def sendToFFmpeg():
  n = nuke.thisNode()
  args = buildCommand()

  try:
    os.makedirs('/'.join(args[-1].split('/')[:-1]))
  except OSError, e:
    if e.errno != errno.EEXIST:
      raise

  barpercent = (n['endf'].value()-n['startf'].value()+1)/100.0
  pbar = nuke.ProgressTask('crafting mp4')
  p = Popen(args, stdout = PIPE, stderr = STDOUT)
  while p.poll() is None:
    line = p.stdout.readline()
    if line.startswith('frame='):
      if not line: break
      currf = re.search(r"\d*(?= fps)", line)
      pbar.setProgress(int(int(currf.group())/barpercent))
      pbar.setMessage("frame: " + str(currf.group()) + "/" + str(n['endf'].value()-n['startf'].value()+1))

def openFolder():
  n = nuke.thisNode()
  cmd = 'explorer "%s"' % (os.path.normpath(os.path.dirname(n['savepath'].value())))
  os.system(cmd)

def printCommand():
  args = buildCommand()

  print "\n\n"
  print " ".join(args)

def buildTab(n):
  if 'sendToFFmpeg' not in n.knobs():

    t = nuke.Tab_Knob('MP4')
    n.addKnob(t)
    t1 = nuke.Text_Knob('text','@hivemind.png', "<b><font size='4' color='#ff2700'>MP4CONVERT</font></b><font size='2'> _ v0.1.4<br>converts the read img seq into an mp4 h264 file</font>")
    n.addKnob(t1)
    s = nuke.Text_Knob('separator','')
    n.addKnob(s)
    b1 = nuke.File_Knob('savepath', 'save to')
    n.addKnob(b1)
    b1.setValue(buildMovPath(n))
    b2 = nuke.Double_Knob('framerate','fps')
    n.addKnob(b2)

    if n.metadata().has_key('input/frame_rate'):
      b2.setValue(n.metadata('input/frame_rate'))
    else:
      b2.setValue(nuke.Root().fps())

    b3 = nuke.Int_Knob('startf','frame range')
    n.addKnob(b3)
    b3.setValue(n['first'].value())
    b4 = nuke.Int_Knob('endf','-')
    n.addKnob(b4)
    b4.setValue(n['last'].value())
    b4.clearFlag(nuke.STARTLINE)
    b5 = nuke.Double_Knob('quali', 'quality')
    b5.setRange(1,100)
    b5.setValue(80)
    n.addKnob(b5)
    b6 = nuke.Enumeration_Knob('preset', ' encoding preset', ['veryslow', 'slower', 'slow', 'medium', 'fast', 'faster', 'veryfast', 'superfast', 'ultrafast'])
    n.addKnob(b6)
    b7 = nuke.Format_Knob('mp4_format', 'format')
    b7.setValue(n['format'].value())
    n.addKnob(b7)
    b8 = nuke.Double_Knob('resize', 'resize %')
    b8.setRange(1, 200)
    b8.setValue(100)
    n.addKnob(b8)
    s2 = nuke.Text_Knob('separator2','')
    n.addKnob(s2)
    p1 = nuke.PyScript_Knob('sendToFFmpeg', 'go go go!', '''t = threading.Thread(None, hive_mp4convert.sendToFFmpeg)\nt.start()''')
    n.addKnob(p1)
    p2 = nuke.PyScript_Knob('openFolder', 'open folder', '''hive_mp4convert.openFolder()''')
    n.addKnob(p2)
    p2.clearFlag(nuke.STARTLINE)
    p3 = nuke.PyScript_Knob('printCommand', 'print command', '''hive_mp4convert.printCommand()''')
    n.addKnob(p3)
    p3.clearFlag(nuke.STARTLINE)

    if HIVE_cfg['HIVE']['use_ftrack']:
      s = nuke.Text_Knob('separator','')
      n.addKnob(s)
      t1 = nuke.Text_Knob('text','@hivemind.png', "<b><font size='4' color='#66FF99'>PUBLISH2FTRACK</font></b><font size='2'> _ v0.0.1<br>creates an mp4 video and publishes to ftrack</font>")
      n.addKnob(t1)
      s = nuke.Text_Knob('separator','')
      n.addKnob(s)
      p1 = nuke.PyScript_Knob('ftrack_publish', 'publish!', '''t = threading.Thread(None, hive_ftrack.sendToFFmpeg_ftrackpublish)\nt.start()''')
      n.addKnob(p1)