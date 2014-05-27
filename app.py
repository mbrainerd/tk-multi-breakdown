# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
A breakdown app which shows what in the scene is out of date.
"""

from tank.platform import Application

import sys
import os

class MultiBreakdown(Application):

    def init_app(self):
        """
        Called as the application is being initialized
        """

        tk_multi_breakdown = self.import_module("tk_multi_breakdown")
        cb = lambda : tk_multi_breakdown.show_dialog(self)
        self.engine.register_command("Scene Breakdown...", cb)



