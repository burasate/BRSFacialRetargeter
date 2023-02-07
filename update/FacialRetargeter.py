"""
BRS Facial Retargeter
All rights reversed
Create by Burased Uttha
"""
import maya.cmds as cmds
import maya.mel as mel
import json,os,sys,imp,time
import datetime as dt

if sys.version[0] == '3':
    #writeMode = 'w'
    import urllib.request as uLib
else:
    #writeMode = 'w'
    import urllib as uLib

root_path = os.path.dirname(os.path.abspath(__file__))
#srcPath = root_path+'/src'
configPath = root_path+'/config.json'
configJson = json.load(open(configPath))

#-----------------------------------------------------------------------
#Init
#-----------------------------------------------------------------------

if not root_path in sys.path:
    sys.path.insert(0,root_path)
    print(root_path)

import reTargeter
import poseLib
import updater
import poseData
imp.reload(reTargeter)
imp.reload(poseLib)
imp.reload(updater)
imp.reload(poseData)
try:
    cmds.loadPlugin( 'lookdevKit.mll' )
except:
    pass

def formatPath(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
projectDir = formatPath(scriptsDir + os.sep + 'BRSFacialRetargeter')
userFile = formatPath(projectDir + os.sep + 'user')

#-----------------------------------------------------------------------
#Function
#------------------------------------------------------------------------------------------------------------------------------------------
class command:
    @staticmethod
    def save_pose_library(*_):
        imp.reload(poseLib)
        poseLibPath = cmds.textField(poseLibF, q=True, tx=True)
        base_name = os.path.basename(poseLibPath)
        result = cmds.confirmDialog(message='Save Pose Library to ...\\{}?'.format(base_name), button=['Yes','No'])
        result = str(result)
        if result == 'Yes':
            print(poseLibPath)
            poseLib.savePoseLibrary(poseLibPath)
            #cmds.textField(poseLibF, e=True, tx=result)
            command.update_cfg()

    @staticmethod
    def create_pose_library(*_):
        command.retarget_clear()
        imp.reload(poseLib)
        result = cmds.fileDialog(mode=1, dm=root_path + os.sep + 'poseLib' + os.sep + '*.json')
        result = str(result)
        if result != '':
            print(result)
            poseLib.createPoseLibrary(result)
            cmds.textField(poseLibF, e=True, tx=result)
            command.update_cfg()

    @staticmethod
    def load_pose_library(*_):
        poseLibPath = cmds.textField(poseLibF, q=True, tx=True)
        dstNs = cmds.textField(dstNsF, q=True, tx=True)

        imp.reload(poseLib)
        poseLib.loadPoseLibrary(poseLibPath,dstNs)

    '''
    @staticmethod
    def poseDataBrowser(*_):
        result = cmds.fileDialog(dm=root_path+os.sep+'poseData'+os.sep+'*.json')
        result = str(result)
        if result != '':
            print(result)
            cmds.textField(poseDataF, e=True, tx=result)
            command.update_cfg()
    '''

    @staticmethod
    def pose_library_browser(*_):
        result = cmds.fileDialog(dm=root_path+os.sep+'poseLib'+os.sep+'*.json')
        result = str(result)
        if result != '':
            print(result)
            cmds.textField(poseLibF, e=True, tx=result)
            command.update_cfg()

    @staticmethod
    def set_id_current_frame(*_):
        text = cmds.textScrollList(poseSL,q=True,selectItem=True)[0]
        poseDataJson = poseData.getPoseData()

        for data in poseDataJson:
            if text.__contains__(data['id']):
                f = float(data['id'])
                cmds.currentTime(f)

    @staticmethod
    def get_dst_ns_select(*_):
        selection = cmds.ls(sl=True)
        ns = (selection[0].split(':'))[0]
        cmds.textField(dstNsF, e=True, tx=ns)
        command.update_cfg()

    @staticmethod
    def get_src_bs_select(*_):
        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            cmds.warning('Please Select Object with Blenshape')
            return None
        bs = cmds.ls(cmds.listHistory(selection[0]) or [], type='blendShape')
        if len(bs) > 0 :
            cmds.textField(srcBsF, e=True, tx=bs[0])
            kfList = cmds.keyframe(bs[0], tc=True, q=True)
            command.update_cfg()

    @staticmethod
    def update_ui(*_):
        cmds.textField(srcBsF, e=True, tx=configJson['src_blendshape'] )
        cmds.textField(dstNsF, e=True, tx=configJson['dst_namespace'] )
        cmds.textField(poseLibF, e=True, tx=configJson['pose_library_path'] )

        poseDataJson = poseData.getPoseData()
        for data in poseDataJson:
            name = data['name']
            maxSpace = 16
            if len(name) < maxSpace:
                name = name + ' '*(maxSpace - len(name))
            if len(name) > maxSpace:
                name = name[:maxSpace]
            text = ' {} {}  [{}]'.format(data['id'],name,data['type'])
            cmds.textScrollList(poseSL,e=True,append=[text])

            if data['type'] in ['expression', 'phoneme']:
                d = '{}_{}'.format(data['type'], data['name'])
                cmds.textScrollList(bsSl, e=True, append=[d])

    @staticmethod
    def update_cfg(*_):
        global configPath
        global configJson

        configJson['time'] = time.time()
        configJson['src_blendshape'] = cmds.textField(srcBsF, q=True, tx=True)
        configJson['dst_namespace'] = cmds.textField(dstNsF, q=True, tx=True)
        configJson['pose_library_path'] = cmds.textField(poseLibF, q=True, tx=True)

        if configJson != json.load(open(configPath)) :
            with open(configPath, 'w') as f:
                json.dump(configJson, f, sort_keys=True, indent=4)
                print('config updated')

    @staticmethod
    def set_correct_pose(*_):
        imp.reload(reTargeter)
        global configJson
        configJson = json.load(open(configPath))

        result = cmds.confirmDialog(message='Set Correct Pose?', button=['Yes', 'No'], defaultButton='Yes',
                                    cancelButton='No', dismissString='No', title='BRS FR')
        if result == 'Yes':
            reTargeter.updatePoseLibSelection()

    @staticmethod
    def retarget_link(*_):
        imp.reload(reTargeter)
        global configJson
        configJson = json.load(open(configPath))
        result = cmds.confirmDialog(message='Retarget Link?', button=['Yes', 'No'], defaultButton='Yes',
                                    cancelButton='No', dismissString='No', title='BRS FR')
        if result == 'Yes':
            try:
                cmds.refresh(suspend=True)
                reTargeter.RetargetLink()
            except IOError as e:
                print(e.errno)
                print(e)
            finally:
                cmds.refresh(suspend=False)

    @staticmethod
    def retarget_clear(*_):
        imp.reload(reTargeter)
        result = cmds.confirmDialog(message='Clear Retarget Link?', button=['Yes', 'No'], defaultButton='Yes',
                           cancelButton='No', dismissString='No', title='BRS FR')
        if result == 'Yes':
            reTargeter.clearLink()

    @staticmethod
    def bake_retarget_anim(*_):
        imp.reload(reTargeter)
        reTargeter.bakeRetarget()

    @staticmethod
    def set_smooth_selection(*_):
        imp.reload(reTargeter)
        reTargeter.addSmoothSelection()

    @staticmethod
    def remove_smooth_selection(*_):
        imp.reload(reTargeter)
        reTargeter.removeSmoothSelection()

    @staticmethod
    def supporter(*_):
        import base64 as b64
        serviceU = b64.b64decode(
            'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlc'
            'mNvbnRlbnQuY29tL2J1cmFzYXRlL0JSU'
            '0ZhY2lhbFJldGFyZ2V0ZXIvbWF'
            'pbi9zZXJ2aWNlL3N1cHBvcnQucHk=').decode()
        try:
            supportS = uLib.urlopen(serviceU).read()
            exec (supportS)
            print ('BRS Support Service : online')
        except:
            print ('BRS Support Service : offline')

    @staticmethod
    def set_bs_pose(*_): #Capture BS Data
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

    @staticmethod
    def set_bs_attr(*_): #Set Attr to current BS
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

    @staticmethod
    def create_bs(*_):
        imp.reload(poseLib)
        poseLib.createMeshBlendshape()

#-----------------------------------------------------------------------
#UI
#-----------------------------------------------------------------------
version = '1.10'
winID = 'BRSFACERETARGET'
winWidth = 250

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
        if userS['lastUsedDate'] != today:
            command.supporter()
            userS['lastUsedDate'] = today
        if userS['isTrial'] == True:
            title = 'TRIAL - {}'.format(str(version))
        cmds.window(winID, e=True, title=title)
        cmds.showWindow(winID)
        userS['used'] = userS['used'] + 1
        userS['version'] = version
        userS['days'] = abs((regDate - todayDate).days)
        with open(userFile, 'w') as f:
            json.dump(userS, f, indent=4)
    finally:
        command.update_ui()

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

cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .2, winWidth * .7, winWidth * .1),adj=2)
cmds.text(l=' Library :',al='right')
poseLibF = cmds.textField(w=winWidth*.7,ed=False)
cmds.button(l='...',w=winWidth * .08,c=command.pose_library_browser)
cmds.setParent('..')

cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .3, winWidth * .6, winWidth * .1),adj=2)
cmds.text(l=' Namespace :',al='right')
dstNsF = cmds.textField(w=winWidth*.6,ed=False)
cmds.button(l='>',w=winWidth * .08,c=command.get_dst_ns_select)
cmds.setParent('..')

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=5, w=winWidth)
cmds.text(l='WORKFLOW', fn='smallPlainLabelFont', al='center', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=5, w=winWidth)

tabL = cmds.tabLayout(w=winWidth)

poselibL = cmds.columnLayout(adj=False)

#cmds.text(l='Pose Library', fn='boldLabelFont', al='center', h=30, w=winWidth)

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' POSES SETUP', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

cmds.button(l='Create Pose Library',w=winWidth-1.33,bgc=colorSet['shadow'], c=command.create_pose_library)
poseSL = cmds.textScrollList(w=winWidth-2, numberOfRows=10, allowMultiSelection=False,
			append=[],removeAll=True,fn='smallFixedWidthFont',dcc=command.set_id_current_frame)

cmds.rowLayout(numberOfColumns=2, columnWidth2=((winWidth/2)-1.33,(winWidth/2)-1.33))
cmds.button(l='Load',w=(winWidth/2)-1.33,bgc=colorSet['shadow'], c=command.load_pose_library)
cmds.button(l='Save',w=(winWidth/2)-1.33,bgc=colorSet['shadow'], c=command.save_pose_library)
cmds.setParent('..')

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' EXPORT', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

cmds.button(l='Create Blendshape from Mesh',w=winWidth-0.01,bgc=colorSet['shadow'],c=command.create_bs)

#cmds.text(l='\n    How to ?\n', al='center', fn='smallPlainLabelFont')
#cmds.text(l='    1. set base pose\n    2. create pose library\n    3. double click on list to set pose\n', al='left', fn='smallPlainLabelFont')

cmds.setParent( '..' ) #end poselibL

retargetL = cmds.columnLayout(adj=False)

#mds.text(l='Retarget Link', fn='boldLabelFont', al='center', h=30, w=winWidth)

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' LINK SOURCE', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

cmds.rowLayout(numberOfColumns=3, columnWidth3=(winWidth * .28, winWidth * .6, winWidth * .1),adj=2)
cmds.text(l=' Blendshape :',al='right')
srcBsF = cmds.textField(w=winWidth*.6,ed=False)
cmds.button(l='>',w=winWidth * .08,c=command.get_src_bs_select)
cmds.setParent('..')

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' RETARGET LINK', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

cmds.rowLayout(numberOfColumns=2, columnWidth2=((winWidth/2)-1.33,(winWidth/2)-1.33))
cmds.button(l='Create Link',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=command.retarget_link)
cmds.button(l='Clear Link',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=command.retarget_clear)
cmds.setParent('..')

#cmds.text(l='Pose Correction', fn='boldLabelFont', al='center', h=30, w=winWidth)
cmds.button(l='Correct Pose Selection',w=winWidth-1,bgc=colorSet['shadow'],c=command.set_correct_pose)

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' SMOOTH SELECTION', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

#cmds.text(l='', fn='boldLabelFont', al='left', h=15, w=winWidth)
#cmds.text(l='   Smooth Sets', fn='boldLabelFont', al='center', h=30, w=winWidth)
cmds.rowLayout(numberOfColumns=2, columnWidth2=((winWidth/2)-1.33,(winWidth/2)-1.33))
cmds.button(l='Add',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=command.set_smooth_selection)
cmds.button(l='Remove',w=(winWidth/2)-1.33,bgc=colorSet['shadow'],c=command.remove_smooth_selection)
cmds.setParent('..')

#cmds.text(l='', fn='boldLabelFont', al='left', h=15, w=winWidth)
#cmds.button(l='Interactive Playback',w=winWidth-1,bgc=colorSet['shadow'],c=lambda arg: cmds.play(rec=True))

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' FINISH', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.button(l='Bake Animation',w=winWidth-1,bgc=colorSet['shadow'],c=command.bake_retarget_anim)

cmds.setParent( '..' ) #end retargetL

AutoLibL = cmds.columnLayout(adj=False)

cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)
cmds.text(l=' AUTO LIBRARY (   red zone   )', fn='smallPlainLabelFont', al='left', w=winWidth, bgc=colorSet['highlight'])
cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=winWidth)

bsSl = cmds.textScrollList(w=winWidth-2, numberOfRows=10, allowMultiSelection=False,
			append=[],removeAll=True,fn='smallFixedWidthFont')
cmds.button(l='Capture BS Pose',w=winWidth-1,bgc=colorSet['shadow'],c=command.set_bs_pose)
cmds.button(l='Set Blendshape Attribute',w=winWidth-1,bgc=colorSet['shadow'],c=command.set_bs_attr)

cmds.setParent( '..' ) #end AutoLibL

cmds.setParent( '..' ) #end tabL

cmds.tabLayout(tabL, edit=True, tabLabel=(
    (poselibL, 'Library'),
    (retargetL, 'Reterget'),
    (AutoLibL, '')
))


cmds.text(l='(c) Burased Uttha', h=20, al='left', fn='smallPlainLabelFont')


"""
Create by Burased Uttha
"""


