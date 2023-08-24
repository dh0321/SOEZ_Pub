# -*- coding: utf-8 -*-

import maya.cmds as cmds
import sys

sys.path.append('/home/rapa/maya/scripts/ez_pub/scripts')
sys.path.append('/home/rapa/maya/scripts/ez_pub/scripts/login')


if cmds.menu('EZMenu', exists=True):
    cmds.menu('EZMenu', e=True, dai=True)
else:
    cmds.setParent('MayaWindow')
    cmds.menu('EZMenu', l="EZPUB", p='MayaWindow', to=True)

cmds.setParent(menu=True)

cmds.menuItem(l="EZPUB", sm=True, to=True)
cmds.menuItem(l="EZPUB_API", c="from login_main import EZPUB; td = EZPUB(); td.auto();",
            ann="Open the EZPUB.", image="/home/rapa/maya/scripts/ez_pub/scripts/image/ezpub.png")
cmds.setParent(menu=True)
