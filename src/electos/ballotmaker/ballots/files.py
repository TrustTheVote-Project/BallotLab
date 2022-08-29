# Finds the source directory for the specified package,
# builds paths and confirms the existence of files

from pathlib import Path


class FileTools:
    def __init__(
        self, file_name="", rel_path="assets/img", package_name="ballotmaker"
    ):
        self.file_name: str = file_name
        self.rel_path: Path = Path(rel_path)
        self.ext: str = ""
        self.file_found: bool = False
        self.package_name: str = package_name
        self.package_path: Path = ""

        # get the absolute path to this module
        self.code_dir = Path(__file__).parent.resolve()
        # TODO: restore test!
        # does the package name appear in the code path?
        # if self.code_dir.match(self.package_name):
        # walk the path upward until the source dir
        path_finder = self.code_dir
        while path_finder.name != self.package_name:
            path_finder = path_finder.parent
        self.package_path = path_finder

        # add a relative path to the source directory, if provided
        self.full_path = Path(self.package_path, self.rel_path)

        if not self.full_path.is_dir():
            raise FileExistsError(f"Directory doesn't exist: {self.full_path}")
        # look for the file, if provided
        if self.file_name:
            self.abs_path_to_file = Path(self.full_path, self.file_name)
            # if the file exists, get the extension and set the file found flag to True
            if self.abs_path_to_file.is_file():
                self.ext = self.abs_path_to_file.suffix
                self.file_found = True


if __name__ == "__main__":  # pragma: no cover
    print("Default settings:")
    file_defaults = FileTools()
    print(f"Default code dir = {file_defaults.code_dir}")
    print(f"Default package dir = {file_defaults.package_path}")
    print(f"Default relative path = {file_defaults.rel_path}")
    print(f"Default full path = {file_defaults.full_path}")
    print(f"Default file found = {file_defaults.file_found}")

    target_file = "writein.png"
    target_dir = "assets/img"
    print(f"Check for file {target_file} in directory {target_dir}")
    file_check = FileTools(target_file, target_dir)
    print(f"File check code dir = {file_check.code_dir}")
    print(f"File check full source path = {file_check.package_path}")
    print(f"File check file name = {file_check.file_name}")
    print(f"File check relative path = {file_check.rel_path}")
    print(f"File check full path = {file_check.full_path}")
    print(f"File check absolute path to file = {file_check.abs_path_to_file}")
    print(f"File check file ext = {file_check.ext}")
    print(f"File check file found = {file_check.file_found}")
