#############################################################
#!/bin/env python
# Copyright ReportLab Europe Ltd. 2000-2011
# see license.txt for license details
# from https://pairlist2.pair.net/pipermail/reportlab-users/2011-February/009951.html


from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Ellipse
from reportlab.lib.colors import white, black


class SelectionOval(_DrawingEditorMixin, Drawing):
    def __init__(self, width=400, height=200, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self.width = 136
        self.height = 140
        oval_y = self.height / 2
        self._add(
            self, Ellipse(21, oval_y, 20, 10), name="oval", validate=None, desc=None
        )
        self.oval.fillColor = white
        self.oval.strokeColor = black
        self.oval.strokeWidth = 1
        # self.oval.y = 20
        # self.oval.width = self.width - 21
        # self.oval.height = self.height - 27


def main():
    from reportlab.lib.units import inch
    from reportlab.platypus.paragraph import Paragraph
    from reportlab.platypus.doctemplate import SimpleDocTemplate
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus.tables import (
        Table,
        TableStyle,
        GRID_STYLE,
        BOX_STYLE,
        LABELED_GRID_STYLE,
        COLORED_GRID_STYLE,
        LIST_STYLE,
        LongTable,
    )
    from reportlab.lib import colors
    import os

    styleSheet = getSampleStyleSheet()
    story = []
    # substitute a small image here
    # imFn = "/code/tools/pythonpoint/demos/leftlogo.gif"
    # I = Image(imFn)
    # I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    # I.drawWidth = 1.25 * inch
    # P = Paragraph(
    #     "<para align=center spaceb=3>The <b>ReportLab Left <font color=red>Logo</font></b> Image</para>",
    #     styleSheet["BodyText"],
    # )

    # B = TableBarChart()
    SO = SelectionOval()
    BP = Paragraph(
        "<para align=center spaceb=3>A bar oval in a cell.</para>",
        styleSheet["BodyText"],
    )

    data = [
        [
            "A",
            "B",
            "C",
            Paragraph(
                "<b>A pa<font color=red>r</font>a<i>graph</i></b><super><font color=yellow>1</font></super>",
                styleSheet["BodyText"],
            ),
            "D",
        ],
        ["10", "11", "12", [SO, BP], "14"],
        ["20", "21", "22", "23", "24"],
        ["30", "31", "32", "33", "34"],
        ["40", "41", "42", [SO, BP], "44"],
    ]

    t = Table(
        data,
        style=[
            ("GRID", (1, 1), (-2, -2), 1, colors.green),
            ("BOX", (0, 0), (1, -1), 2, colors.red),
            ("LINEABOVE", (1, 2), (-2, 2), 1, colors.blue),
            ("LINEBEFORE", (2, 1), (2, -2), 1, colors.pink),
            ("BACKGROUND", (0, 0), (0, 1), colors.pink),
            ("BACKGROUND", (1, 1), (1, 2), colors.lavender),
            ("BACKGROUND", (2, 2), (2, 3), colors.orange),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("VALIGN", (3, 0), (3, 0), "BOTTOM"),
            ("BACKGROUND", (3, 0), (3, 0), colors.limegreen),
            ("BACKGROUND", (3, 1), (3, 1), colors.khaki),
            ("ALIGN", (3, 1), (3, 1), "CENTER"),
            ("BACKGROUND", (3, 2), (3, 2), colors.beige),
            ("ALIGN", (3, 2), (3, 2), "LEFT"),
        ],
    )

    story.append(t)
    SimpleDocTemplate("table-bar-oval.pdf", showBoundary=1).build(story)


if __name__ == "__main__":
    main()
#############################################################
