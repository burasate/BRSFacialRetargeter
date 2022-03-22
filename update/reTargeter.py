"""
BRSFR FACE RETARGETER
"""
import json, os
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))
brsPrefix = 'brsFR_'
frConfig = brsPrefix + 'core'
gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

import imp
import updater
import poseData
imp.reload(updater)
imp.reload(poseData)

def reloadConfig(*_):
    global configJson
    configJson = json.load(open(configPath))

def getIDValue(nameSpace,id):
    poseLibJson = json.load(open(configJson['pose_library_path']))
    data = {}
    for attr in poseLibJson['attributes']:
        if not id in poseLibJson['attributes'][attr]['id']:
            continue
        dstAttr = '{}:{}'.format(nameSpace, attr)
        index = poseLibJson['attributes'][attr]['id'].index(id)
        dstValue = poseLibJson['attributes'][attr]['value'][index]

        data[dstAttr] = dstValue
    return data

def getObjectAttributeName(objects):
    attrNameList = []
    for obj in objects:
        for attr in cmds.listAttr(obj, k=True):
            attrName = '{}.{}'.format(obj, attr)
            attrNameList.append(attrName)
    return attrNameList

def getFrameValue(nameSpace,frame):
    poseLibJson = json.load(open(configJson['pose_library_path']))
    data = {}
    for attr in poseLibJson['attributes']:
        dstAttr = '{}:{}'.format(nameSpace, attr)
        value = cmds.getAttr(dstAttr, t=frame)
        if type(value) == type(list()):
                value = value[0]
        if type(value) == type(bool()):
            value = int(value)

        data[dstAttr] = value
    return data

def getSrcBsData(srcBlendshape,frameList):
    poseDataJson = poseData.getPoseData()
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar');
    cmds.progressBar( gMainProgressBar,
    				edit=True,
    				beginProgress=True,
    				isInterruptable=False,
    				status='Reading Data..',
    				maxValue=len(poseDataJson)+1 )

    srcBsData = {}
    for dataP in poseDataJson:
        bsId = dataP['id']
        cmds.progressBar(gMainProgressBar, edit=True, step=1,
                         status='Loading Blendshape&Expression Data.. {}'.format(dataP['type']))
        if dataP['type'] == 'blendshape':
            bsAttr = '{}.{}'.format(srcBlendshape, dataP['name'])
            srcBsData[bsId] = {
                'name' : bsAttr,
                'frame' : [],
                'value' : []
            }
            for f in frameList:
                bsValue = cmds.getAttr(bsAttr, t=f)
                srcBsData[bsId]['frame'].append(f)
                srcBsData[bsId]['value'].append(bsValue)
        elif dataP['type'] == 'expression':
            expAttr = '{}.{}'.format(frConfig, dataP['name'])
            srcBsData[bsId] = {
                'name': expAttr,
                'frame': [],
                'value': []
            }
            for f in frameList:
                expValue = cmds.getAttr(expAttr, t=f)
                srcBsData[bsId]['frame'].append(f)
                srcBsData[bsId]['value'].append(expValue)
        else:continue
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    return srcBsData

def getResultData(dstNamespace,srcBsData,frame,baseId='001'):
    # create result data
    resultData = getIDValue(nameSpace=dstNamespace,id=baseId)

    for bsId in srcBsData:
        #print('\nid   {}   shape name   {}\n'.format(bsId, srcBsData[bsId]['name']))
        index = srcBsData[bsId]['frame'].index(frame)
        bsValue = srcBsData[bsId]['value'][index]
        poseLibData = getIDValue(nameSpace=dstNamespace,id=bsId)
        currentData = getFrameValue(nameSpace=dstNamespace,frame=frame)
        baseData = getIDValue(nameSpace=dstNamespace,id=baseId)
        #print(bsId)
        #print(srcBsData[bsId]['name'])
        #print(index)
        #print(bsValue)
        for dstAttr in resultData:
            if not dstAttr in poseLibData:
                continue
        #if dstAttr.__contains__('cJaw.rotateZ'):
            #print (dstAttr)
            poseValue = poseLibData[dstAttr]
            baseValue = baseData[dstAttr]
            currentValue = resultData[dstAttr]
            #print ('pose       : {}'.format(poseValue))
            #print ('base       : {}'.format(baseValue))
            #print ('blendshape : {}'.format(bsValue))
            #print ('current    : {}'.format(bsValue))

            # apply result
            # result = ((pose-base) * bs) + result
            # destination = ((capture-base) * bs) + current
            resultData[dstAttr] = ((poseValue - baseValue) * bsValue) + currentValue
            #print ('result     : {}'.format(resultData[dstAttr]))
    return resultData

def BRSFaceRetargeter(srcBlendshape,dstNamespace,libraryPath,frameMin,frameMax):
    # src round keyframe
    srcFrameList = []
    for f in cmds.keyframe(srcBlendshape, tc=True, q=True):
        f = round(f, 0)
        if f in srcFrameList:
            continue
        elif f >= frameMin and f <= frameMax:
            srcFrameList.append(f)
    #print(srcFrameList)

    # clear keyframe
    cutKeyList = []
    for attr in getFrameValue(nameSpace=dstNamespace,frame=0):
        cutKeyList.append(attr)
    cmds.cutKey(cutKeyList,time=(min(srcFrameList),max(srcFrameList)))

    # get src blendshape value by id key
    srcBsData = getSrcBsData(srcBlendshape,srcFrameList)
    #srcBsData[id]
    #print(srcBsData)

    startIndex = srcFrameList.index(frameMin)
    endIndex = srcFrameList.index(frameMax)+1

    for f in srcFrameList[startIndex:endIndex]:
    #for f in srcFrameList:
        #print('frame {}'.format(f))
        #frame = f
        baseId = '001'

        resultData = getResultData(dstNamespace,srcBsData,f,baseId=baseId)
        for dstAttr in resultData:
            cmds.setKeyframe(dstAttr, t=f, v=resultData[dstAttr])
        cmds.currentTime(f)
    print('Blendshape to Pose Retarget is Done   {}F - {}F'.format(frameMin,frameMax))

def updateAttrPoseLib(attrName,srcBlendshape,dstNamespace,libraryPath,learnRate=0.65): #Correct Pose For One Attribute
    poseLibJson = json.load(open(configJson['pose_library_path']))
    curFrame = cmds.currentTime(q=True)
    #print('frame = {}'.format(curFrame))

    baseId = '001'

    #attrName = 'PRE_Full_Armor:cmouth_corner_r.translateX'

    #get new target valuse set
    targetValue = cmds.getAttr(attrName,t=curFrame)
    #print ('target result = {}'.format(targetValue))

    #get current bs attr
    srcBsData = getSrcBsData(srcBlendshape,[curFrame,curFrame+1])

    pmaName = brsPrefix + attrName + '_sum'
    pmaName = pmaName.replace(':', '_').replace('.', '_')
    result = cmds.getAttr(pmaName+'.output1D')
    #print('current result = {}'.format(result))

    diffValue = targetValue - result
    #print('difference value = {}'.format(diffValue))
    if diffValue == 0.0:
        print('skip {} because value not change'.format(attrName))
        return None

    #bsData Normalization
    bsData = {
        'id' : [],
        'value' : [],
    }
    for bsId in srcBsData:
        index = srcBsData[bsId]['frame'].index(curFrame)
        bsValue = srcBsData[bsId]['value'][index]
        poseLibData = getIDValue(nameSpace=dstNamespace,id=bsId)
        baseData = getIDValue(nameSpace=dstNamespace,id=baseId)
        if not attrName in poseLibData:
            continue
        poseValue = poseLibData[attrName]
        baseValue = baseData[attrName]
        if bsValue == 0.0:
            continue
        if poseValue-baseValue == 0.0:
            continue
        bsData['id'].append(bsId)
        bsData['value'].append(bsValue)

    oldValue = 0.0
    newValue = 0.0
    #split value by value/sum ratio
    for i in range(len(bsData['value'])):
        #print('\n')
        bsId = bsData['id'][i]
        bsValue = bsData['value'][i]
        sumValue = sum(bsData['value'])
        bsValue_new = (bsValue / sumValue)
        diffValue_new = (diffValue * bsValue_new)
        #print('id {}   new difference value = {}'.format(bsId,diffValue_new))

        #set new result in PoseLib
        poseLibData = getIDValue(dstNamespace,bsId)
        poseValue = poseLibData[attrName]
        #print('id {}         pose lib value = {}'.format(bsId,poseValue))

        poseValue_new = poseValue + ( diffValue_new * learnRate )
        poseValue_new = round(poseValue_new, 4)
        #print('id {}     new pose lib value = {}'.format(bsId,poseValue_new))

        #apply poseLib data
        attr = attrName.split(':')[1]
        for a in poseLibJson['attributes']:
            if a == attr:
                index = poseLibJson['attributes'][a]['id'].index(bsId)
                poseLibJson['attributes'][a]['value'][index] = poseValue_new
                #print (poseLibJson['attributes'][a]['value'][index])
        oldValue = poseValue
        newValue = poseValue_new

    # save update pose library
    outFile = open(libraryPath, 'wb')
    json.dump(poseLibJson, outFile, sort_keys=True, indent=4)
    print('{} Updated in Pose Library  {}  to  {}'.format(attrName,round(oldValue,4),round(newValue,4)))

def updatePoseLibSelection(*_):
    poseLibJson = json.load(open(configJson['pose_library_path']))
    dstNs = configJson['dst_namespace']
    selection = cmds.ls(sl=True)

    """
    #Reset Config
    frConfig = brsPrefix + 'core'
    for at in configJson['rtg_attr']:
        cmds.setAttr('{}.{}'.format(frConfig, at['name']), e=True, value=at['value'])
    """

    #Update New Pose
    for objName in selection:
        for a in cmds.listAttr(objName,k=True):
            attrName = '{}.{}'.format(objName,a)
            noNamespaceAttr = attrName.split(':')[1]
            if noNamespaceAttr in poseLibJson['attributes']:
                updateAttrPoseLib(
                    attrName,
                    configJson['src_blendshape'],
                    configJson['dst_namespace'],
                    configJson['pose_library_path']
                )
            else:
                continue
    RetargetLink(update=True)
    updater.setRetargetAttribute()
    print ('Update Retarget Link Finish')

def clearBake(*_):
    poseLibJson = json.load(open(configJson['pose_library_path']))
    dstNs = configJson['dst_namespace']
    attrList = []
    for attr in poseLibJson['attributes']:
        attrName = dstNs + ':' + attr
        attrList.append(attrName)
    
    for attr in attrList:
        try:
            cmds.cutKey(attrList)
        except:
            pass

def clearLink(*_):
    clearList = []
    for i in cmds.ls():
        if i.__contains__(brsPrefix):
            clearList.append(i)
    cmds.delete(clearList)

def autoEmotionLink(update=False):
    emoLib = poseData.getEmotionLibrary()
    poseDataJson = poseData.getPoseData()

    emotionList = [data['name'] for data in poseDataJson if data['type'] == 'expression']
    for data in emoLib:  # Error Node
        data_index = emoLib.index(data)
        for emotionName in emotionList:
            emotion_index = emotionList.index(emotionName)

            errorName = brsPrefix + data['name'] + '_' + emotionName + '_error'
            if not cmds.objExists(errorName):
                cmds.createNode('floatMath', n=errorName, skipSelect=True)
                cmds.setAttr(errorName + '.operation', 1)
                cmds.connectAttr('{}.{}'.format(configJson['src_blendshape'], data['name']), errorName + '.floatA')
                weight = data['weight'][emotion_index]
                cmds.setAttr(errorName + '.floatB', weight)

            if update:
                print('weight updated')
                weight = data['weight'][emotion_index]
                cmds.setAttr(errorName + '.floatB', weight)
                return None

            squareName = brsPrefix + data['name'] + '_' + emotionName + '_square'
            if not cmds.objExists(squareName):
                cmds.createNode('floatMath', n=squareName, skipSelect=True)
                cmds.connectAttr(errorName + '.outFloat', squareName + '.floatA')
                cmds.setAttr(squareName + '.floatB', 2)
                cmds.setAttr(squareName + '.operation', 6)

            sqrtName = brsPrefix + data['name'] + '_' + emotionName + '_sqrt'
            if not cmds.objExists(sqrtName):
                cmds.createNode('floatMath', n=sqrtName, skipSelect=True)
                cmds.connectAttr(squareName + '.outFloat', sqrtName + '.floatA')
                cmds.setAttr(sqrtName + '.floatB', 0.5)
                cmds.setAttr(sqrtName + '.operation', 6)

            avgName = brsPrefix + emotionName + '_totalErrorAvg'
            if not cmds.objExists(avgName):
                cmds.createNode('plusMinusAverage', n=avgName, skipSelect=True)
                cmds.setAttr(avgName + '.operation', 3)
            if cmds.objExists(avgName):
                cmds.connectAttr(sqrtName + '.outFloat', avgName + '.input1D[{}]'.format(data_index), f=True)

            weightName = brsPrefix + emotionName + '_weight'
            if not cmds.objExists(weightName):
                cmds.createNode('reverse', n=weightName, skipSelect=True)
            if not cmds.isConnected(avgName + '.output1D', weightName + '.inputX'):
                cmds.connectAttr(avgName + '.output1D', weightName + '.inputX', f=True)

            weightTotalName = brsPrefix + 'emotion' + '_weightTotal'
            if not cmds.objExists(weightTotalName):
                cmds.createNode('plusMinusAverage', n=weightTotalName, skipSelect=True)
            if not cmds.isConnected(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(emotion_index)):
                cmds.connectAttr(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(emotion_index),
                                 f=True)

            weightMinName = brsPrefix + 'emotion' + '_weightMin'
            if not cmds.objExists(weightMinName):
                cmds.createNode('combinationShape', n=weightMinName, skipSelect=True)
                cmds.setAttr(weightMinName + '.combinationMethod', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(emotion_index)):
                cmds.connectAttr(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(emotion_index),
                                 f=True)

            # (weightName - weightMinName)
            weightMinMinusName = brsPrefix + emotionName + '_weightMinMinus'
            if not cmds.objExists(weightMinMinusName):
                cmds.createNode('floatMath', n=weightMinMinusName, skipSelect=True)
                cmds.setAttr(weightMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinMinusName + '.floatA'):
                cmds.connectAttr(weightName + '.outputX', weightMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightMinMinusName + '.floatB', f=True)

            # (weightTotalName - weightMinName)
            weightTotalMinMinusName = brsPrefix + emotionName + '_weightTotalMinMinus'
            if not cmds.objExists(weightTotalMinMinusName):
                cmds.createNode('floatMath', n=weightTotalMinMinusName, skipSelect=True)
                cmds.setAttr(weightTotalMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA'):
                cmds.connectAttr(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB', f=True)

            # (weightName - weightMinName) / (weightTotalName - weightMinName)
            weightDevideName = brsPrefix + emotionName + '_weightDevide'
            if not cmds.objExists(weightDevideName):
                cmds.createNode('multiplyDivide', n=weightDevideName, skipSelect=True)
                cmds.setAttr(weightDevideName + '.operation', 2)
            if not cmds.isConnected(weightMinMinusName + '.outFloat', weightDevideName + '.input1X'):
                cmds.connectAttr(weightMinMinusName + '.outFloat', weightDevideName + '.input1X', f=True)
            if not cmds.isConnected(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X'):
                cmds.connectAttr(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X', f=True)

            """
            # unitConversion
            weightFactorName = brsPrefix + emotionName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, skipSelect=True)
                cmds.setAttr(weightFactorName + '.conversionFactor', 1)  # Tunning
            if not cmds.isConnected(weightDevideName + '.outputX', weightFactorName + '.input'):
                cmds.connectAttr(weightDevideName + '.outputX', weightFactorName + '.input', f=True)
            """

            weightDevideReverseName = brsPrefix + emotionName + '_weightDevideReverse'
            if not cmds.objExists(weightDevideReverseName):
                cmds.createNode('reverse', n=weightDevideReverseName, skipSelect=True)
            if not cmds.isConnected(weightDevideName + '.outputX', weightDevideReverseName + '.inputX'):
                cmds.connectAttr(weightDevideName + '.outputX', weightDevideReverseName + '.inputX', f=True)

            weightMaxReverseName = brsPrefix + 'emotion' + '_weightMaxReverse'
            if not cmds.objExists(weightMaxReverseName):
                cmds.createNode('combinationShape', n=weightMaxReverseName, skipSelect=True)
                cmds.setAttr(weightMaxReverseName + '.combinationMethod', 1)
            if not cmds.isConnected(weightDevideReverseName + '.outputX', weightMaxReverseName + '.inputWeight[{}]'.format(emotion_index)):
                cmds.connectAttr(weightDevideReverseName + '.outputX', weightMaxReverseName + '.inputWeight[{}]'.format(emotion_index),
                                 f=True)

            weightMaxName = brsPrefix + 'emotion' + '_weightMax'
            if not cmds.objExists(weightMaxName):
                cmds.createNode('reverse', n=weightMaxName, skipSelect=True)
            if not cmds.isConnected(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX'):
                cmds.connectAttr(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX', f=True)

            weightOneHotName = brsPrefix + emotionName + '_weightOneHot'
            if not cmds.objExists(weightOneHotName):
                cmds.createNode('condition', n=weightOneHotName, skipSelect=True)
                cmds.setAttr(weightOneHotName + '.colorIfTrueR', 1)
                cmds.setAttr(weightOneHotName + '.colorIfFalseR', 0)
            if not cmds.isConnected(weightDevideName + '.outputX', weightOneHotName + '.firstTerm'):
                cmds.connectAttr(weightDevideName + '.outputX', weightOneHotName + '.firstTerm', f=True)
            if not cmds.isConnected(weightMaxName + '.outputX', weightOneHotName + '.secondTerm'):
                cmds.connectAttr(weightMaxName + '.outputX', weightOneHotName + '.secondTerm', f=True)

            # unitConversion
            weightFactorName = brsPrefix + emotionName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, skipSelect=True)
                cmds.setAttr(weightFactorName + '.conversionFactor', 1)  # Tunning
            if not cmds.isConnected(weightOneHotName + '.outColorR', weightFactorName + '.input'):
                cmds.connectAttr(weightOneHotName + '.outColorR', weightFactorName + '.input', f=True)

def autoMouthLink(update=False):
    mouthLib = poseData.getMouthLibrary()
    poseDataJson = poseData.getPoseData()

    mouthList = [data['name'] for data in poseDataJson if data['type'] == 'phoneme']
    jawOpenList = [data['jaw_open'] for data in poseDataJson if data['type'] == 'phoneme']

    jawOpenRevName = brsPrefix + 'jawOpenReverse'
    if not cmds.objExists(jawOpenRevName):
        cmds.createNode('reverse', n=jawOpenRevName, skipSelect=True)
    if not cmds.isConnected('{}.{}'.format(configJson['src_blendshape'], 'jawOpen'), jawOpenRevName + '.inputX'):
        cmds.connectAttr('{}.{}'.format(configJson['src_blendshape'], 'jawOpen'), jawOpenRevName + '.inputX', f=True)

    for data in mouthLib:  # Error Node
        data_index = mouthLib.index(data)
        for mouthName in mouthList:
            mouth_index = mouthList.index(mouthName)
            jawNode = 'jawOpen'
            isJawOpen = jawOpenList[mouth_index]
            if isJawOpen == False:
                jawNode = 'jawClose'

            errorName = brsPrefix + data['name'] + '_' + mouthName + '_error'
            if not cmds.objExists(errorName):
                cmds.createNode('floatMath', n=errorName, skipSelect=True)
                cmds.setAttr(errorName + '.operation', 1)
                cmds.connectAttr('{}.{}'.format(configJson['src_blendshape'], data['name']), errorName + '.floatA')
                weight = data['weight'][mouth_index]
                cmds.setAttr(errorName + '.floatB', weight)

            if update:
                print('weight updated')
                weight = data['weight'][mouth_index]
                cmds.setAttr(errorName + '.floatB', weight)
                return None

            squareName = brsPrefix + data['name'] + '_' + mouthName + '_square'
            if not cmds.objExists(squareName):
                cmds.createNode('floatMath', n=squareName, skipSelect=True)
                cmds.connectAttr(errorName + '.outFloat', squareName + '.floatA')
                cmds.setAttr(squareName + '.floatB', 2)
                cmds.setAttr(squareName + '.operation', 6)

            sqrtName = brsPrefix + data['name'] + '_' + mouthName + '_sqrt'
            if not cmds.objExists(sqrtName):
                cmds.createNode('floatMath', n=sqrtName, skipSelect=True)
                cmds.connectAttr(squareName + '.outFloat', sqrtName + '.floatA')
                cmds.setAttr(sqrtName + '.floatB', 0.5)
                cmds.setAttr(sqrtName + '.operation', 6)

            avgName = brsPrefix + mouthName + '_totalErrorAvg'
            if not cmds.objExists(avgName):
                cmds.createNode('plusMinusAverage', n=avgName, skipSelect=True)
                cmds.setAttr(avgName + '.operation', 3)
            if cmds.objExists(avgName):
                cmds.connectAttr(sqrtName + '.outFloat', avgName + '.input1D[{}]'.format(data_index), f=True)

            weightName = brsPrefix + mouthName + '_weight'
            if not cmds.objExists(weightName):
                cmds.createNode('reverse', n=weightName, skipSelect=True)
            if not cmds.isConnected(avgName + '.output1D', weightName + '.inputX'):
                cmds.connectAttr(avgName + '.output1D', weightName + '.inputX', f=True)

            weightTotalName = brsPrefix + jawNode + '_weightTotal'
            if not cmds.objExists(weightTotalName):
                cmds.createNode('plusMinusAverage', n=weightTotalName, skipSelect=True)
            if not cmds.isConnected(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(mouth_index)):
                cmds.connectAttr(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(mouth_index),
                                 f=True)

            weightMinName = brsPrefix + jawNode + '_weightMin'
            if not cmds.objExists(weightMinName):
                cmds.createNode('combinationShape', n=weightMinName, skipSelect=True)
                cmds.setAttr(weightMinName + '.combinationMethod', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(mouth_index)):
                cmds.connectAttr(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(mouth_index),
                                 f=True)

            # (weightName - weightMinName)
            weightMinMinusName = brsPrefix + mouthName + '_weightMinMinus'
            if not cmds.objExists(weightMinMinusName):
                cmds.createNode('floatMath', n=weightMinMinusName, skipSelect=True)
                cmds.setAttr(weightMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinMinusName + '.floatA'):
                cmds.connectAttr(weightName + '.outputX', weightMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightMinMinusName + '.floatB', f=True)

            # (weightTotalName - weightMinName)
            weightTotalMinMinusName = brsPrefix + mouthName + '_weightTotalMinMinus'
            if not cmds.objExists(weightTotalMinMinusName):
                cmds.createNode('floatMath', n=weightTotalMinMinusName, skipSelect=True)
                cmds.setAttr(weightTotalMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA'):
                cmds.connectAttr(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB', f=True)

            # (weightName - weightMinName) / (weightTotalName - weightMinName)
            weightDevideName = brsPrefix + mouthName + '_weightDevide'
            if not cmds.objExists(weightDevideName):
                cmds.createNode('multiplyDivide', n=weightDevideName, skipSelect=True)
                cmds.setAttr(weightDevideName + '.operation', 2)
            if not cmds.isConnected(weightMinMinusName + '.outFloat', weightDevideName + '.input1X'):
                cmds.connectAttr(weightMinMinusName + '.outFloat', weightDevideName + '.input1X', f=True)
            if not cmds.isConnected(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X'):
                cmds.connectAttr(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X', f=True)

            """
            # unitConversion
            weightFactorName = brsPrefix + mouthName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, skipSelect=True)
                cmds.setAttr(weightFactorName + '.conversionFactor', 13)  # Tunning
            if not cmds.isConnected(weightDevideName + '.outputX', weightFactorName + '.input'):
                cmds.connectAttr(weightDevideName + '.outputX', weightFactorName + '.input', f=True)
            """

            weightDevideReverseName = brsPrefix + mouthName + '_weightDevideReverse'
            if not cmds.objExists(weightDevideReverseName):
                cmds.createNode('reverse', n=weightDevideReverseName, skipSelect=True)
            if not cmds.isConnected(weightDevideName + '.outputX', weightDevideReverseName + '.inputX'):
                cmds.connectAttr(weightDevideName + '.outputX', weightDevideReverseName + '.inputX', f=True)

            weightMaxReverseName = brsPrefix + jawNode + '_weightMaxReverse'
            if not cmds.objExists(weightMaxReverseName):
                cmds.createNode('combinationShape', n=weightMaxReverseName, skipSelect=True)
                cmds.setAttr(weightMaxReverseName + '.combinationMethod', 1)
            if not cmds.isConnected(weightDevideReverseName + '.outputX',
                                    weightMaxReverseName + '.inputWeight[{}]'.format(mouth_index)):
                cmds.connectAttr(weightDevideReverseName + '.outputX',
                                 weightMaxReverseName + '.inputWeight[{}]'.format(mouth_index),
                                 f=True)

            weightMaxName = brsPrefix + jawNode + '_weightMax'
            if not cmds.objExists(weightMaxName):
                cmds.createNode('reverse', n=weightMaxName, skipSelect=True)
            if not cmds.isConnected(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX'):
                cmds.connectAttr(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX', f=True)

            weightOneHotName = brsPrefix + mouthName + '_weightOneHot'
            if not cmds.objExists(weightOneHotName):
                cmds.createNode('condition', n=weightOneHotName, skipSelect=True)
                cmds.setAttr(weightOneHotName + '.colorIfTrueR', 1)
                cmds.setAttr(weightOneHotName + '.colorIfFalseR', 0)
            if not cmds.isConnected(weightDevideName + '.outputX', weightOneHotName + '.firstTerm'):
                cmds.connectAttr(weightDevideName + '.outputX', weightOneHotName + '.firstTerm', f=True)
            if not cmds.isConnected(weightMaxName + '.outputX', weightOneHotName + '.secondTerm'):
                cmds.connectAttr(weightMaxName + '.outputX', weightOneHotName + '.secondTerm', f=True)

            # Jaw Weight Factor
            jawFactorName = brsPrefix + mouthName + '_jawFactor'
            if not cmds.objExists(jawFactorName):
                cmds.createNode('multiplyDivide', n=jawFactorName, skipSelect=True)
                cmds.setAttr(jawFactorName + '.operation', 1)
            if not cmds.isConnected(weightOneHotName + '.outColorR', jawFactorName + '.input1X'):
                cmds.connectAttr(weightOneHotName + '.outColorR', jawFactorName + '.input1X', f=True)

            # JawWeight
            if isJawOpen:
                if not cmds.isConnected('{}.{}'.format(configJson['src_blendshape'], 'jawOpen'),
                                        jawFactorName + '.input2X'):
                    cmds.connectAttr('{}.{}'.format(configJson['src_blendshape'], 'jawOpen'),
                                     jawFactorName + '.input2X', f=True)
            else:
                if not cmds.isConnected(jawOpenRevName + '.outputX', jawFactorName + '.input2X'):
                    cmds.connectAttr(jawOpenRevName + '.outputX', jawFactorName + '.input2X', f=True)

            # unitConversion
            weightFactorName = brsPrefix + mouthName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, skipSelect=True)
                cmds.setAttr(weightFactorName + '.conversionFactor', 1)  # Tunning
            if not cmds.isConnected(jawFactorName + '.outputX', weightFactorName + '.input'):
                cmds.connectAttr(jawFactorName + '.outputX', weightFactorName + '.input', f=True)

def createConfigGrp(*_):
    poseDataJson = poseData.getPoseData()
    smoothSetsName = brsPrefix + 'smoothSets'
    if not cmds.objExists(smoothSetsName):
        cmds.sets(n=smoothSetsName, empty=True)

    cmds.group(em=True, name=frConfig)
    frExp = brsPrefix + 'updater'
    for attr in cmds.listAttr(frConfig, k=True):  # Clear Transform Attribute
        cmds.setAttr('{}.{}'.format(frConfig, attr), e=True, keyable=False, channelBox=False)
    for at in configJson['rtg_attr']: #Config Attribute
        cmds.addAttr(frConfig, ln=at['name'], at=at['at'], keyable=at['keyable'], min=at['min'], max=at['max'])
        cmds.setAttr('{}.{}'.format(frConfig, at['name']), at['value'], e=True, channelBox=True)
        cmds.setAttr('{}.{}'.format(frConfig, at['name']), e=True, keyable=at['keyable'])
        cmds.setAttr('{}.{}'.format(frConfig, at['name']), e=True, lock=at['lock'])
        if (at['name'] == 'auto_expression'):
            break

    for dataP in poseDataJson: #Expression Attribute
        if dataP['type'] == 'expression':
            cmds.addAttr(frConfig, ln=dataP['name'], at='float', keyable=True, min=0.0, max=1.0)
            cmds.setAttr('{}.{}'.format(frConfig, dataP['name']), 0.0, e=True, channelBox=True)
            cmds.setAttr('{}.{}'.format(frConfig, dataP['name']), e=True, keyable=True)
            cmds.setAttr('{}.{}'.format(frConfig, dataP['name']), e=True, lock=False)
        else:
            continue

    for dataP in poseDataJson:  # Phoneme Attribute
        if dataP['type'] == 'phoneme':
            cmds.addAttr(frConfig, ln=dataP['name'], at='float', keyable=True, min=0.0, max=1.0)
            cmds.setAttr('{}.{}'.format(frConfig, dataP['name']), 0.0, e=True, channelBox=True)
            cmds.setAttr('{}.{}'.format(frConfig, dataP['name']), e=True, keyable=False)
            cmds.setAttr('{}.{}'.format(frConfig, dataP['name']), e=True, lock=False)
        else:
            continue

    phonemeList = [data['name'] for data in poseDataJson if data['type'] == 'phoneme']
    # Phoneme Blend
    for p in phonemeList:
        index = phonemeList.index(p)
        # Phoneme Reverse
        mouthReverseName = brsPrefix + p + '_mouthReverse'
        mouthReverseName = mouthReverseName.replace('.', '_').replace(':', '_')
        if not cmds.objExists(mouthReverseName):
            cmds.createNode('reverse', n=mouthReverseName, skipSelect=True)
        if not cmds.isConnected(frConfig + '.' + p, mouthReverseName + '.inputX'):
            cmds.connectAttr(frConfig + '.' + p, mouthReverseName + '.inputX', f=True)

        mouthRevMinName = brsPrefix + 'mouthRevMin'
        mouthRevMinName = mouthRevMinName.replace('.', '_').replace(':', '_')
        if not cmds.objExists(mouthRevMinName):
            cmds.createNode('combinationShape', n=mouthRevMinName, skipSelect=True)
            cmds.setAttr(mouthRevMinName + '.combinationMethod', 1)
        if not cmds.isConnected(mouthReverseName + '.outputX',
                                mouthRevMinName + '.inputWeight[{}]'.format(index)):
            cmds.connectAttr(mouthReverseName + '.outputX',
                             mouthRevMinName + '.inputWeight[{}]'.format(index),f=True)

    cmds.expression(name=frExp,
                    s=
                    'if (brsFR_core.active == 1 && brsFR_core.deferred == 0)\n' + \
                    '{\npython( \"FacialRetargeter.updater.setRetargetAttribute()\" );\n}\n' + \
                    'else if (brsFR_core.active == 1 && brsFR_core.deferred == 1)' + \
                    '{\npython( \"cmds.evalDeferred(\'FacialRetargeter.updater.setRetargetAttribute()\')\" );\n}\n'
                    )

def poseDataLink(poseData, poseLib, srcBs, dstNs, dataType='blendshape', baseId='001',isUpdate=False):
    """
    :param poseData: poseDataJson
    :param poseLib: poseLibJson
    :param srcBs: source blenshape
    :param dstNs: destination namespace
    :param dataType: 'blendshape', 'expression', 'phoneme'
    :param baseId: 001
    :return: -
    """
    global gMainProgressBar
    mouthShapeList = [data['name'] for data in poseData if data['type'] == 'blendshape' and
                      ('mouth' in data['name'] or 'jaw' in data['name'])]

    # --------------------
    # Main
    # --------------------
    for data in poseData:
        if data['type'] != dataType:
            continue
        bsId = data['id']
        bsAttr = srcBs + '.' + data['name']

        cmds.progressBar(gMainProgressBar, edit=True, step=1,
                         status='Linking {} : {}'.format(data['type'],data['name']))

        for attr in poseLib['attributes']:
            attrName = dstNs + ':' + attr
            #if not 'Jaw_Ctrl.rotateX' in attrName: #Testing for one Attribute
                #continue

            if isUpdate: #skip below when update only
                if not attrName in getObjectAttributeName(cmds.ls(sl=True)):
                    continue

            # Input --------------------
            # Change * Weight
            mdName = brsPrefix + data['name'] + '_' + attrName + '_diffWeight'
            mdName = mdName.replace('.', '_').replace(':', '_')
            if not cmds.objExists(mdName):
                cmds.createNode('multDoubleLinear', n=mdName, skipSelect=True)
            if not isUpdate and dataType in ['blendshape']:
                cmds.connectAttr(bsAttr, mdName + '.input1', f=True)
            elif not isUpdate and dataType in ['expression', 'phoneme']:
                cmds.connectAttr('{}.{}'.format(frConfig, data['name']), mdName + '.input1', f=True)

            if not bsId in poseLib['attributes'][attr]['id']:
                continue
            index = poseLib['attributes'][attr]['id'].index(bsId)
            poseValue = poseLib['attributes'][attr]['value'][index]
            baseData = getIDValue(dstNs,baseId)
            baseValue = baseData[attrName]
            diffValue = poseValue-baseValue
            cmds.setAttr(mdName + '.input2', diffValue)

            if isUpdate == True:
                continue

            # Switch Weight Blend (Optional for other condition weight like mouth switching)
            switchBlendName = brsPrefix + data['name'] + '_' + attrName + '_switchBlend'
            switchBlendName = switchBlendName.replace('.', '_').replace(':', '_')
            if not cmds.objExists(switchBlendName):
                cmds.createNode('multDoubleLinear', n=switchBlendName, skipSelect=True)
                cmds.setAttr(switchBlendName + '.input1', 1)
                cmds.setAttr(switchBlendName + '.input2', 1)
            if not cmds.isConnected(mdName + '.output', switchBlendName + '.input1'):
                cmds.connectAttr(mdName + '.output', switchBlendName + '.input1', f=True)

            # Sum of Weight (Output)
            pmaName = brsPrefix + attrName + '_sum'
            pmaName = pmaName.replace(':', '_').replace('.', '_')
            if not cmds.objExists(pmaName):
                cmds.createNode('plusMinusAverage', n=pmaName, skipSelect=True)
                cmds.setAttr(pmaName + '.input1D[{}]'.format(baseId),baseValue)
            if not cmds.isConnected(switchBlendName + '.output', pmaName + '.input1D[{}]'.format(bsId)):
                cmds.connectAttr(switchBlendName + '.output', pmaName + '.input1D[{}]'.format(bsId), f=True)
            # End of Output --------------------

    # Auto Phoneme Link (Optional)
    if dataType == 'phoneme' and isUpdate == False:
        for data in poseData:
            for attr in poseLib['attributes']:
                attrName = dstNs + ':' + attr

                pmaName = brsPrefix + attrName + '_sum'
                pmaName = pmaName.replace(':', '_').replace('.', '_')
                if not cmds.objExists(pmaName):
                    continue

                # Auto Phoneme Mouth Reverse Link
                for ms in mouthShapeList:
                    switchBlendName = brsPrefix + ms + '_' + attrName + '_switchBlend'
                    switchBlendName = switchBlendName.replace('.', '_').replace(':', '_')
                    mouthRevMinName = brsPrefix + 'mouthRevMin'
                    mouthRevMinName = mouthRevMinName.replace('.', '_').replace(':', '_')
                    if not cmds.objExists(mouthRevMinName) or not cmds.objExists(switchBlendName):
                        continue
                    if not cmds.isConnected(mouthRevMinName + '.outputWeight', switchBlendName + '.input2'):
                        cmds.connectAttr(mouthRevMinName + '.outputWeight', switchBlendName + '.input2', f=True)

def RetargetLink(forceConnect=False,update=False):
    global frConfig, gMainProgressBar
    poseDataJson = poseData.getPoseData()
    poseLibJson = json.load(open(configJson['pose_library_path']))
    srcBs = configJson['src_blendshape']
    dstNs = configJson['dst_namespace']
    baseId = '001'

    clearBake()

    if not update:
        clearLink()
        createConfigGrp()
        autoEmotionLink()
        autoMouthLink()

    totalAttr = len(poseLibJson['attributes'])
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    cmds.progressBar(gMainProgressBar,
                     edit=True,
                     beginProgress=True,
                     isInterruptable=False,
                     maxValue=len(poseDataJson) + 1)

    poseDataLink(poseDataJson, poseLibJson, srcBs, dstNs, dataType='blendshape', baseId=baseId, isUpdate=update)
    poseDataLink(poseDataJson, poseLibJson, srcBs, dstNs, dataType='expression', baseId=baseId, isUpdate=update)
    poseDataLink(poseDataJson, poseLibJson, srcBs, dstNs, dataType='phoneme', baseId=baseId, isUpdate=update)

    """
    # blendshape link
    for data in poseDataJson:
        if data['type'] != 'blendshape':
            continue
        bsId = data['id']
        bsAttr = srcBs + '.' + data['name']

        cmds.progressBar(gMainProgressBar, edit=True, step=1,
                         status='Linking Blendshape To Pose : {} ( total {} attributes )'.format(data['name'],
                                                                                                 totalAttr))

        for attr in poseLibJson['attributes']:
            attrName = dstNs + ':' + attr

            if update: #skip below when update only
                if not attrName in getObjectAttributeName(cmds.ls(sl=True)):
                    continue

            mdName = brsPrefix + data['name'] + '_' + attrName + '_mulDou'
            mdName = mdName.replace('.', '_')
            mdName = mdName.replace(':', '_')
            if not cmds.objExists(mdName):
                cmds.createNode('multDoubleLinear', n=mdName, skipSelect=True)
                cmds.connectAttr(bsAttr, mdName + '.input1', f=True)

            if not bsId in poseLibJson['attributes'][attr]['id']:
                continue
            index = poseLibJson['attributes'][attr]['id'].index(bsId)
            poseValue = poseLibJson['attributes'][attr]['value'][index]
            baseData = getIDValue(dstNs,baseId)
            baseValue = baseData[attrName]
            diffValue = poseValue-baseValue
            cmds.setAttr(mdName + '.input2', diffValue)

            pmaName = brsPrefix + attrName + '_sum'
            pmaName = pmaName.replace(':', '_')
            pmaName = pmaName.replace('.', '_')
            if not cmds.objExists(pmaName):
                cmds.createNode('plusMinusAverage', n=pmaName, skipSelect=True)
                if forceConnect:
                    cmds.connectAttr(pmaName + '.output1D', attrName, f=True)
                cmds.setAttr(pmaName + '.input1D[{}]'.format(baseId),baseValue)
            if not cmds.isConnected(mdName + '.output', pmaName + '.input1D[{}]'.format(bsId)):
                cmds.connectAttr(mdName + '.output', pmaName + '.input1D[{}]'.format(bsId), f=True)
    
    # expression link
    for data in poseDataJson:
        if data['type'] != 'expression':
            continue
        bsId = data['id']
        bsAttr = srcBs + '.' + data['name']

        cmds.progressBar(gMainProgressBar, edit=True, step=1,
                         status='Linking Expression To Pose : {} ( total {} attributes )'.format(data['name'],
                                                                                                 totalAttr))

        for attr in poseLibJson['attributes']:
            attrName = dstNs + ':' + attr

            if update:  # skip below when update only
                if not attrName in getObjectAttributeName(cmds.ls(sl=True)):
                    continue

            mdName = brsPrefix + data['name'] + '_' + attrName + '_mulDou'
            mdName = mdName.replace('.', '_')
            mdName = mdName.replace(':', '_')
            if not cmds.objExists(mdName):
                cmds.createNode('multDoubleLinear', n=mdName, skipSelect=True)
                cmds.connectAttr('{}.{}'.format(frConfig, data['name']), mdName + '.input1', f=True)

            if not bsId in poseLibJson['attributes'][attr]['id']:
                continue
            index = poseLibJson['attributes'][attr]['id'].index(bsId)
            poseValue = poseLibJson['attributes'][attr]['value'][index]
            baseData = getIDValue(dstNs,baseId)
            baseValue = baseData[attrName]
            diffValue = poseValue-baseValue
            cmds.setAttr(mdName + '.input2', diffValue)

            pmaName = brsPrefix + attrName + '_sum'
            pmaName = pmaName.replace(':', '_')
            pmaName = pmaName.replace('.', '_')
            if cmds.objExists(pmaName) and not cmds.isConnected(mdName + '.output', pmaName + '.input1D[{}]'.format(bsId)):
                cmds.connectAttr(mdName + '.output', pmaName + '.input1D[{}]'.format(bsId), f=True)
    """

    """
    emotionList = [data['name'] for data in poseDataJson if data['type'] == 'expression']
    for emotionName in emotionList:
        weightFactorName = brsPrefix + emotionName + '_weightFactor'
        cmds.connectAttr(weightFactorName + '.output', frConfig + '.' + emotionName,
                         f=True)
    """

    #End Progress
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    print('Retarget Link Finish')

def bakeRetarget(*_):
    poseDataJson = poseData.getPoseData()
    poseLibJson = json.load(open(configJson['pose_library_path']))
    srcBs = configJson['src_blendshape']
    dstNs = configJson['dst_namespace']

    attrList = []
    for attr in poseLibJson['attributes']:
        attrName = dstNs + ':' + attr
        if cmds.objExists(attrName):
            attrList.append(attrName)

    minKeyframe = round(cmds.playbackOptions(q=True, minTime=True))
    maxKeyframe = round(cmds.playbackOptions(q=True, maxTime=True))
    cmds.bakeResults(
        attrList,
        simulation=True,
        t=(minKeyframe,maxKeyframe),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=True,
        sparseAnimCurveBake=False,
        minimizeRotation=True
    )
    clearLink()

def addSmoothSelection(*_):
    poseLibJson = json.load(open(configJson['pose_library_path']))
    dstNs = configJson['dst_namespace']
    selection = cmds.ls(sl=True)
    smoothSetsName = brsPrefix + 'smoothSets'
    if not cmds.objExists(smoothSetsName):
        cmds.sets(n=smoothSetsName, empty=True)

    if selection == None or selection == []:
        return None

    for attr in poseLibJson['attributes']:
        objName = '{}:{}'.format(dstNs, attr.split('.')[0])
        if objName in selection:
            cmds.sets(objName, e=True, addElement=smoothSetsName)

def removeSmoothSelection(*_):
    smoothSetsName = brsPrefix + 'smoothSets'
    selection = cmds.ls(sl=True)
    if selection == None or selection == []:
        return None

    for objName in selection:
        cmds.sets(objName, remove=smoothSetsName)

if __name__ == 'reTargeter':
    #clearLink()
    #createConfigGrp()
    #autoEmotionLink()
    #autoMouthLink()
    pass




