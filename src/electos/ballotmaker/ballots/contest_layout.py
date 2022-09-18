# format a ballot contest.
import logging

from electos.ballotmaker.ballots.page_layout import PageLayout
from electos.ballotmaker.data.models import (
    BallotMeasureContestData,
    CandidateContestData,
)
from reportlab.graphics.shapes import Drawing, Ellipse, _DrawingEditorMixin
from reportlab.lib.colors import black, white, yellow
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfform
from reportlab.platypus import Flowable, Paragraph, Table

logging.getLogger(__name__)

OVAL_WIDTH = 13
OVAL_HEIGHT = 5

OVAL_UP = -6
OVAL_DOWN = 2
OVAL_INDENT = 4
SOLID_FILL = 1

ONE_LINE = 12
FOUR_LINES = 48

YES = 1

CHECKBOX_W = 4
CHECKBOX_H = 8
CHECKBOX_X = 3
CHECKBOX_Y = -12
CHECKBOX_STATE = "Off"  # "Yes" or "Off"

WRITE_IN_W = 100
WRITE_IN_H = 24

# Hide form widgets
ANNOTATION_FLAGS = "noview hidden"
# Show form widgets
ANNOTATION_FLAGS = "print"

BALLOT_MEASURE_INSTRUCT = "Vote yes or no"

# define styles
# fill colors
light = PageLayout.light
grey = PageLayout.grey

# font family info
font_normal = PageLayout.font_normal
font_bold = PageLayout.font_bold
font_size = PageLayout.font_size
normal_lead = PageLayout.normal_lead
border_pad = 2  # PageLayout.border_pad
sm_line = PageLayout.thin_line

# start with the sample styles
styles = getSampleStyleSheet()
normal = styles["Normal"]
h1 = styles["Heading1"]
h2 = styles["Heading2"]

# define custom styles for contest tables
# Contest header
PageLayout.define_custom_style(
    h1,
    grey,
    border_pad,
    font_size + 2,
    black,
    font_bold,
    normal_lead,
    sp_after=FOUR_LINES,
    keep_w_next=YES,
)
# Contest instructions
PageLayout.define_custom_style(
    h2,
    light,
    border_pad,
    font_size,
    black,
    font_bold,
    normal_lead,
    sp_before=ONE_LINE,
    keep_w_next=YES,
)
# Contest body text
PageLayout.define_custom_style(
    normal,
    white,
    border_pad,
    font_size,
    black,
    font_normal,
    normal_lead,
)


def build_contest_list(
    title: str, instruction: str, selections: list, text: str = ""
) -> list:
    """
    Builds a table with contest header, instructions
    and choices
    """
    row_1 = [Paragraph(title, h1), ""]
    row_2 = [Paragraph(instruction, h2), ""]
    contest_list = [row_1, row_2]
    if text != "":
        contest_list.append([Paragraph(text, normal), ""])
    contest_list.extend(iter(selections))
    return contest_list


def build_candidate_table(contest_list):
    return Table(
        data=contest_list,
        colWidths=(OVAL_WIDTH * 3, None),
        style=[
            # draw lines below each contestant
            ("LINEBELOW", (1, 2), (1, -1), sm_line, grey),
            # format the header
            ("BACKGROUND", (0, 0), (1, 0), grey),
            ("BACKGROUND", (0, 1), (1, 1), light),
            # draw the outer border on top, left & bottom
            ("LINEABOVE", (0, 0), (1, 0), 1, black),
            ("LINEBEFORE", (0, 0), (0, -1), sm_line, black),
            ("LINEBELOW", (0, -1), (-1, -1), sm_line, black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("SPAN", (0, 0), (1, 0)),
            ("SPAN", (0, 1), (1, 1)),
            # ("FONTSIZE", (1, 2), (-1, -1), 48),
            ("TOPPADDING", (0, 2), (-1, -1), 4),
            # pad the first cell
            ("BOTTOMPADDING", (0, 0), (0, 1), 8),
            # pad below each candidate
            ("BOTTOMPADDING", (0, 2), (-1, -1), 12),
        ],
    )


def build_ballot_measure_table(contest_list):
    return Table(
        data=contest_list,
        colWidths=(OVAL_WIDTH * 3, None),
        style=[
            # draw lines below each selection
            ("LINEBELOW", (1, 2), (1, -1), sm_line, grey),
            # format the header
            ("BACKGROUND", (0, 0), (1, 0), grey),
            ("BACKGROUND", (0, 1), (1, 1), light),
            # draw the outer border on top
            ("LINEABOVE", (0, 0), (1, 0), 1, black),
            ("LINEBEFORE", (0, 0), (0, -1), sm_line, black),
            ("LINEBELOW", (0, -1), (-1, -1), sm_line, black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("SPAN", (0, 0), (-1, 0)),
            ("SPAN", (0, 1), (-1, 1)),
            ("SPAN", (0, 2), (-1, 2)),
            # ("SPAN", (0, 3), (-1, 3)),
            # ("SPAN", (0, 4), (1, 1)),
            # ("FONTSIZE", (1, 2), (-1, -1), 48),
            ("TOPPADDING", (0, 2), (-1, -1), 4),
            # pad the first cell
            ("BOTTOMPADDING", (0, 0), (0, 1), 8),
            # pad below each choice
            ("BOTTOMPADDING", (0, 2), (-1, -1), 12),
        ],
    )


class SelectionOval(_DrawingEditorMixin, Drawing):
    def __init__(self, width=400, height=200, shift_up=False, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)

        self.width = OVAL_WIDTH + PageLayout.border_pad
        self.height = OVAL_HEIGHT + PageLayout.border_pad
        _vertical_shift = OVAL_UP if shift_up else OVAL_DOWN
        oval_cx = (self.width / 2) + OVAL_INDENT
        oval_cy = (self.height / 2) - _vertical_shift
        self._add(
            self,
            Ellipse(oval_cx, oval_cy, OVAL_WIDTH, OVAL_HEIGHT),
            name="oval",
            validate=None,
            desc=None,
        )
        self.oval.fillColor = white  # yellow, white or black
        self.oval.fillOpacity = SOLID_FILL
        self.oval.strokeColor = black
        self.oval.strokeWidth = sm_line


class formCheckButton(Flowable):
    def __init__(self, title, value="Yes", flags="noview"):
        self.title = title
        self.value = value
        self.flags = flags
        self.x = CHECKBOX_X
        self.y = CHECKBOX_Y
        self.width = CHECKBOX_W
        self.height = CHECKBOX_H

    # ensures this element lines up with others in the cell
    def wrap(self, *args):
        self.width = args[0]
        return (self.width, self.height)

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.checkbox(
            name=self.title,
            buttonStyle="check",
            relative=True,
            size=self.width,
            annotationFlags=ANNOTATION_FLAGS,
        )

        self.canv.restoreState()


class formInputField(Flowable):
    def __init__(self, id, value=""):
        self.id = id
        self.value = value
        self.width = 0
        self.height = 10

    def wrap(self, *args):
        self.width = args[0]
        return (self.width, self.height)

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.textfield(
            name=self.id,
            maxlen=60,
            height=WRITE_IN_H,
            width=WRITE_IN_W,
            relative=True,
            y=-7,
            annotationFlags=ANNOTATION_FLAGS,
        )
        self.canv.restoreState()


class CandidateContestLayout:
    """
    Generate a candidate contest table flowable
    """

    def __init__(self, contest_data: CandidateContestData):
        self.id = contest_data.id
        self.title = contest_data.title
        self.votes_allowed = contest_data.votes_allowed
        if self.votes_allowed > 1:
            self.instruct = f"Vote for up to {self.votes_allowed}"
        else:
            self.instruct = f"Vote for {self.votes_allowed}"
        logging.info(f"Candidate contest: {self.title}")
        self.candidate_choices = contest_data.candidates
        _selections = []

        for candidate_choice in self.candidate_choices:

            # add line for write ins
            if candidate_choice.is_write_in:
                logging.info(
                    f"Found write-in candidate: {candidate_choice.id}"
                )
                contest_text = "<b>or write in:</b>"
                # contest_text = ("<br />" * 2) + ("_" * 20)
                contest_object = [Paragraph(contest_text, normal)]
                # Add text field with ID and suffix
                input_id = f"{candidate_choice.id}_text"
                contest_object.append(formInputField(input_id))
            else:
                contest_text = ""
                for candidate_count, name in enumerate(
                    candidate_choice.name, start=1
                ):
                    if candidate_count > 1:
                        contest_text += "<br />and<br />"
                    # make the candidate name bold
                    contest_text += f"<b>{name}</b>"
                # add party abbreviation in plain text
                party_count = len(candidate_choice.party)
                if party_count == 1:
                    contest_text += (
                        f"<br />{candidate_choice.party[0].abbreviation}"
                    )
                elif party_count > 1:
                    raise NotImplementedError(
                        f"Multiple party tickets not supported (parties found: {party_count})"
                    )

                logging.info(f"Ticket: {contest_text}")
                contest_object = [Paragraph(contest_text, normal)]

            vote_mark = [
                formCheckButton(candidate_choice.id, CHECKBOX_STATE),
                SelectionOval(shift_up=True),
            ]
            contest_row = [vote_mark, contest_object]
            _selections.append(contest_row)
            # build the contest table, an attribute of the Contest object

        self.contest_list = build_contest_list(
            self.title, self.instruct, _selections
        )
        self.contest_table = build_candidate_table(self.contest_list)


class BallotMeasureLayout:
    """
    Generate a candidate contest table flowable
    """

    def __init__(self, contest_data: BallotMeasureContestData):
        self.id = contest_data.id
        self.title = contest_data.title
        self.instruct = BALLOT_MEASURE_INSTRUCT
        self.text = contest_data.text
        self.choices = contest_data.choices
        logging.info(f"Ballot measure: {self.title}")

        oval = SelectionOval()
        _selections = []
        for choose in self.choices:
            choice_text = f"<b>{choose.choice}</b>"
            logging.info(f"Choice: {choice_text} (ID = {choose.id})")

            vote_mark = [
                formCheckButton(choose.id, CHECKBOX_STATE),
                SelectionOval(shift_up=True),
            ]
            contest_row = [vote_mark, Paragraph(choice_text, normal)]
            _selections.append(contest_row)

        self.contest_list = build_contest_list(
            self.title, self.instruct, _selections, self.text
        )
        self.contest_table = build_ballot_measure_table(self.contest_list)
