import unicodedata
import xml.etree.ElementTree as Et
import re
import pickle
import glob
import os

latin_letters = {}


def is_latin(uchr):
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in unicodedata.name(uchr))


def only_roman_chars(unistr):
    return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())  # isalpha suggested by John Machin


def translate_to_iso_codes(text):
    first_letter_code = 192
    all_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
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
    russian_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
    for letter in text:
        try:
            letter_code = int.from_bytes(letter.encode('latin-1'), 'big')
        except UnicodeEncodeError:
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
        else:
            letter_number = int(letter[2:-1]) - 192
            ru_letter = russian_letters[letter_number]

        output_text = output_text.replace(letter, ru_letter)

    return output_text


class Monster:
    attribute_names_translation = {'name': 'имя', 'charisma': 'хар', 'constitution': 'тел', 'dexterity': 'лов', 'intelligence': 'инт', 'strength': 'сил', 'wisdom': 'мдр', 'ac': 'класс доспеха', 'actions': 'действия', 'alignment': 'мировоззрение', 'cr': 'опасность', 'hd': 'кубики хитов',
                                   'hp': 'хиты', 'innatespells': 'врожденные заклинания', 'lairactions': 'действия логова', 'languages': 'языки', 'legendaryactions': 'легендарные действия', 'reactions': 'реакции', 'senses': 'чувства',
                                   'size': 'размер', 'skills': 'умения', 'speed': 'скорость', 'spells': 'заклинания', 'text': 'дополнительный текст', 'traits': 'свойства', 'type': 'тип', 'xp': 'опыт', 'damageresistances': 'сопротивляемость урону',
                                   'conditionimmunities': 'иммунитет к состояниям', 'damagevulnerabilities': 'уязвимость к урону', 'damageimmunities': 'уязвимость к урону', 'savingthrows': 'спасброски'}

    mandatory_attributes_list = ['name', 'charisma', 'constitution', 'dexterity', 'intelligence', 'strength', 'wisdom', 'ac', 'hp']

    path_in_xml = {'name': 'name', 'charisma': 'abilities/charisma/score', 'constitution': 'abilities/constitution/score', 'dexterity': 'abilities/dexterity/score', 'intelligence': 'abilities/intelligence/score', 'strength': 'abilities/strength/score',
                   'wisdom': 'abilities/wisdom/score', 'ac': 'ac', 'alignment': 'alignment', 'cr': 'cr', 'hp': 'hp', 'hd': 'hd', 'languages': 'languages', 'senses': 'senses', 'size': 'size', 'skills': 'skills', 'speed': 'speed', 'text': 'text',
                   'xp': 'xp', 'damageresistances': 'damageresistances', 'conditionimmunities': 'conditionimmunities', 'damagevulnerabilities': 'damagevulnerabilities', 'innatespells': 'innatespells', 'actions': 'actions', 'reactions': 'reactions',
                   'traits': 'traits', 'spells': 'spells', 'savingthrows': 'savingthrows'}

    registered_monsters = {}  # This is needed to correctly assign id- tags for xml

    def __init__(self, register_number=None):
        self.name = None
        self.charisma = None
        self.constitution = None
        self.dexterity = None
        self.intelligence = None
        self.strength = None
        self.wisdom = None
        self.ac = None
        self.actions = None
        self.alignment = None
        self.cr = None
        self.hd = None
        self.hp = None
        self.innatespells = None
        self.lairactions = None
        self.languages = None
        self.legendaryactions = None
        self.reactions = None
        self.senses = None
        self.size = None
        self.skills = None
        self.speed = None
        self.spells = None
        self.text = None
        self.traits = None
        self.type = None
        self.xp = None
        self.damageresistances = None
        self.conditionimmunities = None
        self.damagevulnerabilities = None
        self.damageimmunities = None
        self.savingthrows = None

        if register_number:
            if register_number in Monster.registered_monsters.keys():
                Monster.registered_monsters[max(Monster.registered_monsters.keys()) + 1] = self
            else:
                Monster.registered_monsters[register_number] = self
        else:
            if not Monster.registered_monsters:
                Monster.registered_monsters[1] = self
            else:
                last_number = max(Monster.registered_monsters.keys())
                Monster.registered_monsters[last_number + 1] = self

    def __repr__(self):
        text_to_return = '\n'
        for attribute_name in sorted(self.__dict__.keys()):
            value = self.__dict__[attribute_name]
            if not value:
                text_to_return += '%s: %s\n' % (attribute_name, value)
            else:
                if value['en_value'] == value['ru_value']:
                    text_to_return += '%s: %s\n' % (attribute_name, value['en_value'])
                else:
                    text_to_return += '%s: %s (%s)\n' % (attribute_name, value['en_value'], value['ru_value'])
        return text_to_return + '\n'

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
                translated = translate_from_iso_codes(value)
                if only_roman_chars(translated):
                    self.__dict__[key]['en_value'] = translated
                else:
                    self.__dict__[key]['ru_value'] = value

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
            monster = Monster(register_number=int(xml_monster.tag.replace('id-', '')))
            for attribute in monster.__dict__.keys():
                if attribute in Monster.path_in_xml.keys():
                    xml_path = Monster.path_in_xml[attribute]
                    tag = xml_monster.find(xml_path)
                    if tag is None:
                        monster.__setattr__(attribute, '')
                    else:
                        text = tag.text
                        if attribute == 'name':
                            english_name = re.findall(" \((.+)\)$", text)
                            # if '))' in text:
                            #     half_text = text.split('(')[-1] + ')'
                            #     english_name = re.findall("\((.+)\)", half_text)
                            # else:
                            #     english_name = re.findall("\((.+)\)", text)
                            if english_name:
                                monster.name['en_value'] = english_name[-1]
                                if '(' in monster.name['en_value']:
                                    monster.name['en_value'] += ')'

                        inner_tags = tag.findall('*')
                        for itag in inner_tags:
                            text += Et.tostring(itag).decode('utf-8')

                        monster.__setattr__(attribute, text)

    @staticmethod
    def save_to_file():
        with open('monsters.obj', 'wb') as f:
            f.write(pickle.dumps(Monster.registered_monsters))

    @staticmethod
    def load_from_file():
        with open('monsters.obj', 'rb') as f:
            Monster.registered_monsters = pickle.loads(f.read())

    @staticmethod
    def find_several_elements_by_value(attribute_name, value):
        elements_to_return = []
        for element in Monster.registered_monsters.values():
            if attribute_name not in element.__dict__.keys():
                continue
            else:
                values_dict = element.__dict__[attribute_name]
                if value.lower() in values_dict['ru_value'].lower() or value.lower() in values_dict['en_value'].lower():
                    elements_to_return.append(element)

        return elements_to_return

    @staticmethod
    def filter(filters_parameters_dict):
        result_dict = {}
        for monster in Monster.registered_monsters.values():
            match = False
            for attribute in filters_parameters_dict:
                if attribute not in monster.__dict__:
                    continue

                attribute_value = filters_parameters_dict[attribute]
                monster_value_ru = monster.__dict__[attribute]['ru_value']
                monster_value_en = monster.__dict__[attribute]['en_value']
                if monster_value_ru is None:
                    monster_value_ru = ''
                if monster_value_en is None:
                    monster_value_en = ''
                monster_value_en = str(monster_value_en)
                monster_value_ru = str(monster_value_ru)
                if str(attribute_value) in monster_value_ru or str(attribute_value) in monster_value_en:
                    match = True
                else:
                    match = False
                    continue

            if match:
                result_dict[len(result_dict) + 1] = monster

        return result_dict


if __name__ == '__main__':
    # with open('db.xml') as xml_file:
    #     Monster.parse_xml(xml_file.read())
    Monster.load_from_file()
    image_files = [os.path.basename(f).replace('.jpg', '') for f in glob.glob('images/*.jpg')]
    tokens_files = [os.path.basename(f).replace('.png', '') for f in glob.glob('tokens/*.png')]

    for m in Monster.registered_monsters.values():
        ru_name = m.name['ru_value']
        en_name = m.name['en_value']
        print(ru_name)

    # Monster.load_from_file()
    # number = 0
    # for m in Monster.registered_monsters.values():
    #     name = m.name['en_value'].replace(' ', '').replace('-', '_').replace("'", '_').lower()
    #     if name not in tokens_files:
    #         print('%s.png' % name)
    #         number += 1

    #     if name not in image_files:
    #         print('%s.jpg' % name)
    #         number += 1
    #     else:
    #         image_files.remove(name)
    # print(image_files)
    # print(number)
    Monster.save_to_file()
