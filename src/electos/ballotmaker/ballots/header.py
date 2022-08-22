from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph


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

    return f"<font size={font_size}<b>Sample Ballot for {elect_dict['Name']}</b></font>"


def header(canvas, doc):
    width, height = doc.pagesize
    styles = getSampleStyleSheet
    ptext = build_header_text()
    p = Paragraph(ptext, styles["Normal"])
    p.wrapOn(canvas, width, height)
    p.drawOn(canvas, 400, 730)


if __name__ == "__main__":
    header_text = build_header_text()
    print(header_text)
