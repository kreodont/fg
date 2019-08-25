"""
This module is intended for converting HTML file resulted from pdfminer into
Fantasy Ground module structure
python C:\\Users\\Dima\\pdfminer.six\\tools\\pdf2txt.py -o tomb_exported.html
"C:\\YandexDisk\\DnD\\Гробница Аннигиляции.pdf"
Result - object file with list of Fantasy Grounds formatted text
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
    current_page: int
    previous_font_family: str
    previous_font_size: int
    previous_block_type: str = 'null'
    book_started: bool = False
    current_article_text: str = ''


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
    initial_html_file_name = f"./{module_name}.html"
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
    if font_family == 'YGSRYS':
        return True
    if (font_family, font_size) in \
            (
                    ('WCDQSB', 12),
                    # ("YGSRYS", 28),
                    # ("YGSRYS", 20),
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
        previous_block_type: str,
        current_block: TextBlock,
) -> bool:
    if previous_block_type in ('Header', 'null') and \
            not is_block_a_header(current_block):
        return True
    return False


def is_normal_text_block_ended(
        previous_block_type: str,
        current_block: TextBlock,
) -> bool:
    if previous_block_type == 'Normal' and is_block_a_header(current_block):
        return True
    return False


def is_header_block_started(
        previous_block_type: str,
        current_block: TextBlock,
) -> bool:
    if previous_block_type in ('Normal', 'null') and \
            is_block_a_header(current_block):
        return True
    return False


def is_header_block_ended(
        previous_block_type: str,
        current_block: TextBlock,
) -> bool:
    if previous_block_type == 'Header' and not is_block_a_header(current_block):
        return True
    return False


def handle_normal_text(text_block: TextBlock) -> str:
    text_to_return = text_block.text
    text_to_return = text_to_return.strip()
    text_to_return = text_to_return.replace('\n', '')
    # if not text_to_return.endswith(' '):
    #     text_to_return += ' '

    return text_to_return


def reduce_text_blocks(accumulator: Accumulator, next_block: TextBlock):
    if is_block_should_be_completely_ignored(next_block):
        return accumulator

    new_page = is_page_block_a_page_number(
            next_block,
            "TWFNGC",
            10,
    )
    if new_page:
        accumulator.current_page = new_page

    # This is specific for Tomb of Anihilation
    if next_block.text.strip() == 'Ч' \
            and get_font_size(next_block.style) == 105:
        accumulator.current_page = 5
        accumulator.book_started = True

    if accumulator.book_started is False:  # do nothing until book starts
        return accumulator

    print('-----------------------------------------------------------------')
    print(next_block)
    print(f'At page: {accumulator.current_page}')

    if is_new_normal_block_started(accumulator.previous_block_type, next_block):
        accumulator.current_article_text += '<p>'

    if is_normal_text_block_ended(accumulator.previous_block_type, next_block):
        accumulator.current_article_text += '</p>\r\n'

    if is_header_block_started(accumulator.previous_block_type, next_block):
        accumulator.current_article_text += '<h>'

    if is_header_block_ended(accumulator.previous_block_type, next_block):
        accumulator.current_article_text += '</h>\r\n'

    accumulator.current_article_text += handle_normal_text(next_block)

    accumulator.previous_font_family = get_font_family(next_block.style)
    accumulator.previous_font_size = get_font_size(next_block.style)
    if is_block_a_header(next_block):
        accumulator.previous_block_type = 'Header'
    else:
        accumulator.previous_block_type = 'Normal'

    return accumulator


if __name__ == '__main__':
    module_name = "tomb_exported"
    text_blocks = get_page_blocks(module_name)
    articles = functools.reduce(
            reduce_text_blocks,
            text_blocks,
            Accumulator([], 0, '', 0),
    )
    print(articles)
