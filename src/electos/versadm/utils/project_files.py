"""
Access files outsite of the source tree, but in the project directory.
Or, if no project name is provided, search the user's home directory.
"""
# TODO: Revactor with pathlib to normalize paths across operating systems
# PEP 428 -- The pathlib module -- object-oriented filesystem paths | Python.org
# (https://www.python.org/dev/peps/pep-0428/)

from genericpath import isfile
from inspect import getsourcefile
import os


class ProjectFiles:
    def __init__(self, file_name="", rel_path="", project_name=""):
        self.file_name = file_name
        self.rel_path = rel_path
        self.ext = ""
        self.file_found = False
        self.project_name = project_name
        # get the absolute path to this module (platform independent)
        self.code_dir = os.path.dirname(getsourcefile(lambda: 0))

        # if no package name provided, look in the user's home directory
        if not self.project_name:
            self.project_root = os.path.expanduser("~")

        else:
            # look for the project name in the path to this code
            base_len = int(self.code_dir.find(self.project_name))
            if base_len == -1:
                raise Exception("Not executing in the expected package.")
            # if this module is part of the specified package, build the absolute path
            self.project_root = os.path.join(
                self.code_dir[:base_len], self.project_name
            )

        self.root_path = self.project_root

        # add a relative path to the target directory
        if self.rel_path:
            self.root_path = os.path.join(self.root_path, self.rel_path)
        if self.file_name:
            self.abs_path_to_file = os.path.join(self.root_path, self.file_name)
            # if the file exists, get the extension and set the file found flag to True
            if isfile(self.abs_path_to_file):
                self.ext = os.path.splitext(self.file_name)[1]
                self.file_found = True


if __name__ == "__main__":
    print("Default settings:")
    file_defaults = ProjectFiles()
    print(file_defaults.code_dir)
    print(file_defaults.project_root)
    print(file_defaults.root_path)
    print(file_defaults.file_found)

    target_file = "writein.png"
    target_dir = "assets/img"
    project = "BallotLab"
    print(
        "Check for file {} in directory {} of project: {}".format(
            target_file, target_dir, project
        )
    )
    file_check = ProjectFiles(target_file, target_dir, project)
    print(file_check.code_dir)
    print(file_check.project_root)
    print(file_check.file_name)
    print(file_check.rel_path)
    print(file_check.root_path)
    print(file_check.abs_path_to_file)
    print(file_check.file_found)
