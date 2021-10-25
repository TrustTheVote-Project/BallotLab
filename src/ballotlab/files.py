# Get properties of the file system
# TODO: Revactor with pathlib to normalize paths across operating systems
# [PEP 428 -- The pathlib module -- object-oriented filesystem paths | Python.org](https://www.python.org/dev/peps/pep-0428/)

from genericpath import isfile
from inspect import getsourcefile
import os


class FileTools:
    def __init__(self, file_name="", rel_path=""):
        self.file_name = file_name
        self.rel_path = rel_path
        self.ext = ""
        self.file_found = False
        self.package_name = "BallotLab"
        # get the absolute path to this module
        self.code_dir = os.path.dirname(getsourcefile(lambda: 0))
        base_len = int(self.code_dir.find(self.package_name))
        if base_len == -1:
            raise Exception("Not executing in the expected package.")
        # if this module is part of the specified package, build the absolute path
        self.package_root = os.path.join(self.code_dir[:base_len], self.package_name)
        self.full_path = self.package_root
        # add a relative path to the target directory
        if self.rel_path:
            self.full_path = os.path.join(self.full_path, self.rel_path)
        if self.file_name:
            self.abs_path_to_file = os.path.join(self.full_path, self.file_name)
            # if the file exists, get the extension and set the file found flag to True
            if isfile(self.abs_path_to_file):
                self.ext = os.path.splitext(self.file_name)[1]
                self.file_found = True


if __name__ == "__main__":
    print("Default settings:")
    file_defaults = FileTools()
    print(file_defaults.code_dir)
    print(file_defaults.package_root)
    print(file_defaults.package_root)
    print(file_defaults.full_path)
    print(file_defaults.file_found)

    target_file = "writein.png"
    target_dir = "assets/img"
    print("Check for file {} in directory {}".format(target_file, target_dir))
    file_check = FileTools(target_file, target_dir)
    print(file_check.code_dir)
    print(file_check.package_root)
    print(file_check.file_name)
    print(file_check.rel_path)
    print(file_check.full_path)
    print(file_check.abs_path_to_file)
    print(file_check.file_found)
