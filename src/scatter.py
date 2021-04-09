import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random as rand

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatterer = Scatterer()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.selection_lay = self._create_selection_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.selection_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        pass

    def _create_selection_ui(self):
        self.source_btn = QtWidgets.QPushButton("Select Source")
        self.source_le = QtWidgets.QLineEdit("")
        self.destination_btn = QtWidgets.QPushButton("Select Destination")
        self.destination_le = QtWidgets.QLineEdit("")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_btn)
        layout.addWidget(self.source_le)
        layout.addStretch()
        layout.addWidget(self.destination_btn)
        layout.addWidget(self.destination_le)
        return layout


class Scatterer(object):

    def __init__(self):
        self.scale_x = 1
        self.scale_x_min = 1
        self.scale_x_max = 1
        self.scale_y = 1
        self.scale_y_min = 1
        self.scale_y_max = 1
        self.scale_z = 1
        self.scale_z_min = 1
        self.scale_z_max = 1

        self.rot_x = 0
        self.rot_x_min = 0
        self.rot_x_max = 0
        self.rot_y = 0
        self.rot_y_min = 0
        self.rot_y_max = 0
        self.rot_z = 0
        self.rot_z_min = 0
        self.rot_z_max = 40

    def randomize(self):
        self.scale_x = round(rand.uniform(self.scale_x_min, self.scale_x_max), 2)
        self.scale_y = round(rand.uniform(self.scale_y_min, self.scale_y_max), 2)
        self.scale_z = round(rand.uniform(self.scale_z_min, self.scale_z_max), 2)

        self.rot_x = round(rand.uniform(self.rot_x_min, self.rot_x_max), 2)
        self.rot_y = round(rand.uniform(self.rot_y_min, self.rot_y_max), 2)
        self.rot_z = round(rand.uniform(self.rot_z_min, self.rot_z_max), 2)

    def select_source(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        if len(selection) == 1 and cmds.objectType(selection) == "transform":
            self.source_object = selection
            log.info("Source object is now: " + str(selection))
        else:
            log.critical("Select a single transform object")

    def select_destination(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)

        all_verts = True
        for _item in selection:
            if ".vtx" not in _item:
                all_verts = False

        if len(selection) is 0:
            log.critical("Select a single object or multiple vertices")
        elif len(selection) == 1 and cmds.objectType(selection) == "transform":
            self.destination_object = selection
            self.destination_verts = selection
            log.info("Destination object is now: " + str(selection))
            self.destination_verts = cmds.polyListComponentConversion(
                self.destination_object,
                toVertex=True)
            self.destination_verts = cmds.filterExpand(self.destination_verts,
                                                       selectionMask=31)
        elif all_verts is True:
            self.destination_verts = selection
            log.info("Destination verts are now: "
                     + str(self.destination_verts))
        else:
            log.critical("else: Select a single object or multiple vertices")

    def perform_scatter(self):
        for vert in self.destination_verts:
            self.randomize()
            new_instance = cmds.instance(self.source_object)
            position = cmds.pointPosition(vert, world=True)
            cmds.xform(new_instance, translation=position,
                       scale=(self.scale_x, self.scale_y, self.scale_z),
                       rotation=(self.rot_x, self.rot_y, self.rot_z))
