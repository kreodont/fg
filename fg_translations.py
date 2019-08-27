import unicodedata
import re


def only_roman_chars(unistr: str) -> bool:
    latin_letters = {}

    def is_latin(uchr):
        try:
            return latin_letters[uchr]
        except KeyError:
            return latin_letters.setdefault(
                    uchr,
                    'LATIN' in unicodedata.name(uchr),
            )

    return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())


def translate_to_iso_codes(text: str) -> str:
    first_letter_code = 192
    all_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
                  'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    result_text = ''

    for char in text:
        if char == 'ё':
            result_text += '&#184;'
        elif char == 'Ё':
            result_text += '&#168;'
        elif char in all_letters:
            char_position = all_letters.index(char)
            code = first_letter_code + char_position
            result_text += '&#%s;' % code
        else:
            result_text += char

    return result_text


def translate_from_iso_codes(text):
    if isinstance(text, int):
        return text

    russian_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
                      'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    for letter in text:
        try:
            letter_code = int.from_bytes(letter.encode('latin-1'), 'big')
        except UnicodeEncodeError:
            # print('Error: %s' % e)
            continue

        if 192 <= letter_code <= 256:
            text = text.replace(letter, russian_letters[letter_code - 192])
        elif letter_code == 184:
            text = text.replace(letter, 'ё')
        elif letter_code == 168:
            text = text.replace(letter, 'Ё')
    output_text = text
    letters = re.findall('&#.+?;', text)
    for letter in letters:
        if letter == '&#8226;':
            ru_letter = '•'
        elif letter == '&#8212;':
            ru_letter = '—'
        elif letter == '&#8722;':
            ru_letter = '−'
        elif letter == '&#8217;':
            ru_letter = '’'
        elif letter == '&#8211;':
            ru_letter = '–'
        elif letter == '&#184;':
            ru_letter = 'ё'
        elif letter == '&#184;':
            ru_letter = 'Ё'
        else:
            letter_number = int(letter[2:-1]) - 192
            ru_letter = russian_letters[letter_number]

        output_text = output_text.replace(letter, ru_letter)

    return output_text
