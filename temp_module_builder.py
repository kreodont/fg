# -*- coding: utf8 -*-
from story_builder import purge_dist_folder, create_definition_xml, build_xml, zipdir
from fg_translations import translate_to_iso_codes
import shutil
import zipfile
import random

fantasy_grounds_folder = 'C:/Users/Dima/Dropbox/Fantasy Grounds/modules'  # win
# fantasy_grounds_folder = '/Users/dima/Dropbox/Fantasy Grounds/modules'  # mac

text = '''

Логово клаугийлиаматара находится в семидесяти милях от Лейлона. На пути к логову дракона, персонажи имеют следующую встречу в Криптгарденском лесу.
Миркула Патруль
Установите сцену, прочитав вслух следующий текст в рамке:
Сквозь густые лианы и листву впереди можно увидеть танцующее пламя, окружающее плавающий череп. Тени движутся в зелени поблизости, указывая на то, что огненное существо путешествует не в одиночку.
Каранор, а 
огненный череп, созданный Улараном мортусом, приводит упырей в логово Клаугийлиаматара. Количество присутствующих упырей равно количеству персонажей в партии, не считая закадычных друзей. Когда нежить замечает персонажей, они нападают. Каранор не раскрывает подробностей своей миссии, если только это не вызвано магией. Тем не менее, огненный череп не знает большей цели своей миссии, только то, что у него есть приказ от Вианты Круэлхекс атаковать логово.Столкновение

Логово Характеристики
Логово клаугийлиаматара-это естественная пещерная система, усиленная магической связью дракона с природой. Пещера имеет землистый запах и является теплой и влажной. Следующие особенности являются общими во всем.
Потолки. 
Потолки по всей пещере достигают 40 футов в высоту.Свет. 
Фосфоресцирующий мох, растущий на стенах, наполняет пещеры тусклым зеленым светом, накладывая недостаток на проверки мудрости (восприятия), которые полагаются на зрение.Сталактиты. 
Сталагмиты среднего размера встречаются по всей пещере. При использовании этих сталагмитов для защиты, среднее или маленькое существо получает половину покрытия.Статуи. 
Клаугийлиаматар собрал статуи могущественных гуманоидов женского пола со всего Фаэруна и поместил их в свое логово. Каждая статуя имеет высоту 10 футов и весит 1000 фунтов. Персонаж знает фигуру, изображенную статуей, с успешной проверкой интеллекта DC 15 (История).Деревья. 
Деревья за пределами логова 1d6 + 10 футов высотой и не требуют проверки способности подняться.Стены. 
На стенах пещеры растут дикие виноградные лозы. Восхождение на стены без оборудования требует успешной проверки силы DC 11 (Легкая атлетика).













'''

if __name__ == '__main__':
    dist_folder = 'temp_dist'
    module_name = 'TempModule'
    only_assemble_files = False
    module_file_name = '%s.mod' % module_name
    index = random.randint(10, 7000)
    print(index)
    story_index = 'id-%s' % str(index).zfill(5)

    purge_dist_folder()
    create_definition_xml(module_name, dist_folder)

    xml = build_xml(module_name)

    xml.append_under('npc -> index', '%s' % story_index)
    xml.append_under('npc -> index -> %s' % story_index, 'listlink', {"type": "windowreference"})
    xml.append_under('npc -> index -> %s -> listlink' % story_index, 'class', value='encounter')
    xml.append_under('npc -> index -> %s -> listlink' % story_index, 'recordname', value='reference.npcdata.%s@%s' % (story_index, xml.module_name))
    xml.append_under('npc -> index -> %s' % story_index, 'name', {"type": "string"}, value=str(index).zfill(5) + ' ' + translate_to_iso_codes(module_name))
    xml.append_under('npcdata -> category', '%s' % story_index)
    story_path = 'npcdata -> category -> %s' % story_index
    xml.append_under(story_path, 'name', {'type': "string"}, value=translate_to_iso_codes(module_name))
    xml.append_under(story_path, 'text', {'type': "formattedtext"}, value=translate_to_iso_codes(text))

    with open('%s/common.xml' % dist_folder, 'w+') as common_xml:
        common_xml.write(str(xml))
        common_xml.close()

    zip_file = zipfile.ZipFile(module_file_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dist_folder, zip_file)
    zip_file.close()
    print(text)
    print(f'Copying {module_file_name} to {fantasy_grounds_folder}')

    shutil.copy(module_file_name, fantasy_grounds_folder)
    print('Done')
