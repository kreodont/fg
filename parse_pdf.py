from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

raw_file = open('C:\YandexDisk\DnD\Гром Штормового Короля.pdf', 'rb')
parser = PDFParser(raw_file)
