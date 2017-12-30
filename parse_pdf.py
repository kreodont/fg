# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfpage import PDFTextExtractionNotAllowed
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfdevice import PDFDevice
# from pdfminer.layout import LAParams
# from pdfminer.converter import TextConverter
# from io import StringIO
from bs4 import BeautifulSoup
import re
import pickle

# def convert_pdf_to_txt(path):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     codec = 'utf-8'
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#     fp = open(path, 'rb')
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     password = ""
#     maxpages = 0
#     caching = True
#     pagenos = {171}
#
#     for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
#         interpreter.process_page(page)
#
#     text = retstr.getvalue()
#
#     fp.close()
#     device.close()
#     retstr.close()
#     return text
styles_dict = {('LOEWBH', '11'): 'Normal text',
               ('EOQGHV', '11'): 'Normal text',
               ('VQHELN', '11'): 'Normal text',
               ('LOEWBH', '13'): 'Normal text',
               ('QYRATX', '9'): 'Page footer',
               ('MSTCPF', '10'): 'Page number',
               ('QYRATX', '15'): 'Header 1',
               ('UEUYXP', '14'): 'Gray note bold header',
               ('WCPFZL', '12'): 'Bold text',
               ('SWRHVT', '12'): 'Bold text',
               ('UMSYXP', '10'): 'Bold text',
               ('QYRATX', '13'): 'Header 2',
               ('QYRATX', '28'): 'Header 3',
               ('UMSYXP', '12'): 'Header 4',
               ('WCPFZL', '15'): 'Header 5',
               ('UEUYXP', '10'): 'Gray note bold header',
               ('PHFUFZ', '10'): 'Gray note normal text',
               ('KXSQNJ', '10'): 'Gray note normal text',
               ('IUTELN', '10'): 'Green note italic text',
               ('XEYGNJ', '13'): 'Bold italic text',
               ('RSCBHV', '11'): 'Italic text',
               ('NMEDDD', '11'): 'Italic text',
               ('WCPFZL', '25'): 'Image header',
               ('LOEWBH', '18'): 'Image sub-header',
               ('LOEWBH', '9'): 'Image text',
               ('LOEWBH', '4'): 'Image text',
               ('LOEWBH', '2'): 'Image text',
               ('LOEWBH', '5'): 'Image text',
               ('LOEWBH', '3'): 'Image text',
               ('WCPFZL', '11'): 'Image text',
               ('WHTKZL', '55'): 'Image text',
               ('UEUYXP', '24'): 'Image text',
               ('UEUYXP', '17'): 'Image text',
               ('WHTKZL', '48'): 'Image text',
               ('ZEDXPF', '9'): 'Small italic',
               ('IUTELN', '7'): 'Small italic',
               ('PHFUFZ', '7'): 'Small normal',
               ('KXSQNJ', '7'): 'Small normal',
               ('PHFUFZ', '13'): 'Red text',
               ('QYRATX', '20'): 'Image text',
               ('PHFUFZ', '11'): 'Image text',
               ('LJFRBH', '11'): 'Image text',
               ('LJFRBH', '8'): 'Image text',
               ('WHTKZL', '12'): 'Image text',
               ('UMSYXP', '6'): 'Image text',
               ('RSCBHV', '13'): 'Italic text',
               ('PHFUFZ', '6'): 'Unknown',
               ('QGUATX', '6'): 'Unknown',
               ('UMSYXP', '3'): 'Unknown',
               ('UMSYXP', '2'): 'Unknown',
               ('UMSYXP', '4'): 'Unknown',
               ('VQHELN', '6'): 'Unknown',
               ('JGBFZL', '12'): 'Unknown',
               ('UEUYXP', '16'): 'Unknown',
               ('UEUYXP', '11'): 'Unknown',
               ('LZBMBH', '10'): 'Unknown',
               ('WCPFZL', '14'): 'Unknown',
               ('WCPFZL', '35'): 'Unknown',
               ('WCPFZL', '17'): 'Unknown',
               ('LOEWBH', '7'): 'Unknown',
               ('WCPFZL', '24'): 'Unknown',
               ('EOQGHV', '10'): 'Unknown',
               ('ZEDXPF', '10'): 'Unknown',
               ('WCPFZL', '8'): 'Unknown',
               ('LOEWBH', '6'): 'Unknown',
               ('LOEWBH', '10'): 'Unknown',
               ('UEUYXP', '9'): 'Unknown',
               ('QGUATX', '8'): 'Unknown',
               ('RCGGHV', '9'): 'Unknown',
               ('UMSYXP', '8'): 'Unknown',
               ('WCPFZL', '41'): 'Unknown',
               ('LOEWBH', '8'): 'Unknown',
               ('RCGGHV', '12'): 'Unknown',
               ('LOEWBH', '15'): 'Unknown',
               ('WCPFZL', '32'): 'Unknown',
               ('UEUYXP', '12'): 'Unknown',
               ('UEUYXP', '7'): 'Unknown',
               ('UEUYXP', '8'): 'Unknown',
               ('QYRATX', '24'): 'Unknown',
               ('QYRATX', '22'): 'Unknown',
               ('QYRATX', '21'): 'Unknown',
               ('QYRATX', '18'): 'Unknown',
               ('QYRATX', '14'): 'Unknown',
               ('QYRATX', '11'): 'Unknown',
               ('QYRATX', '25'): 'Unknown',
               ('QYRATX', '19'): 'Unknown',
               ('QYRATX', '17'): 'Unknown',
               ('QYRATX', '16'): 'Unknown',
               ('QYRATX', '10'): 'Unknown',
               ('QYRATX', '7'): 'Unknown',
               ('QYRATX', '12'): 'Unknown',
               ('QYRATX', '8'): 'Unknown',
               ('QYRATX', '5'): 'Unknown',
               ('QYRATX', '3'): 'Unknown',
               ('QYRATX', '0'): 'Unknown',
               ('QYRATX', '2'): 'Unknown',
               ('QYRATX', '6'): 'Unknown',
               ('QGUATX', '10'): 'Unknown',
               ('LOEWBH', '1'): 'Unknown',
               ('LOEWBH', '0'): 'Unknown',
               ('LOEWBH', '19'): 'Unknown',
               ('LOEWBH', '17'): 'Unknown',
               ('FNFMVT', '10'): 'Unknown',
               ('WCPFZL', '34'): 'Unknown',
               ('LOEWBH', '14'): 'Unknown',
               ('OYTILB', '10'): 'Unknown',
               ('UMSYXP', '16'): 'Unknown',
               ('WHTKZL', '36'): 'Unknown',
               ('RSCBHV', '14'): 'Unknown'
               }


def parse_style(style_string):
    tokens = re.findall("font-family: b'(.+)\+.+font-size:(\d+)px", style_string)
    if not tokens or len(tokens[0]) < 2:
        return ''
        # raise Exception('Cannot parse style string %s' % style_string)
    if tokens[0] not in styles_dict:
        # print('Unknown')
        print("%s: 'Unknown'," % str(tokens[0]))
        # print(tokens[0])
        styles_dict[tokens[0]] = 'Unknown'
        return 'Unknown'
        # raise Exception('Unknown text style: %s' % str(tokens[0]))
    return styles_dict[tokens[0]]


text = open('short_test.html', encoding="utf-8").read()
# text = open('output.html', encoding="utf-8").read()
soup = BeautifulSoup(text, "html.parser")
paragraphs = soup.find_all('div')
articles_list = []
current_article_header = ''
current_article_text = ''
paragraph_text = ''
starting_tag_added = False
for p in paragraphs:
    if not p.text.strip():  # empty paragraph
        continue
    paragraph_text = ''
    spans = p.find_all('span')
    for span in spans:
        if not span:
            continue

        style = parse_style(span['style'])
        if 'Page' in style or 'Image' in style or 'note' in style:
            continue

        if style == 'Normal text':
            paragraph_text += span.text.replace('-\n', '').replace('\n', ' ')
        elif style == 'Header 1':
            if current_article_header:
                if paragraph_text.strip():
                    if starting_tag_added:
                        current_article_text += '%s</p>\n' % paragraph_text
                    else:
                        current_article_text += '<p>%s</p>\n' % paragraph_text
                    paragraph_text = ''
                    starting_tag_added = False
                articles_list.append({current_article_header: current_article_text.replace("</i><i>-</i><i>", '').replace("</b><b>-</b><b>", '')})

            current_article_header = span.text.strip()
            current_article_text = '<h>%s</h>\n' % span.text.strip()
            starting_tag_added = False
        elif style == 'Header 2':
            if paragraph_text.strip():
                if starting_tag_added:
                    current_article_text += '%s</p>\n' % paragraph_text
                else:
                    current_article_text += '<p>%s</p>\n' % paragraph_text
                paragraph_text = ''
                starting_tag_added = False
            current_article_text += '<h>%s</h>\n' % span.text.strip()
        elif style == 'Bold text':
            paragraph_text += '<b>%s</b>' % span.text.strip()
        elif style == 'Bold italic text':
            paragraph_text += '<i><b>%s</b></i>' % span.text.strip()
        elif style == 'Italic text':
            paragraph_text += '<i>%s</i>' % span.text.strip()
        else:
            print(style)
            exit(1)
    if paragraph_text.strip():
        if paragraph_text.strip().endswith('.'):
            if starting_tag_added:
                current_article_text += '%s</p>\n' % paragraph_text
            else:
                current_article_text += '<p>%s</p>\n' % paragraph_text
                starting_tag_added = False
        else:
            # print(current_article_text)
            # print(paragraph_text)
            # exit(0)
            if starting_tag_added:
                current_article_text +=  paragraph_text
            else:
                current_article_text += '<p>' + paragraph_text
                starting_tag_added = True

for article in articles_list:
    print(list(article.values())[0])
    print('\n\n')

with open('stories.obj', 'wb') as f:
    f.write(pickle.dumps(articles_list))