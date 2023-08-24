# -*- coding: utf-8 -*-

import os
import sys
import gazu
import shutil
import webbrowser
import maya.cmds as cmds
from mtoa import aovs
from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QMainWindow, QFileDialog
from maya import mel
from pymel.core import *

sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts")
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts/ui_py_file")
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts/login")


from login_model import LogIn
from main_ui import Ui_MainWindow as ezui
import import_and_setting
import main_ui


reload(import_and_setting)
reload(main_ui)


class MainWindow(QMainWindow, ezui):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        mel.eval('unifiedRenderGlobalsWindow;')
        mel.eval('initRenderSettingsWindow();')
        mel.eval('deleteUI unifiedRenderGlobalsWindow;')

        self.login = LogIn()

        gazu.client.set_host("http://192.168.3.117/api")
        gazu.log_in("admin@netflixacademy.com", "netflixacademy")

        self.project = None
        self.asset = None
        self.task_type = None
        self.task = None
        self.working_file = None
        self.working_revision = None
        self.output_type = None
        self.output_file = None
        self.output_revision = None
        self.status = None

        # kitsu variable
        self.all_project_infos = gazu.project.all_projects()
        self.set_projects_list()
        self.set_assets_list_by_project()

        # input variable
        self.total_start_frame = 0
        self.total_end_frame = 0
        self.mesh_start_frame = 0
        self.mesh_end_frame = 0
        self.dome_start_frame = 0
        self.dome_end_frame = 0

        self.path = None
        self.name = None
        self.representation = None
        self.full_path = None

        # ren_set var
        self.kitsu_upload_path = None
        self.command_input = None
        self.vid_command_input = None
        self.aov_vid_command_input = None
        self.image_format = None
        self.ren_asset_name = None
        self.current_asset_text = None
        self.current_project_text = None
        self.ren_path = None

        # button tests
        self.pushButton_import.clicked.connect(self.iands)
        self.pushButton_publish.clicked.connect(self.publish)
        self.pushButton_save_scene.clicked.connect(self.save_clicked)
        self.pushButton_scene_path.clicked.connect(self.scene_path_clicked)
        self.checkBox_change_setting.stateChanged.connect(self.chbxStateChange)

        self.lineEdit_mesh_start_frame.textChanged.connect(self.change_frame_value)
        self.lineEdit_mesh_end_frame.textChanged.connect(self.change_frame_value)

        # kitsu change item
        self.listWidget_vid_project.currentItemChanged.connect(self.set_assets_list_by_project)
        self.listWidget_vid_project.itemChanged.connect(self.set_assets_list_by_project)
        self.listWidget_vid_asset.currentItemChanged.connect(self.set_current_asset_text)
        self.listWidget_vid_asset.itemChanged.connect(self.set_current_asset_text)

        # change sample
        self.lineEdit_aa_sam.textChanged.connect(self.change_value)
        self.lineEdit_diffuse_sam.textChanged.connect(self.change_value)
        self.lineEdit_specular_sam.textChanged.connect(self.change_value)
        self.lineEdit_trans_sam.textChanged.connect(self.change_value)
        self.lineEdit_sss_sam.textChanged.connect(self.change_value)
        self.lineEdit_volume_sam.textChanged.connect(self.change_value)

        # detect aov selection
        self.listWidget_availaov.itemClicked.connect(self.set_aov)
        self.listWidget_activaov.itemClicked.connect(self.del_aov)

        # set initial sample
        self.set_initial_render_sampling()

        # go kitsu
        self.commandLinkButton_go_kitsu.clicked.connect(self.go_kitsu)
        self.commandLinkButton_go_kitsu_2.clicked.connect(self.go_kitsu)

        if cmds.ls(selection=True):
            self.label_selected_mesh_name.setText(cmds.ls(selection=True)[0])
            self.selected_mesh = cmds.ls(selection=True)[0]
            self.label_selected_camera_name.setText("turntable_camera")
        else:
            button_result = cmds.confirmDialog(title="Report", message="please select the mesh", messageAlign="center", button="confirm")
            if button_result == "confirm":
                MainWindow.close(self)
                sys.exit()


        ## hdri tab
        # project
        self.hdri_project = gazu.project.get_project_by_name('HDRI Library')

        # all assets
        self.hdri_all_assets = gazu.asset.all_assets_for_project(self.hdri_project["id"])

        # asset
        self.hdri_asset = None

        # task_type
        self.hdri_task_type = gazu.task.get_task_type_by_name('Shading')

        # task
        self.hdri_task = None

        # hdri_list_import
        self.add_item_hdri_list()  # 생성
        self.listWidget_change_hdri_img.itemClicked.connect(self.hdri_list_clicked)

        # hdri_pub
        self.pushButton_hdri_path.clicked.connect(self.pushButton_hdri_path_clicked)
        self.pushButton_publish_hdri_img.clicked.connect(self.pushButton_publish_hdri_img_clicked)

    # hdri function
    def add_item_hdri_list(self):
        self.listWidget_change_hdri_img.clear()  # 초기화
        self.hdri_all_assets = gazu.asset.all_assets_for_project(self.hdri_project["id"])
        for self.hdri_asset in self.hdri_all_assets:
            self.listWidget_change_hdri_img.addItem(self.hdri_asset['name'])

    def hdri_list_clicked(self):
        selected_item = self.listWidget_change_hdri_img.currentItem().text()
        preview_file_id = None
        for self.hdri_asset in self.hdri_all_assets:
            if selected_item == self.hdri_asset["name"]:
                preview_file_id = self.hdri_asset['preview_file_id']
                break

        # 다운로드 함수에 필요한 프리뷰 파일의 아이디를 확인하기 위한 변수
        self.gp = gazu.files.get_preview_file(preview_file_id)

        task_type = None
        task_types = gazu.task.all_task_types_for_project(self.hdri_project)
        for task_type in task_types:
            if task_type['name'] == 'Shading' and task_type['for_entity'] == self.hdri_asset['type']:
                task_type = task_type
                break
        task = gazu.task.get_task_by_name(self.hdri_asset, task_type)

        working_file_info = gazu.files.get_working_files_for_task(task)
        self.path = working_file_info[-1]["path"]
        if os.path.exists(self.path) is False:
            os.makedirs(self.path)
        else:
            pass

        # 다운로드 함수에 필요한 프리뷰 파일패스를 확인하기 위한 변수
        self.dpp = self.path + "/" + self.gp['original_name'] + '.' + self.gp['extension']

        # 실질적으로 다운로드 해주는 함수
        dp = gazu.files.download_preview_file(preview_file=preview_file_id, file_path=self.dpp)
        self.extract_thumbnail_from_exr(self.dpp, self.path, self.gp['original_name'])

        # label을 변경
        self.change_label_preview_hdri_img_import(self.output_file_path)

    def extract_thumbnail_from_exr(self, input_file, output_path, output_file_name):
        input_file_path = input_file

        self.output_dir = "%s/preview_jpg" % (output_path)
        output_name = output_file_name
        output_format = 'jpg'
        self.output_file_path = '%s/%s.%s' % (self.output_dir, output_name, output_format)
        jpeg_pixel = '320'

        command_input = 'ffmpeg -i %s -vf "scale=%s:-1" -vframes 1 %s' % (
            input_file_path, jpeg_pixel, self.output_file_path)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.output_file_path):
            self.run_ffmpeg(command_input)

    def run_ffmpeg(self, commands):
        if os.system(commands) == 0:
            pass

    def change_label_preview_hdri_img_import(self, image):
        hdri_img_to_view = QPixmap(os.path.join(os.path.dirname(__file__), image))
        scaled_hdri_img_to_view = hdri_img_to_view.scaled(self.label_preview_hdri_img_import.size(),
                                                          Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)
        self.label_preview_hdri_img_import.setPixmap(scaled_hdri_img_to_view)

    def pushButton_hdri_path_clicked(self):
        options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                        ".exr(*.exr);; All Files (*)", options=options)

        self.lineEdit_hdri_path.setText(self.file_name)

        dir_path = os.path.dirname(self.file_name)

        name = os.path.basename(self.file_name)

        self.extract_thumbnail_from_exr(self.file_name, dir_path, name)

        self.change_label_preview_hdri_img_add(self.output_file_path)

    def change_label_preview_hdri_img_add(self, image):
        hdri_img_to_view = QPixmap(os.path.join(os.path.dirname(__file__), image))
        scaled_hdri_img_to_view = hdri_img_to_view.scaled(self.label_preview_hdri_img_add.size(),
                                                          Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)
        self.label_preview_hdri_img_add.setPixmap(scaled_hdri_img_to_view)

    def pushButton_publish_hdri_img_clicked(self):
        # asset_type
        asset_type_id = None
        all_asset_types = gazu.asset.all_asset_types_for_project(self.hdri_project)
        if all_asset_types == [] or all_asset_types != "Environment":
            gazu.asset.new_asset_type("Environment")
            asset_type = gazu.asset.get_asset_type_by_name("Environment")
            asset_type_id = asset_type['id']

        for asset_type in all_asset_types:
            if "Environment" == asset_type["name"]:
                asset_type_id = asset_type['id']

        if self.file_name:
            # 파일 경로에서 파일 이름만 추출합니다.
            self.file_name_only = os.path.basename(self.file_name)

        gazu.asset.new_asset(project=self.hdri_project, asset_type=asset_type_id, name=self.file_name_only)

        asset = gazu.asset.get_asset_by_name(self.hdri_project, self.file_name_only)

        # task_type
        all_task_types = gazu.task.all_task_types_for_project(self.hdri_project)
        for task_type in all_task_types:
            if task_type['name'] == 'Concept' and task_type['for_entity'] == asset['type']:
                upload_task_type = task_type
                break

        gazu.task.new_task(asset, upload_task_type)
        task = gazu.task.get_task_by_name(asset, upload_task_type)

        kitsu_upload_path = "%s" % self.file_name

        comment = gazu.task.add_comment(task, '3d24de8b-b327-4c95-a469-392637497234', comment="HDRI uploaded")
        preview = gazu.task.add_preview(task, comment, preview_file_path=kitsu_upload_path)
        gazu.task.set_main_preview(preview['id'])

        self.add_item_hdri_list()
        self.lineEdit_hdri_path.clear()
        self.label_preview_hdri_img_add.clear()

        working_file = gazu.files.new_working_file(task)

        self.delete_jpg_file(self.output_dir)

    def delete_jpg_file(self, jpg_dir):
        shutil.rmtree(jpg_dir)

    # gazu function section

    def get_project(self):
        self.project_name = self.current_project_text
        self.project = gazu.project.get_project_by_name(self.project_name)
        return self.project

    def get_asset(self):
        self.asset_name = self.current_asset_text
        self.asset = gazu.asset.get_asset_by_name(self.project, self.asset_name)
        return self.asset

    def get_task_type(self):
        task_types = gazu.task.all_task_types_for_project(self.project)
        for task_type in task_types:
            if task_type['name'] == 'Shading' and task_type['for_entity'] == self.asset['type']:
                self.task_type = task_type
                break
        return self.task_type

    def get_task(self):
        self.task = gazu.task.get_task_by_name(self.asset, self.task_type)
        return self.task

    def create_working_file(self):
        self.working_file = gazu.files.new_working_file(self.task)
        return self.working_file

    def get_working_revision(self):
        self.working_revision = self.working_file['revision']
        return self.working_revision

    def get_output_type(self):
        self.output_type_name = self.lineEdit_vid_format.text().upper()
        self.output_type_short_name = self.lineEdit_vid_format.text().lower()
        self.output_type = gazu.files.get_output_type_by_name(self.output_type_name)
        return self.output_type

    def create_output_file(self):
        self.output_file = gazu.files.new_entity_output_file(self.asset, self.output_type, self.task_type,
                                                             comment='publish', working_file=self.working_file,
                                                             revision=self.working_file['revision'])
        return self.output_file

    def get_output_revision(self):
        self.output_revision = self.output_file['revision']
        return self.output_revision

    def create_dir(self):
        if os.path.exists(self.working_file['path']) is False:
            os.makedirs(self.working_file['path'])

    def get_status(self):
        self.status_name = 'Todo'  # test
        all_status = gazu.task.all_task_statuses()
        for st in all_status:
            if st.get('name') == self.status_name or st.get('short_name') == self.status_name:
                self.status = st
                break
        return self.status

    # Kitsu Function --------
    def set_projects_list(self):
        self.listWidget_vid_project.clear()
        for project_infos in self.all_project_infos:
            self.listWidget_vid_project.addItem(project_infos['name'])
        # Select the first project by default. = error prevention
        self.listWidget_vid_project.setCurrentItem(self.listWidget_vid_project.item(0))

    def set_assets_list_by_project(self):
        self.listWidget_vid_asset.clear()
        self.set_current_project_text()
        for project_infos in self.all_project_infos:
            if project_infos["name"] == self.current_project_text:
                assets_info = gazu.asset.all_assets_for_project(project_infos["id"])
                if assets_info:
                    for asset in assets_info:
                        self.listWidget_vid_asset.addItem(asset["name"])
                else:
                    self.listWidget_vid_asset.addItem("no asset")
        self.listWidget_vid_asset.setCurrentItem(self.listWidget_vid_asset.item(0))
        self.set_current_asset_text()

    def set_current_project_text(self):
        self.current_project_text = self.listWidget_vid_project.currentItem().text()

    def set_current_asset_text(self):
        if self.listWidget_vid_asset.currentItem():
            self.current_asset_text = self.listWidget_vid_asset.currentItem().text()
        else:
            self.listWidget_vid_asset.setCurrentItem(self.listWidget_vid_asset.item(0))
            self.current_asset_text = self.listWidget_vid_asset.currentItem().text()

    def get_gazu(self):
        self.get_project()
        self.get_asset()
        self.get_task_type()
        self.get_task()
        self.create_working_file()
        self.get_working_revision()
        self.get_output_type()
        self.create_output_file()
        self.get_output_revision()
        self.create_dir()
        self.get_status()

    # Maya Function

    def change_frame_value(self):

        self.total_start_frame = int(self.lineEdit_mesh_start_frame.text())
        self.total_end_frame = int(self.lineEdit_mesh_end_frame.text())

        self.mesh_start_frame = self.total_start_frame
        self.mesh_end_frame = self.total_end_frame / 2
        self.dome_start_frame = self.mesh_end_frame + 1
        self.dome_end_frame = self.total_end_frame

        return self.total_start_frame, self.total_end_frame, self.mesh_start_frame, self.mesh_end_frame, self.dome_start_frame, self.dome_end_frame

    def change_value(self):
        aa_sam = int(self.lineEdit_aa_sam.text())
        diffuse_sam = int(self.lineEdit_diffuse_sam.text())
        specular_sam = int(self.lineEdit_specular_sam.text())
        trans_sam = int(self.lineEdit_trans_sam.text())
        sss_sam = int(self.lineEdit_sss_sam.text())
        volume_sam = int(self.lineEdit_volume_sam.text())

        mel.eval('setAttr "defaultArnoldRenderOptions.AASamples" %d;' % aa_sam)  # Camera(AA)
        mel.eval('setAttr "defaultArnoldRenderOptions.GIDiffuseSamples" %d;' % diffuse_sam)  # Diffuse
        mel.eval('setAttr "defaultArnoldRenderOptions.GISpecularSamples" %d;' % specular_sam)  # Specular
        mel.eval('setAttr "defaultArnoldRenderOptions.GITransmissionSamples" %d;' % trans_sam)  # Transmission
        mel.eval('setAttr "defaultArnoldRenderOptions.GISssSamples" %d;' % sss_sam)  # SSS
        mel.eval('setAttr "defaultArnoldRenderOptions.GIVolumeSamples" %d;' % volume_sam)  # Volume Indirect

    def chbxStateChange(self):
        if self.checkBox_change_setting.isChecked():
            self.lineEdit_mesh_start_frame.setEnabled(True)
            self.lineEdit_mesh_end_frame.setEnabled(True)
            self.lineEdit_img_format.setEnabled(True)
            self.lineEdit_vid_format.setEnabled(True)
            self.lineEdit_img_name.setEnabled(True)
            self.lineEdit_img_path.setEnabled(True)
            self.lineEdit_vid_name.setEnabled(True)
            self.lineEdit_vid_path.setEnabled(True)
            self.listWidget_availaov.setEnabled(True)
            self.listWidget_activaov.setEnabled(True)
            self.lineEdit_aa_sam.setEnabled(True)
            self.lineEdit_diffuse_sam.setEnabled(True)
            self.lineEdit_specular_sam.setEnabled(True)
            self.lineEdit_trans_sam.setEnabled(True)
            self.lineEdit_sss_sam.setEnabled(True)
            self.lineEdit_volume_sam.setEnabled(True)

        else:
            self.lineEdit_mesh_start_frame.setDisabled(True)
            self.lineEdit_mesh_end_frame.setDisabled(True)
            self.lineEdit_img_format.setDisabled(True)
            self.lineEdit_vid_format.setDisabled(True)
            self.lineEdit_img_name.setDisabled(True)
            self.lineEdit_img_path.setDisabled(True)
            self.lineEdit_vid_name.setDisabled(True)
            self.lineEdit_vid_path.setDisabled(True)
            self.listWidget_availaov.setDisabled(True)
            self.listWidget_activaov.setDisabled(True)
            self.lineEdit_aa_sam.setDisabled(True)
            self.lineEdit_diffuse_sam.setDisabled(True)
            self.lineEdit_specular_sam.setDisabled(True)
            self.lineEdit_trans_sam.setDisabled(True)
            self.lineEdit_sss_sam.setDisabled(True)
            self.lineEdit_volume_sam.setDisabled(True)

    def iands(self):
        image_path = self.dpp
        import_and_setting.Set().import_camera()
        import_and_setting.Set().create_skydome_light(image_path)
        import_and_setting.Set().switch_camera()
        import_and_setting.Set().fit_selection_in_frame(self.selected_mesh)

        self.change_frame_value()
        import_and_setting.Set().rotate_objects(self.selected_mesh, self.mesh_start_frame, self.mesh_end_frame)
        import_and_setting.Set().rotate_dome(self.dome_start_frame, self.dome_end_frame)

    def set_aov(self):
        if self.listWidget_availaov.currentItem():
            add_aov = self.listWidget_availaov.currentItem().text()
            rm_row = self.listWidget_availaov.currentRow()

            self.listWidget_activaov.addItem(add_aov)
            new_aov = aovs.AOVInterface()
            new_aov.addAOV(add_aov)
            self.listWidget_availaov.takeItem(rm_row)

    def del_aov(self):
        if self.listWidget_activaov.currentItem():
            add_aov = self.listWidget_activaov.currentItem().text()
            rm_row = self.listWidget_activaov.currentRow()

            self.listWidget_availaov.addItem(add_aov)
            new_aov = aovs.AOVInterface()
            new_aov.removeAOV(add_aov)
            self.listWidget_activaov.takeItem(rm_row)

    def set_initial_render_sampling(self):
        # 아래 코드들을 통해 마지막에 입력된 숫자만큼 렌더 샘플링 설정이 가능하다
        # 모든 값들은 0~10 사이의 값을 가진다. 하지만, AASamples 는 다르게 -3~10 의 값을 가질 수 있다.
        # 각각 값의 label 이름은 옆의 코멘트와 같다
        # 입력된 값들은 default 로 설정하면 좋은 통상 최적화 된 이미지를 뽑는데 좋은 값이다.

        # set values
        aa_sam = 8
        diffuse_sam = 6
        specular_sam = 4
        trans_sam = 4
        sss_sam = 2
        volume_sam = 2

        # setting code
        mel.eval('setAttr "defaultArnoldRenderOptions.AASamples" %d;' % aa_sam)  # Camera(AA)
        mel.eval('setAttr "defaultArnoldRenderOptions.GIDiffuseSamples" %d;' % diffuse_sam)  # Diffuse
        mel.eval('setAttr "defaultArnoldRenderOptions.GISpecularSamples" %d;' % specular_sam)  # Specular
        mel.eval('setAttr "defaultArnoldRenderOptions.GITransmissionSamples" %d;' % trans_sam)  # Transmission
        mel.eval('setAttr "defaultArnoldRenderOptions.GISssSamples" %d;' % sss_sam)  # SSS
        mel.eval('setAttr "defaultArnoldRenderOptions.GIVolumeSamples" %d;' % volume_sam)  # Volume Indirect

    def scene_path_clicked(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_scene_path.setText(file)

    def save_clicked(self):
        self.get_gazu()
        self.path = self.lineEdit_scene_path.text()
        self.name = self.lineEdit_scene_name.text()
        self.representation = self.comboBox_scene_format.currentText()
        self.full_path = self.path + "/" + self.name + self.representation
        maya_path = os.path.dirname(self.full_path)

        if not os.path.exists(maya_path):
            os.makedirs(maya_path)
        cmds.file(rename=self.full_path)
        if self.representation == '.mb':
            cmds.file(save=True, type='mayaBinary', force=True)
            mel.eval('confirmDialog -title "Confirm" -message ".mb file saved Successfully"')
        else:
            cmds.file(save=True, type='mayaAscii', force=True)
            mel.eval('confirmDialog -title "Confirm" -message ".ma file saved Successfully"')

        return self.path, self.name, self.full_path

    def set_publish(self):
        # call function
        self.get_gazu()
        self.ren_path = self.working_file['path']
        self.ren_asset_name = "%s_%s_v%s" % (self.project_name, self.asset_name, self.working_revision)
        self.image_format = self.lineEdit_img_format.text()

        self.command_input = \
            "/usr/autodesk/maya2020/bin/Render" \
            " -r arnold -rd %s/" \
            " -im %s" \
            " -s %d" \
            " -e %d" \
            " -b 1" \
            " -fnc 3" \
            " -of %s" \
            " -cam turntable_camera" \
            " -x 1920 -y 1080" \
            " %s" % (
                self.ren_path, self.ren_asset_name, self.total_start_frame, self.total_end_frame, self.image_format, self.full_path)

        input_directory = self.ren_path
        aov_input_directory = self.ren_path + '/beauty'
        image_sequence_name = self.ren_asset_name
        num_text = '%04d'
        file_extension = self.image_format
        output_directory = self.working_file['path']
        output_name = "%s_%s_v%s" % (self.project_name, self.asset_name, self.output_revision)
        output_video_format = self.lineEdit_vid_format.text()

        self.vid_command_input = 'ffmpeg -i %s/%s.%s.%s -c:v libx265 %s/%s.%s' % (
            input_directory, image_sequence_name, num_text, file_extension, output_directory, output_name,
            output_video_format)

        self.aov_vid_command_input = 'ffmpeg -i %s/%s.%s.%s -c:v libx265 %s/%s.%s' % (
            aov_input_directory, image_sequence_name, num_text, file_extension, output_directory, output_name,
            output_video_format)

        self.kitsu_upload_path = "%s/%s.%s" % (self.working_file['path'], output_name, output_video_format)

        return self.command_input, self.vid_command_input, self.aov_vid_command_input, self.kitsu_upload_path

    def publish(self):
        self.user_comment = self.textEdit_leave_a_comment.toPlainText()
        self.set_publish()

        if self.listWidget_activaov.count() == 0:
            if os.system(self.command_input) == 0:
                if os.system(self.vid_command_input) == 0:
                    comment = gazu.task.add_comment(self.task, '3d24de8b-b327-4c95-a469-392637497234',
                                                    comment=self.user_comment)

                    preview = gazu.task.add_preview(self.task, comment, preview_file_path=self.kitsu_upload_path)

                    gazu.task.set_main_preview(preview['id'], 1)
                    mel.eval('confirmDialog -title "Confirm" -message "Publish Finished Successfully"')

        else:
            if os.system(self.command_input) == 0:
                if os.system(self.aov_vid_command_input) == 0:
                    comment = gazu.task.add_comment(self.task, '3d24de8b-b327-4c95-a469-392637497234',
                                                    comment=self.user_comment)

                    preview = gazu.task.add_preview(self.task, comment, preview_file_path=self.kitsu_upload_path)

                    gazu.task.set_main_preview(preview['id'], 1)
                    mel.eval('confirmDialog -title "Confirm" -message "Publish Finished Successfully"')

    def go_kitsu(self):
        kitsu_productions = "http://192.168.3.117/productions/"
        webbrowser.open(kitsu_productions)


if __name__ == "__main__":

    try:
        MainWindow.close()
        MainWindow.deleteLater()
    except:
        pass

    td = MainWindow()
    td.show()
