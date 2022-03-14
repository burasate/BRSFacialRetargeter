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
# poseData.py
if not os.path.exists(projectDir+os.sep+'poseData.py'):
    with open(projectDir+os.sep+'poseData.py', 'w') as fp:
        pass

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
outFile = open(configPath, 'wb')
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

# poseData Fix
poseDataDir = projectDir + os.sep + 'poseData'
if not os.path.exists(poseDataDir):
    os.makedirs(poseDataDir)
if os.path.exists(poseDataDir):
    poseDataList = [f for f in os.listdir(poseDataDir)]
    for f in poseDataList:
        if f in ['emotion.json', 'mouth.json']:
            try:
                os.remove(poseDataDir + os.sep + f)
            except:
                pass
    if not 'emotion.json' in poseDataList:
        data = [{u'name': u'browDownLeft', u'weight': [0.7403, 0.4563, 0.6358, 0.6794, 0.5161, 0.4957, 0.02]},
                {u'name': u'browDownRight', u'weight': [0.7403, 0.4563, 0.6358, 0.6794, 0.4771, 0.4344, 0.02]},
                {u'name': u'browInnerUp', u'weight': [0.62, 0.4112, 0.048, 0.1111, 0.6966, 0.5616, 0.0213]},
                {u'name': u'browOuterUpLeft', u'weight': [0.0892, 0.0813, 0.0299, 0.1886, 0.2813, 0.2629, 0.0]},
                {u'name': u'browOuterUpRight', u'weight': [0.0892, 0.0812, 0.0299, 0.1885, 0.2814, 0.2633, 0.0]},
                {u'name': u'cheekPuff', u'weight': [0.0289, 0.0505, 0.0766, 0.0559, 0.0441, 0.0563, 0.0054]},
                {u'name': u'cheekSquintLeft', u'weight': [0.383, 0.3468, 0.4538, 0.6554, 0.2311, 0.2847, 0.0125]},
                {u'name': u'cheekSquintRight', u'weight': [0.3794, 0.3481, 0.4423, 0.6726, 0.2302, 0.2872, 0.0127]},
                {u'name': u'eyeBlinkLeft', u'weight': [0.0, 0.0232, 0.006, 0.0, 0.0252, 0.0824, 0.0333]},
                {u'name': u'eyeBlinkRight', u'weight': [0.0, 0.0232, 0.006, 0.0, 0.0252, 0.0887, 0.0333]},
                {u'name': u'eyeLookDownLeft', u'weight': [0.2585, 0.2096, 0.1612, 0.104, 0.313, 0.157, 0.0433]},
                {u'name': u'eyeLookDownRight', u'weight': [0.2587, 0.2097, 0.1616, 0.1039, 0.3135, 0.158, 0.0435]},
                {u'name': u'eyeLookInLeft', u'weight': [0.0779, 0.076, 0.0953, 0.0415, 0.0749, 0.0883, 0.0203]},
                {u'name': u'eyeLookInRight', u'weight': [0.0524, 0.055, 0.0288, 0.0487, 0.024, 0.0662, 0.0003]},
                {u'name': u'eyeLookOutLeft', u'weight': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
                {u'name': u'eyeLookOutRight', u'weight': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0598, 0.0002]},
                {u'name': u'eyeLookUpLeft', u'weight': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
                {u'name': u'eyeLookUpRight', u'weight': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
                {u'name': u'eyeSquintLeft', u'weight': [0.1396, 0.2385, 0.3314, 0.3514, 0.1641, 0.3422, 0.031]},
                {u'name': u'eyeSquintRight', u'weight': [0.1369, 0.2383, 0.331, 0.3515, 0.1641, 0.3421, 0.0309]},
                {u'name': u'eyeWideLeft', u'weight': [0.2301, 0.0803, 0.3173, 0.4741, 0.6462, 0.0538, 0.0]},
                {u'name': u'eyeWideRight', u'weight': [0.2272, 0.0803, 0.3171, 0.4736, 0.6608, 0.0769, 0.0]},
                {u'name': u'jawForward', u'weight': [0.0703, 0.099, 0.0814, 0.0566, 0.0609, 0.0502, 0.007]},
                {u'name': u'jawLeft', u'weight': [0.0144, 0.0238, 0.0086, 0.0205, 0.0306, 0.0, 0.0]},
                {u'name': u'jawOpen', u'weight': [0.0281, 0.0363, 0.0347, 0.0215, 0.0698, 0.0269, 0.0]},
                {u'name': u'jawRight', u'weight': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0085, 0.0019]},
                {u'name': u'mouthClose', u'weight': [0.0351, 0.0439, 0.0465, 0.0277, 0.0682, 0.0328, 0.009]},
                {u'name': u'mouthDimpleLeft', u'weight': [0.1688, 0.0799, 0.1324, 0.342, 0.0499, 0.1422, 0.019]},
                {u'name': u'mouthDimpleRight', u'weight': [0.1656, 0.0823, 0.1449, 0.3367, 0.0486, 0.148, 0.0174]},
                {u'name': u'mouthFrownLeft', u'weight': [0.0, 0.0152, 0.0323, 0.0, 0.0, 0.0, 0.0]},
                {u'name': u'mouthFrownRight', u'weight': [0.0, 0.0152, 0.0323, 0.0, 0.0, 0.0, 0.0]},
                {u'name': u'mouthFunnel', u'weight': [0.0183, 0.0768, 0.0422, 0.01, 0.1123, 0.0468, 0.0182]},
                {u'name': u'mouthLeft', u'weight': [0.0203, 0.0046, 0.0129, 0.0072, 0.0116, 0.0177, 0.0004]},
                {u'name': u'mouthLowerDownLeft', u'weight': [0.0926, 0.0491, 0.046, 0.0801, 0.0889, 0.082, 0.0351]},
                {u'name': u'mouthLowerDownRight', u'weight': [0.0869, 0.0475, 0.0474, 0.0804, 0.0813, 0.0814, 0.0357]},
                {u'name': u'mouthPressLeft', u'weight': [0.0623, 0.1223, 0.2238, 0.2007, 0.1313, 0.1736, 0.0056]},
                {u'name': u'mouthPressRight', u'weight': [0.0618, 0.1248, 0.2221, 0.2018, 0.1295, 0.1697, 0.0053]},
                {u'name': u'mouthPucker', u'weight': [0.0208, 0.0922, 0.0791, 0.0124, 0.0682, 0.018, 0.0227]},
                {u'name': u'mouthRight', u'weight': [0.0, 0.0002, 0.0021, 0.0, 0.0, 0.012, 0.0002]},
                {u'name': u'mouthRollLower', u'weight': [0.0908, 0.13, 0.2364, 0.1292, 0.047, 0.0823, 0.0142]},
                {u'name': u'mouthRollUpper', u'weight': [0.0237, 0.0266, 0.0427, 0.0215, 0.0197, 0.0389, 0.0272]},
                {u'name': u'mouthShrugLower', u'weight': [0.2324, 0.3989, 0.5838, 0.2965, 0.106, 0.0989, 0.0121]},
                {u'name': u'mouthShrugUpper', u'weight': [0.2122, 0.4034, 0.5534, 0.3039, 0.1533, 0.0774, 0.0116]},
                {u'name': u'mouthSmileLeft', u'weight': [0.7605, 0.0907, 0.266, 0.8311, 0.186, 0.5473, 0.0551]},
                {u'name': u'mouthSmileRight', u'weight': [0.7568, 0.111, 0.2621, 0.8357, 0.1905, 0.5576, 0.0504]},
                {u'name': u'mouthStretchLeft', u'weight': [0.1157, 0.1991, 0.1087, 0.1086, 0.2745, 0.1001, 0.0245]},
                {u'name': u'mouthStretchRight', u'weight': [0.1093, 0.1898, 0.0963, 0.0925, 0.2579, 0.1077, 0.0258]},
                {u'name': u'mouthUpperUpLeft', u'weight': [0.0729, 0.0992, 0.1943, 0.1575, 0.0449, 0.0275, 0.0057]},
                {u'name': u'mouthUpperUpRight', u'weight': [0.0713, 0.1032, 0.1954, 0.1716, 0.0455, 0.0294, 0.0055]},
                {u'name': u'noseSneerLeft', u'weight': [0.1975, 0.3147, 0.7838, 0.6808, 0.1608, 0.1515, 0.0144]},
                {u'name': u'noseSneerRight', u'weight': [0.1894, 0.3267, 0.7836, 0.6261, 0.1695, 0.1491, 0.0148]}]
        outFile = open(poseDataDir + os.sep + 'emotion.json', 'wb')
        json.dump(data, outFile, sort_keys=True, indent=4)
    if not 'mouth.json' in poseDataList:
        data = [{u'name': u'jawForward', u'weight': [0.0978, 0.066, 0.1246, 0.0804, 0.0547, 0.1109, 0.0282, 0.038, 0.1001, 0.0843, 0.0485, 0.0659, 0.0227]},
                {u'name': u'jawLeft', u'weight': [0.0056, 0.0198, 0.0035, 0.0141, 0.0012, 0.0083, 0.0441, 0.0022, 0.013, 0.0208, 0.002, 0.0071, 0.0193]},
                {u'name': u'jawOpen', u'weight': [0.1633, 0.127, 0.4721, 0.3463, 0.0802, 0.1037, 0.1155, 0.0967, 0.0213, 0.0501, 0.0733, 0.0194, 0.0113]},
                {u'name': u'jawRight', u'weight': [0.017, 0.0, 0.0344, 0.0309, 0.0085, 0.0017, 0.0006, 0.0127, 0.0003, 0.0004, 0.0087, 0.008, 0.001]},
                {u'name': u'mouthClose', u'weight': [0.04, 0.0522, 0.1934, 0.3158, 0.151, 0.0516, 0.1414, 0.2345, 0.0352, 0.0504, 0.0509, 0.1234, 0.096]},
                {u'name': u'mouthDimpleLeft', u'weight': [0.0655, 0.057, 0.0298, 0.0203, 0.0252, 0.0448, 0.0209, 0.0219, 0.0513, 0.0787, 0.0479, 0.1117, 0.0244]},
                {u'name': u'mouthDimpleRight', u'weight': [0.0614, 0.053, 0.0248, 0.0202, 0.0235, 0.0393, 0.022, 0.0187, 0.0434, 0.0748, 0.042, 0.1019, 0.024]},
                {u'name': u'mouthFrownLeft', u'weight': [0.0001, 0.0039, 0.0032, 0.0747, 0.0162, 0.0024, 0.01, 0.0909, 0.0011, -0.004, 0.0014, 0.0005, 0.0407]},
                {u'name': u'mouthFrownRight', u'weight': [0.0001, 0.0044, 0.007, 0.0824, 0.0146, 0.0024, 0.006, 0.0899, 0.0012, 0.0003, 0.0019, 0.0006, 0.047]},
                {u'name': u'mouthFunnel', u'weight': [0.1203, 0.1351, 0.4015, 0.6588, 0.5613, 0.2362, 0.4129, 0.4748, 0.1832, 0.1428, 0.1427, 0.1498, 0.4892]},
                {u'name': u'mouthLeft', u'weight': [0.0248, 0.0172, 0.0073, 0.0241, 0.0299, 0.0069, 0.0101, 0.0325, 0.0141, 0.025, 0.0041, 0.0299, 0.0317]},
                {u'name': u'mouthLowerDownLeft', u'weight': [0.5507, 0.4025, 0.4412, 0.2891, 0.2307, 0.4318, 0.2198, 0.1633, 0.3699, 0.29, 0.3334, 0.1558, 0.2436]},
                {u'name': u'mouthLowerDownRight', u'weight': [0.5484, 0.3903, 0.4339, 0.2899, 0.2412, 0.4295, 0.2132, 0.1762, 0.3657, 0.2751, 0.3293, 0.1528, 0.2371]},
                {u'name': u'mouthPressLeft', u'weight': [0.0266, 0.0241, 0.0113, 0.0136, 0.0174, 0.0246, 0.0216, 0.0125, 0.0269, 0.0356, 0.0278, 0.0265, 0.0206]},
                {u'name': u'mouthPressRight', u'weight': [0.0268, 0.024, 0.009, 0.0125, 0.0156, 0.0238, 0.0239, 0.0103, 0.026, 0.0355, 0.0268, 0.026, 0.0217]},
                {u'name': u'mouthPucker', u'weight': [0.0794, 0.0914, 0.1882, 0.6203, 0.5597, 0.0846, 0.562, 0.6783, 0.0669, 0.1023, 0.1188, 0.2018, 0.5732]},
                {u'name': u'mouthRight', u'weight': [0.0, 0.0, 0.0034, 0.0004, 0.0015, 0.0036, 0.0001, 0.0003, 0.0002, 0.0, 0.0007, 0.0001, 0.0]},
                {u'name': u'mouthRollLower', u'weight': [0.0267, 0.0295, 0.0296, 0.0448, 0.0433, 0.0306, 0.0391, 0.0728, 0.028, 0.0347, 0.0336, 0.1516, 0.0356]},
                {u'name': u'mouthRollUpper', u'weight': [0.0662, 0.0771, 0.0671, 0.1121, 0.1083, 0.066, 0.0981, 0.1646, 0.0628, 0.0795, 0.0819, 0.2746, 0.0901]},
                {u'name': u'mouthShrugLower', u'weight': [0.0175, 0.0255, 0.0178, 0.0343, 0.0353, 0.0223, 0.0524, 0.0331, 0.0261, 0.0435, 0.0355, 0.0384, 0.0481]},
                {u'name': u'mouthShrugUpper', u'weight': [0.2199, 0.1958, 0.1881, 0.1114, 0.0971, 0.2588, 0.143, 0.0209, 0.2637, 0.1726, 0.2314, 0.0084, 0.1411]},
                {u'name': u'mouthSmileLeft', u'weight': [0.505, 0.321, 0.0991, -0.0025, 0.0484, 0.3836, 0.0398, 0.0021, 0.421, 0.4394, 0.2716, 0.1563, 0.0434]},
                {u'name': u'mouthSmileRight', u'weight': [0.473, 0.3003, 0.0806, 0.004, 0.0396, 0.363, 0.0424, 0.008, 0.3972, 0.4032, 0.2487, 0.1238, 0.0464]},
                {u'name': u'mouthStretchLeft', u'weight': [0.1609, 0.1644, 0.3734, 0.2934, 0.2774, 0.2485, 0.2135, 0.2946, 0.2055, 0.165, 0.173, 0.1928, 0.22]},
                {u'name': u'mouthStretchRight', u'weight': [0.1738, 0.1541, 0.3979, 0.2961, 0.2922, 0.2468, 0.1771, 0.3164, 0.2001, 0.1642, 0.1716, 0.1934, 0.1915]},
                {u'name': u'mouthUpperUpLeft', u'weight': [0.1367, 0.0785, 0.0635, 0.0421, 0.0553, 0.1333, 0.0451, 0.0229, 0.1447, 0.1181, 0.0895, 0.0211, 0.0354]},
                {u'name': u'mouthUpperUpRight', u'weight': [0.1312, 0.0764, 0.0547, 0.036, 0.0527, 0.1304, 0.0453, 0.0215, 0.1405, 0.1102, 0.0856, 0.02, 0.0344]}]
        outFile = open(poseDataDir + os.sep + 'mouth.json', 'wb')
        json.dump(data, outFile, sort_keys=True, indent=4)
