# truetype_font_finder.py
from files import FileTools
import os


def ttf_font_finder(font_family, rel_font_path):

    # determine the path to the font files
    # "getsourcefile" method works across platforms & all execution environments
    ftools = FileTools()
    package_root = ftools.package_root
    fonts_folder = os.path.join(package_root, rel_font_path, font_family)

    # does the font directory even exist?
    try:
        file_list = os.listdir(fonts_folder)
    except FileNotFoundError:
        print("Font directory doesn't exist.")
        return

    # get a list of TrueType fonts in font directory
    font_ext = ".ttf"
    ttf_list = [fname for fname in file_list if fname.endswith(font_ext)]
    # display a formatted columns of fonts found
    font_count = len(ttf_list)

    if font_count > 0:
        # list font files found
        print("Found {} True type font files (*{})".format(font_count, font_ext))
        print("in font directory: {}".format(fonts_folder))
        # font_column = "\n".join(str(elem) for elem in ttf_list)
        # print(font_column)
    else:
        print("No font files found in {}".format(fonts_folder))
        return

    for font_name in ttf_list:
        font_path = os.path.join(fonts_folder, font_name)
        print(font_path)


if __name__ == "__main__":
    ttf_font_finder("Roboto", "assets/fonts")
