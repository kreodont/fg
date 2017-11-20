from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfdevice import PDFDevice


raw_file = open('bestiary.pdf', 'rb')
parser = PDFParser(raw_file)
document = PDFDocument(parser)
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
rsrcmgr = PDFResourceManager()
device = PDFDevice(rsrcmgr)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    print(interpreter.process_page(page))
    exit(0)