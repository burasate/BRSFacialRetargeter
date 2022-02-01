"""
POSE LIBRARY CAPTURE
reference
https://melindaozel.com/FACS-cheat-sheet/?fbclid=IwAR0y0MfuAg1GdXVPrhKZVckFEvMHoejOHdYpaRINS8Lobs2bNNAGJUk-RSU
"""
import json, os, time
import maya.cmds as cmds
import maya.mel as mel

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))

import imp
import poseData
imp.reload(poseData)

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

        #print(cmds.listAttr(obj, keyable=True, unlocked=True))
        for attr in cmds.listAttr(obj, keyable=True, unlocked=True):
            attrList.append('{}.{}'.format(objName, attr))

    return {
        'selection': selection,
        'namespace': namespc,
        'objects': objectList,
        'attributes': attrList
    }

def savePoseLibrary(filePath):
    #poseDataJson = json.load(open(configJson['pose_data_path']))
    poseDataJson = poseData.getPoseData()
    selectData = getSelection()

    data = {
        'attributes': {},
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

            # print('id (frame)  {}     {}  =  {}'.format(frame, fullAttrName, value))


    # delete useless attribute
    delAttrList = []
    for attr in data['attributes']:
        if not cmds.objExists(attr):
            continue
        minValue = min(data['attributes'][attr]['value'])
        maxValue = max(data['attributes'][attr]['value'])
        if minValue == maxValue:
            delAttrList.append(attr)
    for attr in delAttrList:
        del data['attributes'][attr]

    """
    # get min / max value
    for attr in data['attributes']:
        min(data['attributes'][attr]['value'])
    """

    # save pose library
    print('\nPose Capture Finish\n')
    outFile = open(filePath, 'wb')
    json.dump(data, outFile, sort_keys=True, indent=4)

    # backup pose library
    outFile = open(filePath.replace('.json','_Backup.json'), 'wb')
    json.dump(data, outFile, sort_keys=True, indent=4)

def loadPoseLibrary(filePath,dstNs):
    poseLibJson = json.load(open(configJson['pose_library_path']))

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


def createPoseLibrary(filePath):
    #poseDataJson = json.load(open(configJson['pose_data_path']))
    poseDataJson = poseData.getPoseData()
    selectData = getSelection()

    cmds.cutKey(selectData['selection'])
    keyList = []
    for data in poseDataJson:
        keyList.append(data['id'])
    cmds.setKeyframe(selectData['selection'], t=keyList)

    savePoseLibrary(filePath)

#savePoseLibrary(filePath='D:/GoogleDrive/Documents/2021/facialReTargeter/work/poseLib/PRE_Full_Armor.json')