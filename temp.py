# -*- coding: utf8 -*-
import pickle
import codecs
from Monster import Monster, translate_from_iso_codes
from ActionsAndTraits import ActionsAndTraits
import xml.etree.ElementTree as Et
import html
import re

with open('docxsave.obj', 'rb') as f:
    docx_monsters_dict = pickle.loads(f.read())


# del docx_monsters_dict['']
# with open('docxsave.obj', 'wb') as f:
#     f.write(pickle.dumps(docx_monsters_dict))
# print(docx_monsters_dict['Ангелы'])
# exit(0)
# cr_to_xp = {'0': 10, '1/8': 25, '1/4': 50, '1/2': 100, '1': 200, '2': 450, '3': 700, '4': 1100, '5': 1800, '6': 2300, '7': 2900, '8': 3900,'9': 5000, '10': 5900, '11': 7200, '12': 8400, '13': 10000,
#             '14': 11500, '15': 13000, '16': 15000, '17': 18000, '18': 20000,'19': 22000, '20': 25000, '21': 33000, '22': 41000, '23': 50000, '24': 62000, '25': 75000, '26': 90000, '27': 105000, '28': 120000, '29': 135000, '30': 155000}
# sizes_dict = {'Large': 'Большой', 'Medium': 'Средний', 'Small': 'Маленький', 'Tiny': 'Крошечный', 'Huge': 'Огромный', 'Gargantuan': 'Громадный'}
#
# with open('db.xml') as xml_file:
#         monsters_renew = Monster.parse_xml(xml_file.read())
# monsters_renew = Monster.load_from_file('monsters_review.obj')
# current_monsters = Monster.load_from_file('monsters.obj')

# updated_monsters = Monster.parse_xml(open('changes.xml').read().replace('D&D', 'DnD'))

# changes_in_description = Monster.parse_xml(open('TestModule_1513334269.xml', 'rb').read())
# updated_monsters = Monster.load_from_file('updated_monsters.obj')
# xml_text = open('changes_2017_12_25.xml').read()
# # print(xml_text)
#
# changes_in_description = Monster.load_patch_from_xml(html.unescape(xml_text))
# for monster in changes_in_description:
#     if not monster.text['ru_value']:
#         continue
#
#     en_name = re.findall(' \((.+)\)', monster.text['ru_value'])[0].lower()
#     print(en_name)
#     updated_monster = updated_monsters[en_name]
#     updated_monster.text = monster.text['ru_value']
# Monster.save_to_file(updated_monsters, 'updated_monsters.obj')
    # print(monster.text)
# print(changes_in_description)
# for chosen_monster in updated_monsters.values():
# # chosen_monster = updated_monsters['adult red dragon']  # type: Monster
# # print(vampire.traits)
#     for class_name in ('traits', 'legendaryactions', 'actions'):
#         chosen_monster.__dict__[class_name]['ru_value'] = ActionsAndTraits.parse_xml(chosen_monster.get(class_name, encode=False), class_name)


# current_monsters = Monster.load_from_file('monsters.obj')
# eng_monsters = Monster.parse_xml(open('db_1.xml').read())
# eng_monsters = Monster.load_from_file('eng_monsters.obj')
# # for old_name in eng_monsters.copy():
# #     eng_monsters[old_name.lower()] = eng_monsters[old_name]
# #     del eng_monsters[old_name]
# for en_name in eng_monsters:
#     if en_name not in current_monsters:
#         print(en_name)
#
# Monster.save_to_file(eng_monsters, 'eng_monsters.obj')

# for en_name in eng_monsters:
#     print(en_name)
#     if en_name not in current_monsters:
#         print(en_name)
# #
# print(current_monsters['cloud giant'])
# if current_monsters['deva'].actions['ru_value']:
#     current_monsters['deva'].actions['ru_value'] = current_monsters['deva'].actions['ru_value'].replace('\n', '\n\n')
# if current_monsters['deva'].spells['ru_value']:
#     current_monsters['deva'].spells['ru_value'] = current_monsters['deva'].spells['ru_value'].replace('\n', '\n\n')
# if current_monsters['deva'].traits['ru_value']:
#     current_monsters['deva'].traits['ru_value'] = current_monsters['deva'].traits['ru_value'].replace('\n', '\n\n')
# if current_monsters['deva'].innatespells['ru_value']:
#     current_monsters['deva'].innatespells['ru_value'] = current_monsters['deva'].innatespells['ru_value'].replace('\n', '\n\n')
# if current_monsters['deva'].legendaryactions['ru_value']:
#     current_monsters['deva'].legendaryactions['ru_value'] = current_monsters['deva'].legendaryactions['ru_value'].replace('\n', '\n\n')

# for en_monster_name in eng_monsters:
#     en_monster = eng_monsters[en_monster_name]
#     if en_monster_name.lower() not in current_monsters:
#         continue
#     ru_monster = current_monsters[en_monster_name.lower()]
#     en_value = en_monster.savingthrows['en_value']
#     print(en_value)
#     ru_monster.savingthrows['en_value'] = en_value
#   print(en_monster.get('speed', ru=False))
# Monster.save_to_file(eng_monsters, 'eng_monsters.obj')
# for my_monster_name in sorted(current_monsters):
#     if my_monster_name not in eng_monsters:
#         print(my_monster_name)

# print(sorted(current_monsters.keys()))
# for monster_name in monsters_renew.copy():
#     # print(monsters_renew[monster_name].get('savingthrows', encode=False))
#     if not current_monsters[monster_name].savingthrows['ru_value'] and monsters_renew[monster_name].savingthrows['ru_value']:
#         current_monsters[monster_name].savingthrows['ru_value'] = monsters_renew[monster_name].savingthrows['ru_value']
#         print(monster_name)

# Monster.save_to_file(monsters_renew, filename='monsters_review.obj')
# Monster.save_to_file(current_monsters)
# print(monsters_renew['Adult Black Dragon'].legendaryactions)
# print(current_monsters['Adult Black Dragon'].legendaryactions)
# for monster_number in current_monsters:
#     monster = current_monsters[monster_number]
#     monster.number = monster_number
#     eng_name = monster.name['en_value']
#     new_dict[eng_name] = monster
# Monster.save_to_file(new_dict)
# Monster.save_to_file(monsters_renew, 'monsters_review.obj')

# monsters_dict = Monster.filter({'name': 'Adult Black Dragon'})
# print(monsters_dict)

# monster = Monster()
# for attribute in monster.__dict__:
#     if attribute not in Monster.path_in_xml:
#         print(attribute)

        # my_en_names = sorted([monster.name['en_value'].lower() for monster in Monster.registered_monsters.values()])
# with codecs.open('phantom_dict.txt', 'r', 'utf_8_sig') as dict_file:
#     for string in dict_file:
#         en_name, ru_name = string.split('\t')
#         en_name = en_name.strip()
#         ru_name = ru_name.strip()
#         if en_name.lower() not in my_en_names:
#             continue
#
#         current_monsters = Monster.find_several_elements_by_value('name', en_name, strict=True)
#         if len(current_monsters) != 1:
#             print(en_name)
#             print(current_monsters)
#             exit(1)
#         current_monster = current_monsters[0]
#
#         my_ru_name = current_monster.name['ru_value']
#         if my_ru_name.lower() != ru_name.lower():
#             print('%s %s %s' % (en_name, ru_name, my_ru_name))
#             current_monster.name['ru_value'] = ru_name
#             # print(my_en_names)
#             # exit(0)
# print('\n\n')
# for monster in Monster.registered_monsters.values():
#     print(monster.get('name', both=True, encode=False))

# for monster in Monster.registered_monsters.values():
#     size = monster.get('size', ru=False)
#     ru_size = sizes_dict[size]
#     monster.size = ru_size
#     xp = cr_to_xp[str(cr)]
#     monster.xp = xp
#     print(cr, xp)
    # if monster.hp['en_value'] == 0:
    #     hp = 0
    #     hd = ''
    # else:
    #     hp = monster.hp['en_value'].split()[0]
    #     hd = monster.hp['en_value'].split('(')[1].replace(')', '')
    # monster.hp = hp
    # monster.hd = hd
    # print(hp, hd)


#
# del docx_monsters_dict['Прочие демонические повелители']
# with open('docxsave.obj', 'wb') as f:
#     f.write(pickle.dumps(docx_monsters_dict))
#     f.close()
# exit(0)
#
# for docx_monster_name in sorted(docx_monsters_dict.keys()):
#     xml_monsters = Monster.find_several_elements_by_value(current_monsters, 'name', docx_monster_name)
#     if len(xml_monsters) == 0:
#         print(docx_monster_name)
#         print('\n\n')
#         ru_names = sorted([m.name['ru_value'] for m in current_monsters.values()])
#         print(ru_names)
#         print('\n\n')
#         print(docx_monster_name)
#         exit(0)
#     else:
#         print(docx_monster_name)
#         print([x.name['ru_value'] for x in xml_monsters])
#         print('\n\n')
# exit(0)
# doc_name = 'Юголоты'
# ru_names = ['Арканалот', 'Ультролот', 'Меззолот', 'Никалот']
# for ru_name in ru_names:
#     print(ru_name)
#     monster = Monster.find_several_elements_by_value(current_monsters, 'name', ru_name)[0]
#     if not current_monsters[monster.name['en_value'].lower()].text['ru_value']:
#         current_monsters[monster.name['en_value'].lower()].text['ru_value'] = docx_monsters_dict[doc_name]
#     else:
#         current_monsters[monster.name['en_value'].lower()].text['ru_value'] += docx_monsters_dict[doc_name]
#
# del docx_monsters_dict[doc_name]

# Monster.save_to_file(current_monsters, 'monsters.obj')
# with open('docxsave.obj', 'wb') as f:
#     f.write(pickle.dumps(docx_monsters_dict))
#     f.close()
with open('stories.obj', 'rb') as stories_file:
    stories = pickle.loads(stories_file.read())
    for story in stories:
        print(story)
        input()