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
frConfig = brsPrefix + 'config'

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
    # poseDataJson = json.load(open(configJson['pose_data_path']))
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

def updateAttrPoseLib(attrName,srcBlendshape,dstNamespace,libraryPath): #Correct Pose For One Attribute
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
    pmaName = pmaName.replace(':', '_')
    pmaName = pmaName.replace('.', '_')
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

        poseValue_new = poseValue + diffValue_new
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
    frConfig = brsPrefix + 'config'
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
    for i in cmds.ls():
        if i.__contains__(brsPrefix):
            try:
                cmds.delete(i)
            except:
                pass

def createConfigGrp(*_):
    # poseDataJson = json.load(open(configJson['pose_data_path']))
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

    cmds.expression(name=frExp,
                    s=
                    'if (brsFR_config.active == 1 && brsFR_config.deferred == 0)\n' + \
                    '{\npython( \"FacialRetargeter.updater.setRetargetAttribute()\" );\n}\n' + \
                    'else if (brsFR_config.active == 1 && brsFR_config.deferred == 1)' + \
                    '{\npython( \"cmds.evalDeferred(\'FacialRetargeter.updater.setRetargetAttribute()\')\" );\n}\n'
                    )


def RetargetLink(forceConnect=False,update=False):
    # poseDataJson = json.load(open(configJson['pose_data_path']))
    poseDataJson = poseData.getPoseData()
    poseLibJson = json.load(open(configJson['pose_library_path']))
    srcBs = configJson['src_blendshape']
    dstNs = configJson['dst_namespace']
    baseId = '001'

    clearBake()

    if not update:
        clearLink()
        createConfigGrp()

    totalAttr = len(poseLibJson['attributes'])
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    cmds.progressBar(gMainProgressBar,
                     edit=True,
                     beginProgress=True,
                     isInterruptable=False,
                     maxValue=len(poseDataJson) + 1)

    # blendshpae link
    for data in poseDataJson:
        if data['type'] != 'blendshape':
            continue
        bsId = data['id']
        bsAttr = srcBs + '.' + data['name']

        cmds.progressBar(gMainProgressBar, edit=True, step=1,
                         status='Linking Blendshape To Pose : {} ( total {} attributes )'.format(data['name'],
                                                                                                 totalAttr))

        for attr in poseLibJson['attributes']:
            #if attr != 'cJaw.rotateZ':
                #continue

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
            frConfig = brsPrefix + 'config'

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

    #End Progress
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    cmds.select(cl=True)

def bakeRetarget(*_):
    # poseDataJson = json.load(open(configJson['pose_data_path']))
    poseDataJson = poseData.getPoseData()
    poseLibJson = json.load(open(configJson['pose_library_path']))
    srcBs = configJson['src_blendshape']
    dstNs = configJson['dst_namespace']

    attrList = []
    for attr in poseLibJson['attributes']:
        attrName = dstNs + ':' + attr
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
