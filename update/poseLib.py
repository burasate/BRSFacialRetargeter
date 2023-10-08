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

if sys.version[0] == '3':pass

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
            # get attribute value
            fullAttrName = '{}:{}'.format(selectData['namespace'], attr)
            is_setable = cmds.getAttr(fullAttrName, se=1)
            if not cmds.objExists(fullAttrName): continue
            if not is_setable: continue
            value = cmds.getAttr(fullAttrName, time=frame)
            if type(value) == type(list()):
                value = value[0]
            if type(value) == type(bool()):
                value = int(value)

            # add atribute name in data
            if not attr in data['attributes']:
                data['attributes'][attr] = {}
                data['attributes'][attr]['id'] = []
                data['attributes'][attr]['value'] = []

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
            #print(attr, data['attributes'][attr])
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

    # save pose library
    with open(filePath, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        print('Pose Capture Finish\n'),
        f.close()

    # backup pose library
    with open(filePath.replace('.json','_Backup.json'), 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        f.close()

def loadPoseLibrary(filePath,dstNs):
    poseLibJson = json.load(open(configJson['pose_library_path']))

    ctrl_list = [i.split('.')[0] for i in poseLibJson['attributes']]
    ctrl_list = ['{}:{}'.format(dstNs,i) for i in ctrl_list]
    ctrl_list = [i for i in list(set(ctrl_list)) if cmds.objExists(i)]
    cmds.cutKey(cmds.ls(ctrl_list))

    static_attr_ls = [i for i in list(poseLibJson['pose_attribute']) if not i  in list(poseLibJson['attributes'])]
    print('static_attr_ls', sorted(static_attr_ls))
    blendposes_attr_ls = [i for i in list(poseLibJson['pose_attribute']) if i in list(poseLibJson['attributes'])]
    print('blendposes_attr_ls', sorted(blendposes_attr_ls))

    id_ls = list(poseLibJson['attributes'][blendposes_attr_ls[0]]['id'])

    # set blendposes value
    for attr in blendposes_attr_ls:
        attr_name = '{}:{}'.format(dstNs, attr)
        if not cmds.objExists(attr_name): continue
        if not cmds.getAttr(attr_name, se=1): continue
        for idx in range(len(id_ls)):
            frame = float(id_ls[idx])
            value = poseLibJson['attributes'][attr]['value'][idx]
            cmds.setKeyframe(attr_name, t=(frame,), v=value, itt='auto', ott='auto')
            # print([attr_name, (frame,), value])

    # set static value
    for attr in static_attr_ls:
        attr_name = '{}:{}'.format(dstNs, attr)
        if not cmds.objExists(attr_name): continue
        if not cmds.getAttr(attr_name, se=1):continue
        pose_value = poseLibJson['pose_attribute'][attr]
        cmds.setAttr(attr_name, pose_value)
        for idx in range(len(id_ls)):
            frame = float(id_ls[idx])
            cmds.setKeyframe(attr_name, t=(frame,), v=pose_value, itt='auto', ott='auto')

    cmds.select(ctrl_list)
    print(', '.join(ctrl_list)+'\n'),

def createPoseLibrary(filePath):
    poseDataJson = poseData.getPoseData()
    selectData = getSelection()

    cmds.cutKey(selectData['selection'])
    keyList = []
    for data in poseDataJson:
        keyList.append(data['id'])
    cmds.setKeyframe(selectData['selection'], t=keyList, itt='auto', ott='step')

    savePoseLibrary(filePath)

def createMeshBlendshape(*_):
    sel_list = [i for i in cmds.ls(sl=1) if cmds.listRelatives(i, s=1) != None]
    sel_list = [i for i in sel_list if cmds.objectType(cmds.listRelatives(i, s=1)[0]) == 'mesh']

    bs_list = [i for i in poseData.getPoseData() if i['type'] == 'blendshape' or i['type'] == 'expression']

    base_list = []
    cmds.currentTime(1.0)
    for obj in sel_list:
        bs_ext = cmds.duplicate(obj, n=obj + '_extract')[0]
        try:cmds.parent(obj,w=1)
        except:pass
        base_list += [bs_ext]

    for obj in base_list:
        cmds.select(obj)
        obj_idx = list(base_list).index(obj)
        bs = cmds.blendShape(n=obj + '_bs')[0]
        for i in bs_list:
            bs_idx = bs_list.index(i)
            cmds.currentTime(float(i['id']))
            if cmds.objExists(i['name']):
                cmds.delete(i['name'])
            temp_duplicate = cmds.duplicate(sel_list[obj_idx], n=i['name'])[0]
            print(temp_duplicate)
            cmds.blendShape(bs, e=True, target=(obj, bs_idx, temp_duplicate, 1.0))
            cmds.delete(temp_duplicate)
    cmds.currentTime(1.0)
    cmds.parent(base_list, world=1)