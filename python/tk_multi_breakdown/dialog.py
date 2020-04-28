# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import copy

from sgtk.platform.qt import QtGui
from .ui.dialog import Ui_Dialog


class AppDialog(QtGui.QWidget):
    def __init__(self, app):
        QtGui.QWidget.__init__(self)
        self._app = app
        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # set up the browsers
        self.ui.browser.set_app(self._app)
        self.ui.browser.set_label("Items in your Scene")
        self.ui.browser.enable_multi_select(True)

        self.ui.chk_green.toggled.connect(self.setup_scene_list)
        self.ui.chk_red.toggled.connect(self.setup_scene_list)

        self.ui.update.clicked.connect(self.update_items)
        self.ui.select_all.clicked.connect(self.select_all_red)

        # load data from shotgun
        self.setup_scene_list()

    ########################################################################################
    # make sure we trap when the dialog is closed so that we can shut down
    # our threads. Nuke does not do proper cleanup on exit.

    def closeEvent(self, event):
        self.ui.browser.destroy()
        # okay to close!
        event.accept()

    ########################################################################################
    # basic business logic

    def select_all_red(self):
        for x in self.ui.browser.get_items():
            try:  # hack - all items arent breakdown nodes
                if x.is_out_of_date() and not x.is_selected():
                    self.ui.browser.select(x)
            except:
                pass

    def update_items(self):

        curr_selection = self.ui.browser.get_selected_items()

        if len(curr_selection) == 0:
            QtGui.QMessageBox.information(
                self, "Please select", "Please select items to update!"
            )
            return

        data = []
        for x in curr_selection:

            if x.is_latest_version() is None or x.is_latest_version() == True:
                # either unloaded or up to date
                continue

            latest_version = x.get_latest_version_number()
            if latest_version is None:
                continue

            # calculate path based on latest version
            new_fields = copy.deepcopy(x.data["fields"])
            new_fields["version"] = latest_version
            new_path = x.data["template"].apply_fields(new_fields)

            d = {}
            d["node"] = x.data["node_name"]
            d["type"] = x.data["node_type"]
            d["path"] = new_path

            # we need to query the additional publish fields for the new published file
            # so we can update those attributes on the node as well
            additional_publish_fields = self._app.get_setting("additional_publish_fields")
            if additional_publish_fields:
                # add the additional publish fields to query.
                publish_fields = additional_publish_fields

                if tank.util.get_published_file_entity_type(self._app.tank) == "PublishedFile":
                    publish_fields.append("published_file_type")
                else:  # == "TankPublishedFile"
                    publish_fields.append("tank_type")

                publish_data = tank.util.find_publish(self._app.tank, [new_path], fields=publish_fields)
                sg_data = publish_data.get(new_path)

                if sg_data:
                    for publish_field in additional_publish_fields:
                        if publish_field in sg_data:
                            if "sg_data" not in d:
                                d["sg_data"] = dict()
                            d["sg_data"][publish_field] = sg_data[publish_field]

            data.append(d)

        # call out to hook
        self._app.execute_hook_method("hook_scene_operations", "update", items=data)

        # finally refresh the UI
        self.setup_scene_list()

    def setup_scene_list(self):
        self.ui.browser.clear()

        d = {}

        # now analyze the filters
        if self.ui.chk_green.isChecked() and self.ui.chk_red.isChecked():
            # show everything
            d["show_red"] = True
            d["show_green"] = True
        elif self.ui.chk_green.isChecked() and not self.ui.chk_red.isChecked():
            d["show_red"] = False
            d["show_green"] = True
        elif not self.ui.chk_green.isChecked() and self.ui.chk_red.isChecked():
            d["show_red"] = True
            d["show_green"] = False
        else:
            # show all
            d["show_red"] = True
            d["show_green"] = True

        self.ui.browser.load(d)
