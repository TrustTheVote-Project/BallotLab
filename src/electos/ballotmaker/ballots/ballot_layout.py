"""
The Ballot Layout module contains the document specifications,
page templates, and specific pages
"""
import logging
from datetime import datetime
from functools import partial
from pathlib import Path

from electos.ballotmaker.ballots.contest_layout import (
    BallotMeasureLayout,
    CandidateContestLayout,
)
from electos.ballotmaker.ballots.instructions import Instructions
from electos.ballotmaker.ballots.page_layout import PageLayout
from electos.ballotmaker.data.models import BallotStyleData
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
)
from reportlab.platypus.flowables import CondPageBreak

logging.getLogger(__name__)

# TODO: use enums in ContestType: https://github.com/TrustTheVote-Project/BallotLab/pull/113#discussion_r973606562
# Also: see line 147
CANDIDATE = "candidate"
BALLOT_MEASURE = "ballot measure"


# set up frames
# 1 = True, 0 = FALSE
SHOW_BOUNDARY = 0
# get page layout settings
margin = PageLayout.margin
c_width = PageLayout.col_width
c_height = PageLayout.col_height
c_space = PageLayout.col_space
# define 3-column layout with header
left_frame = Frame(
    margin * inch,
    margin * inch,
    width=c_width * inch,
    height=c_height * inch,
    topPadding=0,
    showBoundary=SHOW_BOUNDARY,
)
mid_frame = Frame(
    (margin + c_width + c_space) * inch,
    margin * inch,
    width=c_width * inch,
    height=c_height * inch,
    topPadding=0,
    showBoundary=SHOW_BOUNDARY,
)
right_frame = Frame(
    (margin + (2 * (c_width + c_space))) * inch,
    margin * inch,
    width=c_width * inch,
    height=c_height * inch,
    topPadding=0,
    showBoundary=SHOW_BOUNDARY,
)

one_frame = Frame(
    margin * inch,
    margin * inch,
    width=7 * inch,
    height=c_height * inch,
    topPadding=0,
    showBoundary=SHOW_BOUNDARY,
)


def add_header_line(
    font_size: int, line_text: str, new_line: bool = False
) -> str:
    line_end = "<br />" if new_line else ""
    return f"<font size={font_size}><b>{line_text}</b></font>{line_end}"


def build_header_text(election_header: dict, scope: str) -> str:
    font_size = 12
    formatted_header = add_header_line(
        font_size,
        f"Sample Ballot for {election_header['Name']}",
        new_line=True,
    )
    formatted_header += add_header_line(font_size, scope, new_line=True)
    end_date = datetime.fromisoformat(election_header["EndDate"])
    formatted_date = end_date.strftime("%B %m, %Y")
    formatted_header += add_header_line(font_size, formatted_date)

    return formatted_header


def header(canvas, doc, content):
    canvas.saveState()
    # these variables are used elsewhere by ReportLab
    width, height = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, PageLayout.margin * inch, 10.75 * inch)
    canvas.restoreState()


def build_ballot(
    ballot_data: BallotStyleData, election_header: dict, output_dir: Path
) -> str:
    # create PDF filename
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%dT%H%M%S")
    ballot_label = ballot_data.id
    ballot_scope_count = len(ballot_data.scopes)
    if ballot_scope_count > 1:
        raise NotImplementedError(
            f"Multiple ballot scopes currently unsupported. Found {ballot_scope_count} ballot scopes."
        )
    ballot_scope = ballot_data.scopes[0]
    ballot_name = f"{output_dir}/{ballot_label}_{date_time}.pdf"

    doc = BaseDocTemplate(ballot_name)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    header_text = build_header_text(election_header, ballot_scope)
    header_content = Paragraph(header_text, normal)
    three_column_template = PageTemplate(
        id="3col",
        frames=[left_frame, mid_frame, right_frame],
        onPage=partial(header, content=header_content),
    )
    one_column_template = PageTemplate(
        id="1col",
        frames=[one_frame],
        onPage=partial(
            header,
            content=header_content,
        ),
    )
    doc.addPageTemplates(three_column_template)
    doc.addPageTemplates(one_column_template)

    # TODO: use ballot_data.candidate_contests & .ballot_measures instead.
    # See thread for details: https://github.com/TrustTheVote-Project/BallotLab/pull/113#discussion_r973608016
    candidate_contests = []
    ballot_measures = []
    # get contests
    for count, contest in enumerate(ballot_data.contests, start=1):
        title = contest.title
        con_type = contest.type
        logging.info(f"Found contest: {title} - {con_type}")
        if con_type == CANDIDATE:
            candidate_contests.append(contest)
        elif con_type == BALLOT_MEASURE:
            ballot_measures.append(contest)
        else:
            raise ValueError(f"Unknown contest type: {con_type}")
    logging.info(f"Total: {count} contests.")

    elements = []
    # add voting instructions
    inst = Instructions()
    elements.append(NextPageTemplate("3col"))
    elements = inst.instruction_list

    # add candidate contests
    for can_con_count, candidate_contest in enumerate(
        candidate_contests, start=1
    ):
        candidate_layout = CandidateContestLayout(
            candidate_contest
        ).contest_table
        elements.append(candidate_layout)
        # insert column break after every 2 contests
        if (can_con_count % 2 == 0) and (can_con_count < 4):
            elements.append(CondPageBreak(c_height * inch))
    # TODO: write more informative log message, see: https://github.com/TrustTheVote-Project/BallotLab/pull/113#discussion_r973608278
    logging.info(f"Added {can_con_count} candidate contests.")
    elements.append(NextPageTemplate("1col"))
    elements.append(PageBreak())
    for measures, ballot_measure in enumerate(ballot_measures, start=1):
        ballot_layout = BallotMeasureLayout(ballot_measure).contest_table
        elements.append(ballot_layout)
    logging.info(f"Added {measures} ballot measures.")
    doc.build(elements)
    return str(ballot_name)
