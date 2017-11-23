import unicodedata
import xml.etree.ElementTree as Et
import re

latin_letters = {}


def is_latin(uchr):
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in unicodedata.name(uchr))


def only_roman_chars(unistr):
    return all(is_latin(uchr)
               for uchr in unistr
               if uchr.isalpha())  # isalpha suggested by John Machin


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


def translate_from_iso_codes(text):
    russian_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдежзийклмнопрстуфхцчшщьыъэюя'
    output_text = text
    letters = re.findall('&#.+?;', text)
    for letter in letters:
        letter_number = int(letter[2:-1]) - 192
        output_text = output_text.replace(letter, russian_letters[letter_number])

    return output_text


class Monster:
    attribute_names_translation = {'name': 'имя', 'cha': 'хар', 'con': 'тел', 'dex': 'лов', 'int': 'инт', 'str': 'сил', 'wis': 'мдр', 'ac': 'класс доспеха', 'actions': 'действия', 'alignment': 'мировоззрение', 'cr': 'опасность', 'hd': 'кубики хитов',
                                   'hp': 'хиты', 'innatespells': 'врожденные заклинания', 'lairactions': 'действия логова', 'languages': 'языки', 'legendaryactions': 'легендарные действия', 'reactions': 'реакции', 'senses': 'чувства',
                                   'size': 'размер', 'skills': 'умения', 'speed': 'скорость', 'spells': 'заклинания', 'text': 'дополнительный текст', 'traits': 'свойства', 'type': 'тип', 'xp': 'опыт'}
    mandatory_attributes_list = ['name', 'cha', 'con', 'dex', 'int', 'str', 'wis', 'ac', 'hp']
    registered_monsters = {}  # This is needed to correctly assign id- tags for xml

    def __init__(self, register_number=None):
        self.name = None
        self.cha = None
        self.con = None
        self.dex = None
        self.int = None
        self.str = None
        self.wis = None
        self.ac = None
        self.actions = []
        self.alignment = None
        self.cr = None
        self.hd = None
        self.hp = None
        self.innatespells = []
        self.lairactions = []
        self.languages = None
        self.legendaryactions = []
        self.reactions = []
        self.senses = None
        self.size = None
        self.skills = None
        self.speed = None
        self.spells = []
        self.text = None
        self.traits = []
        self.type = None
        self.xp = None
        if register_number:
            Monster.registered_monsters[register_number] = self
        else:
            if not Monster.registered_monsters:
                Monster.registered_monsters[1] = self
            else:
                last_number = max(Monster.registered_monsters.keys())
                Monster.registered_monsters[last_number + 1] = self

    def __repr__(self):
        return '%s (%s)' % (self.name['en_value'], self.name['ru_value'])

    def __setattr__(self, key, value):
        if value is None:
            self.__dict__[key] = {'ru_name': Monster.attribute_names_translation[key], 'ru_value': None, 'en_value': None}
            return
        elif isinstance(value, list):
            self.__dict__[key] = value
            return
        else:
            try:
                value_int = int(value)
                self.__dict__[key]['ru_value'] = value_int
                self.__dict__[key]['en_value'] = value_int
                return
            except (TypeError, ValueError):
                if only_roman_chars(value):
                    self.__dict__[key]['en_value'] = value
                    return
                else:
                    self.__dict__[key]['ru_value'] = value
                    return

    def find_attribute_by_ru_name(self, ru_name):
        ru_to_en_translation = {v: k for k, v in Monster.attribute_names_translation.items()}
        if ru_name.lower() not in ru_to_en_translation.keys():
            raise Exception('Russian name "%s" is not found. Possible Russian names: %s' % (ru_name, ', '.join(ru_to_en_translation.keys())))
        else:
            return self.__getattribute__(ru_to_en_translation[ru_name.lower()])

    def not_complete(self):
        result = {}
        for attribute_name in Monster.mandatory_attributes_list:
            if not self.__getattribute__(attribute_name)['ru_value']:
                if 'reason' not in result.keys():
                    result['reason'] = ''
                result['reason'] += 'Russian attribute "%s" value is not set\n' % attribute_name

            if not self.__getattribute__(attribute_name)['en_value']:
                if 'reason' not in result.keys():
                    result['reason'] = ''
                result['reason'] += 'English attribute "%s" value is not set\n' % attribute_name

        return result

    @staticmethod
    def parse_xml(xml_text):
        if not xml_text:
            raise Exception('Empty XML provided')

        root_element = Et.fromstring(xml_text)
        npc_element = root_element.find('npc')
        if not npc_element:
            raise Exception('Tag npc not found')

        category_element = npc_element.find('category')
        if not category_element:
            raise Exception('There should be tag category under npc tag')

        xml_monsters = category_element.findall('*')
        for xml_monster in xml_monsters:
            monster_number = int(xml_monster.tag.replace('id-', ''))
            monster = Monster()


if __name__ == '__main__':
    print(translate_from_iso_codes('&#210;&#197;&#209;&#210; &#242;&#229;&#241;&#242;!'))
    # test_monster = Monster()
    # test_monster.name = 'Тестовое имя'
    # test_monster.name = 'Test name 1'
    # test_monster.dex = 2
    # print(test_monster.find_attribute_by_ru_name('хиты'))
    # with open('common.xml') as xml_file:
    #     Monster.parse_xml(xml_file.read())
    #
    # print(Monster.registered_monsters)
    # if test_monster.not_complete():
    #     print(test_monster.not_complete()['reason'])
