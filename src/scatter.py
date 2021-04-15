import logging

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random as rand

log = logging.getLogger(__name__)


def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(500)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatterer = Scatterer()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.selection_lay = self._create_selection_ui()
        self.percentage_lay = self._create_percentage_ui()
        self.translation_lay = self._create_translation_ui()
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.selection_lay)
        self.main_lay.addLayout(self.percentage_lay)
        self.main_lay.addLayout(self.translation_lay)
        self.main_lay.addWidget(self.scatter_btn)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.source_btn.clicked.connect(self._select_source)
        self.destination_btn.clicked.connect(self._select_destination)
        self.scatter_btn.clicked.connect(self._perform_scatter)

    def _set_scatterer_properties_from_ui(self):
        self.scatterer.scale_x_min = float(self.scale_x_min_le.text())
        self.scatterer.scale_x_max = float(self.scale_x_max_le.text())
        self.scatterer.scale_y_min = float(self.scale_y_min_le.text())
        self.scatterer.scale_y_max = float(self.scale_y_max_le.text())
        self.scatterer.scale_z_min = float(self.scale_z_min_le.text())
        self.scatterer.scale_z_max = float(self.scale_z_max_le.text())

        self.scatterer.rot_x_min = float(self.rot_x_min_le.text())
        self.scatterer.rot_x_max = float(self.rot_x_max_le.text())
        self.scatterer.rot_y_min = float(self.rot_y_min_le.text())
        self.scatterer.rot_y_max = float(self.rot_y_max_le.text())
        self.scatterer.rot_z_min = float(self.rot_z_min_le.text())
        self.scatterer.rot_z_max = float(self.rot_z_max_le.text())

        self.scatterer.percentage = float(self.percentage_le.text()) / 100


    @QtCore.Slot()
    def _select_source(self):
        self.scatterer.select_source()
        self.source_lbl.setText(str(self.scatterer.source_object[0]))

    @QtCore.Slot()
    def _select_destination(self):
        self.scatterer.select_destination()
        if self.scatterer.destination_object is None:
            self.destination_lbl.setText("vertices")
        else:
            self.destination_lbl.setText(
                str(self.scatterer.destination_object[0]))

    @QtCore.Slot()
    def _perform_scatter(self):
        self._set_scatterer_properties_from_ui()
        self.scatterer.perform_scatter()

    def _create_selection_ui(self):
        self.source_btn = QtWidgets.QPushButton("Select Source")
        self.source_lbl = QtWidgets.QLabel("")
        self.source_lbl.setMinimumWidth(50)
        self.destination_btn = QtWidgets.QPushButton("Select Destination")
        self.destination_lbl = QtWidgets.QLabel("")
        self.destination_lbl.setMinimumWidth(50)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_btn)
        layout.addWidget(self.source_lbl)
        layout.addStretch()
        layout.addWidget(self.destination_btn)
        layout.addWidget(self.destination_lbl)
        return layout

    def _create_percentage_ui(self):
        self.percentage_lbl = QtWidgets.QLabel("Percentage:")
        self.percentage_le = QtWidgets.QLineEdit("100")
        only_double = QtGui.QDoubleValidator()
        self.percentage_le.setValidator(only_double)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.percentage_lbl)
        layout.addWidget(self.percentage_le)
        return layout

    def _create_scale_values_ui(self):
        self.scale_min_lbl = QtWidgets.QLabel("Min")
        self.scale_max_lbl = QtWidgets.QLabel("Max")
        self.scale_x_lbl = QtWidgets.QLabel("X")
        self.scale_y_lbl = QtWidgets.QLabel("Y")
        self.scale_z_lbl = QtWidgets.QLabel("Z")
        self.scale_x_min_le = QtWidgets.QLineEdit("1")
        self.scale_x_max_le = QtWidgets.QLineEdit("1")
        self.scale_y_min_le = QtWidgets.QLineEdit("1")
        self.scale_y_max_le = QtWidgets.QLineEdit("1")
        self.scale_z_min_le = QtWidgets.QLineEdit("1")
        self.scale_z_max_le = QtWidgets.QLineEdit("1")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_min_lbl, 0, 1)
        layout.addWidget(self.scale_max_lbl, 0, 2)
        layout.addWidget(self.scale_x_lbl, 1, 0)
        layout.addWidget(self.scale_y_lbl, 2, 0)
        layout.addWidget(self.scale_z_lbl, 3, 0)
        layout.addWidget(self.scale_x_min_le, 1, 1)
        layout.addWidget(self.scale_x_max_le, 1, 2)
        layout.addWidget(self.scale_y_min_le, 2, 1)
        layout.addWidget(self.scale_y_max_le, 2, 2)
        layout.addWidget(self.scale_z_min_le, 3, 1)
        layout.addWidget(self.scale_z_max_le, 3, 2)
        return layout

    def _create_rot_values_ui(self):
        self.rot_min_lbl = QtWidgets.QLabel("Min")
        self.rot_max_lbl = QtWidgets.QLabel("Max")
        self.rot_x_lbl = QtWidgets.QLabel("X")
        self.rot_y_lbl = QtWidgets.QLabel("Y")
        self.rot_z_lbl = QtWidgets.QLabel("Z")
        self.rot_x_min_le = QtWidgets.QLineEdit("0")
        self.rot_x_max_le = QtWidgets.QLineEdit("0")
        self.rot_y_min_le = QtWidgets.QLineEdit("0")
        self.rot_y_max_le = QtWidgets.QLineEdit("0")
        self.rot_z_min_le = QtWidgets.QLineEdit("0")
        self.rot_z_max_le = QtWidgets.QLineEdit("0")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rot_min_lbl, 0, 1)
        layout.addWidget(self.rot_max_lbl, 0, 2)
        layout.addWidget(self.rot_x_lbl, 1, 0)
        layout.addWidget(self.rot_y_lbl, 2, 0)
        layout.addWidget(self.rot_z_lbl, 3, 0)
        layout.addWidget(self.rot_x_min_le, 1, 1)
        layout.addWidget(self.rot_x_max_le, 1, 2)
        layout.addWidget(self.rot_y_min_le, 2, 1)
        layout.addWidget(self.rot_y_max_le, 2, 2)
        layout.addWidget(self.rot_z_min_le, 3, 1)
        layout.addWidget(self.rot_z_max_le, 3, 2)
        return layout

    def _create_scale_ui(self):
        self.scale_lbl = QtWidgets.QLabel("Scale")
        self.scale_lbl.setStyleSheet("font: bold 12px")
        self.scale_values_lay = self._create_scale_values_ui()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scale_lbl)
        layout.addLayout(self.scale_values_lay)
        return layout

    def _create_rot_ui(self):
        self.rot_lbl = QtWidgets.QLabel("Rotation")
        self.rot_lbl.setStyleSheet("font: bold 12px")
        self.rot_values_lay = self._create_rot_values_ui()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.rot_lbl)
        layout.addLayout(self.rot_values_lay)
        return layout

    def _create_translation_ui(self):
        self.scale_lay = self._create_scale_ui()
        self.rot_lay = self._create_rot_ui()

        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.scale_lay)
        layout.addStretch()
        layout.addLayout(self.rot_lay)
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
        self.rot_z_max = 0

        self.percentage = 0.5

    def randomize(self):
        self.scale_x = rand.uniform(self.scale_x_min, self.scale_x_max)
        self.scale_y = rand.uniform(self.scale_y_min, self.scale_y_max)
        self.scale_z = rand.uniform(self.scale_z_min, self.scale_z_max)

        self.rot_x = rand.uniform(self.rot_x_min, self.rot_x_max)
        self.rot_y = rand.uniform(self.rot_y_min, self.rot_y_max)
        self.rot_z = rand.uniform(self.rot_z_min, self.rot_z_max)

    def select_source(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        if len(selection) == 1 and cmds.objectType(selection) == "transform":
            self.source_object = selection
            # self.source_object = self.source_object[0]
            log.info("Source object is now: " + str(selection))
        else:
            log.critical("Select a single transform object")

    def select_destination(self):
        self.destination_object = None
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
        percentage_destination = []
        for idx in range(0, len(self.destination_verts)):
            rand.seed(idx)
            rand_value = rand.random()
            if rand_value <= self.percentage:
                percentage_destination.append(self.destination_verts[idx])

        for vert in percentage_destination:
            self.randomize()
            new_instance = cmds.instance(self.source_object)
            position = cmds.pointPosition(vert, world=True)
            cmds.xform(new_instance, translation=position,
                       scale=(self.scale_x, self.scale_y, self.scale_z),
                       rotation=(self.rot_x, self.rot_y, self.rot_z))
