# -*- coding: utf8 -*-
import pickle
from Monster import Monster, translate_to_iso_codes
Monster.load_from_file()

# with open('docxsave.obj', 'rb') as f:
#     docx_monsters_dict = pickle.loads(f.read())

# del docx_monsters_dict['']
# with open('docxsave.obj', 'wb') as f:
#     f.write(pickle.dumps(docx_monsters_dict))
# print(docx_monsters_dict['Ангелы'])
# exit(0)
cr_to_xp = {'0': 10, '1/8': 25, '1/4': 50, '1/2': 100, '1': 200, '2': 450, '3': 700, '4': 1100, '5': 1800, '6': 2300, '7': 2900, '8': 3900,'9': 5000, '10': 5900, '11': 7200, '12': 8400, '13': 10000,
            '14': 11500, '15': 13000, '16': 15000, '17': 18000, '18': 20000,'19': 22000, '20': 25000, '21': 33000, '22': 41000, '23': 50000, '24': 62000, '25': 75000, '26': 90000, '27': 105000, '28': 120000, '29': 135000, '30': 155000}
sizes_dict = {'Large': 'Большой', 'Medium': 'Средний', 'Small': 'Маленький', 'Tiny': 'Крошечный', 'Huge': 'Огромный', 'Gargantuan': 'Громадный'}
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

# for docx_monster_name in sorted(docx_monsters_dict.keys()):
#     xml_monsters = Monster.find_several_elements_by_value('name', docx_monster_name)
#     if len(xml_monsters) == 0:
#         print('No monsters with name "%s" found' % docx_monster_name)
#         # print('Available names: %s' % '\n'.join([m.name['ru_value'] for m in Monster.registered_monsters.values()]))
#         # exit(0)
#     else:
#         for matched_monster in xml_monsters:
#             matched_monster = xml_monsters[0]
#             matched_monster.text = docx_monsters_dict[docx_monster_name]
Monster.save_to_file()

    # if docx_monster_name not in Monster.find_several_elements_by_value('name', docx_monster_name):
    #     print('"%s"' % docx_monster_name)
    #     exit(0)