"""
POSE DATA
"""

import json, os, time
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))

poseData = [
    {
        "id": "001",
        "name": "base",
        "sets": "all",
        "type": "base"
    },
    {
        "id": "002",
        "name": "joyful",
        "sets": "all",
        "type": "expression"
    },
    {
        "id": "003",
        "name": "sad",
        "sets": "all",
        "type": "expression"
    },
    {
        "id": "004",
        "name": "mad",
        "sets": "all",
        "type": "expression"
    },
    {
        "id": "005",
        "name": "powerful",
        "sets": "all",
        "type": "expression"
    },
    {
        "id": "006",
        "name": "scared",
        "sets": "all",
        "type": "expression"
    },
{
        "id": "007",
        "name": "peaceful",
        "sets": "all",
        "type": "expression"
    },
    {
        "id": "051",
        "name": "IY",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "052",
        "name": "AA",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "053",
        "name": "AH",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "054",
        "name": "ER",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "055",
        "name": "S",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "056",
        "name": "SH",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "057",
        "name": "F",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "058",
        "name": "TH",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "059",
        "name": "MBP",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "060",
        "name": "W",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "061",
        "name": "K",
        "sets": "mouth_all",
        "type": "phoneme"
    },
    {
        "id": "101",
        "name": "browDownLeft",
        "sets": "brow",
        "type": "blendshape"
    },
    {
        "id": "102",
        "name": "browDownRight",
        "sets": "brow",
        "type": "blendshape"
    },
    {
        "id": "103",
        "name": "browInnerUp",
        "sets": "brow",
        "type": "blendshape"
    },
    {
        "id": "104",
        "name": "browOuterUpLeft",
        "sets": "brow",
        "type": "blendshape"
    },
    {
        "id": "105",
        "name": "browOuterUpRight",
        "sets": "brow",
        "type": "blendshape"
    },
    {
        "id": "106",
        "name": "cheekPuff",
        "sets": "cheek_lower",
        "type": "blendshape"
    },
    {
        "id": "107",
        "name": "cheekSquintLeft",
        "sets": "cheek_upper",
        "type": "blendshape"
    },
    {
        "id": "108",
        "name": "cheekSquintRight",
        "sets": "cheek_upper",
        "type": "blendshape"
    },
    {
        "id": "109",
        "name": "eyeBlinkLeft",
        "sets": "eye_lid",
        "type": "blendshape"
    },
    {
        "id": "110",
        "name": "eyeBlinkRight",
        "sets": "eye_lid",
        "type": "blendshape"
    },
    {
        "id": "111",
        "name": "eyeLookDownLeft",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "112",
        "name": "eyeLookDownRight",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "113",
        "name": "eyeLookInLeft",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "114",
        "name": "eyeLookInRight",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "115",
        "name": "eyeLookOutLeft",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "116",
        "name": "eyeLookOutRight",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "117",
        "name": "eyeLookUpLeft",
        "sets": "eye_look",
        "type": "blendshape"
    },
    {
        "id": "118",
        "name": "eyeLookUpRight",
        "sets": "eye_look",
		"type": "blendshape"
    },
    {
        "id": "119",
        "name": "eyeSquintLeft",
        "sets": "eye_lid",
        "type": "blendshape"
    },
    {
        "id": "120",
        "name": "eyeSquintRight",
        "sets": "eye_lid",
        "type": "blendshape"
    },
    {
        "id": "121",
        "name": "eyeWideLeft",
        "sets": "eye_lid",
        "type": "blendshape"
    },
    {
        "id": "122",
        "name": "eyeWideRight",
        "sets": "eye_lid",
        "type": "blendshape"
    },
    {
        "id": "123",
        "name": "jawForward",
        "sets": "mouth_jaw",
        "type": "blendshape"
    },
    {
        "id": "124",
        "name": "jawLeft",
        "sets": "mouth_jaw",
        "type": "blendshape"
    },
    {
        "id": "125",
        "name": "jawOpen",
        "sets": "mouth_jaw",
        "type": "blendshape"
    },
    {
        "id": "126",
        "name": "jawRight",
        "sets": "mouth_jaw",
        "type": "blendshape"
    },
    {
        "id": "127",
        "name": "mouthClose",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "128",
        "name": "mouthDimpleLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "129",
        "name": "mouthDimpleRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "130",
        "name": "mouthFrownLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "131",
        "name": "mouthFrownRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "132",
        "name": "mouthFunnel",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "133",
        "name": "mouthLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "134",
        "name": "mouthLowerDownLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "135",
        "name": "mouthLowerDownRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "136",
        "name": "mouthPressLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "137",
        "name": "mouthPressRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "138",
        "name": "mouthPucker",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "139",
        "name": "mouthRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "140",
        "name": "mouthRollLower",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "141",
        "name": "mouthRollUpper",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "142",
        "name": "mouthShrugLower",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "143",
        "name": "mouthShrugUpper",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "144",
        "name": "mouthSmileLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "145",
        "name": "mouthSmileRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "146",
        "name": "mouthStretchLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "147",
        "name": "mouthStretchRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "148",
        "name": "mouthUpperUpLeft",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "149",
        "name": "mouthUpperUpRight",
        "sets": "mouth_lip",
        "type": "blendshape"
    },
    {
        "id": "150",
        "name": "noseSneerLeft",
        "sets": "nose",
        "type": "blendshape"
    },
    {
        "id": "151",
        "name": "noseSneerRight",
        "sets": "nose",
        "type": "blendshape"
    },
    {
        "id": "201",
        "name": "stretch",
        "sets": "all",
        "type": "limiter"
    },
    {
        "id": "202",
        "name": "squash",
        "sets": "all",
        "type": "limiter"
    }
]

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