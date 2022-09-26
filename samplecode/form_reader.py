import PyPDF2 as pypdf

pdfobject = open(
    "/Users/neil/repos/BallotLabFork/samplecode/ballot_demo_2022_09_13T095513.pdf",
    "rb",
)
pdf = pypdf.PdfFileReader(pdfobject)
form_data = pdf.get_fields()
print(form_data)
