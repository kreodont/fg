"""
This module is intended for converting HTML file resulted from pdfminer into
Fantasy Ground module structure
python C:\\Users\\Dima\\pdfminer.six\\tools\\pdf2txt.py -o tomb_exported.html
"C:\\YandexDisk\\DnD\\Гробница Аннигиляции.pdf"
Result - object file with list of Fantasy Grounds formatted text

Tags:
p - Indicates paragraph using normal formatting.

h - Indicates a paragraph using header formatting.

frame - Indicates a paragraph using chat frame formatting.

frameid - Used within the frame tag, immediately following the frame open tag.
Indicates the speaker for chat text.

list - Indicates a list.

li - Used within the list tag. Supports a numerical indent attribute.
Indicates an entry in the list, and contains the text to display for
this list item.

linklist - Indicates a list of shortcut links.
(similar to windowreferencecontrols)

link - Used within the linklist tag. Supports a numerical indent attribute.
Indicates an entry in the link text, and contains the text to display next
to the link.

b - Used within p, li or link tags. Indicates that the text within
the tags should be bold.

i - Used within p, li or link tags. Indicates that the text within
the tags should be italicized.

u - Used within p, li or link tags. Indicates that the text within the
tags should be underlined.

table - Indicates a table. Tables can not be created or edited, only
accessed via modules created outside of FG.

tr - Used within the table tag. Indicates a table row.

td - Used within the tr tag. Supports a colspan attribute, similar to HTML
formatting. Indicates a table cell, and the text to display within the cell.
"""

from dataclasses import dataclass
from typing import Union, List
import bs4
import os
import pickle
import functools
import re


@dataclass
class Error:
    text: str

    def __repr__(self):
        return f'Error: {self.text}'


def get_font_family(style_string: str) -> Union[str, Error]:
    tokens = re.findall("font-family: b'(.+)\+.+font-size:(\d+)px",
                        style_string)
    if not tokens or len(tokens) != 1 or len(tokens[0]) != 2:
        return Error(f'Cannot parse string: {style_string}\n'
                     f'Found {len(tokens)} tokens instead of 2: {tokens}')
    return tokens[0][0]


def get_font_size(style_string: str) -> Union[int, Error]:
    tokens = re.findall("font-family: b'(.+)\+.+font-size:(\d+)px",
                        style_string)
    if not tokens or len(tokens) != 1 or len(tokens[0]) != 2:
        return Error(f'Cannot parse string: {style_string}\n'
                     f'Found {len(tokens)} tokens instead of 2: {tokens}')

    return int(tokens[0][1])


@dataclass
class TextBlock:
    text: str
    style: str

    def __repr__(self):
        font_family = get_font_family(self.style)
        font_size = get_font_size(self.style)
        return f'("{font_family}", {font_size}),\nText:\n{self.text}'


@dataclass
class Article:
    text: str


@dataclass
class Accumulator:
    articles: List[Article]
    current_page: int = 0
    # previous_font_family: str
    # previous_font_size: int
    previous_block: TextBlock = TextBlock('', '')
    # previous_block_type: str = 'null'
    book_started: bool = False
    current_article_text: str = ''
    current_text_block_number: int = 0
    temporary_article: str = ''


# def get_font_family(style_string: str) -> Union[str, Error]:
#     tokens = re.findall("font-family: b'(.+)\+.+font-size:(\d+)px",
#                         style_string)
#     if not tokens or len(tokens) != 1 or len(tokens[0]) != 2:
#         return Error(f'Cannot parse string: {style_string}\n'
#                      f'Found {len(tokens)} tokens instead of 2: {tokens}')
#     return tokens[0][0]


def is_page_block_a_page_number(
        page_block: TextBlock,
        expected_font_family: str,
        expected_font_size: int,
) -> int:
    if (get_font_family(page_block.style) == expected_font_family and
            get_font_size(page_block.style) == expected_font_size and
            page_block.text.strip().isdigit()):
        return int(page_block.text)

    return 0


def maybe(func):
    def runner(*args, **kwargs):
        for positional_parameter in args:
            if isinstance(positional_parameter, Error):
                return positional_parameter

        for parameter_name in kwargs:
            parameter = kwargs[parameter_name]
            if isinstance(parameter, Error):
                return parameter
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Error(f'{type(e)}: {e}')

    return runner


@maybe
def get_file_text(filename: str) -> Union[str, Error]:
    with open(filename, encoding="utf-8") as input_file:
        return input_file.read()


@maybe
def parse_into_beautiful_soup_html(
        text: Union[str, Error],
) -> Union[Error, bs4.BeautifulSoup]:
    return bs4.BeautifulSoup(text, "html.parser")


def get_paragraph_spans(paragraph: bs4.element.Tag) -> List[TextBlock]:
    if not paragraph.text.strip():
        return []

    return [TextBlock(span.text, span['style'])
            for span in paragraph.find_all('span')]


@maybe
def get_page_blocks(
        name: str,
        force_reread: bool = False,
) -> Union[List[TextBlock], Error]:
    cache_file_name = f'{name}_pickle.obj'
    if os.path.isfile(cache_file_name) and not force_reread:
        try:
            return pickle.loads(open(cache_file_name, 'rb').read())
        except (TypeError, EOFError):
            pass
    initial_html_file_name = f"./{name}.html"
    file_text = get_file_text(initial_html_file_name)
    # I found no way to pickle soup object due to high level of recursion
    print('Starting parsing html')
    soup = parse_into_beautiful_soup_html(file_text)
    print('Parsing html done')
    paragraphs: list = soup.find_all('div')
    spans_lists = map(get_paragraph_spans, paragraphs)
    page_blocks = list((item for t in spans_lists for item in t))
    open(cache_file_name, 'wb').write(pickle.dumps(page_blocks))
    return page_blocks


def is_block_a_header(text_block: TextBlock):
    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    # if font_family == 'YGSRYS':
    #     return True
    if (font_family, font_size) in \
            (
                    # ('WCDQSB', 12),
                    ("YGSRYS", 28),
                    ("YGSRYS", 20),
            ):
        return True
    return False


def is_block_a_normal_text(text_block: TextBlock):
    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    if (font_family, font_size) in \
            (
                    ("SXQHSE", 11),
                    ("EFQWEG", 105),
                    ("LKERYS", 11),

            ):
        return True
    return False


def is_block_an_itallic(text_block: TextBlock):
    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    if (font_family, font_size) in \
            (
                    ("KGULKU", 11),

            ):
        return True
    return False


def is_block_should_be_completely_ignored(text_block: TextBlock):
    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    if isinstance(font_family, Error) or isinstance(font_size, Error):
        return True
    if font_family == 'GARIGC' and text_block.text.strip() == '-':
        return True
    if font_family == 'TWFNGC' and font_size == 10:  # new page
        return True
    if font_family == 'YGSRYS' and font_size == 28:  # out of text header
        return True
    if is_block_a_normal_text(text_block) and text_block.text.strip() == '-':
        return True
    return False


def is_block_an_annotation(text_block: TextBlock):
    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    if (font_family, font_size) in \
            (
                    ("FBHCSE", 10),

            ):
        return True
    return False


def is_block_is_bold(text_block: TextBlock):
    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    if (font_family, font_size) in \
            (
                    ("WCDQSB", 12),

            ):
        return True
    return False


def is_new_normal_block_started(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if is_block_a_header(previous_block) and \
            not is_block_a_header(current_block):
        return True
    return False


def is_new_bold_block_started(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if not is_block_is_bold(previous_block) and is_block_is_bold(current_block):
        return True
    return False


def is_bold_block_ended(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if is_block_is_bold(previous_block) and not is_block_is_bold(current_block):
        return True
    return False


def is_new_italic_block_started(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if not is_block_an_itallic(previous_block) and \
            is_block_an_itallic(current_block):
        return True
    return False


def is_italic_block_ended(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if is_block_an_itallic(previous_block) and \
            not is_block_an_itallic(current_block):
        return True
    return False


def is_normal_text_block_ended(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if not is_block_a_header(previous_block) and \
            is_block_a_header(current_block):
        return True
    return False


def is_header_block_started(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if not is_block_a_header(previous_block) and \
            is_block_a_header(current_block):
        return True
    return False


def is_header_block_ended(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> bool:
    if is_block_a_header(previous_block) and \
            not is_block_a_header(current_block):
        return True
    return False


def transform_text(
        current_text: str,
        previous_text: str,
) -> str:
    text_to_return = current_text

    # text_to_return = text_to_return.strip()
    if delete_leading_and_ending_tags(previous_text).endswith('.\n'):
        text_to_return = '.' + text_to_return

    text_to_return = text_to_return.replace('\n', '')
    text_to_return = restich_string(text_to_return)
    if delete_leading_and_ending_tags(previous_text).endswith('.\n') and \
            text_to_return.startswith('.'):
        text_to_return = text_to_return[1:]
    # if not text_to_return.endswith(' '):
    #     text_to_return += ' '

    return text_to_return


def delete_leading_and_ending_tags(string):
    return re.sub(r'(</?.+?>)+', '', string)


def restich_string(input_string: str) -> str:
    return re.sub(r'(\.)([А-Я])+', r'\g<1></p><p>\g<2>', input_string)


def reduce_text_blocks(acc: Accumulator, current_block: TextBlock):
    acc.current_text_block_number += 1

    new_page = is_page_block_a_page_number(
            current_block,
            "TWFNGC",
            10,
    )
    if new_page:
        acc.current_page = new_page

    if is_block_should_be_completely_ignored(current_block):
        return acc

    # This is specific for Tomb of Anihilation
    if current_block.text.strip() == 'Ч' \
            and get_font_size(current_block.style) == 105:
        acc.current_page = 5
        acc.book_started = True

    if acc.book_started is False:  # do nothing until book starts
        return acc

    print('-----------------------------------------------------------------')
    print(current_block)
    print(f'At page: {acc.current_page}')

    text_to_be_added = ''
    previous_text = acc.previous_block.text

    if is_normal_text_block_ended(acc.previous_block, current_block):
        text_to_be_added += '</p>'

    if is_header_block_ended(acc.previous_block, current_block):
        text_to_be_added += '</h>'

    # if is_italic_block_ended(acc.previous_block, current_block):
    #     text_to_be_added += '</i>'
    #
    # if is_bold_block_ended(acc.previous_block, current_block):
    #     text_to_be_added += '</b>'

    if is_header_block_started(acc.previous_block, current_block):
        text_to_be_added += '<h>'

    if is_new_normal_block_started(acc.previous_block, current_block):
        text_to_be_added += '<p>'

    # if is_new_bold_block_started(acc.previous_block, current_block):
    #     text_to_be_added += '<b>'
    #
    # if is_new_italic_block_started(acc.previous_block, current_block):
    #     text_to_be_added += '<i>'

    text_to_be_added += current_block.text
    acc.current_article_text += transform_text(text_to_be_added, previous_text)

    acc.previous_font_family = get_font_family(current_block.style)
    acc.previous_font_size = get_font_size(current_block.style)

    # if is_block_a_header(current_block):
    #     acc.previous_block_type = 'Header'
    # else:
    #     acc.previous_block_type = 'Normal'

    acc.previous_block = current_block
    return acc


if __name__ == '__main__':
    module_name = "tomb_exported"
    text_blocks = get_page_blocks(module_name)
    articles = functools.reduce(
            reduce_text_blocks,
            text_blocks,
            Accumulator([]),
    )
    articles.current_article_text += '</p>'
    print(articles)

    with open('stories.obj', 'wb') as f:
        f.write(pickle.dumps(articles.current_article_text))
