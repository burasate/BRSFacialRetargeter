"""
POSE LIBRARY CAPTURE
reference
https://melindaozel.com/FACS-cheat-sheet/?fbclid=IwAR0y0MfuAg1GdXVPrhKZVckFEvMHoejOHdYpaRINS8Lobs2bNNAGJUk-RSU
"""
import json, os, time, sys, random
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))

import imp
import poseData
imp.reload(poseData)

if sys.version[0] == '3':
    writeMode = 'w'
else:
    writeMode = 'wb'

def getSelection(*_):
    selection = cmds.ls(sl=True)
    objectList = []
    attrList = []
    namespc = None
    if selection[0].__contains__(':'):
        namespc = selection[0].split(':')[0]

    for obj in selection:
        objName = obj
        if obj.__contains__(':'):
            objName = obj.split(':')[-1]
        objectList.append(objName)

        keyList = cmds.listAttr(obj, keyable=True, unlocked=True)
        if keyList == None:
            print('skip {} because havn\'t keyframe'.format(obj))
            continue
        for attr in keyList:
            attrList.append('{}.{}'.format(objName, attr))

    return {
        'selection': selection,
        'namespace': namespc,
        'objects': objectList,
        'attributes': attrList
    }

def savePoseLibrary(filePath):

    poseDataJson = poseData.getPoseData()
    selectData = getSelection()

    data = {
        'attributes': {},
        'pose_attribute': {},
        'metadata': {
            'created' : time.time()
        }
    }
    for dataP in poseDataJson:
        frame = dataP['id']
        cmds.currentTime(frame)
        # print ('Record Frame to ID {}'.format(frame))

        for attr in selectData['attributes']:
            # add atribute name in data
            if not attr in data['attributes']:
                data['attributes'][attr] = {}
                data['attributes'][attr]['id'] = []
                data['attributes'][attr]['value'] = []

            # get attribute value
            fullAttrName = '{}:{}'.format(selectData['namespace'], attr)
            if not cmds.objExists(fullAttrName):
                continue
            value = cmds.getAttr(fullAttrName, time=frame)
            if type(value) == type(list()):
                value = value[0]
            if type(value) == type(bool()):
                value = int(value)

            # add id and value in data
            data['attributes'][attr]['id'].append(str(frame))
            data['attributes'][attr]['value'].append(value)
            if dataP['id'] == "001": # is Base
                data['pose_attribute'][attr] = round(value, 6)

            # print('id (frame)  {}     {}  =  {}'.format(frame, fullAttrName, value))

    # share sets value
    setsList = [d['sets'] for d in poseDataJson]
    idList = [int(d['id']) for d in poseDataJson]
    #zip_setsId = zip(idList,setsList)
    for attr in data['attributes']:
        effectiveList = []
        valueDict = {}
        for i in range(len(idList)):
            s = setsList[i]
            if not s in valueDict:
                valueDict[s] = []
            v = data['attributes'][attr]['value'][i]
            v = round(v,6)
            valueDict[s].append(v)
        #print(attr, valueDict)

        setAvg = {}
        shareRate_avg = 0.0
        for s in valueDict:
            avg = sum(valueDict[s])/len(valueDict[s])
            rate = 0.01
            shareRate = avg * rate
            setAvg[s] = shareRate
            #print('shareRate', s,shareRate)
            #print('average', s, sum(valueDict[s]),len(valueDict[s]), avg) #setAvg in line

            value_base = data['attributes'][attr]['value'][0] # value from base pose
            for i in range(len(idList)): #get share rate
                value_id = data['attributes'][attr]['value'][i]
                isEffective = (setsList[i] == s) and (value_base != value_id)
                if isEffective:
                    if not s in effectiveList: # for report effective
                        effectiveList.append(s)

                shareRateList = [setAvg[s] for s in setAvg if s in effectiveList]
                if shareRateList != []:
                    shareRate_avg = sum(shareRateList)/len(shareRateList)
                shareRate_avg = abs(round(shareRate_avg, 6))

        # report effective with
        if effectiveList != []:
            print('{} effect with {}  Share Rate {}\n'.format(attr, effectiveList, shareRate_avg)),

        # apply average to same set name
        for i in range(len(idList)):
            if setsList[i] in effectiveList:
                shareRate_rand = round( random.uniform(shareRate_avg * -1, shareRate_avg) , 6)
                new_v = data['attributes'][attr]['value'][i] + shareRate_rand
                data['attributes'][attr]['value'][i] = new_v
                #print('{} {} {} seed = {} , new value = {}'.format(attr, idList[i], setsList[i], shareRate_rand, new_v))


    # delete useless attribute
    delAttrList = []
    print ('before cleanup attr', len(data['attributes']))
    for attr in data['attributes']:
        minValue = min(data['attributes'][attr]['value'])
        maxValue = max(data['attributes'][attr]['value'])
        if minValue == maxValue:
            delAttrList.append(attr)
    for attr in delAttrList:
        del data['attributes'][attr]
    print ('after cleanup attr', len(data['attributes']))

    """
    # get min / max value
    for attr in data['attributes']:
        min(data['attributes'][attr]['value'])
    """

    # save pose library
    outFile = open(filePath, writeMode)
    json.dump(data, outFile, sort_keys=True, indent=4)
    print('Pose Capture Finish\n'),

    # backup pose library
    outFile = open(filePath.replace('.json','_Backup.json'), writeMode)
    json.dump(data, outFile, sort_keys=True, indent=4)

def loadPoseLibrary(filePath,dstNs):
    poseLibJson = json.load(open(configJson['pose_library_path']))

    sel = []
    for attr in poseLibJson['attributes']:
        attrName = '{}:{}'.format(dstNs,attr)
        if not cmds.objExists(attrName):
            cmds.warning('not found {}'.format(attrName))
            continue
        cmds.cutKey(attrName)
        for f in poseLibJson['attributes'][attr]['id']:
            index = poseLibJson['attributes'][attr]['id'].index(f)
            value = poseLibJson['attributes'][attr]['value'][index]
            cmds.setKeyframe(attrName, t=f, v=value)
        sel.append(attrName)
    sel = list(set([i.split('.')[0] for i in sel]))
    cmds.select(sel)

def createPoseLibrary(filePath):
    poseDataJson = poseData.getPoseData()
    selectData = getSelection()

    cmds.cutKey(selectData['selection'])
    keyList = []
    for data in poseDataJson:
        keyList.append(data['id'])
    cmds.setKeyframe(selectData['selection'], t=keyList)

    savePoseLibrary(filePath)