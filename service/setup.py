"""
BRS FACIAL RETARGETER SHELF INSTALLER
"""
from maya import cmds
from maya import mel
import os, json
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

# -------------
# CREATE USER
# -------------
today = str(dt.date.today())
dataSet = {}

try:
    with open(userFile, 'r') as f:
        dataSet = json.load(f)
except:
    # Email Register
    while True:
        user = cmds.promptDialog(
            title='BRS Loc Delay Register',
            message='BRS Loc Delay Register\nConfirm Your Email',
            button=['Confirm'],
            defaultButton='Confirm',
            cancelButton='Cancel',
            dismissString='Cancel', bgc=(.2, .2, .2))
        if user == 'Confirm':
            dataSet['email'] = cmds.promptDialog(query=True, text=True)
        else:
            dataSet['email'] = ''

        if not dataSet['email'].__contains__('@') or not dataSet['email'].__contains__('.'):
            pass
        else:
            break

    # Create New Dataset
    dataSet['isTrial'] = True
    dataSet['registerDate'] = today
    dataSet['lastUsedDate'] = today
    dataSet['lastUpdate'] = today
    dataSet['days'] = 0
    dataSet['used'] = 0
    dataSet['version'] = ''

    # Create User
    with open(userFile, 'w') as f:
        json.dump(dataSet, f, indent=4)

finally:
    # Create Shelf
    topShelf = mel.eval('$nul = $gShelfTopLevel')
    currentShelf = cmds.tabLayout(topShelf, q=1, st=1)
    command = 'from BRSLocDelay import BRSLocDelaySystem \
    \nBRSLocDelaySystem.showBRSUI()'
    imagePath = projectDir + os.sep + 'BRSLocDelaySystem.png'
    cmds.shelfButton(stp='python', iol='DELAY', parent=currentShelf, ann='BRS LOCATOR DELAY SYSTEM', i=imagePath, c=command)

    # Finish
    cmds.confirmDialog(title='BRS LOCATOR DELAY', message='Installation Successful.', button=['OK'])
    exec ('from BRSLocDelay import BRSLocDelaySystem \
    \nBRSLocDelaySystem.showBRSUI()')
