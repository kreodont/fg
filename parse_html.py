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
        return style_string
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
    start_next_paragraph_when_font_changes: bool = False
    # book_started: bool = False
    current_article_text: str = ''
    current_text_block_number: int = 0
    temporary_article: str = ''
    debug: bool = False
    currently_open_tags: list = field(default_factory=list)


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
    # if not paragraph.text.strip():
    #     return [TextBlock('', paragraph['style'])]

    spans = [TextBlock(span.text, span['style']) for
             span in paragraph.find_all('span')]
    if not spans:
        return [TextBlock(paragraph.text, paragraph['style']), ]
    return spans
    # return [TextBlock(span.text, span['style'])
    #         for span in paragraph.find_all('span')]


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


def is_block_should_be_completely_ignored(
        text_block: TextBlock,
        previous_block: TextBlock):

    if isinstance(text_block, Error):
        return False

    font_family = get_font_family(text_block.style)
    font_size = get_font_size(text_block.style)
    previous_font_size = get_font_size(previous_block.style)
    # if font_size == 0:
    #     return True
    if isinstance(font_family, Error) or isinstance(font_size, Error):
        return True
    if font_family in (
            "GARIGC+Mookmania-Italic",
            "TANMCH+OpenSans",
            "UISOUA+OpenSans-Bold",
            "LKERYS+Mookmania",
            "IQTUIY+OpenSansLight-Italic",
    ) and text_block.text.strip() == '-':
        return True
    if font_family == "TWFNGC+Mr.NigaSmallCaps" and font_size == 10:  # new page
        return True
    if (font_family, font_size) in (
            # ("YGSRYS+Mr.NigaSmallCaps", 28),
            ("YGSRYS+Mr.NigaSmallCaps", 9),
    ):
        return True

    if (font_family, font_size) in (
            ("YGSRYS+Mr.NigaSmallCaps", 28),
    ) and previous_font_size == 0:
        return True

    return False


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
    if isinstance(current_text, Error):
        return ''
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

    # Put new line before every number which is single paragraph
    if text_to_return.strip().isdecimal():
        text_to_return = f'*{text_to_return}'

    if len(delete_leading_and_ending_tags(current_text)) > 0 \
            and delete_leading_and_ending_tags(current_text)[0].isdecimal():
        text_to_return = f'*{text_to_return}'

    # if len(text_to_return.strip()) > 0 and
    # text_to_return.strip()[0].isdecimal():
    #     text_to_return = f'*{text_to_return}'

    return text_to_return


def delete_leading_and_ending_tags(string):
    return re.sub(r'(</?.+?>)+', '', string)


def restich_string(input_string: str) -> str:
    return re.sub(r'(\.)([А-Я])+', r'\g<1>*\g<2>', input_string)


def get_block_tag(
        *,
        current_block: TextBlock,
        # previous_block: TextBlock,
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
                    # ("VDMYED+OpenSans-Bold", 12),
            ):
        return 'h'

    if 'italic' in current_font_family.lower():
        return 'i'

    if 'bold' in current_font_family.lower():
        return 'b'

    # previous_font_family = get_font_family(previous_block.style)

    # frame_styles = ('SXQHSE+Mookmania', 'EPUBEG+OpenSans-Bold-SC700',
    #                 'FBHCSE+OpenSans', )
    #
    # if previous_font_family in frame_styles + ('', ) and \
    #         current_font_family in frame_styles:
    #     return 'frame'

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


def tags_should_be_closed(
        *,
        currently_openning_tag: str,
        current_block: TextBlock,
        previous_block: TextBlock,
        previously_opened_tags: List[str],
) -> List[str]:
    current_font_family = get_font_family(current_block.style)
    previous_font_family = get_font_family(previous_block.style)
    previous_block_tag = get_block_tag(current_block=previous_block)

    if currently_openning_tag == previous_block_tag and \
            current_font_family == previous_font_family:
        return []

    if currently_openning_tag == 'b':
        return ['b']

    if currently_openning_tag == 'i':
        if previously_opened_tags and previously_opened_tags[-1] == 'b':
            return ['b', 'i']
        return ['i']

    if currently_openning_tag in ('p', 'h'):
        return ['b', 'i']

    # if currently_openning_tag == 'frame':
    #     return ['i', 'b', 'frame']

    return []


def open_p_paragraph(currently_opened_tags: List[str]) -> List[str]:
    return [f'</{tag}>' for tag in currently_opened_tags[::-1]] + ['<p>', ]


def open_header(currently_opened_tags: List[str]):
    return [f'</{tag}>' for tag in currently_opened_tags[::-1]] + ['<h>', ]


def tags_should_be_opened(
        *,
        current_tag: str,
        previously_opened_tags: List[str],
        current_block: TextBlock,
        previous_block: TextBlock,
        acc: Accumulator,
) -> List[str]:
    current_font_family = get_font_family(current_block.style)
    current_font_size = get_font_size(current_block.style)

    previous_font_family = get_font_family(previous_block.style)
    previous_font_size = get_font_size(previous_block.style)
    previous_block_tag = get_block_tag(current_block=previous_block)
    if current_tag == previous_block_tag and \
            current_font_family == previous_font_family:
        return []

    if (current_font_family, current_font_size) == \
            ("FBHCSE+OpenSans", 10) and \
            (previous_font_family, previous_font_size) not in  \
            (
                    ("FBHCSE+OpenSans", 10),
                    ("VDMYED+OpenSans-Bold", 10),
                    ("OXHEKR+OpenSans-Italic", 10),
                    ("TANMCH+OpenSans", 10),
            ):
        acc.start_next_paragraph_when_font_changes = True
        return ['frame', ]

    if current_tag in ('b', 'i'):
        if current_tag in previously_opened_tags:
            return []
        elif 'p' not in previously_opened_tags:
            return ['p', current_tag]
        else:
            return [current_tag, ]

    return []


def new_header_should_be_started(current_block, previous_block) -> bool:
    if previous_block.is_starting_block and \
            get_block_tag(current_block=current_block) == 'h':
        return True

    if get_block_tag(current_block=current_block) == 'h' and \
            get_block_tag(current_block=previous_block) != 'h':
        return True

    return False


def new_paragraph_should_be_started(current_block, previous_block, acc) -> bool:
    current_tag = get_block_tag(current_block=current_block)
    previous_tag = get_block_tag(current_block=previous_block)
    previous_font_family = get_font_family(previous_block.style)
    previous_font_size = get_font_size(previous_block.style)
    current_font_family = get_font_family(current_block.style)
    current_font_size = get_font_size(current_block.style)

    if previous_block.is_starting_block and current_tag != 'h':
        return True

    if previous_tag == 'h' and current_tag != 'h':
        return True

    if (current_font_family, current_font_size) == \
            ("EFQWEG+VictorianGothicThree", 105):
        return True

    if (current_font_family, current_font_size) == \
            ("VDMYED+OpenSans-Bold", 10) and \
            (previous_font_family, previous_font_size) != \
            ("VDMYED+OpenSans-Bold", 10):
        return True

    if (current_font_family, current_font_size) == \
            ("WCDQSB+Mookmania-Bold", 12):
        text = current_block.text.strip()
        if len(text) > 0 and text[0].isdecimal():
            return True

    if (current_font_family, current_font_size) == \
            ("MWRSMQ+OpenSansLight-Italic", 9) and \
            (previous_font_family, previous_font_size) != \
            ("MWRSMQ+OpenSansLight-Italic", 9):
        acc.start_next_paragraph_when_font_changes = True
        return True

    return False


def reduce_text_blocks2(acc: Accumulator, current_block: TextBlock):
    acc.current_text_block_number += 1
    current_tag = get_block_tag(
            current_block=current_block,
            # previous_block=acc.previous_block,
    )
    text_to_add = ''

    if acc.debug:
        print(current_block)
        print(f'Block number: {acc.current_text_block_number}')

    if is_block_should_be_completely_ignored(current_block, acc.previous_block):
        return acc

    if not blocks_font_the_same(current_block, acc.previous_block):
        if new_header_should_be_started(current_block, acc.previous_block):
            text_to_add = ''.join(open_header(acc.currently_open_tags))
            acc.currently_open_tags = ['h', ]
        elif new_paragraph_should_be_started(
                current_block,
                acc.previous_block,
                acc):
            text_to_add = ''.join(open_p_paragraph(acc.currently_open_tags))
            acc.currently_open_tags = ['p', ]
        elif acc.start_next_paragraph_when_font_changes:
            text_to_add = ''.join(open_p_paragraph(acc.currently_open_tags))
            acc.currently_open_tags = ['p', ]
            acc.start_next_paragraph_when_font_changes = False

        tags_to_be_closed = tags_should_be_closed(
                currently_openning_tag=current_tag,
                current_block=current_block,
                previous_block=acc.previous_block,
                previously_opened_tags=acc.currently_open_tags,
        )
        for currently_opened_tag in acc.currently_open_tags[::-1]:
            if currently_opened_tag in tags_to_be_closed:
                acc.currently_open_tags.remove(currently_opened_tag)
                text_to_add += f'</{currently_opened_tag}>'

        tags_to_be_opened = tags_should_be_opened(
                current_tag=current_tag,
                previously_opened_tags=acc.currently_open_tags,
                current_block=current_block,
                previous_block=acc.previous_block,
                acc=acc,
        )
        for tag_to_be_opened in tags_to_be_opened:
            acc.currently_open_tags.append(tag_to_be_opened)
            text_to_add += f'<{tag_to_be_opened}>'

        # tags_to_be_closed = tags_should_be_closed(
        #         current_tag,
        #         # acc.currently_open_tags,
        # )
        #
        # for tag in acc.currently_open_tags[::-1]:
        #     if tag in tags_to_be_closed:
        #         acc.currently_open_tags.remove(tag)
        #         text_to_add += f'</{tag}>'
        #
        # if should_open_new_tag(
        #         previously_opened_tags=acc.currently_open_tags,
        #         previous_block=acc.previous_block,
        #         preprevious_block=acc.preprevious_block,
        #         current_block=current_block,
        # ):
        #
        #     if current_tag in ('b', 'i') and 'p' not in
        #     acc.currently_open_tags:
        #         acc.currently_open_tags.append('p')
        #         text_to_add += '<p>'
        #
        #     acc.currently_open_tags.append(current_tag)
        #     text_to_add += f'<{current_tag}>'
        #     # print(f'New tag should be opened: {current_tag}')

    text_to_add += get_text_from_block(acc.previous_block, current_block)
    acc.current_article_text += transform_text(
            text_to_add,
            acc.previous_block.text,
    )

    if acc.debug:
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
    text_blocks = get_page_blocks(mod_name, force_reread=False)
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
    print(get_stories("tomb_exported", (1530, 1600), debug=True)[0])
    # with open('stories.obj', 'wb') as f:
    #     f.write(pickle.dumps(get_stories("tomb_exported")))
