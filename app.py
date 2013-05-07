"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

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



