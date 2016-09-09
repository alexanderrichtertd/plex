



import libShot
import libFileService


#************************
# REPORT
#************************
def setMetaData(shot, metaObj): 
    tmpShot = libShot.Shot()
    tmpShot.__dict__ = libShot.getShot(shot)

    # should check if one of the settings is empty then use the default (000)
    metaObj.setPlainText(tmpShot.__call__())


def setErrorCount(ui):
    ui.lblErrorCount.setText(str(len(libFileService.getFolderList(s.PATH["data_report"], "*.json"))))
