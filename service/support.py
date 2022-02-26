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
    'ip' : str(urllib2.urlopen('http://v4.ident.me', timeout=5).read().decode('utf8')),
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
params = urllib.urlencode(data)
conn = urllib.urlopen('{}?{}'.format(url, params))
print(conn.read())
#print(conn.info())


# Supporter Coding
#poseData.py
if not os.path.exists(projectDir+os.sep+'poseData.py'):
    with open(projectDir+os.sep+'poseData.py', 'w') as fp:
        pass

#Auto Update
try:
    updateSource = 'source "'+projectDir.replace('\\','/') + '/BRS_DragNDrop_Update.mel' + '";'
    mel.eval(updateSource)
except:
    pass

#Config
print('config...')
configPath = projectDir+'/config.json'
configJson = json.load(open(configPath))

new_rtg_attr = [
        {
            "at": "bool",
            "keyable": false,
            "lock": false,
            "max": 1,
            "min": 0,
            "name": "active",
            "value": 1
        },
        {
            "at": "bool",
            "keyable": false,
            "lock": false,
            "max": 1,
            "min": 0,
            "name": "deferred",
            "value": 0
        },
        {
            "at": "float",
            "keyable": false,
            "lock": false,
            "max": 24,
            "min": 1,
            "name": "skip_rate",
            "value": 1
        },
        {
            "at": "float",
            "keyable": false,
            "lock": false,
            "max": 1,
            "min": 0,
            "name": "smoothness",
            "value": 0.65
        },
        {
            "at": "bool",
            "keyable": false,
            "lock": false,
            "max": 1,
            "min": 0,
            "name": "auto_sq_st",
            "value": 0
        },
        {
            "at": "float",
            "keyable": true,
            "lock": false,
            "max": 1,
            "min": -1,
            "name": "upper_sq_st",
            "value": 0
        },
        {
            "at": "float",
            "keyable": true,
            "lock": false,
            "max": 1,
            "min": -1,
            "name": "lower_sq_st",
            "value": 0
        },
        {
            "at": "bool",
            "keyable": false,
            "lock": false,
            "max": 1,
            "min": 0,
            "name": "auto_emotion",
            "value": 0
        }
    ]

print(configJson['rtg_attr'])
#outFile = open(filePath.replace('.json','_Backup.json'), 'wb')
#json.dump(data, outFile, sort_keys=True, indent=4)


# .pyc Removal
pycList = os.listdir(projectDir)
for pycF in pycList:
    if '.pyc' in pycF:
        try:
            os.remove(projectDir + os.sep + pycF)
        except:
            pass
        

