"""
BRSFR FACE UPDATER
"""
import json, os, time, random
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))
brsPrefix = 'brsFR_'
frConfig = brsPrefix + 'config'

#Init
prevTime = time.time()

def lerp(a, b, factor):
    if factor > 1:
        factor = 1
    elif factor <= 0:
        factor = 0
    v = a + (b-a)*factor
    return v


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
    # Apply Retarget Value
    attrList = list(poseLibJson['attributes'])
    random.shuffle(attrList)
    for attr in attrList:
        attrName = dstNs + ':' + attr
        if not cmds.objExists(attrName):
            continue
        pmaName = brsPrefix + attrName + '_sum'
        pmaName = pmaName.replace(':', '_')
        pmaName = pmaName.replace('.', '_')
        objName = '{}:{}'.format(dstNs, attr.split('.')[0])
        if cmds.listConnections(attrName) != None:
            lastConnected = cmds.listConnections(attrName)[-1]
            if 'unitConversion' in lastConnected and not dstNs in lastConnected:
                cmds.disconnectAttr(lastConnected + '.output', attrName)
            if lastConnected == pmaName:
                cmds.disconnectAttr(lastConnected + '.output1D', attrName)
        if cmds.objExists(pmaName):
            prevValue = cmds.getAttr(attrName)
            newValue = cmds.getAttr(pmaName + '.output1D')
            if cmds.getAttr(attrName) != newValue and not cmds.getAttr(attrName, lock=True):
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

    #After Update
    cmds.refresh(su=False)
    prevTime = time.time()
