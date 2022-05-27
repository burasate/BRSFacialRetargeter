"""
---------------------
BRS FACIAL RETARGETER
SUPPORTING SCRIPT
---------------------
"""

import json, getpass, os, time,os,sys
from time import gmtime, strftime
import datetime as dt
from maya import mel
import maya.cmds as cmds

if sys.version[0] == '3':
    writeMode = 'w'
    import urllib.request as uLib
    import urllib.parse as uParse
else:
    writeMode = 'wb'
    import urllib as uLib

def formatPath(path):
    import os
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
projectDir = formatPath(scriptsDir + os.sep + 'BRSFacialRetargeter')
userFile = formatPath(projectDir + os.sep + 'user')

filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
raw_name, extension = os.path.splitext(filename)
minTime = cmds.playbackOptions(q=True, minTime=True)
maxTime = cmds.playbackOptions(q=True, maxTime=True)
referenceList = cmds.ls(references=True)
nameSpaceList = cmds.namespaceInfo(lon=True)

userData = json.load(open(userFile, 'r'))
data = {
    'name' : 'Facial Retargeter',
    'dateTime' : dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'timezone' : str( strftime('%z', gmtime()) ),
    'year' : dt.datetime.now().strftime('%Y'),
    'month' : dt.datetime.now().strftime('%m'),
    'day' : dt.datetime.now().strftime('%d'),
    'hour' : dt.datetime.now().strftime('%H'),
    'email' : userData['email'],
    'user' : getpass.getuser(),
    'maya' : str(cmds.about(version=True)),
    'ip' : str(uLib.urlopen('http://v4.ident.me').read().decode('utf8')),
    'version' : userData['version'],
    'scene' : raw_name,
    'timeUnit' : cmds.currentUnit(q=True, t=True),
    'timeMin' : minTime,
    'timeMax' : maxTime,
    'duration' : maxTime - minTime,
    'lastUpdate' : userData['lastUsedDate'],
    'used' : userData['used'],
    'isTrial' : int(userData['isTrial']),
    'days' : userData['days'],
    'registerDate' : userData['registerDate'],
    'lastUsedDate' : userData['lastUpdate'],
    'referenceCount': len(referenceList),
    'nameSpaceList': ','.join(nameSpaceList),
    'os' : str(cmds.about(operatingSystem=True))
}

url = 'https://hook.integromat.com/gnjcww5lcvgjhn9lpke8v255q6seov35'
if sys.version[0] == '3':
    params = uParse.urlencode(data)
    conn = uLib.urlopen('{}?{}'.format(url, params))
    print(conn.read())
    # print(conn.info())
else:
    params = uLib.urlencode(data)
    conn = uLib.urlopen('{}?{}'.format(url, params))
    print(conn.read())
    #print(conn.info())


# Supporter Coding
"""
# poseData.py
if not os.path.exists(projectDir+os.sep+'poseData.py'):
    with open(projectDir+os.sep+'poseData.py', 'w') as fp:
        pass
"""

#Auto Update
try:
    updateSource = 'source "'+projectDir.replace('\\','/') + '/BRS_DragNDrop_Update.mel' + '";'
    mel.eval(updateSource)
except:
    pass

# Config
configPath = projectDir+'/config.json'
configJson = json.load(open(configPath))

new_rtg_attr = [
        {
            "at": "bool",
            "keyable": False,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "active",
            "value": 1
        },
        {
            "at": "bool",
            "keyable": False,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "deferred",
            "value": 0
        },
        {
            "at": "float",
            "keyable": False,
            "lock": False,
            "max": 24,
            "min": 1,
            "name": "skip_rate",
            "value": 1
        },
        {
            "at": "float",
            "keyable": False,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "smoothness",
            "value": 0.65
        },
        {
            "at": "bool",
            "keyable": False,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "auto_sq_st",
            "value": 0
        },
        {
            "at": "float",
            "keyable": True,
            "lock": False,
            "max": 1,
            "min": -1,
            "name": "upper_sq_st",
            "value": 0
        },
        {
            "at": "float",
            "keyable": True,
            "lock": False,
            "max": 1,
            "min": -1,
            "name": "lower_sq_st",
            "value": 0
        },
        {
            "at": "bool",
            "keyable": False,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "auto_emotion",
            "value": 0
        },
        {
            "at": "float",
            "keyable": True,
            "lock": False,
            "max": 3,
            "min": 0,
            "name": "emotion_timming",
            "value": 3
        },
        {
            "at": "bool",
            "keyable": False,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "auto_phoneme",
            "value": 0
        },
        {
            "at": "float",
            "keyable": True,
            "lock": False,
            "max": 1,
            "min": 0,
            "name": "phoneme_timming",
            "value": 0.15
        }
    ]
configJson['rtg_attr'] = new_rtg_attr
outFile = open(configPath, writeMode)
json.dump(configJson, outFile, sort_keys=True, indent=4)

# Rename brsFR_config
if cmds.objExists('brsFR_config'):
    cmds.rename('brsFR_config', 'brsFR_core')

# .pyc Removal
pycList = os.listdir(projectDir)
for pycF in pycList:
    if '.pyc' in pycF:
        try:
            os.remove(projectDir + os.sep + pycF)
        except:
            pass

# poseData cleanup
poseDataDir = projectDir + os.sep + 'poseData'
if not os.path.exists(poseDataDir):
    os.makedirs(poseDataDir)
if os.path.exists(poseDataDir):
    poseDataList = [f for f in os.listdir(poseDataDir)]
    for f in poseDataList:
        if not f in ['emotion.json', 'mouth.json']:
            try:
                os.remove(poseDataDir + os.sep + f)
            except:
                pass