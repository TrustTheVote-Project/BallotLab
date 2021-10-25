# instructions.py
# Build the ballot instructions


from page_layout import PageLayout
from images import EmbeddedImage
from reportlab.platypus.flowables import CondPageBreak, PageBreak, Spacer
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class Instructions:
    """
    Ballot Instructions class encapsulates static
    instructional text and instructional graphics
    """

    # these variables are hardcoded for now
    # may be read from a settings file later?
    def __init__(self):
        self.instruction_list = []

        def build_instruction_list():
            """
            Build a list of paragraph flowables for the
            ballot instructions section
            """
            instruct_head = "Instructions"
            fill_head = "Making Selections"
            fill_txt = (
                "Fill in the oval to the left of "
                "the name of your choice. "
                "You must blacken the oval "
                "completely, and do not make "
                "any marks outside of the "
                "oval. You do not have to vote "
                "in every race."
            )
            fill_warn_txt = (
                "Do not cross out or "
                "erase, or your vote may "
                "not count. If you make a "
                "mistake or a stray mark, "
                "ask for a new ballot from "
                "the poll workers."
            )
            write_in_head = "Optional write-in"
            write_in_text = (
                "To add a candidate, fill in "
                "the oval to the left of “or "
                "write-in” and print the name "
                "clearly on the dotted line."
            )
            turn_in_head = "Turning in the ballot"
            turn_in_text = (
                "Insert the completed ballot "
                "into the ballot sleeve. Hand "
                "in the ballot to be counted."
            )
            turn_in_warn = "Do not fold the ballot."

            # get images
            image1 = EmbeddedImage("filled_bubble.png", image_width)
            image1_graf = image1.embed_text
            image2 = EmbeddedImage("writein.png", image_width)
            image2_graf = image2.embed_text
            warn_width = 0.25 * inch
            warn_icon = EmbeddedImage("warn_cyan.png", warn_width)
            warn_icon_graf = warn_icon.embed_text
            spacing = border_pad / 3

            self.instruction_list = [
                (Paragraph(instruct_head, h1)),
                (Spacer(0, spacing)),
                (Paragraph(fill_head, h2)),
                (Paragraph(image1_graf, img_graf)),
                (Paragraph(fill_txt, normal)),
                (Spacer(0, spacing)),
                (Paragraph(warn_icon_graf, normal)),
                (Paragraph(fill_warn_txt, warn_text)),
                (Spacer(0, spacing)),
                (Paragraph(write_in_head, h2)),
                (Paragraph(image2_graf, img_graf)),
                (Paragraph(write_in_text, normal)),
                (Spacer(0, spacing)),
                (Paragraph(turn_in_head, h2)),
                (Paragraph(turn_in_text, normal)),
                (Paragraph(warn_icon_graf, normal)),
                (Paragraph(turn_in_warn, warn_text)),
                # Instructions always appear in their own column
                (CondPageBreak(col_height * inch)),
                # (PageBreak()),
            ]

        # define styles
        # set up the page layout settings

        # fill colors
        dark = PageLayout.dark
        light = PageLayout.light
        white = PageLayout.white
        black = PageLayout.black

        # font family info
        font_normal = PageLayout.font_normal
        font_bold = PageLayout.font_bold
        font_size = PageLayout.font_size
        normal_lead = PageLayout.normal_lead
        head_lead = PageLayout.head_lead
        border_pad = PageLayout.border_pad
        space_before = PageLayout.space_before
        col_height = PageLayout.col_height
        no_space = 0

        # image dimensions
        col_width = PageLayout.col_width
        image_width = (col_width * inch) - (border_pad * 2)

        # start with the sample styles
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        warn_text = styles["BodyText"]
        h1 = styles["Heading1"]
        h2 = styles["Heading2"]
        img_graf = styles["Italic"]

        # define our custom styles
        PageLayout.define_custom_style(
            h1, dark, border_pad, font_size + 2, white, font_bold, head_lead
        )
        PageLayout.define_custom_style(
            h2,
            light,
            border_pad,
            font_size,
            black,
            font_bold,
            head_lead,
        )
        PageLayout.define_custom_style(
            normal, light, border_pad, font_size, black, font_normal, normal_lead
        )
        PageLayout.define_custom_style(
            warn_text, light, border_pad, font_size, dark, font_bold, normal_lead
        )
        PageLayout.define_custom_style(
            img_graf,
            light,
            border_pad,
            font_size,
            black,
            font_normal,
            normal_lead,
            no_space,
        )
        # build the list, an attribute of the Instructions object
        build_instruction_list()


if __name__ == "__main__":
    instruct = Instructions()
    print(instruct.instruction_list)
