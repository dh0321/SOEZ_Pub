# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts")

from login_controller import LoginWindow


class EZPUB:
    def __init__(self):
        self.lg = LoginWindow()

    def auto(self):
        self.lg = LoginWindow()

