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

from dataclasses import dataclass, field
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


def get_font_family(style_string: str) -> str:
    tokens = re.findall("font-family: b\\'(.+)\\'",
                        style_string)
    if not tokens or len(tokens) < 1:
        return ''
    return tokens[0]


def get_font_size(style_string: str) -> int:
    tokens = re.findall("font-family: b'(.+)\+.+font-size:(\d+)px",
                        style_string)
    if not tokens or len(tokens) != 1 or len(tokens[0]) != 2:
        return 0

    return int(tokens[0][1])


@dataclass
class TextBlock:
    text: str
    style: str
    is_starting_block: bool = False

    def __repr__(self):
        font_family = get_font_family(self.style)
        font_size = get_font_size(self.style)
        return f'("{font_family}", {font_size}),\nText:\n{self.text}'


@dataclass
class Accumulator:
    articles: List[str]
    current_page: int = 0
    previous_block: TextBlock = TextBlock('', '')
    preprevious_block: TextBlock = TextBlock('', '')
    # book_started: bool = False
    current_article_text: str = ''
    current_text_block_number: int = 0
    temporary_article: str = ''
    debug: bool = False
    currently_open_tags: list = field(default_factory=list)


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


def get_text_from_block(
        previous_block: TextBlock,
        current_block: TextBlock,
) -> str:
    if current_block.text.strip() == '-' and \
            not previous_block.text.endswith(' '):
        return ''
    if current_block.text == '\n' and not previous_block.text.endswith(' '):
        return ' '
    return current_block.text

#
# def close_opened_tags(tags_list: List[str]) -> str:
#     return ''.join([f'</{t}>' for t in tags_list[::-1]])
#
#
# def is_block_should_be_completely_ignored(text_block: TextBlock):
#     if isinstance(text_block, Error):
#         return False
#
#     font_family = get_font_family(text_block.style)
#     font_size = get_font_size(text_block.style)
#     if isinstance(font_family, Error) or isinstance(font_size, Error):
#         return True
#     if font_family in (
#             "GARIGC+Mookmania-Italic",
#             "TANMCH+OpenSans",
#             "UISOUA+OpenSans-Bold",
#     ) and \
#             text_block.text.strip() == '-':
#         return True
#     if font_family == "TWFNGC+Mr.NigaSmallCaps" and font_size == 10# new page
#         return True
#     # if font_family == 'YGSRYS' and font_size == 28:  # out of text header
#     #     return True
#     return False
#
#
# def is_block_a_normal_text(text_block: TextBlock):
#     if isinstance(text_block, Error):
#         return False
#
#     font_family = get_font_family(text_block.style)
#     font_size = get_font_size(text_block.style)
#     if (font_family, font_size) in \
#             (
#                     ("EFQWEG+VictorianGothicThree", 105),
#                     ("LKERYS+Mookmania", 11),
#                     ("EPUBEG+OpenSans-Bold-SC700", 24),
#                     ("EPUBEG+OpenSans-Bold-SC700", 17),
#                     ("TEDIGC+OpenSans-Light", 11),
#                     ("TANMCH+OpenSans", 10),
#                     ("SXQHSE+Mookmania", 11),
#                     ("VDMYED+OpenSans-Bold", 12),
#                     ("KGULKU+Mookmania-Italic", 11),
#                     ("WCDQSB+Mookmania-Bold", 12),
#             ):
#         return True
#     return False
#
#
# def should_start_new_paragraph(
#         previous_block: TextBlock,
#         current_block: TextBlock,
#         currently_opened_tags: List[str],
# ):
#     if 'frame' in currently_opened_tags:
#         return False
#
#     current_font_family = get_font_family(current_block.style)
#     current_font_size = get_font_size(current_block.style)
#     if (current_font_family, current_font_size) in (
#             ("VDMYED+OpenSans-Bold", 10),
#             ("EFQWEG+VictorianGothicThree", 105),
#             # ("WCDQSB+Mookmania-Bold", 12),
#     ) and is_previous_block_font_differs_from_current(
#             previous_block,
#             current_block,
#     ):
#         return True
#
#     if re.findall(r'\.\.\d+', previous_block.text):
#         return True
#
#     # if '•' in current_block.text:
#     #     return True
#
#     return False
#
#
# def is_previous_block_font_differs_from_current(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ):
#     if get_font_family(previous_block.style) == \
#             get_font_family(current_block.style) and \
#             get_font_size(previous_block.style) == \
#             get_font_size(current_block.style):
#         return False
#     return True
#
#
# def is_normal_block_started(
#         previous_block: TextBlock,
#         current_block: TextBlock,
#         preprevious_block: TextBlock,
#         currently_opened_tags: List[str]
# ) -> bool:
#     # if not is_block_a_normal_text(previous_block) and \
#     #         is_block_a_normal_text(current_block):
#
#     if previous_block.is_starting_block and \
#             not is_header_block(current_block):
#         return True
#
#     if is_block_a_normal_text(current_block) and 'p' in currently_opened_tags:
#         return False
#
#     # if 'frame' in currently_opened_tags:
#     #     return False
#
#     if (is_header_block(previous_block) or
#         is_aloud_block(preprevious_block, previous_block)) and \
#             is_block_a_normal_text(current_block):
#         return True
#
#     # if is_block_a_normal_text(current_block) and \
#     #         is_previous_block_font_differs_from_current(
#     #                 previous_block, current_block):
#     #     return True
#
#     return False
#
#
# def is_normal_block_ended(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ) -> bool:
#     if not is_header_block(previous_block) and \
#             is_header_block(current_block):
#         return True
#     return False
#
#
# def is_bold_block(text_block: TextBlock):
#     if isinstance(text_block, Error):
#         return False
#
#     font_family = get_font_family(text_block.style)
#     if 'bold' in font_family.lower():
#         return True
#     # font_size = get_font_size(text_block.style)
#     # if (font_family, font_size) in \
#     #         (
#     #                 ("WCDQSB", 12),
#     #                 # ("TANMCH", 10),
#     #                 ("VDMYED", 12),
#     #                 ("VDMYED", 10),
#     #
#     #         ):
#     #     return True
#     return False
#
#
# def is_bold_block_started(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ) -> bool:
#     if not is_bold_block(previous_block) and is_bold_block(current_block):
#         return True
#     return False
#
#
# def is_bold_block_ended(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ) -> bool:
#     if is_bold_block(previous_block) and not is_bold_block(current_block):
#         return True
#     return False
#
#
# def is_italic_block(text_block: TextBlock):
#     if isinstance(text_block, Error):
#         return False
#
#     font_family = get_font_family(text_block.style)
#     if 'italic' in font_family.lower():
#         return True
#     # font_size = get_font_size(text_block.style)
#     # if (font_family, font_size) in \
#     #         (
#     #                 ("KGULKU", 11),
#     #                 ("MWRSMQ", 9),
#     #
#     #         ):
#     return False
#
#
# def is_italic_block_started(
#         previous_block: TextBlock,
#         current_block: TextBlock,
#         # currently_opened_tags: List[str],
# ) -> bool:
#     # if 'b' in currently_opened_tags:
#     #     return False
#
#     if not is_italic_block(previous_block) and \
#             is_italic_block(current_block):
#         return True
#     return False
#
#
# def is_italic_block_ended(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ) -> bool:
#     if is_italic_block(previous_block) and \
#             not is_italic_block(current_block):
#         return True
#     return False
#
#
# def is_aloud_block(previous_block: TextBlock, current_block: TextBlock):
#     current_font = get_font_family(current_block.style)
#     if current_font not in ('FBHCSE+OpenSans',):
#         return False
#
#     previous_font = get_font_family(previous_block.style)
#     if previous_font not in ('SXQHSE+Mookmania',
#                              '',
#                              'EPUBEG+OpenSans-Bold-SC700',
#                              'FBHCSE+OpenSans',
#                              ):
#         return False
#     return True
#
#
# def is_aloud_block_started(
#         previous_block: TextBlock,
#         current_block: TextBlock,
#         preprevious_block: TextBlock,
#         currently_opened_tags: List[str],
# ) -> bool:
#     if is_aloud_block(previous_block, current_block) and \
#             'frame' in currently_opened_tags:
#         return False
#     if not is_aloud_block(preprevious_block, previous_block) and \
#             is_aloud_block(previous_block, current_block):
#         return True
#     return False
#
#
# def is_aloud_block_ended(
#         previous_block: TextBlock,
#         current_block: TextBlock,
#         preprevious_block: TextBlock
# ) -> bool:
#     if is_aloud_block(preprevious_block, previous_block) and \
#             not is_aloud_block(previous_block, current_block):
#         return True
#     return False
#
#
# def is_header_block(text_block: TextBlock):
#     if isinstance(text_block, Error):
#         return False
#
#     font_family = get_font_family(text_block.style)
#     font_size = get_font_size(text_block.style)
#
#     if (font_family, font_size) in \
#             (
#                     ("FTEHSE+NodestoCyrillic", 55),
#                     ("YGSRYS+Mr.NigaSmallCaps", 28),
#                     ("FTEHSE+NodestoCyrillic", 54),
#                     ("YGSRYS+Mr.NigaSmallCaps", 15),
#                     ("YGSRYS+Mr.NigaSmallCaps", 20),
#                     ("YGSRYS+Mr.NigaSmallCaps", 13),
#             ):
#         return True
#     return False
#
#
# def is_header_block_started(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ) -> bool:
#     if (not is_header_block(previous_block) or
#         previous_block.is_starting_block) and \
#             is_header_block(current_block):
#         return True
#     return False
#
#
# def is_header_block_ended(
#         previous_block: TextBlock,
#         current_block: TextBlock,
# ) -> bool:
#     if is_header_block(previous_block) and \
#             not is_header_block(current_block):
#         return True
#     return False


def close_opened_tags(tags_list: List[str]) -> str:
    return ''.join([f'</{t}>' for t in tags_list[::-1]])


def normalize_word(word: str) -> str:
    stripped_word = word.strip()
    if len(stripped_word) < 3:
        return word

    first_letter = word.lstrip()[0]
    last_part = word.split(first_letter)[1].lower()
    before_first_letter = word.split(first_letter)[0]
    return f'{before_first_letter}{first_letter}{last_part}'


def transform_text(
        current_text: str,
        previous_text: str,
        # currently_opened_tags: List[str]
) -> str:
    text_to_return = current_text

    # text_to_return = text_to_return.strip()
    if delete_leading_and_ending_tags(previous_text).endswith('.\n'):
        text_to_return = '.' + text_to_return

    text_to_return = text_to_return.replace('\n', '')
    # if 'frame' not in currently_opened_tags:
    text_to_return = text_to_return.replace('•', '*•')
    text_to_return = restich_string(text_to_return)
    if delete_leading_and_ending_tags(previous_text).endswith('.\n') and \
            text_to_return.startswith('.'):
        text_to_return = text_to_return[1:]

    if text_to_return.strip().isdecimal():
        text_to_return = f'*{text_to_return} '

    # words = delete_leading_and_ending_tags(text_to_return).split(' ')
    # normalized_words = ' '.join(map(normalize_word, words))
    # text_to_return = text_to_return.replace(
    #         delete_leading_and_ending_tags(text_to_return),
    #         normalized_words)

    return text_to_return


def delete_leading_and_ending_tags(string):
    return re.sub(r'(</?.+?>)+', '', string)


def restich_string(input_string: str) -> str:
    return re.sub(r'(\.)([А-Я])+', r'\g<1>*\g<2>', input_string)

#
# def reduce_text_blocks(acc: Accumulator, current_block: TextBlock):
#     acc.current_text_block_number += 1
#
#     new_page = is_page_block_a_page_number(
#             current_block,
#             "TWFNGC",
#             10,
#     )
#     if new_page:
#         acc.current_page = new_page
#
#     if is_block_should_be_completely_ignored(current_block):
#         return acc
#
#     text_to_be_added = ''
#
#     if is_italic_block_ended(acc.previous_block, current_block):
#         text_to_be_added += '</i>'
#         acc.currently_open_tags = list(filter(
#                 lambda x: x != 'i', acc.currently_open_tags))
#
#     if is_bold_block_ended(acc.previous_block, current_block):
#         text_to_be_added += '</b>'
#         acc.currently_open_tags = list(filter(
#                 lambda x: x != 'b', acc.currently_open_tags))
#
#     if is_header_block_started(acc.previous_block, current_block):
#         text_to_be_added += close_opened_tags(acc.currently_open_tags)
#         text_to_be_added += '<h>'
#         acc.currently_open_tags = ['h', ]
#
#     if is_normal_block_started(
#             acc.previous_block,
#             current_block,
#             acc.preprevious_block,
#             acc.currently_open_tags,
#     ):
#         text_to_be_added += close_opened_tags(acc.currently_open_tags)
#         text_to_be_added += '<p>'
#         acc.currently_open_tags = ['p', ]
#
#     if should_start_new_paragraph(
#             acc.previous_block,
#             current_block,
#             acc.currently_open_tags
#     ):
#         text_to_be_added += close_opened_tags(acc.currently_open_tags)
#         text_to_be_added += '<p>'
#         acc.currently_open_tags = ['p', ]
#
#     if is_aloud_block_started(
#             acc.previous_block,
#             current_block,
#             acc.preprevious_block,
#             acc.currently_open_tags,
#     ):
#         # if acc.currently_open_tags:
#         #     text_to_be_added += close_opened_tags(acc.currently_open_tags)
#         text_to_be_added += '<frame>'
#         acc.currently_open_tags.append('frame')
#
#     if is_bold_block_started(acc.previous_block, current_block):
#         text_to_be_added += '<b>'
#         acc.currently_open_tags.append('b')
#
#     if is_italic_block_started(
#             acc.previous_block, current_block):
#         text_to_be_added += '<i>'
#         acc.currently_open_tags.append('i')
#
#     text_to_be_added += get_text_from_block(acc.previous_block, current_block)
#     acc.current_article_text += transform_text(
#             text_to_be_added,
#             acc.previous_block.text,
#             # acc.currently_open_tags
#     )
#
#     if acc.debug:
#         print(current_block)
#         print(f'Block number: {acc.current_text_block_number}')
#         print(f'Currently opened tags: {acc.currently_open_tags}')
#         print('\n\n')
#         # print(f'At page: {acc.current_page}')
#
#     acc.preprevious_block = acc.previous_block
#     acc.previous_block = current_block
#     return acc


def get_block_tag(
        *,
        current_block: TextBlock,
        previous_block: TextBlock,
) -> str:
    current_font_family = get_font_family(current_block.style)
    current_font_size = get_font_size(current_block.style)
    if (current_font_family, current_font_size) in \
            (
                    ("FTEHSE+NodestoCyrillic", 55),
                    ("YGSRYS+Mr.NigaSmallCaps", 28),
                    ("FTEHSE+NodestoCyrillic", 54),
                    ("YGSRYS+Mr.NigaSmallCaps", 15),
                    ("YGSRYS+Mr.NigaSmallCaps", 20),
                    ("YGSRYS+Mr.NigaSmallCaps", 13),
                    ("EPUBEG+OpenSans-Bold-SC700", 11),
                    ("EPUBEG+OpenSans-Bold-SC700", 16),
            ):
        return 'h'

    if 'italic' in current_font_family.lower():
        return 'i'

    if 'bold' in current_font_family.lower():
        return 'b'

    previous_font_family = get_font_family(previous_block.style)

    frame_styles = ('SXQHSE+Mookmania', 'EPUBEG+OpenSans-Bold-SC700',
                    'FBHCSE+OpenSans', )

    if previous_font_family in frame_styles + ('', ) and \
            current_font_family in frame_styles:
        return 'frame'

    return 'p'  # normal text paragraph


def blocks_font_the_same(block1: TextBlock, block2: TextBlock):
    block1_font_family = get_font_family(block1.style)
    block2_font_family = get_font_family(block2.style)
    block1_font_size = get_font_size(block1.style)
    block2_font_size = get_font_size(block2.style)

    if block1_font_family != block2_font_family:
        return False
    if block1_font_size != block2_font_size:
        return False
    return True


def should_open_new_tag(
        *,
        previously_opened_tags: List[str],
        previous_block: TextBlock,
        current_block: TextBlock,
        preprevious_block: TextBlock,
):
    # assuming that previous font and current font are different
    if len(previously_opened_tags) == 0:
        return True

    current_block_tag = get_block_tag(current_block=current_block,
                                      previous_block=previous_block)
    current_font_family = get_font_family(current_block.style)
    previous_font_family = get_font_family(previous_block.style)
    previous_block_tag = get_block_tag(current_block=previous_block,
                                       previous_block=preprevious_block)

    if current_block_tag == previous_block_tag and \
            current_font_family == previous_font_family:
        return False

    if current_block_tag == 'h':
        return True

    if current_block_tag == 'p':
        return True

    if current_block_tag == 'b':
        if 'b' not in previously_opened_tags:
            return True

    if current_block_tag == 'i':
        if 'i' not in previously_opened_tags:
            return True

    if current_block_tag == 'frame':
        if 'frame' not in previously_opened_tags:
            return True

    return False


def tags_should_be_closed(
        currently_openning_tag: str,
        # previously_opened_tags: List[str],
) -> List[str]:
    if currently_openning_tag == 'h':
        return ['h', 'p', 'i', 'b', 'frame']

    if currently_openning_tag == 'p':
        return ['h', 'p', 'i', 'b', 'frame']

    if currently_openning_tag == 'b':
        return ['b', 'h']

    if currently_openning_tag == 'i':
        return ['i', 'h']

    if currently_openning_tag == 'frame':
        return ['h', 'p', 'i', 'b', 'frame']

    return []


def reduce_text_blocks2(acc: Accumulator, current_block: TextBlock):
    acc.current_text_block_number += 1
    current_tag = get_block_tag(
            current_block=current_block,
            previous_block=acc.previous_block,
    )
    text_to_add = ''

    if not blocks_font_the_same(current_block, acc.previous_block):
        if should_open_new_tag(
                previously_opened_tags=acc.currently_open_tags,
                previous_block=acc.previous_block,
                preprevious_block=acc.preprevious_block,
                current_block=current_block,
        ):
            tags_to_be_closed = tags_should_be_closed(
                    current_tag,
                    # acc.currently_open_tags,
            )

            for tag in acc.currently_open_tags[::-1]:
                if tag in tags_to_be_closed:
                    acc.currently_open_tags.remove(tag)
                    text_to_add += f'</{tag}>'

            if current_tag in ('b', 'i') and 'p' not in acc.currently_open_tags:
                acc.currently_open_tags.append('p')
                text_to_add += '<p>'

            acc.currently_open_tags.append(current_tag)
            text_to_add += f'<{current_tag}>'
            # print(f'New tag should be opened: {current_tag}')

    text_to_add += get_text_from_block(acc.previous_block, current_block)
    acc.current_article_text += transform_text(
            text_to_add,
            acc.previous_block.text,
    )

    if acc.debug:
        print(current_block)
        print(f'Block number: {acc.current_text_block_number}')
        print(f'Currently opened tags: {acc.currently_open_tags}')
        print('\n\n')

    acc.preprevious_block = acc.previous_block
    acc.previous_block = current_block
    return acc


@maybe
def get_stories(
        mod_name: str,
        blocks_from_to: tuple = (),
        debug: bool = False,
) -> List[str]:
    text_blocks = get_page_blocks(mod_name)
    if blocks_from_to:
        text_blocks = text_blocks[blocks_from_to[0]:blocks_from_to[1]]

    articles = functools.reduce(
            reduce_text_blocks2,
            text_blocks,
            Accumulator(
                    [],
                    debug=debug,
                    previous_block=TextBlock('', '', is_starting_block=True),
                    preprevious_block=TextBlock('', '', is_starting_block=True),
            ),
    )
    # if articles.current_article_text and \
    #         not articles.current_article_text.startswith('<p>'):
    #     articles.current_article_text = '<p>' + articles.current_article_text
    #
    # if articles.current_article_text \
    #         and not articles.current_article_text.endswith('</p>'):
    #     articles.current_article_text += '</p>'

    articles.current_article_text += close_opened_tags(
            articles.currently_open_tags)
    articles.articles.append(articles.current_article_text)
    return articles.articles


if __name__ == '__main__':
    print(get_stories("tomb_exported", (0, 300), debug=True)[0])
    # with open('stories.obj', 'wb') as f:
    #     f.write(pickle.dumps(get_stories("tomb_exported")))
