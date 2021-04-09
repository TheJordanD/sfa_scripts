import logging

import maya.cmds as cmds
import random as rand

log = logging.getLogger(__name__)


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
            print(self.rot_z)
            new_instance = cmds.instance(self.source_object)
            position = cmds.pointPosition(vert, world=True)
            cmds.xform(new_instance, translation=position,
                       scale=(self.scale_x, self.scale_y, self.scale_z),
                       rotation=(self.rot_x, self.rot_y, self.rot_z))
