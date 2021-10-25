# native_font_list.py
# lists the fonts built into ReportLab

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

VERT_START_POINT = 750
RIGHT_MARGIN = 30
TAB_STOP_X = 12
# anything bigger than 24 is going to be a problem
FONT_SIZE = 24
LINE_HEIGHT_FACTOR = 1.3
line_height = int(FONT_SIZE * LINE_HEIGHT_FACTOR)


def print_font_list(my_canvas, fonts):
    pos_y = VERT_START_POINT
    for font in fonts:
        # display font
        print(font)
        my_canvas.setFont(font, FONT_SIZE)
        my_canvas.drawString(RIGHT_MARGIN, pos_y, font)
        # label font
        my_canvas.setFont("Courier", FONT_SIZE / 2)
        my_canvas.drawString(RIGHT_MARGIN * TAB_STOP_X, pos_y, font)
        pos_y -= line_height


if __name__ == "__main__":
    my_canvas = canvas.Canvas("native_font_list.pdf", pagesize=letter)
    fonts = my_canvas.getAvailableFonts()
    print_font_list(my_canvas, fonts)
    my_canvas.save()
