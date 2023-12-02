"""
BRSFR FACE RETARGETER
"""
import json, os, sys, time
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

if sys.version[0] == '3':pass

def reloadConfig(*_):
    global configJson
    configJson = json.load(open(configPath))

def getIDValue(nameSpace,id):
    poseLibJson = json.load(open(configJson['pose_library_path']))

    attr_list = [attr for attr in poseLibJson['attributes'] if id in poseLibJson['attributes'][attr]['id']]
    dstAttr_list = ['{}:{}'.format(nameSpace, attr) for attr in attr_list]
    index_list = [poseLibJson['attributes'][attr]['id'].index(id) for attr in attr_list]
    dstValue_list = [poseLibJson['attributes'][attr]['value'][i] for i,attr in zip(index_list,attr_list)]

    data = {}
    for dstAttr,dstValue in zip(dstAttr_list,dstValue_list):
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
                         status='Readind Blendshape&Expression Data.. {}'.format(dataP['type']))
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

def get_update_attr_poselib(pose_lib_json,attrName,srcBlendshape,dstNamespace,learnRate=0.75): #Correct Pose For One Attribute
    #pose_lib_json = json.load(open(configJson['pose_library_path']))
    poseDataJson = poseData.getPoseData()
    curFrame = cmds.currentTime(q=True)
    #print('frame = {}'.format(curFrame))

    baseId = '001'

    #attrName = 'PRE_Full_Armor:cmouth_corner_r.translateX'

    #get new target valuse set
    targetValue = cmds.getAttr(attrName,t=curFrame)
    #print ('target result = {}'.format(targetValue))

    #get current bs attr
    srcBsData = getSrcBsData(srcBlendshape,[curFrame,curFrame+1])
    #print(srcBsData)

    pmaName = brsPrefix + attrName + '_sum'
    pmaName = pmaName.replace(':', '_').replace('.', '_')
    result = cmds.getAttr(pmaName+'.output1D')
    #print('current result = {}'.format(result))

    diffValue = targetValue - result
    #print('difference value = {}'.format(diffValue))
    if diffValue == 0.0:
        #print('skip {} because value not change'.format(attrName))
        return None

    #bsData Normalization
    bsData = {
        'id' : [],
        'value' : [],
        'sets' : [],
    }
    baseData = getIDValue(nameSpace=dstNamespace, id=baseId)
    for bsId in sorted(list(srcBsData)):
        index = srcBsData[bsId]['frame'].index(curFrame)
        bsValue = srcBsData[bsId]['value'][index]
        poseLibData = getIDValue(nameSpace=dstNamespace,id=bsId)
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
        setsName = [poseDataJson[i]['sets'] for i in range(len(poseDataJson)) if poseDataJson[i]['id'] == bsId][0]
        bsData['sets'].append(setsName)

    #split value by value/sum ratio
    oldValue,newValue = (0.00,0.00)
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

        pose_value_new = poseValue + ( diffValue_new * learnRate )
        pose_value_new = round(pose_value_new, 4)
        #print('id {}     new pose lib value = {}'.format(bsId,pose_value_new))

        #apply poseLib data
        attr = attrName.split(':')[1]
        a_ls = [a for a in pose_lib_json['attributes'] if a == attr]
        for a in a_ls:
            idx = pose_lib_json['attributes'][a]['id'].index(bsId)
            pose_lib_json['attributes'][a_ls[0]]['value'][idx] = pose_value_new
            print (pose_value_new,pose_lib_json['attributes'][a]['value'][index])
        #for a in [a for a in pose_lib_json['attributes'] if a == attr]:
            #if a == attr:
                #index = pose_lib_json['attributes'][a]['id'].index(bsId)
                #pose_lib_json['attributes'][a]['value'][index] = pose_value_new

        #oldValue = poseValue
        #newValue = pose_value_new
    return pose_lib_json

def updatePoseLibSelection(*_):
    pose_lib_json = json.load(open(configJson['pose_library_path']))
    dstNs = configJson['dst_namespace']
    sel = cmds.ls(sl=1)
    update_sel_ls = []

    cache_data = {}

    #Update New Pose
    for obj_name in sel:
        for a in cmds.listAttr(obj_name,k=1):
            attr_name = '{}.{}'.format(obj_name,a)
            no_ns_attr = attr_name.split(':')[1]
            if no_ns_attr in pose_lib_json['attributes']:
                update_pl = get_update_attr_poselib(pose_lib_json,attr_name,
                                                     configJson['src_blendshape'],configJson['dst_namespace'])
                if not update_pl == None:
                    cache_data = update_pl
                    update_sel_ls.append(obj_name)
                    print('{} Updated in Pose Library\n'.format(attr_name)),
            else:
                continue
    update_sel_ls = list(set(update_sel_ls))
    if cache_data == {} or cache_data == None:
        return None
    else:
        # save update pose library
        with open(configJson['pose_library_path'], 'w') as f:
            json.dump(cache_data, f, sort_keys=True, indent=4, separators=(',', ':'))
            f.close()

    #update
    cmds.select(update_sel_ls)
    RetargetLink(update=True)
    cmds.select(sel)
    updater.setRetargetAttribute()
    print ('Update Retarget Link Finish\n'),

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
                cmds.createNode('floatMath', n=errorName, ss=1)
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
                cmds.createNode('floatMath', n=squareName, ss=1)
                cmds.connectAttr(errorName + '.outFloat', squareName + '.floatA')
                cmds.setAttr(squareName + '.floatB', 2)
                cmds.setAttr(squareName + '.operation', 6)

            sqrtName = brsPrefix + data['name'] + '_' + emotionName + '_sqrt'
            if not cmds.objExists(sqrtName):
                cmds.createNode('floatMath', n=sqrtName, ss=1)
                cmds.connectAttr(squareName + '.outFloat', sqrtName + '.floatA')
                cmds.setAttr(sqrtName + '.floatB', 0.5)
                cmds.setAttr(sqrtName + '.operation', 6)

            avgName = brsPrefix + emotionName + '_totalErrorAvg'
            if not cmds.objExists(avgName):
                cmds.createNode('plusMinusAverage', n=avgName, ss=1)
                cmds.setAttr(avgName + '.operation', 3)
            if cmds.objExists(avgName):
                cmds.connectAttr(sqrtName + '.outFloat', avgName + '.input1D[{}]'.format(data_index), f=True)

            weightName = brsPrefix + emotionName + '_weight'
            if not cmds.objExists(weightName):
                cmds.createNode('reverse', n=weightName, ss=1)
            if not cmds.isConnected(avgName + '.output1D', weightName + '.inputX'):
                cmds.connectAttr(avgName + '.output1D', weightName + '.inputX', f=True)

            weightTotalName = brsPrefix + 'emotion' + '_weightTotal'
            if not cmds.objExists(weightTotalName):
                cmds.createNode('plusMinusAverage', n=weightTotalName, ss=1)
            if not cmds.isConnected(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(emotion_index)):
                cmds.connectAttr(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(emotion_index),
                                 f=True)

            weightMinName = brsPrefix + 'emotion' + '_weightMin'
            if not cmds.objExists(weightMinName):
                cmds.createNode('combinationShape', n=weightMinName, ss=1)
                cmds.setAttr(weightMinName + '.combinationMethod', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(emotion_index)):
                cmds.connectAttr(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(emotion_index),
                                 f=True)

            # (weightName - weightMinName)
            weightMinMinusName = brsPrefix + emotionName + '_weightMinMinus'
            if not cmds.objExists(weightMinMinusName):
                cmds.createNode('floatMath', n=weightMinMinusName, ss=1)
                cmds.setAttr(weightMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinMinusName + '.floatA'):
                cmds.connectAttr(weightName + '.outputX', weightMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightMinMinusName + '.floatB', f=True)

            # (weightTotalName - weightMinName)
            weightTotalMinMinusName = brsPrefix + emotionName + '_weightTotalMinMinus'
            if not cmds.objExists(weightTotalMinMinusName):
                cmds.createNode('floatMath', n=weightTotalMinMinusName, ss=1)
                cmds.setAttr(weightTotalMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA'):
                cmds.connectAttr(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB', f=True)

            # (weightName - weightMinName) / (weightTotalName - weightMinName)
            weightDevideName = brsPrefix + emotionName + '_weightDevide'
            if not cmds.objExists(weightDevideName):
                cmds.createNode('multiplyDivide', n=weightDevideName, ss=1)
                cmds.setAttr(weightDevideName + '.operation', 2)
            if not cmds.isConnected(weightMinMinusName + '.outFloat', weightDevideName + '.input1X'):
                cmds.connectAttr(weightMinMinusName + '.outFloat', weightDevideName + '.input1X', f=True)
            if not cmds.isConnected(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X'):
                cmds.connectAttr(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X', f=True)

            """
            # unitConversion
            weightFactorName = brsPrefix + emotionName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, ss=1)
                cmds.setAttr(weightFactorName + '.conversionFactor', 1)  # Tunning
            if not cmds.isConnected(weightDevideName + '.outputX', weightFactorName + '.input'):
                cmds.connectAttr(weightDevideName + '.outputX', weightFactorName + '.input', f=True)
            """

            weightDevideReverseName = brsPrefix + emotionName + '_weightDevideReverse'
            if not cmds.objExists(weightDevideReverseName):
                cmds.createNode('reverse', n=weightDevideReverseName, ss=1)
            if not cmds.isConnected(weightDevideName + '.outputX', weightDevideReverseName + '.inputX'):
                cmds.connectAttr(weightDevideName + '.outputX', weightDevideReverseName + '.inputX', f=True)

            weightMaxReverseName = brsPrefix + 'emotion' + '_weightMaxReverse'
            if not cmds.objExists(weightMaxReverseName):
                cmds.createNode('combinationShape', n=weightMaxReverseName, ss=1)
                cmds.setAttr(weightMaxReverseName + '.combinationMethod', 1)
            if not cmds.isConnected(weightDevideReverseName + '.outputX', weightMaxReverseName + '.inputWeight[{}]'.format(emotion_index)):
                cmds.connectAttr(weightDevideReverseName + '.outputX', weightMaxReverseName + '.inputWeight[{}]'.format(emotion_index),
                                 f=True)

            weightMaxName = brsPrefix + 'emotion' + '_weightMax'
            if not cmds.objExists(weightMaxName):
                cmds.createNode('reverse', n=weightMaxName, ss=1)
            if not cmds.isConnected(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX'):
                cmds.connectAttr(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX', f=True)

            weightOneHotName = brsPrefix + emotionName + '_weightOneHot'
            if not cmds.objExists(weightOneHotName):
                cmds.createNode('condition', n=weightOneHotName, ss=1)
                cmds.setAttr(weightOneHotName + '.colorIfTrueR', 1)
                cmds.setAttr(weightOneHotName + '.colorIfFalseR', 0)
            if not cmds.isConnected(weightDevideName + '.outputX', weightOneHotName + '.firstTerm'):
                cmds.connectAttr(weightDevideName + '.outputX', weightOneHotName + '.firstTerm', f=True)
            if not cmds.isConnected(weightMaxName + '.outputX', weightOneHotName + '.secondTerm'):
                cmds.connectAttr(weightMaxName + '.outputX', weightOneHotName + '.secondTerm', f=True)

            # unitConversion
            weightFactorName = brsPrefix + emotionName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, ss=1)
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
        cmds.createNode('reverse', n=jawOpenRevName, ss=1)
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
                cmds.createNode('floatMath', n=errorName, ss=1)
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
                cmds.createNode('floatMath', n=squareName, ss=1)
                cmds.connectAttr(errorName + '.outFloat', squareName + '.floatA')
                cmds.setAttr(squareName + '.floatB', 2)
                cmds.setAttr(squareName + '.operation', 6)

            sqrtName = brsPrefix + data['name'] + '_' + mouthName + '_sqrt'
            if not cmds.objExists(sqrtName):
                cmds.createNode('floatMath', n=sqrtName, ss=1)
                cmds.connectAttr(squareName + '.outFloat', sqrtName + '.floatA')
                cmds.setAttr(sqrtName + '.floatB', 0.5)
                cmds.setAttr(sqrtName + '.operation', 6)

            avgName = brsPrefix + mouthName + '_totalErrorAvg'
            if not cmds.objExists(avgName):
                cmds.createNode('plusMinusAverage', n=avgName, ss=1)
                cmds.setAttr(avgName + '.operation', 3)
            if cmds.objExists(avgName):
                cmds.connectAttr(sqrtName + '.outFloat', avgName + '.input1D[{}]'.format(data_index), f=True)

            weightName = brsPrefix + mouthName + '_weight'
            if not cmds.objExists(weightName):
                cmds.createNode('reverse', n=weightName, ss=1)
            if not cmds.isConnected(avgName + '.output1D', weightName + '.inputX'):
                cmds.connectAttr(avgName + '.output1D', weightName + '.inputX', f=True)

            weightTotalName = brsPrefix + jawNode + '_weightTotal'
            if not cmds.objExists(weightTotalName):
                cmds.createNode('plusMinusAverage', n=weightTotalName, ss=1)
            if not cmds.isConnected(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(mouth_index)):
                cmds.connectAttr(weightName + '.outputX', weightTotalName + '.input1D[{}]'.format(mouth_index),
                                 f=True)

            weightMinName = brsPrefix + jawNode + '_weightMin'
            if not cmds.objExists(weightMinName):
                cmds.createNode('combinationShape', n=weightMinName, ss=1)
                cmds.setAttr(weightMinName + '.combinationMethod', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(mouth_index)):
                cmds.connectAttr(weightName + '.outputX', weightMinName + '.inputWeight[{}]'.format(mouth_index),
                                 f=True)

            # (weightName - weightMinName)
            weightMinMinusName = brsPrefix + mouthName + '_weightMinMinus'
            if not cmds.objExists(weightMinMinusName):
                cmds.createNode('floatMath', n=weightMinMinusName, ss=1)
                cmds.setAttr(weightMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightName + '.outputX', weightMinMinusName + '.floatA'):
                cmds.connectAttr(weightName + '.outputX', weightMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightMinMinusName + '.floatB', f=True)

            # (weightTotalName - weightMinName)
            weightTotalMinMinusName = brsPrefix + mouthName + '_weightTotalMinMinus'
            if not cmds.objExists(weightTotalMinMinusName):
                cmds.createNode('floatMath', n=weightTotalMinMinusName, ss=1)
                cmds.setAttr(weightTotalMinMinusName + '.operation', 1)
            if not cmds.isConnected(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA'):
                cmds.connectAttr(weightTotalName + '.output1D', weightTotalMinMinusName + '.floatA', f=True)
            if not cmds.isConnected(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB'):
                cmds.connectAttr(weightMinName + '.outputWeight', weightTotalMinMinusName + '.floatB', f=True)

            # (weightName - weightMinName) / (weightTotalName - weightMinName)
            weightDevideName = brsPrefix + mouthName + '_weightDevide'
            if not cmds.objExists(weightDevideName):
                cmds.createNode('multiplyDivide', n=weightDevideName, ss=1)
                cmds.setAttr(weightDevideName + '.operation', 2)
            if not cmds.isConnected(weightMinMinusName + '.outFloat', weightDevideName + '.input1X'):
                cmds.connectAttr(weightMinMinusName + '.outFloat', weightDevideName + '.input1X', f=True)
            if not cmds.isConnected(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X'):
                cmds.connectAttr(weightTotalMinMinusName + '.outFloat', weightDevideName + '.input2X', f=True)

            """
            # unitConversion
            weightFactorName = brsPrefix + mouthName + '_weightFactor'
            if not cmds.objExists(weightFactorName):
                cmds.createNode('unitConversion', n=weightFactorName, ss=1)
                cmds.setAttr(weightFactorName + '.conversionFactor', 13)  # Tunning
            if not cmds.isConnected(weightDevideName + '.outputX', weightFactorName + '.input'):
                cmds.connectAttr(weightDevideName + '.outputX', weightFactorName + '.input', f=True)
            """

            weightDevideReverseName = brsPrefix + mouthName + '_weightDevideReverse'
            if not cmds.objExists(weightDevideReverseName):
                cmds.createNode('reverse', n=weightDevideReverseName, ss=1)
            if not cmds.isConnected(weightDevideName + '.outputX', weightDevideReverseName + '.inputX'):
                cmds.connectAttr(weightDevideName + '.outputX', weightDevideReverseName + '.inputX', f=True)

            weightMaxReverseName = brsPrefix + jawNode + '_weightMaxReverse'
            if not cmds.objExists(weightMaxReverseName):
                cmds.createNode('combinationShape', n=weightMaxReverseName, ss=1)
                cmds.setAttr(weightMaxReverseName + '.combinationMethod', 1)
            if not cmds.isConnected(weightDevideReverseName + '.outputX',
                                    weightMaxReverseName + '.inputWeight[{}]'.format(mouth_index)):
                cmds.connectAttr(weightDevideReverseName + '.outputX',
                                 weightMaxReverseName + '.inputWeight[{}]'.format(mouth_index),
                                 f=True)

            weightMaxName = brsPrefix + jawNode + '_weightMax'
            if not cmds.objExists(weightMaxName):
                cmds.createNode('reverse', n=weightMaxName, ss=1)
            if not cmds.isConnected(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX'):
                cmds.connectAttr(weightMaxReverseName + '.outputWeight', weightMaxName + '.inputX', f=True)

            weightOneHotName = brsPrefix + mouthName + '_weightOneHot'
            if not cmds.objExists(weightOneHotName):
                cmds.createNode('condition', n=weightOneHotName, ss=1)
                cmds.setAttr(weightOneHotName + '.colorIfTrueR', 1)
                cmds.setAttr(weightOneHotName + '.colorIfFalseR', 0)
            if not cmds.isConnected(weightDevideName + '.outputX', weightOneHotName + '.firstTerm'):
                cmds.connectAttr(weightDevideName + '.outputX', weightOneHotName + '.firstTerm', f=True)
            if not cmds.isConnected(weightMaxName + '.outputX', weightOneHotName + '.secondTerm'):
                cmds.connectAttr(weightMaxName + '.outputX', weightOneHotName + '.secondTerm', f=True)

            # Jaw Weight Factor
            jawFactorName = brsPrefix + mouthName + '_jawFactor'
            if not cmds.objExists(jawFactorName):
                cmds.createNode('multiplyDivide', n=jawFactorName, ss=1)
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
                cmds.createNode('unitConversion', n=weightFactorName, ss=1)
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
            cmds.createNode('reverse', n=mouthReverseName, ss=1)
        if not cmds.isConnected(frConfig + '.' + p, mouthReverseName + '.inputX'):
            cmds.connectAttr(frConfig + '.' + p, mouthReverseName + '.inputX', f=True)

        mouthRevMinName = brsPrefix + 'mouthRevMin'
        mouthRevMinName = mouthRevMinName.replace('.', '_').replace(':', '_')
        if not cmds.objExists(mouthRevMinName):
            cmds.createNode('combinationShape', n=mouthRevMinName, ss=1)
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
    pl_attr_ls = [i for i in poseLib['attributes']]
    for data in poseData:
        if data['type'] != dataType:
            continue
        bsId = data['id']
        bsAttr = srcBs + '.' + data['name']

        cmds.progressBar(gMainProgressBar, edit=True, step=1,
                         status='Linking {} : {}'.format(data['type'],data['name']))

        for attr in pl_attr_ls:
            attrName = dstNs + ':' + attr
            objName = dstNs + ':' + attr.split('.')[0]
            if cmds.objExists(objName):
                cmds.cutKey(objName)
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
                cmds.createNode('multDoubleLinear', n=mdName, ss=1)
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
                cmds.createNode('multDoubleLinear', n=switchBlendName, ss=1)
                cmds.setAttr(switchBlendName + '.input1', 1)
                cmds.setAttr(switchBlendName + '.input2', 1)
            if not cmds.isConnected(mdName + '.output', switchBlendName + '.input1'):
                cmds.connectAttr(mdName + '.output', switchBlendName + '.input1', f=True)

            # Sum of Weight (Output)
            pmaName = brsPrefix + attrName + '_sum'
            pmaName = pmaName.replace(':', '_').replace('.', '_')
            if not cmds.objExists(pmaName):
                cmds.createNode('plusMinusAverage', n=pmaName, ss=1)
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

    if not cmds.objExists(srcBs):
        cmds.error('\ncan\'t found source blendshape, please check.\n')

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

    #End Progress
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    print('Retarget Link Finish\n'),

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




