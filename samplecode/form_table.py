# from https://groups.google.com/g/reportlab-users/c/KRx3oLi34Dc/m/3GGnhy3qCQAJ
# import PyPDF2
from reportlab.pdfbase import pdfform
from reportlab.platypus import Flowable, SimpleDocTemplate, Table

# from pprint import pprint


class formCheckButton(Flowable):
    def __init__(self, title, value="Yes"):
        self.title = title
        self.value = value
        self.width = 16
        self.height = 16

    def wrap(self, *args):
        self.width = args[0]
        return (self.width, self.height)

    def draw(self):
        self.canv.saveState()
        pdfform.buttonFieldRelative(
            self.canv,
            self.title,
            self.value,
            0,
            0,
            # including w & h shift the buttons up
            # width=self.width,
            # height=self.height,
        )
        self.canv.restoreState()


class createExamplePDFFormFile:
    def __init__(self, filename):
        data = []
        value = "Yes"
        for i in range(10):
            title = f"title {i}"
            checkbox = formCheckButton(title, value)
            data.append([title, checkbox])
        dataTable = Table(data)
        print([dataTable])
        doc = SimpleDocTemplate(filename)
        doc.build([dataTable])


# class readExamplePDFFormFile:
#     def __init__(self, filename):
#         f = PyPDF2.PdfFileReader(filename)
#         data = f.getFields()
#         for title, value in data.items():
#             pprint(value)


ORIGINAL_FILE = "OriginalFile.pdf"
EDITED_FILE = "EditedFile.pdf"

createExamplePDFFormFile(ORIGINAL_FILE)
# readExamplePDFFormFile(ORIGINAL_FILE)
# readExamplePDFFormFile(EDITED_FILE)
