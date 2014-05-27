# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import nuke
from tank import Hook

class BreakdownSceneOperations(Hook):

    def scan_scene(self, **kwargs):

        reads = []

        # first let's look at maya references
        for node in nuke.allNodes("Read"):
            node_name = node.name()

            # note! We are getting the "abstract path", so contains
            # %04d and %V rather than actual values.
            path = node.knob('file').value().replace("/", os.path.sep)

            reads.append( {"node": node_name, "type": "Read", "path": path})

        return reads

    def update(self, items, **kwargs):

        # items is a list of dicts. Each dict has items node_type, node_name and path

        for i in items:
            node_name = i["node_name"]
            node_type = i["node_type"]
            new_path = i["path"]

            engine = self.parent.engine
            engine.log_debug("%s: Updating to version %s" % (node_name, new_path))

            if node_type == "Read":
                node = nuke.toNode(node_name)
                # make sure slashes are handled correctly - always forward
                new_path = new_path.replace(os.path.sep, "/")
                node.knob("file").setValue(new_path)
            else:
                raise Exception("Unknown node type %s" % node_type)

