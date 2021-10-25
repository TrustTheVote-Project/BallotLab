# contest.py
# format a ballot contest.

from page_layout import PageLayout
from images import EmbeddedImage
from reportlab.platypus import Table
from reportlab.platypus import Paragraph
from reportlab.lib.styles import LineStyle, getSampleStyleSheet
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.graphics.shapes import Ellipse
from reportlab.lib.colors import white, black

oval_width = 10
oval_height = 4


class SelectionOval(_DrawingEditorMixin, Drawing):
    def __init__(self, width=400, height=200, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)

        self.width = oval_width + PageLayout.border_pad
        self.height = oval_height + PageLayout.border_pad
        oval_cx = self.width / 2
        oval_cy = self.height / 2
        self._add(
            self,
            Ellipse(oval_cx, oval_cy, oval_width, oval_height),
            name="oval",
            validate=None,
            desc=None,
        )
        self.oval.fillColor = white
        self.oval.strokeColor = black
        self.oval.strokeWidth = 0.5


class Contest:
    """
    Ballot Contest class encapsulates
    the generation of a ballot contest
    table
    """

    def __init__(self):
        # set up the page layout settings
        self.contest_list = []
        self.contestants = []
        self.contest_title = ""
        self.contest_instruct = ""

        def get_contest_data():
            self.contest_title = "President and Vice-President of the United States"
            self.contest_instruct = "Vote for 1 pair"
            self.contestants = [
                ("Joseph Barchi and Joseph Hallaren", "Blue"),
                ("Adam Cramer and Greg Vuocolo", "Yellow"),
                ("Daniel Court and Amy Blumhard", "Purple"),
                ("Alvin Boone and James Lian", "Orange"),
                ("Austin Hildebrand and James Garritty", "Pink"),
                ("Martin Patterson and Clay Lariviere", "Gold"),
                ("Elizabeth Harp and Antoine Jefferson", "Gray"),
                ("Marzena Pazgier and Welton Phelps", "Brown"),
            ]

        def build_contest_list(contestants, contestant_party_list):
            oval = SelectionOval()
            for contestant, party in contestants:
                # add newlines around " and "
                if contestant.find(" and "):
                    contestant = contestant.replace(" and ", "<br />and<br />")
                contest_line = "<b>{}</b><br />{}".format(contestant, party)
                contest_row = [oval, Paragraph(contest_line, normal)]
                contestant_party_list.append(contest_row)

        def build_contest_table():
            """
            Builds a table with contest header, instructions
            and choices
            """
            # get the contest data from the data source
            get_contest_data()
            # build the contest header
            row_1 = [Paragraph(self.contest_title, h1), ""]
            row_2 = [Paragraph(self.contest_instruct, h2), ""]
            self.contest_list = [row_1]
            self.contest_list.append(row_2)
            build_contest_list(self.contestants, self.contest_list)

            # construct and format the contest table
            self.contest_table = Table(
                data=self.contest_list,
                colWidths=(oval_width * 3, None),
                style=[
                    # draw lines below each contestant
                    ("LINEBELOW", (1, 2), (1, -1), 1, grey),
                    # format the header
                    ("BACKGROUND", (0, 0), (1, 0), grey),
                    ("BACKGROUND", (0, 1), (1, 1), light),
                    # draw the outer border on top
                    ("LINEABOVE", (0, 0), (1, 0), 3, black),
                    ("LINEBEFORE", (0, 0), (0, -1), 1, black),
                    ("LINEBELOW", (0, -1), (-1, -1), 1, black),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("SPAN", (0, 0), (1, 0)),
                    ("SPAN", (0, 1), (1, 1)),
                    # ("FONTSIZE", (1, 2), (-1, -1), 48),
                    ("TOPPADDING", (0, 2), (-1, -1), 4),
                    # pad the first cell
                    ("BOTTOMPADDING", (0, 0), (0, 1), 8),
                    # pad below each contestant
                    ("BOTTOMPADDING", (0, 2), (-1, -1), 16),
                ],
            )
            # self.contest_table._linecmds(["ROUNDEDCORNERS", 1])

        # define styles
        # fill colors
        light = PageLayout.light
        white = PageLayout.white
        black = PageLayout.black
        grey = PageLayout.grey

        # font family info
        font_normal = PageLayout.font_normal
        font_bold = PageLayout.font_bold
        font_size = PageLayout.font_size
        normal_lead = PageLayout.normal_lead
        border_pad = PageLayout.border_pad / 2

        # image dimensions
        col_width = PageLayout.col_width

        # start with the sample styles
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        h1 = styles["Heading1"]
        h2 = styles["Heading2"]

        # define custom styles for contest tables
        PageLayout.define_custom_style(
            h1,
            grey,
            border_pad,
            font_size + 2,
            black,
            font_bold,
            normal_lead,
            sp_before=12,
            sp_after=48,
        )
        PageLayout.define_custom_style(
            h2,
            light,
            border_pad,
            font_size,
            black,
            font_bold,
            normal_lead,
            sp_before=12,
            sp_after=48,
        )
        PageLayout.define_custom_style(
            normal,
            white,
            border_pad,
            font_size,
            black,
            font_normal,
            normal_lead,
        )
        # build the contest table, an attribute of the Contest object
        build_contest_table()


if __name__ == "__main__":
    contest_1 = Contest()
    print(contest_1.contest_list)
