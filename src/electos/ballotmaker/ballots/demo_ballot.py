"""
ballot.py
The Demo Ballot module contains the document specifications,
page templates, and specific pages
"""
from datetime import datetime
from functools import partial
from pathlib import Path

# from reportlab.lib.styles import getSampleStyleSheet
from electos.ballotmaker.ballots.contest import CandidateContest
from electos.ballotmaker.ballots.header import header
from electos.ballotmaker.ballots.instructions import Instructions
from electos.ballotmaker.ballots.page_layout import PageLayout
from electos.ballotmaker.demo_data import spacetown_data
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
)
from reportlab.platypus.flowables import CondPageBreak

# set up frames
# 1 = True, 0 = FALSE
SHOW_BOUNDARY = 0
# get page layout settings
margin = PageLayout.margin
c_width = PageLayout.col_width
c_height = PageLayout.col_height
c_space = PageLayout.col_space


def get_election_header() -> dict:
    return {
        "Name": "General Election",
        "StartDate": "2024-11-05",
        "EndDate": "2024-11-05",
        "Type": "general",
        "ElectionScope": "Spacetown Precinct, Orbit City",
    }


def add_header_line(font_size, line_text, new_line=False):
    line_end = "<br />" if new_line else ""
    header_line = f"<font size={font_size}><b>{line_text}</b></font>{line_end}"
    return header_line


def build_header_text():
    elect_dict = get_election_header()
    font_size = 12
    formatted_header = add_header_line(
        font_size + 2, f"Sample Ballot for {elect_dict['Name']}", new_line=True
    )
    formatted_header += "<br />"
    formatted_header += add_header_line(
        font_size, elect_dict["ElectionScope"], new_line=True
    )
    end_date = datetime.fromisoformat(elect_dict["EndDate"])
    formatted_date = end_date.strftime("%B %m, %Y")
    formatted_header += add_header_line(font_size, formatted_date)

    return formatted_header


def header(canvas, doc, content):
    canvas.saveState()
    width, height = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, 0.5 * inch, 10.6 * inch)
    canvas.restoreState()


def build_ballot():

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

    # create PDF filename
    # create datestamp string for PDF
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%dT%H%M%S")
    home_dir = Path.home()
    ballot_name = f"{home_dir}/ballot_demo_{date_time}.pdf"

    doc = BaseDocTemplate(ballot_name)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    head_text = build_header_text()
    header_content = Paragraph(head_text, normal)
    pg_template = PageTemplate(
        id="3col",
        frames=[left_frame, mid_frame, right_frame],
        onPage=partial(header, content=header_content),
    )
    doc.addPageTemplates(pg_template)

    elements = []
    # add voting instructions
    inst = Instructions()
    elements = inst.instruction_list
    elements.append(NextPageTemplate("3col"))
    # add a ballot contest to the second frame (colomn)
    contest_1 = CandidateContest(spacetown_data.can_con_1)
    elements.append(contest_1.contest_table)
    contest_2 = CandidateContest(spacetown_data.can_con_2)
    elements.append(contest_2.contest_table)
    contest_3 = CandidateContest(spacetown_data.can_con_3)
    elements.append(contest_3.contest_table)
    elements.append(CondPageBreak(c_height * inch))
    contest_4 = CandidateContest(spacetown_data.can_con_4)
    elements.append(contest_4.contest_table)
    doc.build(elements)


if __name__ == "__main__":
    build_ballot()
