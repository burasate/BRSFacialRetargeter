"""
---------------------
BRS FACIAL RETARGETER
SUPPORTING SCRIPT
---------------------
"""

import json, getpass, os, time,urllib,os,sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds


def formatPath(path):
    import os
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
projectDir = formatPath(scriptsDir + os.sep + 'BRSFacialRetargeter')
userFile = formatPath(projectDir + os.sep + 'user')




# Supporter Coding
print('Supporter is working now')

try:
    updateSource = 'source "'+projectDir.replace('\\','/') + '/BRS_DragNDrop_Update.mel' + '";'
    mel.eval(updateSource)
except:
    pass

# .pyc Removal
pycList = os.listdir(projectDir)
for pycF in pycList:
    if '.pyc' in pycF:
        try:
            os.remove(projectDir + os.sep + pycF)
        except:
            pass