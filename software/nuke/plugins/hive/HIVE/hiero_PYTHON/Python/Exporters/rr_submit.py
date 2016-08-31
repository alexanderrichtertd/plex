import hiero.core
import hiero.core.log as log
from hiero.core import *
from hiero.exporters.FnSubmission import Submission

import os
import sys
import time
from subprocess import Popen, PIPE, STDOUT

import PySide.QtCore
import PySide.QtGui

# Hiero RR submitter - based on the "rush_render_start_irush.py" example script

class rrRenderTask(hiero.core.TaskBase):
    def __init__(self, jobType, initDict, scriptPath, scenename, prio, seqdivmin, seqdivmax, senddisabled, seqcheck, overwritefiles):
        hiero.core.TaskBase.__init__(self, initDict)

        self._scriptPath = scriptPath
        self._finished = False
        self._progress = 0.0
        self._jobID = 0

        self.RR_scenename = scenename
        self.RR_prio = prio
        self.RR_seqdivmin = seqdivmin
        self.RR_seqdivmax = seqdivmax
        self.RR_senddisabled = senddisabled
        self.RR_seqcheck = seqcheck
        self.RR_overwritefiles = overwritefiles
        
        # Do different stuff to seqs and clips/trackitems
        if isinstance(self._item, Sequence):
            self._last = self._sequence.duration()-1
            self._start = 0
        elif isinstance(self._item, Clip) or isinstance(self._item, TrackItem):
            start, end = self.outputRange(ignoreRetimes=True,clampToSource=False)
            self._start = start
            self._last = end

        self._frameList = range(self._start, self._last+1)

    def sendToRR(self, scriptPath):
        """ submit nukefile to RR """

        scenename = 'Hiero'
        versionname = self.RR_scenename
        prio = str(self.RR_prio)
        seqDiv = '1'
        seqDivMin = str(self.RR_seqdivmin)
        seqDivMax = str(self.RR_seqdivmax)        
        createVideo = '0'        
        dontShowPreviewJpgs = '1'
        renderPreviewFirst = '0'
        previewImages = '0'

        if isinstance(self._item, Sequence):
          shotname = 'Seq'
        elif isinstance(self._item, Clip) or isinstance(self._item, TrackItem):
          shotname = 'Clip'

        if self.RR_senddisabled:
          sendDisabled = '1'
        else:
          sendDisabled = '0'          

        if self.RR_seqcheck:
          seqCheck = '1'
        else:
          seqCheck = '0'

        if self.RR_overwritefiles:
          overwriteFiles = '1'
        else:
          overwriteFiles = '0'

        dialog = False # use rrSubmitterconsole or UI

        rrPath = ''    
        if dialog:
            rrPath = os.environ['RR_Root']+"\\win__rrSubmitter.bat"
        else:
            rrPath = os.environ['RR_Root']+"\\bin\\win\\rrSubmitterconsole.exe"

        # make shell command
        args = []
        args.append(rrPath) # rrSubmitterconsole path
        args.append("\""+scriptPath+"\"") # nuke script path
        #following args are all optional
        args.append("CSCN=0~"+scenename) # scene-name
        args.append("CSHN=0~"+shotname) # shot-name
        args.append("CVN=0~"+versionname) # version-name
        args.append("Priority=1~"+prio) # priority
        args.append("SequenceDivide=1~"+seqDiv) # sequence devide
        args.append("SeqDivMINComp=1~"+seqDivMin) # sequence devide min
        args.append("SeqDivMAXComp=1~"+seqDivMax) # sequence devide max
        args.append("SendJobDisabled=1~"+sendDisabled) # submit job disabled
        args.append("PPCreateSmallVideo=1~"+createVideo) # create small web video
        args.append("PPSequenceCheck=1~"+seqCheck) # perform sequence check
        args.append("DoNotShotPreviewJpegs=0~"+dontShowPreviewJpgs) # show preview jpgs
        args.append("RenderPreviewFirst=1~"+renderPreviewFirst) # render preview images first
        args.append("NumberPreview=0~"+previewImages) # number of preview images
        args.append("Overwriteexistingfiles=0~"+overwriteFiles) # overwrite existing files on disk
        #args.append()

        cmd = ' '.join(args)
        print cmd
        p = Popen(cmd, stdout = PIPE, stderr = STDOUT)

    def startTask(self):
        # send out task to the FQ submitter

        if sys.platform in ['darwin','win32']:
            print hiero.ui.CodecSettings().quickTimeCodec()
        if sys.platform == 'linux2': 
            pass

        self.sendToRR(self._scriptPath)
 
    def taskStep(self):
        # Process is considered a Background task when taskStep returns False and progress is less than 1.0
        if self._finished == True:
            return True
        else:
            return False

    def finishTask(self):
        # currently useless because we set the progress to finsihed on submission...
        log.info(" ++ finished RR job ")
        pass
    
    def forcedAbort(self):
        # Abort will not affect the FQ render    
        log.info(" ++ Hiero abort does not affect RR render yet")
        pass

    def progress(self):
        """ get render process to set Hiero task progress bar """
        # if self._finished:
        #   return 1.0
        # return float(self._progress)

        return 1.0 #set finished

# Create a Submission and add our Task
class rrSubmission(Submission):
    def __init__(self):
        Submission.__init__(self)

    def initialise(self):
        """display the settings dialog"""

        dialog = RRsettingsDialog()
        self._ret, self.RR_scenename, self.RR_prio, self.RR_seqdivmin, self.RR_seqdivmax, self.RR_senddisabled, self.RR_seqcheck, self.RR_overwritefiles = dialog.exec_()

        if self._ret:
            dialogState = "accepted"
        else:
            dialogState = "rejected"

        log.debug("")
        log.debug("__________ RR settings dialog __________")
        log.debug("")
        log.debug("         accepted: %s", dialogState)
        log.debug("             name: %s", self.RR_scenename)
        log.debug("             prio: %s", self.RR_prio)
        log.debug("      seq dev min: %s", self.RR_seqdivmin)
        log.debug("      seq dev max: %s", self.RR_seqdivmax)
        log.debug("    send disabled: %s", self.RR_senddisabled)
        log.debug("   check sequence: %s", self.RR_seqcheck)
        log.debug("  overwrite files: %s", self.RR_overwritefiles)
        log.debug("")    

    def addJob(self, jobType, initDict, filePath):
        """ return out render task"""
        if self._ret:
            return rrRenderTask( Submission.kCommandLine, initDict, filePath, self.RR_scenename, self.RR_prio, self.RR_seqdivmin, self.RR_seqdivmax, self.RR_senddisabled, self.RR_seqcheck, self.RR_overwritefiles)
        else:
            # 2Do : still creates entries in hieros export cue ... shouldn't do that
            return 

class RRsettingsDialog(PySide.QtGui.QDialog):
    
    def __init__(self):
        PySide.QtGui.QDialog.__init__(self)
        self.build()

    def build(self):
        self.setWindowTitle("RR settings")
        self.setLayout(PySide.QtGui.QFormLayout())
        self.setWindowFlags(PySide.QtCore.Qt.CustomizeWindowHint | PySide.QtCore.Qt.WindowTitleHint) # gets rid of the close button

        self.header_text = PySide.QtGui.QLabel()
        self.header_text.setText("Hiero > RR submitter v0.1.3")
        self.header_text.setStyleSheet("QLabel {color: rgb(255, 50, 50); font-weight: bold;}")
        self.header_text.setAlignment(PySide.QtCore.Qt.AlignCenter)
        self.layout().addRow('', self.header_text)

        self.farm_settings = PySide.QtGui.QGroupBox("")
        self.farm_settings.setStyleSheet("QGroupBox {background-color: rgb(40, 40, 40); border: 1px solid rgb(150, 150, 150);}")
        #self.layout().addRow('FQ settings', self.farm_settings)

        self.layout().addRow('', self.farm_settings)
        
        #self.proc_edit = PySide.QtGui.QComboBox()        
        #self.proc_list = ['1','2','4','6','8','10','12'] # define the proc options
        #self.proc_edit.addItems(self.proc_list)
        #self.proc_edit.setCurrentIndex(1)

        self.scenename_label = PySide.QtGui.QLabel('task name')

        self.scenename_edit = PySide.QtGui.QLineEdit()
        self.scenename_edit.setText("Transcode")        

        self.prio_label = PySide.QtGui.QLabel('priority')

        self.prio_edit = PySide.QtGui.QSpinBox()
        self.prio_edit.setValue(20)
        self.prio_edit.setMinimum(1)
        self.prio_edit.setMaximum(99)
        self.prio_edit.setAlignment(PySide.QtCore.Qt.AlignRight)

        self.seq_label = PySide.QtGui.QLabel('seq devide')

        self.seqdivmin_label = PySide.QtGui.QLabel('min')

        self.seqdivmin_edit = PySide.QtGui.QSpinBox()
        self.seqdivmin_edit.setMaximum(10000)
        self.seqdivmin_edit.setValue(100)
        self.seqdivmin_edit.setMinimum(1)

        self.seqdivmax_label = PySide.QtGui.QLabel('max')

        self.seqdivmax_edit = PySide.QtGui.QSpinBox()
        self.seqdivmax_edit.setMaximum(10000)
        self.seqdivmax_edit.setValue(1000)
        self.seqdivmax_edit.setMinimum(1)

        self.sendDisabled_check = PySide.QtGui.QCheckBox()
        self.sendDisabled_check.setText("send jobs disabled")

        self.seqCheck_check = PySide.QtGui.QCheckBox()
        self.seqCheck_check.setText("check sequence")

        self.overwriteFiles_check = PySide.QtGui.QCheckBox()
        self.overwriteFiles_check.setText("overwrite files")

        self.grid = PySide.QtGui.QGridLayout(self.farm_settings)
        self.grid.setSpacing(10)

        self.grid.addWidget(self.scenename_label, 1, 0)
        self.grid.addWidget(self.scenename_edit, 1, 1)        

        self.grid.addWidget(self.prio_label, 2, 0)
        self.grid.addWidget(self.prio_edit, 2, 1)
        self.grid.addWidget(self.seq_label, 3, 0)

        self.hlayout = PySide.QtGui.QHBoxLayout()        
        self.hlayout.addWidget(self.seqdivmin_label)
        self.hlayout.addWidget(self.seqdivmin_edit)       
        self.hlayout.addWidget(self.seqdivmax_label)
        self.hlayout.addWidget(self.seqdivmax_edit)

        self.grid.addLayout(self.hlayout, 3, 1)        
        
        self.grid.addWidget(self.sendDisabled_check, 4, 1)
        self.grid.addWidget(self.seqCheck_check, 5, 1)
        self.grid.addWidget(self.overwriteFiles_check, 6, 1)

        #buttonbox = PySide.QtGui.QDialogButtonBox(PySide.QtGui.QDialogButtonBox.StandardButton.Ok | PySide.QtGui.QDialogButtonBox.StandardButton.Cancel)    
        self.buttonbox = PySide.QtGui.QDialogButtonBox(PySide.QtGui.QDialogButtonBox.StandardButton.Ok)
        self.buttonbox.button(PySide.QtGui.QDialogButtonBox.StandardButton.Ok).setText("submit to RR")
        self.buttonbox.button(PySide.QtGui.QDialogButtonBox.StandardButton.Ok).setAutoDefault(True)
        
        self.buttonbox.accepted.connect(self.acceptDialog)
        self.buttonbox.rejected.connect(self.rejectDialog)
        self.layout().addWidget(self.buttonbox)

    def acceptDialog(self):    
        self.accept()

    def rejectDialog(self):
        pass

    def exec_(self):
        if PySide.QtGui.QDialog.exec_(self) == PySide.QtGui.QDialog.Accepted:
            return [1,
                    self.scenename_edit.text(),
                    self.prio_edit.value(),
                    self.seqdivmin_edit.value(),
                    self.seqdivmax_edit.value(),
                    self.sendDisabled_check.isChecked(),
                    self.seqCheck_check.isChecked(),
                    self.overwriteFiles_check.isChecked()]
        else:
            #pressed cancel or closed the "fq settings dialog"
            return [0,0,0,0,0,0,0,0]

# Add the Custom Task Submission to the Export Queue           
registry = hiero.core.taskRegistry
registry.addSubmission( "send to RR", rrSubmission )