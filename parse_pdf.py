from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = {171}

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


text = convert_pdf_to_txt('king.pdf')
with open('king.txt', 'w') as output_file:
    output_file.write(text)

# parser = PDFParser(raw_file)
# document = PDFDocument(parser)
# for i in range(1, 100):
#     print(document.getobj(i))
#
# # for (level, title, dest, a, se) in document.g():
# #     print(level, title, dest, a, se)
# exit(0)
# if not document.is_extractable:
#     raise PDFTextExtractionNotAllowed
# rsrcmgr = PDFResourceManager()
# device = PDFDevice(rsrcmgr)
# interpreter = PDFPageInterpreter(rsrcmgr, device)
# for page in PDFPage.create_pages(document):
#     print(page)
#     print(interpreter.process_page(page))
#     exit(0)