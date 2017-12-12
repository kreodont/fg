import unicodedata
import xml.etree.ElementTree as Et
import re
import pickle
import glob
import os
from FgXml import FgXml

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
            print('Error')
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
    attribute_names_translation = {'name': 'имя', 'charisma': 'хар', 'constitution': 'тел', 'dexterity': 'лов', 'intelligence': 'инт', 'strength': 'сил', 'wisdom': 'мдр', 'ac': 'класс доспеха', 'actions': 'действия', 'alignment': 'мировоззрение',
                                   'cr': 'опасность', 'hd': 'кубики хитов',
                                   'hp': 'хиты', 'innatespells': 'врожденные заклинания', 'lairactions': 'действия логова', 'languages': 'языки', 'legendaryactions': 'легендарные действия', 'reactions': 'реакции', 'senses': 'чувства',
                                   'size': 'размер', 'skills': 'умения', 'speed': 'скорость', 'spells': 'заклинания', 'text': 'дополнительный текст', 'traits': 'свойства', 'type': 'тип', 'xp': 'опыт', 'damageresistances': 'сопротивляемость урону',
                                   'conditionimmunities': 'иммунитет к состояниям', 'damagevulnerabilities': 'уязвимость к урону', 'damageimmunities': 'уязвимость к урону', 'savingthrows': 'спасброски'}

    mandatory_attributes_list = ['name', 'charisma', 'constitution', 'dexterity', 'intelligence', 'strength', 'wisdom', 'ac', 'hp']

    path_in_xml = {'name': 'name', 'charisma': 'abilities/charisma/score', 'constitution': 'abilities/constitution/score', 'dexterity': 'abilities/dexterity/score', 'intelligence': 'abilities/intelligence/score',
                   'strength': 'abilities/strength/score',
                   'wisdom': 'abilities/wisdom/score', 'ac': 'ac', 'alignment': 'alignment', 'cr': 'cr', 'hp': 'hp', 'hd': 'hd', 'languages': 'languages', 'senses': 'senses', 'size': 'size', 'skills': 'skills', 'speed': 'speed', 'text': 'text',
                   'xp': 'xp', 'damageresistances': 'damageresistances', 'conditionimmunities': 'conditionimmunities', 'damagevulnerabilities': 'damagevulnerabilities', 'innatespells': 'innatespells', 'actions': 'actions', 'reactions': 'reactions',
                   'traits': 'traits', 'spells': 'spells', 'savingthrows': 'savingthrows', 'damageimmunities': 'damageimmunities', 'lairactions': 'lairactions', 'legendaryactions': 'legendaryactions', 'type': 'type'}

    cr_to_xp = {'0': 10, '1/8': 25, '1/4': 50, '1/2': 100, '1': 200, '2': 450, '3': 700, '4': 1100, '5': 1800, '6': 2300, '7': 2900, '8': 3900, '9': 5000, '10': 5900, '11': 7200, '12': 8400, '13': 10000,
                '14': 11500, '15': 13000, '16': 15000, '17': 18000, '18': 20000, '19': 22000, '20': 25000, '21': 33000, '22': 41000, '23': 50000, '24': 62000, '25': 75000, '26': 90000, '27': 105000, '28': 120000, '29': 135000, '30': 155000}
    sizes_dict = {'Large': 'Большой', 'Medium': 'Средний', 'Small': 'Маленький', 'Tiny': 'Крошечный', 'Huge': 'Огромный', 'Gargantuan': 'Громадный'}

    def __init__(self, number=0):
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
        self.number = number

        # if register_number:
        #     if register_number in Monster.registered_monsters.keys():
        #         Monster.registered_monsters[max(Monster.registered_monsters.keys()) + 1] = self
        #     else:
        #         Monster.registered_monsters[register_number] = self
        # else:
        #     if not Monster.registered_monsters:
        #         Monster.registered_monsters[1] = self
        #     else:
        #         last_number = max(Monster.registered_monsters.keys())
        #         Monster.registered_monsters[last_number + 1] = self

    def __repr__(self):
        text_to_return = '\n'
        for attribute_name in sorted(self.__dict__.keys()):
            if attribute_name == 'number':
                continue

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
        if key == 'number':
            self.__dict__[key] = value
            return

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
                    self.__dict__[key]['ru_value'] = translated

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

    def find_image(self):
        if self.name['en_value'].replace('/', ' ') in [os.path.basename(f).replace('.jpg', '') for f in glob.glob('images/*.jpg')]:
            return 'images/%s.jpg' % self.name['en_value'].replace('/', ' ')

    def find_token(self):
        name = self.name['en_value'].replace(' ', '').replace('-', '_').replace("'", '_').replace('/', '').lower()
        tokens_filenames = glob.glob('tokens/*.png')
        matched_filename = None
        for token_filename in tokens_filenames:
            if name == token_filename.replace('tokens\\', '').replace('.png', '').replace(' ', '').replace('-', '_').lower():
                matched_filename = token_filename
                break

        return matched_filename

    def get(self, attribute_name, ru=True, both=False, encode=True):
        if attribute_name not in self.__dict__:
            return ''

        value_dict = self.__getattribute__(attribute_name)
        ru_value = str(value_dict['ru_value'])
        en_value = str(value_dict['en_value'])
        if ru_value == 'None':
            ru_value = ''
        if en_value == 'None':
            en_value = ''
        if encode:
            ru_value = translate_to_iso_codes(ru_value)
        if both:
            if not ru_value and not en_value:
                return ''
            if not ru_value:
                return en_value
            if not en_value:
                return ru_value
            else:
                return '%s (%s)' % (ru_value, en_value)
        if ru:
            return ru_value
        else:
            return en_value

    @staticmethod
    def parse_xml(xml_text):
        if not xml_text:
            raise Exception('Empty XML provided')

        monsters_dict = {}
        root_element = Et.fromstring(xml_text)
        npc_element = root_element.find('npc')
        if not npc_element:
            raise Exception('Tag npc not found')

        category_element = npc_element.find('category')
        if not category_element:
            raise Exception('There should be tag category under npc tag')

        xml_monsters = category_element.findall('*')
        for xml_monster in xml_monsters:
            monster = Monster(number=int(xml_monster.tag.replace('id-', '')))
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

            monsters_dict[monster.name['en_value']] = monster

        return monsters_dict

    @staticmethod
    def save_to_file(dictionary_to_save, filename='monsters.obj'):
        with open(filename, 'wb') as f:
            f.write(pickle.dumps(dictionary_to_save))

    @staticmethod
    def load_from_file(filename='monsters.obj'):
        with open(filename, 'rb') as f:
            loaded_monsters = pickle.loads(f.read())
            return loaded_monsters

    @staticmethod
    def find_several_elements_by_value(monsters_dict, attribute_name, value, strict=False):
        elements_to_return = []
        for element in monsters_dict.values():
            if attribute_name not in element.__dict__.keys():
                continue
            else:
                values_dict = element.__dict__[attribute_name]
                if strict:
                    if value.lower() in (values_dict['ru_value'].lower(), values_dict['en_value'].lower()):
                        elements_to_return.append(element)
                else:
                    if value.lower() in values_dict['ru_value'].lower() or value.lower() in values_dict['en_value'].lower():
                        elements_to_return.append(element)

        return elements_to_return

    @staticmethod
    def filter(monsters_dict, filters_parameters_dict):
        result_dict = {}
        for monster in monsters_dict.values():
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

    def append_to_xml(self, root):
        if not isinstance(root, FgXml):
            return

        FgXml.last_monster_number += 1
        monster_nubmer = FgXml.last_monster_number
        monster_index = 'id-%s' % str(monster_nubmer).zfill(5)
        image_file_name = self.find_image()
        token_file_name = self.find_token()
        additional_text = ''
        if not token_file_name:
            token_file_name = 'tokens/%s.png' % self.get('name', ru=False)[0].upper()
        if image_file_name:
            FgXml.last_picture_number += 1
            monster_picture_number = FgXml.last_picture_number
            monster_picture_index = 'id-%s' % str(monster_picture_number).zfill(5)
            additional_text = '<linklist>\n<link class="imagewindow" recordname="reference.imagedata.%s">%s</link>\n</linklist>\n' % (monster_picture_index, self.get('name', both=True))
            root.append_under('imagewindow -> index', '%s' % monster_picture_index)
            root.append_under('imagewindow -> index -> %s' % monster_picture_index, 'listlink', {"type": "windowreference"})
            root.append_under('imagewindow -> index -> %s -> listlink' % monster_index, 'class', value='imagewindow')
            root.append_under('imagewindow -> index -> %s -> listlink' % monster_index, 'recordname', value='reference.imagedata.%s@%s' % (monster_picture_index, root.module_name))
            root.append_under('imagewindow -> index -> %s' % monster_picture_index, 'name', {"type": "string"}, value=self.get('name', both=True))

            root.append_under('reference -> imagedata -> category', '%s' % monster_picture_index)
            root.append_under('reference -> imagedata -> category -> %s' % monster_picture_index, 'image', {'type': "image"})
            root.append_under('reference -> imagedata -> category -> %s -> image' % monster_picture_index, 'bitmap', value='%s' % image_file_name)
            root.append_under('reference -> imagedata -> category -> %s' % monster_picture_index, 'isidentified', {'type': "number"}, value='0')
            root.append_under('reference -> imagedata -> category -> %s' % monster_picture_index, 'name', {'type': "string"}, value=self.get('name', both=True))

        root.append_under('npc -> index', '%s' % monster_index)
        root.append_under('npc -> index -> %s' % monster_index, 'listlink', {"type": "windowreference"})
        root.append_under('npc -> index -> %s -> listlink' % monster_index, 'class', value='npc')
        root.append_under('npc -> index -> %s -> listlink' % monster_index, 'recordname', value='reference.npcdata.%s@%s' % (monster_index, root.module_name))
        root.append_under('npc -> index -> %s' % monster_index, 'name', {"type": "string"}, value=self.get('name', both=True))
        root.append_under('npcdata -> category', '%s' % monster_index)
        monster_path = 'npcdata -> category -> %s' % monster_index
        root.append_under(monster_path, 'abilities')
        root.append_under('%s -> abilities' % monster_path, 'charisma')
        root.append_under('%s -> abilities -> charisma' % monster_path, 'bonus', {'type': "number"}, value=str((self.charisma['en_value'] - 10) // 2))
        root.append_under('%s -> abilities -> charisma' % monster_path, 'score', {'type': "number"}, value=str(self.charisma['en_value']))
        root.append_under('%s -> abilities' % monster_path, 'constitution')
        root.append_under('%s -> abilities -> constitution' % monster_path, 'bonus', {'type': "number"}, value=str((self.constitution['en_value'] - 10) // 2))
        root.append_under('%s -> abilities -> constitution' % monster_path, 'score', {'type': "number"}, value=str(self.constitution['en_value']))
        root.append_under('%s -> abilities' % monster_path, 'dexterity')
        root.append_under('%s -> abilities -> dexterity' % monster_path, 'bonus', {'type': "number"}, value=str((self.dexterity['en_value'] - 10) // 2))
        root.append_under('%s -> abilities -> dexterity' % monster_path, 'score', {'type': "number"}, value=str(self.dexterity['en_value']))
        root.append_under('%s -> abilities' % monster_path, 'intelligence')
        root.append_under('%s -> abilities -> intelligence' % monster_path, 'bonus', {'type': "number"}, value=str((self.intelligence['en_value'] - 10) // 2))
        root.append_under('%s -> abilities -> intelligence' % monster_path, 'score', {'type': "number"}, value=str(self.intelligence['en_value']))
        root.append_under('%s -> abilities' % monster_path, 'strength')
        root.append_under('%s -> abilities -> strength' % monster_path, 'bonus', {'type': "number"}, value=str((self.strength['en_value'] - 10) // 2))
        root.append_under('%s -> abilities -> strength' % monster_path, 'score', {'type': "number"}, value=str(self.strength['en_value']))
        root.append_under('%s -> abilities' % monster_path, 'wisdom')
        root.append_under('%s -> abilities -> wisdom' % monster_path, 'bonus', {'type': "number"}, value=str((self.wisdom['en_value'] - 10) // 2))
        root.append_under('%s -> abilities -> wisdom' % monster_path, 'score', {'type': "number"}, value=str(self.wisdom['en_value']))

        root.append_under('%s' % monster_path, 'ac', {'type': "number"}, value=self.get('ac'))
        root.append_under('%s' % monster_path, 'actions', value=self.get('actions'))
        root.append_under('%s' % monster_path, 'alignment', {'type': "string"}, value=self.get('alignment'))
        root.append_under('%s' % monster_path, 'cr', {'type': "string"}, value=str(self.cr['en_value']))
        root.append_under('%s' % monster_path, 'hd', {'type': "string"}, value=str(self.hd['en_value']))
        root.append_under('%s' % monster_path, 'hp', {'type': "number"}, value=str(self.hp['en_value']))
        root.append_under('%s' % monster_path, 'innatespells', value=str(self.get('innatespells')))
        root.append_under('%s' % monster_path, 'lairactions', value=str(self.get('lairactions')))
        root.append_under('%s' % monster_path, 'legendaryactions', value=str(self.get('legendaryactions')))
        root.append_under('%s' % monster_path, 'reactions', value=str(self.get('reactions')))
        root.append_under('%s' % monster_path, 'languages', {'type': "string"}, value=self.get('languages'))
        root.append_under('%s' % monster_path, 'locked', {'type': "number"}, value='1')
        root.append_under('%s' % monster_path, 'name', {'type': "string"}, value=self.get('name', both=True))
        root.append_under('%s' % monster_path, 'senses', {'type': "string"}, value=self.get('senses'))
        root.append_under('%s' % monster_path, 'size', {'type': "string"}, value=self.get('size', ru=False))
        root.append_under('%s' % monster_path, 'skills', {'type': "string"}, value=self.get('skills', ru=False))
        root.append_under('%s' % monster_path, 'speed', {'type': "string"}, value=self.get('speed'))
        root.append_under('%s' % monster_path, 'spells', value=self.get('spells'))

        root.append_under('%s' % monster_path, 'conditionimmunities', {'type': "string"}, value=self.get('conditionimmunities'))
        root.append_under('%s' % monster_path, 'damageresistances', {'type': "string"}, value=self.get('damageresistances'))
        root.append_under('%s' % monster_path, 'damagevulnerabilities', {'type': "string"}, value=self.get('damagevulnerabilities'))
        root.append_under('%s' % monster_path, 'damageimmunities', {'type': "string"}, value=self.get('damageimmunities'))
        root.append_under('%s' % monster_path, 'savingthrows', {'type': "string"}, value=self.get('savingthrows', ru=False))

        additional_text += self.get('text')
        root.append_under('%s' % monster_path, 'text', {'type': "formattedtext"}, value=additional_text)
        root.append_under('%s' % monster_path, 'token', {'type': "token"}, value='%s@%s' % (token_file_name, root.module_name))
        root.append_under('%s' % monster_path, 'traits', value=str(self.get('traits')))
        root.append_under('%s' % monster_path, 'type', {'type': "string"}, value=self.get('type'))
        root.append_under('%s' % monster_path, 'xp', {'type': "number"}, value=self.get('xp'))

        return image_file_name, token_file_name


if __name__ == '__main__':
    # with open('db.xml') as xml_file:
    #     Monster.parse_xml(xml_file.read())
    all_monsters = Monster.load_from_file()
    # image_files = [os.path.basename(f).replace('.jpg', '') for f in glob.glob('images/*.jpg')]
    # tokens_files = [os.path.basename(f).replace('.png', '') for f in glob.glob('tokens/*.png')]

    # Monster.load_from_file()
    # number = 0
    # for m in all_monsters.values():
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
    Monster.save_to_file(all_monsters)
