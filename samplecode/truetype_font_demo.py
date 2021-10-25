# truetype_font_demo.py

from inspect import getsourcefile
import os

from reportlab.lib.fonts import tt2ps

# import reportlab

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics

# from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def ttf_font_demo(font_family, rel_font_path):

    # PDF to create
    font_canvas = canvas.Canvas("ttf_font_demo.pdf", pagesize=letter)
    # determine the path to the font files
    # "getsourcefile" method works across platforms & all execution environments
    code_dir = os.path.dirname(getsourcefile(lambda: 0))
    module_dir = os.path.realpath(os.path.join(code_dir, os.pardir))
    fonts_folder = os.path.join(module_dir, rel_font_path, font_family)

    # does the font directory even exist?
    try:
        file_list = os.listdir(fonts_folder)
    except:
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
        font_column = "\n".join(str(elem) for elem in ttf_list)
        print(font_column)
    else:
        print("No font files found in {}".format(fonts_folder))
        return

    # Register the fonts so we can use them
    for font_name in ttf_list:
        font_path = os.path.join(fonts_folder, font_name)

        print(font_path)
    # Usage: TTFont(name,filename)
    # vera_font = TTFont("Vera", font_path)
    # pdfmetrics.registerFont(vera_font)

    # pdfmetrics.registerFontFamily(
    #     "Vera", normal="Vera", bold="VeraBd", italic="VeraIt", boldItalic="VeraBI")
    # Use a generic font
    # font_canvas.setFont("Helvetica", 40)
    # font_canvas.drawString(10, 730, "The Helvetica font")

    # Use the font!
    # font_canvas.setFont("Vera", 40)
    # font_canvas.drawString(10, 690, "The Vera font")
    # font_canvas.save()


if __name__ == "__main__":
    ttf_font_demo("Roboto", "assets/fonts/")
