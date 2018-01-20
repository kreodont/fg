from bs4 import BeautifulSoup
import re
import pickle

# styles_dict = {('LOEWBH', '11'): 'Normal text',
#                ('EOQGHV', '11'): 'Normal text',
#                ('VQHELN', '11'): 'Normal text',
#                ('LOEWBH', '13'): 'Normal text',
#                ('QYRATX', '9'): 'Page footer',
#                ('MSTCPF', '10'): 'Page number',
#                ('QYRATX', '15'): 'Header 1',
#                ('UEUYXP', '14'): 'Gray note bold header',
#                ('WCPFZL', '12'): 'Bold text',
#                ('SWRHVT', '12'): 'Bold text',
#                ('UMSYXP', '10'): 'Bold text',
#                ('QYRATX', '13'): 'Header 2',
#                ('QYRATX', '28'): 'Header 3',
#                ('UMSYXP', '12'): 'Header 4',
#                ('WCPFZL', '15'): 'Header 5',
#                ('UEUYXP', '10'): 'Gray note bold header',
#                ('PHFUFZ', '10'): 'Gray note normal text',
#                ('KXSQNJ', '10'): 'Gray note normal text',
#                ('IUTELN', '10'): 'Green note italic text',
#                ('XEYGNJ', '13'): 'Bold italic text',
#                ('RSCBHV', '11'): 'Italic text',
#                ('NMEDDD', '11'): 'Italic text',
#                ('WCPFZL', '25'): 'Image header',
#                ('LOEWBH', '18'): 'Image sub-header',
#                ('LOEWBH', '9'): 'Image text',
#                ('LOEWBH', '4'): 'Image text',
#                ('LOEWBH', '2'): 'Image text',
#                ('LOEWBH', '5'): 'Image text',
#                ('LOEWBH', '3'): 'Image text',
#                ('WCPFZL', '11'): 'Image text',
#                ('WHTKZL', '55'): 'Image text',
#                ('UEUYXP', '24'): 'Image text',
#                ('UEUYXP', '17'): 'Image text',
#                ('WHTKZL', '48'): 'Image text',
#                ('MUMUVP', '61'): 'Image text',
#                ('DEWSZH', '24'): 'Image text',
#                ('DEWSZH', '17'): 'Image text',
#                ('JAWCFV', '11'): 'Bold text',
#                ('PJYMLJ', '10'): 'Normal text',
#                ('DRUSZH', '10'): 'Bold text',
#                ('BBXGXL', '28'): 'Header 6',
#                ('BBXGXL', '19'): 'Header 6',
#                ('ACIAJN', '11'): 'Normal text',
#                ('TPWKPB', '15'): 'Header 7',
#                ('UTLQDZ', '11'): 'Unknown',
#                ('KZLITT', '10'): 'Unknown',
#                ('UBJLDZ', '11'): 'Italic text',
#                ('OSHBXL', '11'): 'Unknown',
#                ('KMJDTT', '9'): 'Small italic',
#                ('GBGFPB', '9'): 'Unknown',
#                ('DRUSZH', '12'): 'Bold text',
#                ('AKGAJN', '11'): 'Normal text',
#                ('PJYMLJ', '7'): 'Small text',
#                ('OSHBXL', '7'): 'Small italic',
#                ('PJYMLJ', '13'): 'Red text',
#                ('FCWZBD', '30'): 'Header 8',
#                ('FCWZBD', '21'): 'Header 8',
#                ('EYHTNF', '13'): 'Header 9',
#                ('EYHTNF', '13'): 'Header 10',
#                ('ACIAJN', '12'): 'Header 11',
#                ('TPWKPB', '28'): 'Header 12',
#                ('PJYMLJ', '12'): 'Page number',
#                ('TPWKPB', '12'): 'Page footer',
#                ('TPWKPB', '20'): 'Header 13',
#                ('DEWSZH', '16'): 'Header 14',
#                ('OSHBXL', '10'): 'Italic text',
#                ('XQVDTT', '13'): 'Bold text',
#                ('XQVDTT', '9'): 'Bold text',
#                ('TPWKPB', '13'): 'Image text',
#                ('EYHTNF', '12'): 'Normal text',
#                ('DEWSZH', '14'): 'Note header',
#                ('DEWSZH', '10'): 'Note header',
#                ('UJHLDZ', '10'): 'Bold text',
#                ('QGUWOM', '12'): 'Normal text',
#                ('AKGAJN', '10'): 'Normal text',
#                ('CPHQVO', '10'): 'Normal text',
#                ('LLTJHR', '10'): 'Normal text',
#                ('MTVAVU', '13'): 'Bold italic text',
#                ('KMJDTT', '10'): 'Italic text',
#                ('TPWKPB', '7'): 'Normal text',
#                ('PJYMLJ', '9'): 'Footer text',
#                ('PJYMLJ', '15'): 'Underscored text',
#                ('VATRRX', '10'): 'Normal text',
#                ('DRUSZH', '16'): 'Normal text',
#                ('GBGFPB', '10'): 'Normal text',
#                ('ACIAJN', '6'): 'Normal text',
#                ('NWVVJN', '12'): 'Normal text',
#                ('OSHBXL', '9'): 'Footer text',
#                ('KZLITT', '9'): 'Normal text',
#                ('VNWRRX', '13'): 'Unknown',
#                ('RCTTNF', '10'): 'Unknown',
#                ('XQVDTT', '11'): 'Normal text',
#                ('XQVDTT', '8'): 'Normal text',
#                ('MUMUVP', '36'): 'Image text',
#                ('ACIAJN', '15'): 'Image text',
#                ('UTLQDZ', '15'): 'Image text',
#                ('ACIAJN', '14'): 'Image text',
#                ('UBJLDZ', '14'): 'Image text',
#                ('DEWSZH', '11'): 'Header 14',
#                ('ZEDXPF', '9'): 'Small italic',
#                ('IUTELN', '7'): 'Small italic',
#                ('PHFUFZ', '7'): 'Small normal',
#                ('KXSQNJ', '7'): 'Small normal',
#                ('PHFUFZ', '13'): 'Red text',
#                ('QYRATX', '20'): 'Image text',
#                ('PHFUFZ', '11'): 'Image text',
#                ('LJFRBH', '11'): 'Image text',
#                ('LJFRBH', '8'): 'Image text',
#                ('WHTKZL', '12'): 'Image text',
#                ('UMSYXP', '6'): 'Image text',
#                ('RSCBHV', '13'): 'Italic text',
#                ('PHFUFZ', '6'): 'Unknown',
#                ('QGUATX', '6'): 'Unknown',
#                ('UMSYXP', '3'): 'Unknown',
#                ('UMSYXP', '2'): 'Unknown',
#                ('UMSYXP', '4'): 'Unknown',
#                ('VQHELN', '6'): 'Unknown',
#                ('JGBFZL', '12'): 'Unknown',
#                ('UEUYXP', '16'): 'Unknown',
#                ('UEUYXP', '11'): 'Unknown',
#                ('LZBMBH', '10'): 'Unknown',
#                ('WCPFZL', '14'): 'Unknown',
#                ('WCPFZL', '35'): 'Unknown',
#                ('WCPFZL', '17'): 'Unknown',
#                ('LOEWBH', '7'): 'Unknown',
#                ('WCPFZL', '24'): 'Unknown',
#                ('EOQGHV', '10'): 'Unknown',
#                ('ZEDXPF', '10'): 'Unknown',
#                ('WCPFZL', '8'): 'Unknown',
#                ('LOEWBH', '6'): 'Unknown',
#                ('LOEWBH', '10'): 'Unknown',
#                ('UEUYXP', '9'): 'Unknown',
#                ('QGUATX', '8'): 'Unknown',
#                ('RCGGHV', '9'): 'Unknown',
#                ('UMSYXP', '8'): 'Unknown',
#                ('WCPFZL', '41'): 'Unknown',
#                ('LOEWBH', '8'): 'Unknown',
#                ('RCGGHV', '12'): 'Unknown',
#                ('LOEWBH', '15'): 'Unknown',
#                ('WCPFZL', '32'): 'Unknown',
#                ('UEUYXP', '12'): 'Unknown',
#                ('UEUYXP', '7'): 'Unknown',
#                ('UEUYXP', '8'): 'Unknown',
#                ('QYRATX', '24'): 'Unknown',
#                ('QYRATX', '22'): 'Unknown',
#                ('QYRATX', '21'): 'Unknown',
#                ('QYRATX', '18'): 'Unknown',
#                ('QYRATX', '14'): 'Unknown',
#                ('QYRATX', '11'): 'Unknown',
#                ('QYRATX', '25'): 'Unknown',
#                ('QYRATX', '19'): 'Unknown',
#                ('QYRATX', '17'): 'Unknown',
#                ('QYRATX', '16'): 'Unknown',
#                ('QYRATX', '10'): 'Unknown',
#                ('QYRATX', '7'): 'Unknown',
#                ('QYRATX', '12'): 'Unknown',
#                ('QYRATX', '8'): 'Unknown',
#                ('QYRATX', '5'): 'Unknown',
#                ('QYRATX', '3'): 'Unknown',
#                ('QYRATX', '0'): 'Unknown',
#                ('QYRATX', '2'): 'Unknown',
#                ('QYRATX', '6'): 'Unknown',
#                ('QGUATX', '10'): 'Unknown',
#                ('LOEWBH', '1'): 'Unknown',
#                ('LOEWBH', '0'): 'Unknown',
#                ('LOEWBH', '19'): 'Unknown',
#                ('LOEWBH', '17'): 'Unknown',
#                ('FNFMVT', '10'): 'Unknown',
#                ('WCPFZL', '34'): 'Unknown',
#                ('LOEWBH', '14'): 'Unknown',
#                ('OYTILB', '10'): 'Unknown',
#                ('UMSYXP', '16'): 'Unknown',
#                ('WHTKZL', '36'): 'Unknown',
#                ('RSCBHV', '14'): 'Unknown',
#                ('HNDKZK', '55'): 'Other',
#                ('JQCWBG', '55'): 'Header',
#                ('GOOELM', '39'): 'Header',
#                ('FKZYXO', '24'): 'Image text',
#                ('FKZYXO', '17'): 'Image',
#                ('DHAMVS', '28'): 'Header',
#                ('ASSZND', '11'): 'Normal',
#                ('UROKHP', '11'): 'Normal',
#                ('QLQMDX', '11'): 'Italic text',
#                ('TSEETR', '11'): 'Italic text',
#                ('LWZDLH', '10'): 'Bold text',
#                ('DKYHDX', '10'): 'Normal',
#                ('JTARJL', '10'): 'Normal',
#                ('LWZDLH', '12'): 'Header',
#                ('VVZLNI', '11'): 'Normal',
#                ('RPBNJQ', '11'): 'Normal',
#                ('QLMHVS', '9'): 'Small italic',
#                ('JTARJL', '7'): 'Small text',
#                ('HHYJCP', '7'): 'Small italic',
#                ('DKYHDX', '7'): 'Normal',
#                ('JTARJL', '13'): 'Red text',
#                ('HHYJCP', '10'): 'Italic text',
#                ('QNMSYX', '15'): 'Header',
#                ('ASSZND', '13'): 'Normal',
#                ('DHAMVS', '20'): 'Header',
#                ('FKZYXO', '14'): 'Header part',
#                ('FKZYXO', '10'): 'Header part',
#                ('ZBCJRA', '10'): 'Page number',
#                ('DHAMVS', '9'): 'Header',
#                ('OQLVTW', '15'): 'Comment italic',
#                ('DHAMVS', '15'): 'Header',
#                ('DHAMVS', '13'): 'Header',
#                ('FKZYXO', '16'): 'Header part',
#                ('FKZYXO', '11'): 'Header part',
#                ('SJMOXO', '13'): 'Bold text',
#                ('DHAMVS', '10'): 'Page number',
#                ('OQLVTW', '16'): 'Comment italic',
#                ('LXEEMC', '10'): 'Other',
#                ('OQLVTW', '14'): 'Comment italic',
#                ('OQLVTW', '18'): 'Other',
#                ('OQLVTW', '17'): 'Other',
#                ('TIWULM', '9'): 'Other',
#                ('DKYHDX', '9'): 'Other',
#                ('JTARJL', '9'): 'Comment',
#                ('YZPACC', '10'): 'Other',
#                ('QNMSYX', '12'): 'Header',
#                ('JQCWBG', '36'): 'Header',
#                ('ASSZND', '14'): 'Normal text',
#                ('TSEETR', '14'): 'Italic text'
#
#                }

known_styles = {'normal': {'open': '', 'close': '', 'name': 'normal', 'opens_paragraph': True, 'closes_paragraph': False},
                'bold': {'open': '<p>', 'close': '</p>', 'name': 'bold', 'opens_paragraph': True, 'closes_paragraph': False},
                'italic': {'open': '<p>', 'close': '</p>', 'name': 'italic', 'opens_paragraph': True, 'closes_paragraph': False},
                'header': {'open': '<h>', 'close': '</h>\r\n', 'name': 'header', 'opens_paragraph': False, 'closes_paragraph': True},
                'bold italic': {'open': '<p>', 'close': '</p>', 'name': 'bold italic', 'opens_paragraph': True, 'closes_paragraph': False},
                'small': {'open': '', 'close': '', 'name': 'small', 'opens_paragraph': True, 'closes_paragraph': True},
                'context': {'open': '', 'close': '', 'name': 'context', 'opens_paragraph': True, 'closes_paragraph': False}}

king_styles = {('WHTKZL', '55'): 'Other',
               ('UEUYXP', '24'): 'Other',
               ('UMSYXP', '10'): 'Bold text',
               ('KXSQNJ', '10'): 'Normal text',
               ('PHFUFZ', '10'): 'Normal text',
               ('QYRATX', '28'): 'Header',
               ('LOEWBH', '11'): 'Normal text',
               ('UEUYXP', '14'): 'Header',
               ('UEUYXP', '10'): 'Header',
               ('IUTELN', '10'): 'Italic text',
               ('WHTKZL', '48'): 'Other',
               ('ZEDXPF', '9'): 'Small text',
               ('UMSYXP', '12'): 'Other',
               ('EOQGHV', '11'): 'Other',
               ('PHFUFZ', '7'): 'Small text',
               ('IUTELN', '7'): 'Small italic',
               ('KXSQNJ', '7'): 'Other',
               ('PHFUFZ', '13'): 'Other',
               ('UEUYXP', '17'): 'Other',
               ('WCPFZL', '15'): 'Header',
               ('VQHELN', '11'): 'Normal text',
               ('LOEWBH', '13'): 'Normal text',
               ('RSCBHV', '13'): 'Italic text',
               ('RSCBHV', '11'): 'Italic text',
               ('QYRATX', '20'): 'Header',
               ('PHFUFZ', '11'): 'Other',
               ('QYRATX', '9'): 'Other',
               ('MSTCPF', '10'): 'Page number',
               ('QYRATX', '15'): 'Header',
               ('LJFRBH', '11'): 'Other',
               ('LJFRBH', '8'): 'Other',
               ('QYRATX', '13'): 'Header',
               ('WCPFZL', '12'): 'Bold text',
               ('NMEDDD', '11'): 'Italic text',
               ('WHTKZL', '12'): 'Other',
               ('UMSYXP', '6'): 'Other',
               ('PHFUFZ', '6'): 'Other',
               ('QGUATX', '6'): 'Other',
               ('UMSYXP', '3'): 'Other',
               ('UMSYXP', '2'): 'Other',
               ('UMSYXP', '4'): 'Other',
               ('VQHELN', '6'): 'Other',
               ('JGBFZL', '12'): 'Other',
               ('UEUYXP', '16'): 'Header',
               ('UEUYXP', '11'): 'Header',
               ('LZBMBH', '10'): 'Bold text',
               ('WCPFZL', '14'): 'Other',
               ('WCPFZL', '35'): 'Other',
               ('WCPFZL', '17'): 'Other',
               ('LOEWBH', '7'): 'Other',
               ('XEYGNJ', '13'): 'Bold italic text',
               ('SWRHVT', '12'): 'Bold text',
               ('WCPFZL', '24'): 'Other',
               ('EOQGHV', '10'): 'Normal text',
               ('ZEDXPF', '10'): 'Normal text',
               ('WCPFZL', '8'): 'Other',
               ('WCPFZL', '11'): 'Other',
               ('LOEWBH', '6'): 'Other',
               ('LOEWBH', '10'): 'Other',
               ('UEUYXP', '9'): 'Other',
               ('QGUATX', '8'): 'Other',
               ('RCGGHV', '9'): 'Other',
               ('UMSYXP', '8'): 'Other',
               ('WCPFZL', '41'): 'Other',
               ('LOEWBH', '9'): 'Other',
               ('LOEWBH', '8'): 'Other',
               ('RCGGHV', '12'): 'Other',
               ('LOEWBH', '15'): 'Other',
               ('WCPFZL', '32'): 'Other',
               ('UEUYXP', '12'): 'Other',
               ('UEUYXP', '7'): 'Other',
               ('UEUYXP', '8'): 'Other',
               ('QYRATX', '24'): 'Other',
               ('QYRATX', '22'): 'Other',
               ('QYRATX', '21'): 'Other',
               ('QYRATX', '18'): 'Other',
               ('QYRATX', '14'): 'Other',
               ('QYRATX', '11'): 'Other',
               ('QYRATX', '25'): 'Other',
               ('QYRATX', '19'): 'Other',
               ('QYRATX', '17'): 'Other',
               ('QYRATX', '16'): 'Other',
               ('QYRATX', '10'): 'Other',
               ('QYRATX', '7'): 'Other',
               ('QYRATX', '12'): 'Other',
               ('QYRATX', '8'): 'Other',
               ('QYRATX', '5'): 'Other',
               ('QYRATX', '3'): 'Other',
               ('QYRATX', '0'): 'Other',
               ('QYRATX', '2'): 'Other',
               ('QYRATX', '6'): 'Other',
               ('LOEWBH', '4'): 'Other',
               ('LOEWBH', '3'): 'Other',
               ('QGUATX', '10'): 'Bold text',
               ('LOEWBH', '5'): 'Other',
               ('LOEWBH', '2'): 'Other',
               ('LOEWBH', '1'): 'Other',
               ('LOEWBH', '0'): 'Other',
               ('LOEWBH', '19'): 'Other',
               ('LOEWBH', '17'): 'Other',
               ('FNFMVT', '10'): 'Italic text',
               ('WCPFZL', '34'): 'Other',
               ('LOEWBH', '18'): 'Other',
               ('WCPFZL', '25'): 'Other',
               ('LOEWBH', '14'): 'Other',
               ('OYTILB', '10'): 'Normal text',
               ('UMSYXP', '16'): 'Header',
               ('WHTKZL', '36'): 'Other',
               ('RSCBHV', '14'): 'Other'

               }

texts_examples = {}


def parse_style(style_string, this_paragraph_text, page_number=0):
    tokens = re.findall("font-family: b'(.+)\+.+font-size:(\d+)px", style_string)

    if not tokens or len(tokens[0]) < 2:
        return ''
    else:
        tokens = tokens[0]

    if tokens not in king_styles:
        king_styles[tokens] = 'Unknown'

    if tokens not in texts_examples:
        texts_examples[tokens] = ''

    if len(texts_examples[tokens]) < 10000:
        texts_examples[tokens] += '\n' + this_paragraph_text + ' (page %s)' % page_number
    return king_styles[tokens]


text = open('king.html', encoding="utf-8").read()
soup = BeautifulSoup(text, "html.parser")
paragraphs = soup.find_all('div')
articles_list = []
current_page_number = 1
current_article_header = ''
current_article_text = ''
paragraph_text = ''
full_text = ''
previous_style = {}
current_style = {}
paragraph_opened = False
header_opened = False

for p in paragraphs:
    if not p.text.strip():  # empty paragraph
        continue
    spans = p.find_all('span')
    if 'page' in p.text.lower() and ',' not in p.text:
        current_page_number = int(p.text.lower().replace('page ', ''))
        continue

    if not paragraph_opened and not header_opened:
        full_text += '<p>'
        paragraph_opened = True

    for span in spans:
        if not span:
            continue

        style = parse_style(span['style'], span.text, current_page_number)
        if not style:
            continue
        if not span.text:
            continue

        if 'other' in style.lower() or 'unknown' in style.lower() or 'page' in style.lower():
            continue

        current_style = ''
        for style_name in known_styles:
            if style_name.lower() in style.lower():
                current_style = known_styles[style_name]

        if not current_style:
            print(style)
            exit(1)

        if previous_style != current_style:
            if previous_style:
                full_text += previous_style['close']
                if previous_style['name'] == 'header':
                    header_opened = False

            if previous_style and previous_style['closes_paragraph'] and paragraph_opened:
                full_text += '</p>\r\n'
                paragraph_opened = False

            if current_style['closes_paragraph'] and paragraph_opened:
                full_text += '</p>\r\n'
                paragraph_opened = False

            if current_style['opens_paragraph'] and not paragraph_opened and not header_opened:
                full_text += '<p>'
                paragraph_opened = True

            full_text += current_style['open']
            if current_style['name'] == 'header':
                header_opened = True
        span_text = span.text.replace('-\n', '').replace('\n', ' ')
        if span_text.strip() == '-':
            span_text = span_text.replace('-', '')

        if not header_opened:
            span_text = re.sub('\.([^<\\. >\d,])', r'.</p>\n<p>\1', span_text)

        full_text += span_text
        previous_style = current_style

    if paragraph_opened and (full_text.strip().endswith('.') or full_text.strip().endswith('»')) and current_style['name'] == 'normal':
        full_text += current_style['close']
        full_text += '</p>\r\n'
        paragraph_opened = False

full_text += '</p>\r\n'
full_text = full_text.replace('<p></p>\r\n', '')

# full_text = re.sub('\.([^<\\. >\d,])', r'.</p>\n<p>\1', full_text)

print(full_text[150000:350000])

for style in texts_examples:
    if king_styles[style] == 'Unknown':
        print(style)
        print(texts_examples[style])
        print('-' * 80)

with open('stories.obj', 'wb') as f:
    f.write(pickle.dumps(full_text))
