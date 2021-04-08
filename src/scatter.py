import maya.cmds as cmds

selection = cmds.ls(orderedSelection=True, flatten=True)
vertex_names = cmds.filterExpand(selectionMask=31, expand=True)
sourceObject = selection[0]

if vertex_names is None:
    destinationObject = selection[1]
    vertex_names = cmds.polyListComponentConversion(destinationObject, toVertex=True)
    vertex_names = cmds.filterExpand(vertex_names, selectionMask=31)
    print("Scatter destination: Verts on " + destinationObject)
else:
    print("Scatter destination: Verts")


def perform_scatter():
    if cmds.objectType(sourceObject) == "transform":
        for vert in vertex_names:
            new_instance = cmds.instance(sourceObject)
            position = cmds.pointPosition(vert, world=True)
            cmds.xform(new_instance, translation=position)
    else:
        print("Please ensure the first object you select is a transfrom")


perform_scatter()
