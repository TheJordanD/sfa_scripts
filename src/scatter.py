import maya.cmds as cmds

selection = cmds.ls(orderedSelection=True, flatten=True)
vertexNames = cmds.filterExpand(selectionMask=31, expand=True,)
sourceObject = selection[0]


def check_for_verts():
    if vertexNames == None:
        return False
    else:
        return True


if check_for_verts() is False:
    print("Scatter destination: " + selection[1])
else:
    print("Scatter destination: Verts")



#if cmds.objectType(sourceObject) == "transform":
#    for vert in vertexNames:
#        newInstance = cmds.instance(sourceObject)
#        position = cmds.pointPosition(vert, world=True)
#       cmds.xform(newInstance, translation=position)
#else:
#    print("Please ensure the first object you select is a transfrom")
