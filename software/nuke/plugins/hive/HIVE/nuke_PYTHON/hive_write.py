"""
    Hive Nuke environment
    hive_write.py

    create and manage hive_write nodes

    version: v0.0.1
    date:    20151001
    by:      Carl Schroter

    2Do:
"""

import sys, os, json, re
import nuke, nukescripts
import hive_functions
from vuRenderThreads.plugin_nuke import plugin_nuke as vuRenderThreadsNuke
import SendToRoyalRender

HIVE = os.getenv('HIVE')
with open(HIVE + '/HIVE_cfg.json') as data_file:
  HIVE_cfg = json.load(data_file)

def HIVE_getProjectName():
  return HIVE_cfg['project_name']

def HIVE_getProjectLogo():
  return os.getenv('HIVE') + "/" + HIVE_cfg['project_logo']

def HIVE_getProjectLogoSize():
  return float(HIVE_cfg['project_logo_size'])

def HIVE_writerKnobChanged(tn, kn):

  if kn == 'letterbox':
    if tn['letterbox'].value() == 'none':
      #tn\['letterbox_ratio'].setVisible(False)
      tn['letterbox_ratio'].setFlag(nuke.INVISIBLE)
      tn['letterbox_opacity'].setFlag(nuke.DISABLED)
    elif tn['letterbox'].value() == 'custom':
      #tn\['letterbox_ratio'].setVisible(True)
      tn['letterbox_ratio'].clearFlag(nuke.INVISIBLE)
      tn['letterbox_opacity'].clearFlag(nuke.DISABLED)
      pass
    else:
      #tn\['letterbox_ratio'].setVisible(False)
      tn['letterbox_ratio'].setFlag(nuke.INVISIBLE)
      tn['letterbox_opacity'].clearFlag(nuke.DISABLED)
      lb_xy = tn['letterbox'].value().split(':')
      tn['letterbox_ratio'].setValue(float(lb_xy[0]),0)
      tn['letterbox_ratio'].setValue(float(lb_xy[1]),1)

  elif kn == 'render_via':
    if tn['render_via'].value() == 'vuRenderThreads':
      tn['render_threads'].clearFlag(nuke.INVISIBLE)
    else:
      tn['render_threads'].setFlag(nuke.INVISIBLE)

  elif kn in ['burnin_watermark_text', 'burnin_watermark', 'burnin_status', 'letterbox_ratio', 'burnin_font_size', 'jpg_path', 'HIVE_WRITER', 'render_via', 'burnin_tab', 'burnin_date', 'burnin_color', 'jpg_write', 'exr_path', 'burnin_watermark_size', 'letterbox_opacity', 'burnin_version', 'letterbox', 'burnin_time', 'render_btn', 'status', 'exr_label', 'burnin_margin_ctrl', 'burnin_comment_text', 'burnin_logo_size', 'render_threads', 'burnin_projectname_mult', 'burnin_color_panelDropped', 'burnin_watermark_opacity', 'jpg_label', 'burnin_label', 'jpg_btn1', 'burnin_comment_check', 'burnin_project', 'exr_btn1', 'exr_write', 'burnin_font', 'valid', 'burnin_frames', 'burnin_logo']:
    try:
      tn['jpg_path'].setValue(HIVE_buildWriterPath(tn, 'jpg'))
      tn['exr_path'].setValue(HIVE_buildWriterPath(tn, 'exr'))
    except:
      nuke.tprint('\nHIVE :: failed to build writerpath')

def HIVE_buildWriterPath(tn, ext):
  #E:\060_Shots\DM_020\100_DM_020_COMP\DM_020_COMP_OUT\DM_020_comp_v001_cs\1920x1080_exr\DM_020_comp_v001_cs.4475.exr

  if nuke.root().name() == 'Root': #saved before
    return False

  scriptpath = nuke.root().name()

  nameparts = hive_functions.HIVE_splitBasename(scriptpath)

  write_path = re.sub('COMP_WORK', 'COMP_OUT', scriptpath)
  write_path = re.sub('.nk', '/', write_path)
  write_path += str(tn.input(0).format().width()) + "x" + str(tn.input(0).format().height()) + "_EXT/"
  write_path += "_".join(nameparts[:-1]) + ".%0" + HIVE_cfg['padding'] + "d.EXT"

  write_path = re.sub('EXT', ext, write_path)
  return write_path

def HIVE_writerRender(n):

  if hive_functions.HIVE_pipelineConform():
    if hive_functions.HIVE_pipelineConform(n['jpg_path'].value()):

      first_frame = int(nuke.root()['first_frame'].value())
      last_frame = int(nuke.root()['last_frame'].value())

      # writeNodes2render = []
      # for i in nuke.allNodes('Write', group=n):
      #   if not i['disable'].value():
      #     if i.name().endswith('exr'):
      #       i['file'].setValue(n['exr_path'].value())
      #     elif i.name().endswith('jpg'):
      #       i['file'].setValue(n['jpg_path'].value())

      # for i in nuke.allNodes('H_write'):
      #     writeNodes2render.append(i.name())

      if n['render_via'].value() == 'local':
        #print "render go! local"

        nuke.execute(nuke.thisNode(),start=first_frame,end=last_frame,incr=1)

      elif n['render_via'].value() == 'vuRenderThreads':
        #print "render go! vuRenderThreads"

        numRenderThreads = int(n['render_threads'].value())

        #createThreads(frameStart, frameEnd, numThreads, writeNodes=None)
        vuRenderThreadsNuke.createThreads(first_frame, last_frame, numRenderThreads, [n.name()])

      elif n['render_via'].value() == 'RoyalRender':
        #print "render go! RR"


        HIVE_rrSubmitNuke5(n, nuke.root().name(), first_frame, last_frame) #no userdetail/comment for now

    else:
      nuke.message("<b><font size='4' color='#FF0066'>OBEY THE PIPELINE!</fon></b>\nRethink and try again.")
  else:
    nuke.message("<b><font size='4' color='#FF0066'>OBEY THE PIPELINE!</fon></b>\nRethink and try again.")


def HIVE_rrSubmitNuke5(n, scriptName, first_frame='', last_frame=''):

  #maybe save to a different location for rr to copy script from
  nuke.scriptSave()

  ##RUGBYBUGS EDIT
  # rrRoot = os.environ['RR_Root']

  # if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
  #   os.system(rrRoot+"\\win__rrSubmitter.bat  \""+scriptName+"\" \"CSCN=0~"+shotdetail+"\" \"CSHN=0~"+versiondetail+"\" \"CVN=0~"+artistdetail+"\" \"CustomUserInfo=AC~"+userdetail+"\" \"SendJobDisabled=1~1\"") #- SHOT VERSION
  # elif (sys.platform.lower() == "darwin"):
  #   os.system(rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter  \""+scriptName+"\"")
  # else:
  #   os.system(rrRoot+"/lx__rrSubmitter.sh  \""+scriptName+"\"")

###############################

  # node = nuke.thisNode()
  # nuke.scriptSave()

  # newJob = SendToRoyalRender.rrJob()
  # SendToRoyalRender.rrSubmit_fillGlobalSceneInfo(newJob)

  # newJob.layer= node['name'].value()

  # newJob.seqStart = nodes[0]['first'].value()
  # newJob.seqEnd = nodes[0]['last'].value()
  # newJob.isActive = True


  # mainDone = False
  # for wNode in nodes:
  #   Type = wNode["file"].value()[-4:-1]
  #   fileName = node["value_outPath" + Type].value()

  #   if not mainDone:
  #     newJob.imageFileName = fileName
  #     mainDone = True
  #   else:
  #     newJob.maxChannels += 1
  #     newJob.channelFileName.append(fileName)
  #     newJob.channelExtension.append("." + Type.lower())

  # submitOptions="AllowLocalSceneCopy=0~0"
  # SendToRoyalRender.submitJobsToRR([newJob],submitOptions)

  nuke.scriptSave()
  newJob = SendToRoyalRender.rrJob()
  SendToRoyalRender.rrSubmit_fillGlobalSceneInfo(newJob)

  newJob.layer = n.name()
  newJob.seqStart = first_frame
  newJob.seqEnd = last_frame
  newJob.isActive = True
  newJob.imageFileName = n['jpg_path'].value()

  if n['exr_write'].value():
    newJob.maxChannels += 1
    newJob.channelFileName.append(n['exr_path'].value())
    newJob.channelExtension.append(".exr")


  # for i in nuke.allNodes('Write', group=n):
  #   if not i['disable'].value():

  #     # if i.name().endswith('exr'):
  #     #   i['file'].setValue(n['exr_path'].value())
  #     # elif i.name().endswith('jpg'):
  #     #   i['file'].setValue(n['jpg_path'].value())


  #     newJob.imageFileName = i['file'].getEvaluatedValue()

  #     rrJobs.append(newJob)



  details = hive_functions.HIVE_splitBasename(scriptName)

  args = []
  args.append("CSCN=0~"+details[0]) # scene-name
  args.append("CSHN=0~"+details[1]) # shot-name
  args.append("CVN=0~"+details[3]) # version-name
  args.append("Priority=1~"+'50') # priority
  # args.append("SequenceDivide=1~"+seqDiv) # sequence devide
  # args.append("SeqDivMINComp=1~"+seqDivMin) # sequence devide min
  # args.append("SeqDivMAXComp=1~"+seqDivMax) # sequence devide max
  # args.append("SendJobDisabled=1~"+sendDisabled) # submit job disabled
  args.append("PPCreateSmallVideo=1~"+'0') # create small web video
  args.append("PPSequenceCheck=1~"+'0') # perform sequence check
  args.append("DoNotShotPreviewJpegs=0~"+'0') # show preview jpgs
  args.append("RenderPreviewFirst=1~"+'1') # render preview images first
  args.append("NumberPreview=0~"+'5') # number of preview images
  # args.append("Overwriteexistingfiles=0~"+overwriteFiles) # overwrite existing files on disk
  args.append("AllowLocalSceneCopy=0~"+'0') #copy script to render-machine

  submitOptions = ' '.join(args)
  SendToRoyalRender.submitJobsToRR([newJob],submitOptions)