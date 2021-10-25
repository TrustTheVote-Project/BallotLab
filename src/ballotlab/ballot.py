"""
ballot.py
The Ballot Class contains the document specifications,
page templates, and specific pages
"""
from datetime import datetime
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    # Paragraph,
    # NextPageTemplate,
    # PageBreak,
    PageTemplate,
)
from reportlab.lib.units import inch

# from reportlab.lib.styles import getSampleStyleSheet
from contest import Contest
from instructions import Instructions
from page_layout import PageLayout


def build_ballot():

    # set up frames
    # 1 = True, 0 = FALSE
    SHOW_BOUNDARY = 0
    # get page layout settings
    margin = PageLayout.margin
    c_width = PageLayout.col_width
    c_height = PageLayout.col_height
    c_space = PageLayout.col_space

    # define 3-column layout
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

    # styles = getSampleStyleSheet()

    # add voting instructions
    inst = Instructions()
    elements = inst.instruction_list
    # add a ballot contest to the second frame (colomn)
    contest_1 = Contest()
    elements.append(contest_1.contest_table)

    # create PDF filename
    # create datestamp string for PDF
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%dT%H%M%S")
    ballot_name = "pdfs/ballot_{0}.pdf".format(date_time)

    ballot_doc = BaseDocTemplate(ballot_name)
    ballot_doc.addPageTemplates(
        PageTemplate(id="3col", frames=[left_frame, mid_frame, right_frame])
    )
    ballot_doc.build(elements)


if __name__ == "__main__":
    build_ballot()
