def translate_to_iso_codes(text):
    first_letter_code = 192
    all_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдежзийклмнопрстуфхцчшщьыъэюя'
    result_text = ''

    for char in text:
        if char in all_letters:
            char_position = all_letters.index(char)
            code = first_letter_code + char_position
            result_text += '&#%s' % code
        else:
            result_text += char

    return result_text

print(translate_to_iso_codes('Заклинатель This is rule'))