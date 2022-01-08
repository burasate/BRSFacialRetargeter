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

# Update
updateListURL = 'https://raw.githubusercontent.com/burasate/BRSFacialRetargeter/main/service/update.json'
updateFilePath = urllib2.urlopen(updateListURL, timeout=30).read()
fileNameSet = json.loads(updateFilePath)

gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar(gMainProgressBar,
                     edit=True,
                     beginProgress=True,
                     isInterruptable=False,
                     maxValue=len(fileNameSet) + 1)
for file in fileNameSet:
    cmds.progressBar(gMainProgressBar, edit=True, step=1,
                     status='initialize.. {}'.format(file.replace('.py', '')) )

    url = fileNameSet[file]
    urlReader = ''
    mainReader = ''
    try:
        mainReader = open(projectDir + os.sep + file, 'r').readlines()
    except:
        cmds.confirmDialog(title='Update Failed',
                           message='can\'t find \"{}\"\nPlease make sure path is correct\n'.format(file) + projectDir + os.sep,
                           button=['OK'])
    else:
        mainReader = open(projectDir + os.sep + file, 'r').readlines()
        mainWriter = open(projectDir + os.sep + file, 'w')
        try:
            urlReader = urllib2.urlopen(url, timeout=60).readlines()
            mainWriter.writelines(urlReader)
            mainWriter.close()
            #print('{} was loaded'.format(file.replace('.py', '').capitalize()))
        except:
            mainWriter.writelines(mainReader)
            mainWriter.close()
            cmds.confirmDialog(title='failed',
                               message='can\'t find \"{}\"\nPlease make sure path is correct\n'.format(file) + projectDir + os.sep,
                               button=['OK'])

# Finish
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
