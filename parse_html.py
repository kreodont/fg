"""
This module is intended for converting HTML file resulted from pdfminer into
Fantasy Ground module structure
python C:\\Users\\Dima\\pdfminer.six\\tools\\pdf2txt.py -o Tomb.html
"C:\\YandexDisk\\DnD\\Гробница Аннигиляции.pdf"
Result - object file with list of Fantasy Grounds formatted text
"""
from dataclasses import dataclass
from typing import Union


@dataclass
class Error:
    text: str

    def __repr__(self):
        return f'Error: {self.text}'


def maybe(func):
    def runner(*args, **kwargs):
        for positional_parameter in args:
            if isinstance(positional_parameter, Error):
                return positional_parameter

        for parameter_name in kwargs:
            parameter = kwargs[parameter_name]
            if isinstance(parameter, Error):
                return parameter

        return func(*args, **kwargs)
    return runner


@maybe
def get_file_text(filename: str) -> Union[str, Error]:
    try:
        with open(filename, encoding="utf-8") as input_file:
            return input_file.read()
    except Exception as e:
        return Error(str(e))


if __name__ == '__main__':
    initial_pdf_file_name = "./tomb1.html"
    file_text = get_file_text(initial_pdf_file_name)
    print(file_text)
