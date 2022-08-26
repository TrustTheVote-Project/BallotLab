# format a ballot contest.

from electos.ballotmaker.ballots.contest_data import (
    CandidateContestData,
    CandidateData,
)
from electos.ballotmaker.ballots.page_layout import PageLayout
from reportlab.graphics.shapes import Drawing, Ellipse, _DrawingEditorMixin
from reportlab.lib.colors import black, white
from reportlab.lib.styles import LineStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table

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


class CandidateContestLayout:
    """
    Ballot Contest Laout class encapsulates
    the generation of a ballot contest
    table flowable
    """

    def __init__(self, contest_data: CandidateContestData):
        self.contest_list = []
        self.contest_id = contest_data.id
        self.contest_title = contest_data.title
        self.votes_allowed = contest_data.votes_allowed
        if self.votes_allowed > 1:
            self.contest_instruct = f"Vote for up to {self.votes_allowed}"
        else:
            self.contest_instruct = f"Vote for {self.votes_allowed}"
        self.candidates = contest_data.candidates

        def build_contest_list(candidates, contest_list):
            oval = SelectionOval()
            for candidate in candidates:
                # add newlines around " and "
                # if candidate.find(" and "):
                #     candidate = candidate.replace(" and ", "<br />and<br />")
                contest_line = f"<b>{candidate.name}</b>"
                if candidate.party_abbr != "":
                    contest_line += f"<br />{candidate.party_abbr}"
                contest_row = [oval, Paragraph(contest_line, normal)]
                contest_list.append(contest_row)

        def build_contest_table():
            """
            Builds a table with contest header, instructions
            and choices
            """
            # build the contest header
            row_1 = [Paragraph(self.contest_title, h1), ""]
            row_2 = [Paragraph(self.contest_instruct, h2), ""]
            self.contest_list = [row_1]
            self.contest_list.append(row_2)
            build_contest_list(self.candidates, self.contest_list)

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
            keep_w_next=1,
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
            keep_w_next=1,
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


if __name__ == "__main__":  # pragma: no cover
    from electos.ballotmaker.demo_data import spacetown_data

    contest_1 = CandidateContestData(spacetown_data.can_con_1)
    print(contest_1.candidates)
    layout_1 = CandidateContestLayout(contest_1)
    print(layout_1.contest_list)
