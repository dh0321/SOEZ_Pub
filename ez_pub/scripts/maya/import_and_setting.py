# -*- coding: utf-8 -*-

import maya.cmds as cmds
import os


class Set:
    def __init__(self):

        self.mesh_start_frame = None
        self.mesh_end_frame = None
        self.dome_start_frame = None
        self.dome_end_frame = None

    def import_camera(self):
        asset_path = "/home/rapa/maya/scripts/ez_pub/scripts/assets_default/turntable_camera.mb"

        if os.path.exists(asset_path):
            cmds.file(asset_path, i=True)
        else:
            print('wrong path')

    # import hdri
    def create_skydome_light(self, image_path):
        skydome_light = cmds.shadingNode('aiSkyDomeLight', asLight=True)
        file_node = cmds.shadingNode('file', asTexture=True)
        cmds.setAttr(file_node + ".fileTextureName", image_path, type="string")
        cmds.connectAttr(file_node + ".outColor", skydome_light + ".color")
        cmds.rename(skydome_light, "awesome_skydome")
        return skydome_light

    # change hdri path
    def change_skydome_image_path(self, image_path):
        file_node = cmds.listConnections("awesome_skydome" + ".color", type="file")

        if file_node:
            cmds.setAttr(file_node[0] + ".fileTextureName", image_path, type="string")
            print("Skydome image path changed to: " + image_path)
        else:
            print("No file node connected to the skydome light.")

    # change camera view
    def switch_camera(self):
        cmds.lookThru("turntable_camera")

    # fit to frame
    def fit_selection_in_frame(self, selected_mesh):

        if cmds.ls(selection=True):
            cmds.viewFit(selected_mesh, fitFactor=1, animate=True)
        else:
            print("Please select the objects")

    # draw anim graph
    def rotate_objects(self, selected_mesh, sf, ef):
        print(sf, ef)
        self.mesh_start_frame = sf
        self.mesh_end_frame = ef

        cmds.select(selected_mesh, visible=True)
        cmds.setKeyframe(selected_mesh, value=0, attribute='rotateY', time=self.mesh_start_frame)
        cmds.setKeyframe(selected_mesh, value=360, attribute='rotateY', time=self.mesh_end_frame)
        cmds.keyTangent(selected_mesh, inTangentType='linear', outTangentType='linear', time=(self.mesh_start_frame, self.mesh_end_frame))

    def rotate_dome(self, sf, ef):
        self.dome_start_frame = sf
        self.dome_end_frame = ef

        cmds.select("awesome_skydome", visible=True)
        cmds.setKeyframe("awesome_skydome", value=0, attribute='rotateY', time=self.dome_start_frame)
        cmds.setKeyframe("awesome_skydome", value=360, attribute='rotateY', time=self.dome_end_frame)
        cmds.keyTangent("awesome_skydome", inTangentType='linear', outTangentType='linear', time=(self.dome_start_frame, self.dome_end_frame))
