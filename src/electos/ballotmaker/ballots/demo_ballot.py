"""
The Demo Ballot module contains the document specifications,
page templates, and specific pages
"""
from datetime import datetime
from functools import partial
from pathlib import Path

from electos.ballotmaker.ballots.contest_layout import (
    BallotMeasureData,
    BallotMeasureLayout,
    CandidateContestData,
    CandidateContestLayout,
)
from electos.ballotmaker.ballots.instructions import Instructions
from electos.ballotmaker.ballots.page_layout import PageLayout
from electos.ballotmaker.demo_data import spacetown_data
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
    return f"<font size={font_size}><b>{line_text}</b></font>{line_end}"


def build_header_text():
    elect_dict = get_election_header()
    font_size = 12
    formatted_header = add_header_line(
        font_size, f"Sample Ballot for {elect_dict['Name']}", new_line=True
    )
    formatted_header += add_header_line(
        font_size, elect_dict["ElectionScope"], new_line=True
    )
    end_date = datetime.fromisoformat(elect_dict["EndDate"])
    formatted_date = end_date.strftime("%B %m, %Y")
    formatted_header += add_header_line(font_size, formatted_date)

    return formatted_header


def header(canvas, doc, content):
    canvas.saveState()
    # these variables are used elsewhere by ReportLab
    width, height = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, PageLayout.margin * inch, 10.75 * inch)
    canvas.restoreState()


def build_ballot() -> str:
    # create PDF filename; include
    # datestamp string for PDF
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%dT%H%M%S")
    home_dir = Path.home()
    ballot_name = f"{home_dir}/ballot_demo_{date_time}.pdf"

    doc = BaseDocTemplate(ballot_name)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    head_text = build_header_text()
    header_content = Paragraph(head_text, normal)
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
    # add a ballot contest to the second frame (colomn)
    layout_1 = CandidateContestLayout(
        CandidateContestData(spacetown_data.can_con_1)
    )
    layout_2 = CandidateContestLayout(
        CandidateContestData(spacetown_data.can_con_2)
    )
    layout_3 = CandidateContestLayout(
        CandidateContestData(spacetown_data.can_con_3)
    )
    layout_4 = CandidateContestLayout(
        CandidateContestData(spacetown_data.can_con_4)
    )
    layout_5 = BallotMeasureLayout(
        BallotMeasureData(spacetown_data.ballot_measure_1)
    )
    layout_6 = BallotMeasureLayout(
        BallotMeasureData(spacetown_data.ballot_measure_2)
    )
    elements = []
    # add voting instructions
    inst = Instructions()
    elements = inst.instruction_list
    elements.append(NextPageTemplate("3col"))
    elements.append(layout_1.contest_table)
    elements.append(layout_2.contest_table)
    elements.append(layout_3.contest_table)
    elements.append(CondPageBreak(c_height * inch))
    elements.append(layout_4.contest_table)
    elements.append(NextPageTemplate("1col"))
    elements.append(PageBreak())
    elements.append(layout_5.contest_table)
    elements.append(layout_6.contest_table)
    doc.build(elements)
    return str(ballot_name)


if __name__ == "__main__":  # pragma: no cover
    build_ballot()
