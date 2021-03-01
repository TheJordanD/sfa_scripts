class SceneFile(object):
    """An abstract represetnation of a Scene file"""
    def __init__(self, folder_path, descriptor, task, ver, ext):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.ver = ver
        self.ext = ext

scene_file = SceneFile("Macintosh HD/Users/jordan/", "tank", "model", "v001", ".ma")
print(scene_file.descriptor)