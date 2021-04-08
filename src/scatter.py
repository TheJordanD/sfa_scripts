import logging

import maya.cmds as cmds

log = logging.getLogger(__name__)


class Scatterer(object):

    def __init__(self):
        pass

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
            destination_object = selection
            log.info("Destination object is now: " + str(selection))
            self.destination_verts = cmds.polyListComponentConversion(
                destination_object,
                toVertex=True)
            self.destination_verts = cmds.filterExpand(self.destination_verts,
                                                  selectionMask=31)
        elif all_verts is True:
            destination_verts = selection
            log.info("Destination verts are now: " + str(destination_verts))
        else:
            log.critical("Select a single object or multiple vertices")

    def perform_scatter(self):
        for vert in self.destination_verts:
            new_instance = cmds.instance(self.source_object)
            position = cmds.pointPosition(vert, world=True)
            cmds.xform(new_instance, translation=position)
