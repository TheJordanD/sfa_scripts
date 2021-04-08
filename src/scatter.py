import maya.cmds as cmds

selection = cmds.ls(orderedSelection=True, flatten=True)

vertexNames = cmds.filterExpand(selectionMask=31, expand=True, )

objectToInstance = selection[0]

if cmds.objectType(objectToInstance) == "transform":

    for vert in vertexNames:
        newInstance = cmds.instance(objectToInstance)

        position = cmds.pointPosition(vert, world=True)

        cmds.xform(newInstance, translation=position)

else:
    print("Please ensure the first object you select is a transfrom")
