"""
ballot.py
The Ballot Class contains the document specifications,
page templates, and specific pages
"""
from datetime import datetime
from functools import partial
from pathlib import Path

# from reportlab.lib.styles import getSampleStyleSheet
from electos.ballotmaker.ballots.contest import Contest
from electos.ballotmaker.ballots.header import header
from electos.ballotmaker.ballots.instructions import Instructions
from electos.ballotmaker.ballots.page_layout import PageLayout
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
)

# set up frames
# 1 = True, 0 = FALSE
SHOW_BOUNDARY = 1
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
        "ElectionScope": "Port Precinct, The State of Farallon",
    }


def build_header_text():
    elect_dict = get_election_header()
    font_size = 14

    return f"<font size={font_size}><b>Sample Ballot for {elect_dict['Name']}</b></font>"


def header(canvas, doc, content):
    canvas.saveState()
    width, height = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, 0.5 * inch, 11 * inch)
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
    contest_1 = Contest()
    elements.append(contest_1.contest_table)

    doc.build(elements)
    # doc.build(elements)


if __name__ == "__main__":
    build_ballot()
