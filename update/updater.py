"""
BRSFR FACE UPDATER
"""
import json, os, time, random, sys
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))
brsPrefix = 'brsFR_'
frConfig = brsPrefix + 'core'

#Init
prevTime = time.time()

def lerp(a, b, factor):
    if factor > 1:
        factor = 1
    elif factor <= 0:
        factor = 0
    v = a + (b-a)*factor
    return v

def getFPS(*_):
    timeUnitSet = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
    timeUnit = cmds.currentUnit(q=True, t=True)
    if timeUnit in timeUnitSet:
        fps = timeUnitSet[timeUnit]
    elif timeUnit.__contains__('fps'):
        fps = str(cmds.currentUnit(q=True, t=True))[:-3]
    elif timeUnit.__contains__('df'):
        fps = str(cmds.currentUnit(q=True, t=True))[:-2]
    return int(float(fps))

def autoEmotion(*_):
    import poseData
    fps = getFPS()
    poseDataJson = poseData.getPoseData()
    emotionList = [data['name'] for data in poseDataJson if data['type'] == 'expression']
    timming = cmds.getAttr('{}.{}'.format(frConfig, 'emotion_timming'))
    isAuto = cmds.getAttr('{}.{}'.format(frConfig,'auto_emotion'))
    for emotionName in emotionList:
        weightFactorName = brsPrefix + emotionName + '_weightFactor'
        if not cmds.objExists(weightFactorName):
            continue
        prevValue = cmds.getAttr('{}.{}'.format(frConfig, emotionName))
        newValue = cmds.getAttr(weightFactorName + '.output')
        if isAuto:
            sm = 1 / (timming * fps)
            v = lerp(prevValue, newValue, sm)
            cmds.setAttr('{}.{}'.format(frConfig, emotionName), v, clamp=True)
            #cmds.connectAttr(weightFactorName + '.output', '{}.{}'.format(frConfig, emotionName), f=True)
        elif not isAuto:
            pass
            #cmds.disconnectAttr(weightFactorName + '.output', '{}.{}'.format(frConfig, emotionName))

def autoMouth(*_):
    import poseData
    fps = getFPS()
    poseDataJson = poseData.getPoseData()
    mouthList = [data['name'] for data in poseDataJson if data['type'] == 'phoneme']
    timming = cmds.getAttr('{}.{}'.format(frConfig,'phoneme_timming'))
    isAuto = cmds.getAttr('{}.{}'.format(frConfig,'auto_phoneme'))
    for mouthName in mouthList:
        weightFactorName = brsPrefix + mouthName + '_weightFactor'
        if not cmds.objExists(weightFactorName):
            continue
        prevValue = cmds.getAttr('{}.{}'.format(frConfig, mouthName))
        newValue = cmds.getAttr(weightFactorName + '.output')
        if isAuto:
            sm = 1 / (timming*fps)
            v = lerp(prevValue, newValue, sm)
            cmds.setAttr('{}.{}'.format(frConfig, mouthName), v, clamp=True)
            #cmds.connectAttr(weightFactorName + '.output', '{}.{}'.format(frConfig, mouthName), f=True)
        elif not isAuto:
            #cmds.disconnectAttr(weightFactorName + '.output', '{}.{}'.format(frConfig, mouthName))
            cmds.setAttr('{}.{}'.format(frConfig, mouthName), 0.0)

def setRetargetAttribute(*_): #Main Update
    # Before Update
    global prevTime
    #FacialRetargeter.updater.setRetargetAttribute()
    poseLibJson = json.load(open(configJson['pose_library_path']))
    dstNs = configJson['dst_namespace']
    smoothSetsName = brsPrefix + 'smoothSets'
    smoothSetsList = cmds.sets(smoothSetsName, q=True)
    if smoothSetsList == None:
        smoothSetsList = []

    # Update
    autoEmotion()
    autoMouth()
    # Apply Retarget Value
    attrList = list(poseLibJson['attributes'])
    random.shuffle(attrList)
    for attr in attrList:
        attrName = dstNs + ':' + attr
        if not cmds.objExists(attrName):
            continue
        pmaName = brsPrefix + attrName + '_sum'
        pmaName = pmaName.replace(':', '_').replace('.', '_')
        objName = '{}:{}'.format(dstNs, attr.split('.')[0])
        if not cmds.objExists(pmaName):
            continue
        # Clear Connection
        if cmds.listConnections(attrName) != None:
            lastConnected = cmds.listConnections(attrName)[-1]
            if 'unitConversion' in lastConnected and not dstNs in lastConnected:
                cmds.disconnectAttr(lastConnected + '.output', attrName)
            if lastConnected == pmaName:
                cmds.disconnectAttr(lastConnected + '.output1D', attrName)
        # Main Motion Capture Set Attribute
        if cmds.objExists(pmaName):
            prevValue = cmds.getAttr(attrName)
            newValue = cmds.getAttr(pmaName + '.output1D')
            if cmds.getAttr(attrName) != newValue and cmds.getAttr(attrName, settable=True)[0]:
                if objName in smoothSetsList:
                    sm = 1 - cmds.getAttr('{}.{}'.format(frConfig, 'smoothness'))
                    v = lerp(prevValue, newValue, sm)
                    cmds.setAttr(attrName, v, clamp=True)
                else:
                    cmds.setAttr(attrName, newValue, clamp=True)
        #Time Checker
        durTime = time.time() - prevTime
        #print(durTime)
        if durTime > ( 1 / cmds.getAttr('{}.{}'.format(frConfig, 'skip_rate')) ):
            break
    # Resets Unusing Attribute
    if 'pose_attribute' in poseLibJson:
        rsAttr = [attr for attr in list(poseLibJson['pose_attribute']) if attr not in attrList]
        for attr in rsAttr:
            attrName = dstNs + ':' + attr
            v = poseLibJson['pose_attribute'][attr]
            if not cmds.objExists(attrName):
                continue
            if cmds.getAttr(attrName) != v:
                cmds.setAttr(attrName, v, clamp=True)
                cmds.cutKey(attrName)

    #After Update
    prevTime = time.time()
