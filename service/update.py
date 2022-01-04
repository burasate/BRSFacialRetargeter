"""
BRS FACIAL RETARGETER UPDATER
"""
from maya import cmds
from maya import mel
import os, json, urllib2, getpass
import datetime as dt

def formatPath(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
projectDir = formatPath(scriptsDir + os.sep + 'BRSFacialRetargeter')
userFile = formatPath(projectDir + os.sep + 'user')

# print ('mayaAppDir = ' + mayaAppDir)
# print ('scriptsDir = ' + scriptsDir)
# print ('projectDir = ' + projectDir)
# print ('userSetupFile = ' + userFile)

"""
# Update
scriptUpdater = 'https://raw.py'
urlReader = ''
mainReader = ''
try:
    mainReader = open(projectDir + os.sep + 'BRSLocDelaySystem.py', 'r').readlines()
except:
    cmds.confirmDialog(title='Update Failed',
                       message='Could not find \"FacialRetargeter.py\"\nPlease make sure path is correct\n' + projectDir + os.sep,
                       button=['OK'])
else:
    mainReader = open(projectDir + os.sep + 'FacialRetargeter.py', 'r').readlines()
    mainWriter = open(projectDir + os.sep + 'FacialRetargeter.py', 'w')
    try:
        urlReader = urllib2.urlopen(scriptUpdater, timeout=60).readlines()
        mainWriter.writelines(urlReader)
        mainWriter.close()
        print('Update Successful')
        # cmds.confirmDialog(title='BRS FACIAL RETARGETER', message='Update Successful', button=['OK'])
    except:
        mainWriter.writelines(mainReader)
        mainWriter.close()
        print('Update Failed')
        cmds.confirmDialog(title='Update Failed',
                           message='Could not find \"FacialRetargeter.py\"\nPlease make sure path is correct\n' + projectDir + os.sep,
                           button=['OK'])

"""

# Finish
cmds.inViewMessage(amg='BRS FACIAL RETARGETER : Update <hl>Successful</hl>', pos='botCenter', fade=True,
                   fit=250, fst=2000, fot=250)
