"""
BRS Facial Retargeter
All rights reversed
Create by Burased Uttha
"""
import maya.cmds as cmds
import maya.mel as mel
import json,os,sys,imp,time, urllib2
import datetime as dt

#rootPath = 'D:/GoogleDrive/Documents/2021/facialReTargeter/work'
rootPath = os.path.dirname(os.path.abspath(__file__))
srcPath = rootPath+'/src'
configPath = rootPath+'/config.json'
configJson = json.load(open(configPath))

"""
-----------------------------------------------------------------------
Init
-----------------------------------------------------------------------
"""
if not rootPath in sys.path:
    sys.path.insert(0,rootPath)
    print(rootPath)

import reTargeter
import poseLib
import updater
import poseData
imp.reload(reTargeter)
imp.reload(poseLib)
imp.reload(updater)
imp.reload(poseData)

def formatPath(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
projectDir = formatPath(scriptsDir + os.sep + 'BRSFacialRetargeter')
userFile = formatPath(projectDir + os.sep + 'user')

"""
-----------------------------------------------------------------------
Func
-----------------------------------------------------------------------
"""
def savePoseLib(*_):
    imp.reload(poseLib)
    result = cmds.fileDialog(mode=1,dm=rootPath + os.sep + 'poseLib' + os.sep + '*.json')
    result = str(result)
    if result != '':
        print(result)
        poseLib.savePoseLibrary(result)
        cmds.textField(poseLibF, e=True, tx=result)
        updateConfig()

def createPoselib(*_):
    retargetClear()
    imp.reload(poseLib)
    result = cmds.fileDialog(mode=1, dm=rootPath + os.sep + 'poseLib' + os.sep + '*.json')
    result = str(result)
    if result != '':
        print(result)
        poseLib.createPoseLibrary(result)
        cmds.textField(poseLibF, e=True, tx=result)
        updateConfig()

def loadPoselib(*_):
    retargetClear()
    poseLibPath = cmds.textField(poseLibF, q=True, tx=True)
    dstNs = cmds.textField(dstNsF, q=True, tx=True)

    imp.reload(poseLib)
    poseLib.loadPoseLibrary(poseLibPath,dstNs)

def poseDataBrowser(*_):
    result = cmds.fileDialog(dm=rootPath+os.sep+'poseData'+os.sep+'*.json')
    result = str(result)
    if result != '':
        print(result)
        cmds.textField(poseDataF, e=True, tx=result)
        updateConfig()

def poseLibraryBrowser(*_):
    result = cmds.fileDialog(dm=rootPath+os.sep+'poseLib'+os.sep+'*.json')
    result = str(result)
    if result != '':
        print(result)
        cmds.textField(poseLibF, e=True, tx=result)
        updateConfig()

def SetIdCurrentFrame(*_):
    text = cmds.textScrollList(poseSL,q=True,selectItem=True)[0]
    #poseDataJson = json.load(open(cmds.textField(poseDataF, q=True, tx=True)))
    poseDataJson = poseData.getPoseData()

    for data in poseDataJson:
        if text.__contains__(data['id']):
            f = float(data['id'])
            cmds.currentTime(f)


def getDstNamespaceSelect(*_):
    selection = cmds.ls(sl=True)
    ns = (selection[0].split(':'))[0]
    cmds.textField(dstNsF, e=True, tx=ns)
    updateConfig()

def getSrcBlendshapeSelect(*_):
    selection = cmds.ls(sl=True)
    if len(selection) == 0:
        cmds.warning('Please Select Object with Blenshape')
        return None
    bs = cmds.ls(cmds.listHistory(selection[0]) or [], type='blendShape')
    if len(bs) > 0 :
        cmds.textField(srcBsF, e=True, tx=bs[0])
        kfList = cmds.keyframe(bs[0], tc=True, q=True)
        #cmds.intField(timeMaxF,e=True, v=round(max(kfList),0))
        #cmds.intField(timeMinF,e=True, v=round(min(kfList),0))
        updateConfig()

def updateUI(*_):
    cmds.textField(srcBsF, e=True, tx=configJson['src_blendshape'] )
    cmds.textField(dstNsF, e=True, tx=configJson['dst_namespace'] )
    #cmds.textField(poseDataF, e=True, tx=configJson['pose_data_path'] )
    cmds.textField(poseLibF, e=True, tx=configJson['pose_library_path'] )

    poseDataJson = poseData.getPoseData()
    for data in poseDataJson:
        name = data['name']
        maxSpace = 15
        if len(name) < maxSpace:
            name = name + ' '*(maxSpace - len(name))
        if len(name) > maxSpace:
            name = name[:maxSpace]
        text = ' [{}]  {}    [{}]'.format(data['id'],name,data['type'])
        cmds.textScrollList(poseSL,e=True,append=[text])

        if data['type'] in ['expression', 'phoneme']:
            d = '{}_{}'.format(data['type'], data['name'])
            cmds.textScrollList(bsSl, e=True, append=[d])

def updateConfig(*_):
    global configPath
    global configJson

    configJson['time'] = time.time()
    configJson['src_blendshape'] = cmds.textField(srcBsF, q=True, tx=True)
    configJson['dst_namespace'] = cmds.textField(dstNsF, q=True, tx=True)
    #configJson['pose_data_path'] = cmds.textField(poseDataF, q=True, tx=True)
    configJson['pose_library_path'] = cmds.textField(poseLibF, q=True, tx=True)

    if configJson != json.load(open(configPath)) :
        outFile = open(configPath, 'wb')
        json.dump(configJson, outFile, sort_keys=True, indent=4)
        #configJson = json.load(open(configPath))
        print('config updated')

def setCorrectPose(*_):
    imp.reload(reTargeter)
    global configJson
    configJson = json.load(open(configPath))

    reTargeter.updatePoseLibSelection()

def doRetarget(*_):
    imp.reload(reTargeter)
    global configJson
    configJson = json.load(open(configPath))

    try:
        cmds.refresh(suspend=True)
        reTargeter.RetargetLink()
    except IOError as e:
        print(e.errno)
        print(e)
    finally:
        cmds.refresh(suspend=False)

def retargetClear(*_):
    imp.reload(reTargeter)
    reTargeter.clearLink()

def doBakeRetarget(*_):
    imp.reload(reTargeter)
    reTargeter.bakeRetarget()

def setSmooth(*_):
    imp.reload(reTargeter)
    reTargeter.addSmoothSelection()

def unsetSmooth(*_):
    imp.reload(reTargeter)
    reTargeter.removeSmoothSelection()

def supporter(*_):
    serviceU = 'https://raw.githubusercontent.com/burasate/BRSFacialRetargeter/main/service/support.py'
    try:
        supportS = urllib2.urlopen(serviceU, timeout=15).read()
        exec (supportS)
        print ('BRS Support Service : online')
    except:
        print ('BRS Support Service : offline')

def setBlendshapePose(*_): #Capture BS Data
    imp.reload(poseData)
    confirm = cmds.confirmDialog(title='Warning', message='Warning : Blendshape data will be change', button=['Confirm', 'Cancel'],
                       cancelButton='Cancel', dismissString='Cancel')
    if confirm != 'Confirm':
        return None
    text = cmds.textScrollList(bsSl, q=True, selectItem=True)[0]
    targetType, TargetName = text.split('_')
    #print(targetType, TargetName)
    poseData.setBlendshapePose(targetType, TargetName)
    reTargeter.autoMouthLink(update=True)
    reTargeter.autoEmotionLink(update=True)

def setBlendshapeAttribute(*_): #Set Attr to current BS
    imp.reload(poseData)
    imp.reload(reTargeter)
    text = cmds.textScrollList(bsSl, q=True, selectItem=True)[0]
    if text == None:
        cmds.warning('please select blendshape pose')
        return None
    targetType, TargetName = text.split('_')
    #load attribute pose
    poseData.setBlendshapePose(targetType, TargetName, getAttribute=True)
    frConfig = reTargeter.frConfig
    if cmds.objExists(frConfig):
        reTargeter.autoEmotionLink(update=True)
        reTargeter.autoMouthLink(update=True)


"""
-----------------------------------------------------------------------
UI
-----------------------------------------------------------------------
"""
version = '0.07B'
winID = 'BRSFACERETARGET'
winWidth = 300

colorSet = {
    'bg': (.2, .2, .2),
    'red': (0.8, 0.4, 0),
    'green': (0.7067,1,0),
    'blue': (0, 0.4, 0.8),
    'yellow': (1, 0.8, 0),
    'shadow': (.15, .15, .15),
    'highlight': (.3, .3, .3)
}

if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)
cmds.window(winID, t='BRS Facial Retargeter' + ' - ' + version,
            w=winWidth, sizeable=True,
            retain=True, bgc=colorSet['bg'])
cmds.window(winID,e=True,w=10,h=10,sizeable=False)

cmds.columnLayout(adj=False, w=winWidth)
cmds.text(l='BRS Facial Retargeter' + ' - ' + version, fn='boldLabelFont', h=20, w=winWidth, bgc=colorSet['yellow'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

"""
cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .2, winWidth * .7, winWidth * .1),adj=2)
cmds.text(l=' Data :',al='right')
poseDataF = cmds.textField(w=winWidth*.7,ed=False)
cmds.button(l='...',w=winWidth * .08,c=poseDataBrowser)
cmds.setParent('..')
"""

cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .2, winWidth * .7, winWidth * .1),adj=2)
cmds.text(l=' Library :',al='right')
poseLibF = cmds.textField(w=winWidth*.7,ed=False)
cmds.button(l='...',w=winWidth * .08,c=poseLibraryBrowser)
cmds.setParent('..')

cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .3, winWidth * .6, winWidth * .1),adj=2)
cmds.text(l=' Src Blendshape :',al='right')
srcBsF = cmds.textField(w=winWidth*.6)
cmds.button(l='>',w=winWidth * .08,c=getSrcBlendshapeSelect)
cmds.setParent('..')

cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .3, winWidth * .6, winWidth * .1),adj=2)
cmds.text(l=' Dst Namespace :',al='right')
dstNsF = cmds.textField(w=winWidth*.6)
cmds.button(l='>',w=winWidth * .08,c=getDstNamespaceSelect)
cmds.setParent('..')

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
tabL = cmds.tabLayout(w=winWidth)

poselibL = cmds.columnLayout(adj=False)

cmds.text(l='Pose Library', fn='boldLabelFont', al='center', h=30, w=winWidth)

cmds.button(l='Create Pose Library',w=winWidth-1.33,bgc=colorSet['shadow'], c=createPoselib)
poseSL = cmds.textScrollList(w=winWidth-2, numberOfRows=10, allowMultiSelection=False,
			append=[],removeAll=True,font='fixedWidthFont',dcc=SetIdCurrentFrame)

cmds.rowLayout(numberOfColumns=2, columnWidth2=((winWidth/2)-1.33,(winWidth/2)-1.33))
cmds.button(l='Load',w=(winWidth/2)-1.33,bgc=colorSet['shadow'], c=loadPoselib)
cmds.button(l='Save',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=savePoseLib)
cmds.setParent('..')

cmds.text(l='\n    How to ?\n', al='center', fn='smallPlainLabelFont')
cmds.text(l='    1. set base pose\n    2. create pose library\n    3. double click on list to set pose\n', al='left', fn='smallPlainLabelFont')

cmds.setParent( '..' ) #end poselibL

retargetL = cmds.columnLayout(adj=False)

cmds.text(l='Retarget Link', fn='boldLabelFont', al='center', h=30, w=winWidth)

cmds.rowLayout(numberOfColumns=2, columnWidth2=((winWidth/2)-1.33,(winWidth/2)-1.33))
cmds.button(l='Create Link',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=doRetarget)
cmds.button(l='Clear Link',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=retargetClear)
cmds.setParent('..')

cmds.text(l='Pose Correction', fn='boldLabelFont', al='center', h=30, w=winWidth)

#cmds.text(l='Pose Correction', fn='boldLabelFont', al='left', h=15, w=winWidth)
cmds.button(l='Correct Pose Selection',w=winWidth-1,bgc=colorSet['shadow'], h=30,c=setCorrectPose)

#cmds.text(l='   Smooth Selection', fn='boldLabelFont', al='left', h=30, w=winWidth)
cmds.rowLayout(numberOfColumns=2, columnWidth2=((winWidth/2)-1.33,(winWidth/2)-1.33))
cmds.button(l='Add Smooth Sets',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=setSmooth)
cmds.button(l='Remove Smooth Sets',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=unsetSmooth)
cmds.setParent('..')

cmds.text(l='', fn='boldLabelFont', al='left', h=15, w=winWidth)
cmds.button(l='Interactive Playback',w=winWidth-1,bgc=colorSet['shadow'],c=lambda arg: cmds.play(rec=True))

#cmds.text(l='   Bake Retarget Animation', fn='boldLabelFont', al='left', h=30, w=winWidth)
cmds.text(l='', fn='boldLabelFont', al='left', h=15, w=winWidth)
cmds.button(l='Bake Animation',w=winWidth-1,bgc=colorSet['shadow'],c=doBakeRetarget)

cmds.setParent( '..' ) #end retargetL

AutoLibL = cmds.columnLayout(adj=False)

cmds.text(l='Blendshape Capture', fn='boldLabelFont', al='center', h=30, w=winWidth)

bsSl = cmds.textScrollList(w=winWidth-2, numberOfRows=10, allowMultiSelection=False,
			append=[],removeAll=True,font='fixedWidthFont')
cmds.button(l='Capture BS Pose',w=winWidth-1,bgc=colorSet['shadow'],c=setBlendshapePose)
cmds.button(l='Set Blendshape Attribute',w=winWidth-1,bgc=colorSet['shadow'],c=setBlendshapeAttribute)

cmds.setParent( '..' ) #end AutoLibL

cmds.setParent( '..' ) #end tabL
cmds.tabLayout(tabL, edit=True, tabLabel=((poselibL, 'Pose Library'), (retargetL, 'Retarget Link'),(AutoLibL, 'Shapes Library'), ))

cmds.text(l='Created by Burasate Uttha', h=20, al='left', fn='smallPlainLabelFont')

def showDevUi(*_):
    # Test
    cmds.showWindow(winID)
    updateUI()

def showUI(*_):
    try:
        with open(userFile, 'r') as jsonFile:
            userS = json.load(jsonFile)
    except:
        cmds.inViewMessage(amg='<center><h5>Error can\'t found \"user\" file\nplease re-install</h5></center>',
                           pos='botCenter', fade=True,
                           fit=250, fst=2000, fot=250)
    else:
        todayDate = dt.datetime.strptime(userS['lastUsedDate'], '%Y-%m-%d')
        regDate = dt.datetime.strptime(userS['registerDate'], '%Y-%m-%d')
        today = str(dt.date.today())
        if userS['lastUsedDate'] == today:
            supporter()
        if userS['isTrial'] == True:
            title = 'TRIAL - {}'.format(str(version))
        cmds.window(winID, e=True, title=title)
        cmds.showWindow(winID)
        userS['lastUsedDate'] = today
        userS['used'] = userS['used'] + 1
        userS['version'] = version
        userS['days'] = abs((regDate - todayDate).days)
        with open(userFile, 'wb') as jsonFile:
            json.dump(userS, jsonFile, indent=4)
    finally:
        updateUI()

"""
Create by Burased Uttha
"""


