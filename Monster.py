import unicodedata

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


class Monster:
    attribute_names_translation = {'name': 'имя', 'cha': 'хар', 'con': 'тел', 'dex': 'лов', 'int': 'инт', 'str': 'сил', 'wis': 'мдр', 'ac': 'класс доспеха', 'actions': 'действия', 'alignment': 'мировоззрение', 'cr': 'опасность', 'hd': 'кубики хитов',
                                   'hp': 'хиты', 'innatespells': 'врожденные заклинания', 'lairactions': 'действия логова', 'languages': 'языки', 'legendaryactions': 'легендарные действия', 'reactions': 'реакции', 'senses': 'чувства',
                                   'size': 'размер', 'skills': 'умения', 'speed': 'скорость', 'spells': 'заклинания', 'text': 'дополнительный текст', 'traits': 'свойства', 'type': 'тип', 'xp': 'опыт'}
    mandatory_attributes_list = ['name', 'cha', 'con', 'dex', 'int', 'str', 'wis', 'ac', 'hp']

    def __init__(self):
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

    def parse_xml(self, xml_text):
        pass

if __name__ == '__main__':
    test_monster = Monster()
    test_monster.name = 'Тестовое имя'
    test_monster.name = 'Test name 1'
    test_monster.dex = 2
    print(test_monster.find_attribute_by_ru_name('хиты'))
    # if test_monster.not_complete():
    #     print(test_monster.not_complete()['reason'])
