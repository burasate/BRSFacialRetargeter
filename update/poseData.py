"""
POSE DATA
"""

import json, os, time
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))

emotionPath = rootPath+'/poseData/emotion.json'
emotionLib = json.load(open(emotionPath))
mouthPath = rootPath+'/poseData/mouth.json'
mouthLib = json.load(open(mouthPath))
poseData = [
    {
        "id" : "001",
        "name" : "base",
        "sets" : "all",
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
"""
#[joyful,sad,mad,powerful,scared,peaceful]
emotionLib = [
    {
        "name" : "browDownLeft",
        "weight" : [0.0, 1.0, 1.0, 1.0, 1.0, 0.24]
    },
    {
        "name" : "browDownRight",
        "weight" : [0.0, 1.0, 1.0, 1.0, 1.0, 0.0]
    },
    {
        "name" : "browInnerUp",
        "weight" : [1.0, 1.0, 0.0, 0.14, 1.0, 1.0]
    },
    {
        "name" : "browOuterUpLeft",
        "weight" : [0.53, 0.0, 0.1, 0.43, 0.0, 0.25]
    },
    {
        "name" : "browOuterUpRight",
        "weight" : [0.53, 0.0, 0.1, 0.43, 0.0, 0.25]
    },
    {
        "name" : "cheekPuff",
        "weight" : [0.13, 0.0, 0.35, 0.13, 0.0, 0.13]
    },
    {
        "name" : "cheekSquintLeft",
        "weight" : [0.12, 1.0, 0.68, 0.79, 0.3, 0.55]
    },
    {
        "name" : "cheekSquintRight",
        "weight" : [0.12, 1.0, 0.68, 0.79, 0.3, 0.55]
    },
    {
        "name" : "eyeBlinkLeft",
        "weight" : [0.0, 0.05, 0.08, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeBlinkRight",
        "weight" : [0.0, 0.05, 0.08, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookDownLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookDownRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookInLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookInRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookOutLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookOutRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookUpLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeLookUpRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "eyeSquintLeft",
        "weight" : [0.29, 0.3, 0.55, 0.45, 0.06, 0.74]
    },
    {
        "name" : "eyeSquintRight",
        "weight" : [0.21, 0.3, 0.55, 0.45, 0.06, 0.74]
    },
    {
        "name" : "eyeWideLeft",
        "weight" : [1.0, 0.0, 0.7, 1.0, 1.0, 0.21]
    },
    {
        "name" : "eyeWideRight",
        "weight" : [0.92, 0.0, 0.7, 1.0, 1.0, 0.3]
    },
    {
        "name" : "jawForward",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "jawLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "jawOpen",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "jawRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthClose",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthDimpleLeft",
        "weight" : [0.35, 0.19, 0.13, 0.56, 0.0, 0.0]
    },
    {
        "name" : "mouthDimpleRight",
        "weight" : [0.28, 0.19, 0.35, 0.56, 0.0, 0.0]
    },
    {
        "name" : "mouthFrownLeft",
        "weight" : [0.0, 0.6, 0.43, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthFrownRight",
        "weight" : [0.0, 0.6, 0.43, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthFunnel",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthLowerDownLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthLowerDownRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthPressLeft",
        "weight" : [0.0, 0.0, 0.11, 0.34, 0.23, 0.51]
    },
    {
        "name" : "mouthPressRight",
        "weight" : [0.0, 0.0, 0.09, 0.34, 0.2, 0.51]
    },
    {
        "name" : "mouthPucker",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthRollLower",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthRollUpper",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthShrugLower",
        "weight" : [0.0, 0.33, 1.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthShrugUpper",
        "weight" : [0.0, 0.33, 0.9, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthSmileLeft",
        "weight" : [1.0, 0.0, 0.0, 0.86, 0.0, 0.65]
    },
    {
        "name" : "mouthSmileRight",
        "weight" : [1.0, 0.0, 0.0, 0.86, 0.0, 0.65]
    },
    {
        "name" : "mouthStretchLeft",
        "weight" : [0.0, 0.52, 0.0, 0.0, 0.6, 0.0]
    },
    {
        "name" : "mouthStretchRight",
        "weight" : [0.0, 0.52, 0.0, 0.0, 0.6, 0.0]
    },
    {
        "name" : "mouthUpperUpLeft",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "mouthUpperUpRight",
        "weight" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name" : "noseSneerLeft",
        "weight" : [0.21, 0.8, 1.0, 0.74, 0.0, 0.25]
    },
    {
        "name" : "noseSneerRight",
        "weight" : [0.01, 0.8, 1.0, 0.54, 0.0, 0.25]
    }
]

#[IY,AA,AH,ER,S,SH,F,TH,MBP,W,K]
#[1,2,3,4,5,6,7,8,9,10,11]
mouthLib = [
    {
        "name": "jawForward",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "jawLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "jawOpen",
        "weight": [0.17, 0.34, 0.56, 0.15, 0.0, 0.03, 0.06, 0.16, 0.0, 0.0, 0.08,0]
    },
    {
        "name": "jawRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthClose",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthDimpleLeft",
        "weight": [0.4, 0.25, 0.0, 0.06, 0.52, 0.0, 0.74, 0.45, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthDimpleRight",
        "weight": [0.4, 0.25, 0.0, 0.08, 0.52, 0.0, 0.56, 0.49, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthFrownLeft",
        "weight": [0.0, 0.0, 0.07, 0.35, 0.0, 0.0, 0.33, 0.14, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthFrownRight",
        "weight": [0.0, 0.0, 0.07, 0.46, 0.0, 0.0, 0.37, 0.17, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthFunnel",
        "weight": [0.0, 0.0, 0.0, 0.22, 0.0, 0.56, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthLowerDownLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.34, 0.0, 0.46, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthLowerDownRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.34, 0.0, 0.46, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthPressLeft",
        "weight": [0.4, 0.13, 0.0, 0.0, 0.3, 0.0, 0.12, 0.0, 0.31, 0.0, 0.3,0]
    },
    {
        "name": "mouthPressRight",
        "weight": [0.4, 0.13, 0.0, 0.0, 0.3, 0.0, 0.13, 0.0, 0.31, 0.0, 0.31,0]
    },
    {
        "name": "mouthPucker",
        "weight": [0.0, 0.0, 0.0, 0.47, 0.0, 0.18, 0.51, 0.0, 0.0, 0.9, 0.0,0]
    },
    {
        "name": "mouthRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthRollLower",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.25, 0.0, 0.0,0]
    },
    {
        "name": "mouthRollUpper",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.11, 0.0, 0.0,0]
    },
    {
        "name": "mouthShrugLower",
        "weight": [0.0, 0.0, 0.0, 0.57, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthShrugUpper",
        "weight": [0.0, 0.0, 0.0, 0.01, 0.46, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthSmileLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthSmileRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthStretchLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthStretchRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthUpperUpLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "mouthUpperUpRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.18, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "noseSneerLeft",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    },
    {
        "name": "noseSneerRight",
        "weight": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0]
    }
]
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

def setBlendshapePose(targetType, targetName, blend = 0.2, bsName=configJson['src_blendshape'], getAttribute=False):
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
        outFile = open(wPath, 'wb')
        json.dump(wLibrary, outFile, sort_keys=True, indent=4)
        print('Set Blendshape {} : {}'.format(targetType, targetName))






