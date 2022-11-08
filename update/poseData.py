"""
POSE DATA
"""

import json, os, time, sys
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))

"""
Init
"""
if sys.version[0] == '3':
    writeMode = 'w'
else:
    writeMode = 'w'

poseData = [
    {
        "id" : "001",
        "name" : "base",
        "sets" : "base",
        "type" : "base"
    },
    {
        "id" : "002",
        "name" : "joyful",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "003",
        "name" : "sad",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "004",
        "name" : "mad",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "005",
        "name" : "powerful",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "006",
        "name" : "scared",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "007",
        "name" : "peaceful",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "008",
        "name" : "natural",
        "sets" : "all",
        "type" : "expression"
    },
    {
        "id" : "051",
        "name" : "AAA",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "052",
        "name" : "Eh",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "053",
        "name" : "AHH",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "054",
        "name" : "OHH",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "055",
        "name" : "UUU",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "056",
        "name" : "IEE",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "057",
        "name" : "RRR",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "058",
        "name" : "WWW",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : True
    },
    {
        "id" : "059",
        "name" : "SSS",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : False
    },
    {
        "id" : "060",
        "name" : "FFF",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : False
    },
    {
        "id" : "061",
        "name" : "TTH",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : False
    },
    {
        "id" : "062",
        "name" : "BP",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : False
    },
    {
        "id" : "063",
        "name" : "SSH",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : False
    },
    {
        "id" : "064",
        "name" : "M",
        "sets" : "mouth_all",
        "type" : "phoneme",
        "jaw_open" : False
    },
    {
        "id" : "101",
        "name" : "browDownLeft",
        "sets" : "brow",
        "type" : "blendshape"
    },
    {
        "id" : "102",
        "name" : "browDownRight",
        "sets" : "brow",
        "type" : "blendshape"
    },
    {
        "id" : "103",
        "name" : "browInnerUp",
        "sets" : "brow",
        "type" : "blendshape"
    },
    {
        "id" : "104",
        "name" : "browOuterUpLeft",
        "sets" : "brow",
        "type" : "blendshape"
    },
    {
        "id" : "105",
        "name" : "browOuterUpRight",
        "sets" : "brow",
        "type" : "blendshape"
    },
    {
        "id" : "106",
        "name" : "cheekPuff",
        "sets" : "cheek_lower",
        "type" : "blendshape"
    },
    {
        "id" : "107",
        "name" : "cheekSquintLeft",
        "sets" : "cheek_upper",
        "type" : "blendshape"
    },
    {
        "id" : "108",
        "name" : "cheekSquintRight",
        "sets" : "cheek_upper",
        "type" : "blendshape"
    },
    {
        "id" : "109",
        "name" : "eyeBlinkLeft",
        "sets" : "eye_lid",
        "type" : "blendshape"
    },
    {
        "id" : "110",
        "name" : "eyeBlinkRight",
        "sets" : "eye_lid",
        "type" : "blendshape"
    },
    {
        "id" : "111",
        "name" : "eyeLookDownLeft",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "112",
        "name" : "eyeLookDownRight",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "113",
        "name" : "eyeLookInLeft",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "114",
        "name" : "eyeLookInRight",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "115",
        "name" : "eyeLookOutLeft",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "116",
        "name" : "eyeLookOutRight",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "117",
        "name" : "eyeLookUpLeft",
        "sets" : "eye_look",
        "type" : "blendshape"
    },
    {
        "id" : "118",
        "name" : "eyeLookUpRight",
        "sets" : "eye_look",
		"type" : "blendshape"
    },
    {
        "id" : "119",
        "name" : "eyeSquintLeft",
        "sets" : "eye_lid",
        "type" : "blendshape"
    },
    {
        "id" : "120",
        "name" : "eyeSquintRight",
        "sets" : "eye_lid",
        "type" : "blendshape"
    },
    {
        "id" : "121",
        "name" : "eyeWideLeft",
        "sets" : "eye_lid",
        "type" : "blendshape"
    },
    {
        "id" : "122",
        "name" : "eyeWideRight",
        "sets" : "eye_lid",
        "type" : "blendshape"
    },
    {
        "id" : "123",
        "name" : "jawForward",
        "sets" : "mouth_jaw",
        "type" : "blendshape"
    },
    {
        "id" : "124",
        "name" : "jawLeft",
        "sets" : "mouth_jaw",
        "type" : "blendshape"
    },
    {
        "id" : "125",
        "name" : "jawOpen",
        "sets" : "mouth_jaw",
        "type" : "blendshape"
    },
    {
        "id" : "126",
        "name" : "jawRight",
        "sets" : "mouth_jaw",
        "type" : "blendshape"
    },
    {
        "id" : "127",
        "name" : "mouthClose",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "128",
        "name" : "mouthDimpleLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "129",
        "name" : "mouthDimpleRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "130",
        "name" : "mouthFrownLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "131",
        "name" : "mouthFrownRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "132",
        "name" : "mouthFunnel",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "133",
        "name" : "mouthLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "134",
        "name" : "mouthLowerDownLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "135",
        "name" : "mouthLowerDownRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "136",
        "name" : "mouthPressLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "137",
        "name" : "mouthPressRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "138",
        "name" : "mouthPucker",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "139",
        "name" : "mouthRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "140",
        "name" : "mouthRollLower",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "141",
        "name" : "mouthRollUpper",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "142",
        "name" : "mouthShrugLower",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "143",
        "name" : "mouthShrugUpper",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "144",
        "name" : "mouthSmileLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "145",
        "name" : "mouthSmileRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "146",
        "name" : "mouthStretchLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "147",
        "name" : "mouthStretchRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "148",
        "name" : "mouthUpperUpLeft",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "149",
        "name" : "mouthUpperUpRight",
        "sets" : "mouth_lip",
        "type" : "blendshape"
    },
    {
        "id" : "150",
        "name" : "noseSneerLeft",
        "sets" : "nose",
        "type" : "blendshape"
    },
    {
        "id" : "151",
        "name" : "noseSneerRight",
        "sets" : "nose",
        "type" : "blendshape"
    },
    {
        "id" : "201",
        "name" : "stretch",
        "sets" : "all",
        "type" : "limiter"
    },
    {
        "id" : "202",
        "name" : "squash",
        "sets" : "all",
        "type" : "limiter"
    }
]

emotionPath = rootPath+'/poseData/emotion.json'
mouthPath = rootPath+'/poseData/mouth.json'
zeroEmotionList = [0.0] * len([i for i in poseData if i['type'] == 'expression'])
emotionLib = [{'name': 'browDownLeft', 'weight': zeroEmotionList},
                {'name': 'browDownRight', 'weight': zeroEmotionList},
                {'name': 'browInnerUp', 'weight': zeroEmotionList},
                {'name': 'browOuterUpLeft', 'weight': zeroEmotionList},
                {'name': 'browOuterUpRight', 'weight': zeroEmotionList},
                {'name': 'cheekPuff', 'weight': zeroEmotionList},
                {'name': 'cheekSquintLeft', 'weight': zeroEmotionList},
                {'name': 'cheekSquintRight', 'weight': zeroEmotionList},
                {'name': 'eyeBlinkLeft', 'weight': zeroEmotionList},
                {'name': 'eyeBlinkRight', 'weight': zeroEmotionList},
                #{'name': 'eyeLookDownLeft', 'weight': zeroEmotionList},
                #{'name': 'eyeLookDownRight', 'weight': zeroEmotionList},
                #{'name': 'eyeLookInLeft', 'weight': zeroEmotionList},
                #{'name': 'eyeLookInRight', 'weight': zeroEmotionList},
                #{'name': 'eyeLookOutLeft', 'weight': zeroEmotionList},
                #{'name': 'eyeLookOutRight', 'weight': zeroEmotionList},
                #{'name': 'eyeLookUpLeft', 'weight': zeroEmotionList},
                #{'name': 'eyeLookUpRight', 'weight': zeroEmotionList},
                {'name': 'eyeSquintLeft', 'weight': zeroEmotionList},
                {'name': 'eyeSquintRight', 'weight': zeroEmotionList},
                {'name': 'eyeWideLeft', 'weight': zeroEmotionList},
                {'name': 'eyeWideRight', 'weight': zeroEmotionList},
                #{'name': 'jawForward', 'weight': zeroEmotionList},
                #{'name': 'jawLeft', 'weight': zeroEmotionList},
                #{'name': 'jawOpen', 'weight': zeroEmotionList},
                #{'name': 'jawRight', 'weight': zeroEmotionList},
                #{'name': 'mouthClose', 'weight': zeroEmotionList},
                {'name': 'mouthDimpleLeft', 'weight': zeroEmotionList},
                {'name': 'mouthDimpleRight', 'weight': zeroEmotionList},
                {'name': 'mouthFrownLeft', 'weight': zeroEmotionList},
                {'name': 'mouthFrownRight', 'weight': zeroEmotionList},
                {'name': 'mouthFunnel', 'weight': zeroEmotionList},
                {'name': 'mouthLeft', 'weight': zeroEmotionList},
                {'name': 'mouthLowerDownLeft', 'weight': zeroEmotionList},
                {'name': 'mouthLowerDownRight', 'weight': zeroEmotionList},
                {'name': 'mouthPressLeft', 'weight': zeroEmotionList},
                {'name': 'mouthPressRight', 'weight': zeroEmotionList},
                {'name': 'mouthPucker', 'weight': zeroEmotionList},
                {'name': 'mouthRight', 'weight': zeroEmotionList},
                {'name': 'mouthRollLower', 'weight': zeroEmotionList},
                {'name': 'mouthRollUpper', 'weight': zeroEmotionList},
                {'name': 'mouthShrugLower', 'weight': zeroEmotionList},
                {'name': 'mouthShrugUpper', 'weight': zeroEmotionList},
                {'name': 'mouthSmileLeft', 'weight': zeroEmotionList},
                {'name': 'mouthSmileRight', 'weight': zeroEmotionList},
                {'name': 'mouthStretchLeft', 'weight': zeroEmotionList},
                {'name': 'mouthStretchRight', 'weight': zeroEmotionList},
                {'name': 'mouthUpperUpLeft', 'weight': zeroEmotionList},
                {'name': 'mouthUpperUpRight', 'weight': zeroEmotionList},
                {'name': 'noseSneerLeft', 'weight': zeroEmotionList},
                {'name': 'noseSneerRight', 'weight': zeroEmotionList}]
zeroPhonemeList = [0.0] * len([i for i in poseData if i['type'] == 'phoneme'])
mouthLib = [{'name': 'jawForward', 'weight': zeroPhonemeList },
                {'name': 'jawLeft', 'weight': zeroPhonemeList },
                {'name': 'jawOpen', 'weight': zeroPhonemeList },
                {'name': 'jawRight', 'weight': zeroPhonemeList },
                {'name': 'mouthClose', 'weight': zeroPhonemeList },
                {'name': 'mouthDimpleLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthDimpleRight', 'weight': zeroPhonemeList },
                {'name': 'mouthFrownLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthFrownRight', 'weight': zeroPhonemeList },
                {'name': 'mouthFunnel', 'weight': zeroPhonemeList },
                {'name': 'mouthLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthLowerDownLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthLowerDownRight', 'weight': zeroPhonemeList },
                {'name': 'mouthPressLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthPressRight', 'weight': zeroPhonemeList },
                {'name': 'mouthPucker', 'weight': zeroPhonemeList },
                {'name': 'mouthRight', 'weight': zeroPhonemeList },
                {'name': 'mouthRollLower', 'weight': zeroPhonemeList },
                {'name': 'mouthRollUpper', 'weight': zeroPhonemeList },
                {'name': 'mouthShrugLower', 'weight': zeroPhonemeList },
                {'name': 'mouthShrugUpper', 'weight': zeroPhonemeList },
                {'name': 'mouthSmileLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthSmileRight', 'weight': zeroPhonemeList },
                {'name': 'mouthStretchLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthStretchRight', 'weight': zeroPhonemeList },
                {'name': 'mouthUpperUpLeft', 'weight': zeroPhonemeList },
                {'name': 'mouthUpperUpRight', 'weight': zeroPhonemeList }]

if __name__ == 'BRSFacialRetargeter.poseData' or 'poseData':
    # Create startup Json
    poseDataDir = rootPath + os.sep + 'poseData'
    if os.path.exists(poseDataDir):
        poseDataList = [f for f in os.listdir(poseDataDir)]
        if not 'emotion.json' in poseDataList:
            with open(emotionPath, writeMode) as outFile:
                #outFile = open(emotionPath, writeMode)
                json.dump(emotionLib, outFile, sort_keys=True, indent=4)
                outFile.close()
        if not 'mouth.json' in poseDataList:
            with open(mouthPath, writeMode) as outFile:
                #outFile = open(mouthPath, writeMode)
                json.dump(mouthLib, outFile, sort_keys=True, indent=4)
                outFile.close()

    # Index Checking
    mouth_len_old = len(json.load(open(mouthPath))[0]['weight'])
    mouth_len_new = len(mouthLib[0]['weight'])
    if not mouth_len_old == mouth_len_new:
        os.remove(mouthPath)
        with open(mouthPath, writeMode) as outFile:
            #outFile = open(mouthPath, writeMode)
            json.dump(mouthLib, outFile, sort_keys=True, indent=4)
            outFile.close()
        cmds.warning('reset phoneme poses data')
    emotion_len_old = len(json.load(open(emotionPath))[0]['weight'])
    emotion_len_new = len(emotionLib[0]['weight'])
    if not emotion_len_old == emotion_len_new:
        os.remove(emotionPath)
        with open(emotionPath, writeMode) as outFile:
            #outFile = open(emotionPath, writeMode)
            json.dump(emotionLib, outFile, sort_keys=True, indent=4)
            outFile.close()
            cmds.warning('reset emotion poses data')

emotionLib = json.load(open(emotionPath))
mouthLib = json.load(open(mouthPath))

"""
Function
"""
def isUnderscoreBSAlias(bsName=configJson['src_blendshape']):
    try:
        bsCount = len(cmds.getAttr(bsName + '.weight')[0])
        for i in range(bsCount):
            bsAlias = cmds.aliasAttr(bsName + '.weight[{}]'.format(i), q=True)
            if '_L' in bsAlias or '_R' in bsAlias:
                return True
            if 'Right' in bsAlias or 'Left' in bsAlias:
                return False
    except:
        return False

def getPoseData(*_):
    underscore = isUnderscoreBSAlias()
    rec = []
    for data in poseData:
        skipReplace = ['jawLeft','jawRight','mouthLeft','mouthRight']
        if data['type'] == 'blendshape' and underscore and not data['name'] in skipReplace:
            data['name'] =  data['name'].replace('Right','_R')
            data['name'] =  data['name'].replace('Left','_L')
        rec.append(data)
    return rec

def getEmotionLibrary(*_):
    underscore = isUnderscoreBSAlias()
    rec = []
    for data in emotionLib:
        if min(data['weight']) == max(data['weight']):
            continue
        skipReplace = ['jawLeft', 'jawRight', 'mouthLeft', 'mouthRight']
        if underscore and not data['name'] in skipReplace:
            data['name'] = data['name'].replace('Right', '_R')
            data['name'] = data['name'].replace('Left', '_L')
        rec.append(data)
    return rec

def getMouthLibrary(*_):
    underscore = isUnderscoreBSAlias()
    rec = []
    for data in mouthLib:
        if min(data['weight']) == max(data['weight']):
            continue
        skipReplace = ['jawLeft', 'jawRight', 'mouthLeft', 'mouthRight']
        if underscore and not data['name'] in skipReplace:
            data['name'] = data['name'].replace('Right', '_R')
            data['name'] = data['name'].replace('Left', '_L')
        rec.append(data)
    return rec

def setBlendshapePose(targetType, targetName, blend = 0.5, bsName=configJson['src_blendshape'], getAttribute=False):
    """
    :param targetType:
    :param targetName:
    :param blend: blend percentile
    :param bsName:
    :param getAttribute:  load / set blendshape attribute to bsName (for checking)
    :return:
    """
    global emotionLib, mouthLib
    targetList = [data['name'] for data in getPoseData() if data['type'] == targetType]
    if not targetType in ['expression', 'phoneme'] or not targetName in targetList:
        return None
    underscore = isUnderscoreBSAlias()
    targetIndex = targetList.index(targetName)
    #print('target {}'.format(targetList))
    #print('emotionData {}'.format(emotionLib))
    #print('is underscore {}'.format(underscore))
    #print('target Name {}'.format(targetName))
    #print('target Index {}'.format(targetIndex))

    bsCount = len(cmds.getAttr(bsName + '.weight')[0])
    bsAlias = []
    bsValue = []
    for i in range(bsCount):
        wName = cmds.aliasAttr(bsName + '.weight[{}]'.format(i), q=True)
        value = cmds.getAttr('{}.{}'.format(bsName, wName))
        value = round(value,4)
        bsValue.append(value)
        if underscore:
            wName = wName.replace('_R','Right').replace('_L','Left')
        bsAlias.append(wName)
    #print('bs alias {}'.format(bsAlias))
    #print('bs value {}'.format(bsValue))

    if targetType == 'expression':
        wLibrary = emotionLib
        wPath = emotionPath
    elif targetType == 'phoneme':
        wLibrary = mouthLib
        wPath = mouthPath
    
    for data in wLibrary:
        #print(data['name'])
        aliasIndex = bsAlias.index(data['name'])
        aliasValue = bsValue[aliasIndex]
        #print('new value {}'.format(aliasValue))
        oldValue = data['weight'][targetIndex]
        #print('old value {}'.format(oldValue))
        result = ((aliasValue - oldValue)*blend) + oldValue
        #print('result {}'.format(result))
        if not getAttribute:
            #print (wLibrary[wLibrary.index(data)]['weight'])
            wLibrary[wLibrary.index(data)]['weight'][targetIndex] = round(result, 4)
            #print (wLibrary[wLibrary.index(data)]['weight'])
        elif getAttribute:
            curTime = round(cmds.currentTime(q=True), 0)
            aliasName = bsAlias[aliasIndex]
            skipReplace = ['jawLeft', 'jawRight', 'mouthLeft', 'mouthRight']
            if underscore and not aliasName in skipReplace:
                aliasName = aliasName.replace('Right', '_R')
                aliasName = aliasName.replace('Left', '_L')
            cmds.cutKey('{}.{}'.format(bsName, aliasName), t=(curTime, curTime + 0.99))
            cmds.setAttr('{}.{}'.format(bsName, aliasName),oldValue)

    if not getAttribute:
        with open(wPath, writeMode) as outFile:
            #outFile = open(wPath, writeMode)
            json.dump(wLibrary, outFile, sort_keys=True, indent=4)
        print('Set Blendshape {} : {}'.format(targetType, targetName))
