"""
BRS FACIAL RETARGETER SHELF INSTALLER
"""
from maya import cmds
from maya import mel
import os, json, getpass
import datetime as dt

def formatPath(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

#mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
#scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
#projectDir = formatPath(scriptsDir + os.sep + 'BRSFacialRetargeter')

try:
    tool_dir = os.path.dirname(os.path.abspath(__file__))
except:
    maya_app_dir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
    scripts_dir = formatPath(os.path.abspath(maya_app_dir + os.sep + 'scripts'))
    tool_dir = formatPath(os.path.abspath(scripts_dir + os.sep + 'BRSFacialRetargeter'))
finally:
    user_file = formatPath(tool_dir + os.sep + 'user')

# -------------
# CREATE USER
# -------------
today = str(dt.date.today())
dataSet = {}

try:
    with open(user_file, 'r') as f:
        dataSet = json.load(f)
except:
    # Email Register
    while True:
        user = cmds.promptDialog(
            title='BRS',
            message='BRS Register - Please Confirm Your Email',
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
    dataSet['user'] = getpass.getuser()

    # Create User
    with open(user_file, 'w') as f:
        json.dump(dataSet, f, indent=4)

finally:
    # Create Shelf
    topShelf = mel.eval('$nul = $gShelfTopLevel')
    currentShelf = cmds.tabLayout(topShelf, q=1, st=1)
    command = 'import imp\n' \
              'try:\n' \
              '    imp.reload(FacialRetargeter)\n' \
              '    imp.reload(FacialRetargeter.reTargeter)\n' \
              '    imp.reload(FacialRetargeter.poseLib)\n' \
              '    imp.reload(FacialRetargeter.updater)\n' \
              '    FacialRetargeter.showUI()\n' \
              'except:\n' \
              '    from BRSFacialRetargeter import FacialRetargeter\n' \
              '    FacialRetargeter.showUI()'

    imagePath = projectDir + os.sep + 'BRSFacialRetargeter.png'
    cmds.shelfButton(stp='python', iol='FR', parent=currentShelf, ann='BRS FACIAL RETARGETER', i=imagePath, c=command)

    # Finish
    cmds.confirmDialog(title='BRS FACIAL RETARGETER', message='Installation Successful.', button=['OK'])
    exec (command)
