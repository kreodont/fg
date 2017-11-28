# -*- coding: utf8 -*-
import pickle
from Monster import Monster, translate_to_iso_codes
Monster.load_from_file()
with open('docxsave.obj', 'rb') as f:
    docx_monsters_dict = pickle.loads(f.read())

# del docx_monsters_dict['']
# with open('docxsave.obj', 'wb') as f:
#     f.write(pickle.dumps(docx_monsters_dict))


for docx_monster_name in sorted(docx_monsters_dict.keys()):
    xml_monsters = Monster.find_several_elements_by_value('name', docx_monster_name)
    if len(xml_monsters) == 0:
        print('No monsters with name "%s" found' % docx_monster_name)
        print('Available names: %s' % '\n'.join([m.name['ru_value'] for m in Monster.registered_monsters.values()]))
        exit(0)
    elif len(xml_monsters) > 1:
        print('More than 1 monster with name %s found' % docx_monster_name)
        exit(0)
    # if docx_monster_name not in Monster.find_several_elements_by_value('name', docx_monster_name):
    #     print('"%s"' % docx_monster_name)
    #     exit(0)