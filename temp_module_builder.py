from story_builder import purge_dist_folder, create_definition_xml, build_xml, zipdir
from fg_translations import translate_to_iso_codes
import shutil
import zipfile

fantasy_grounds_folder = 'C:/Users/Dima/Dropbox/Fantasy Grounds/modules'  # win
# fantasy_grounds_folder = '/Users/dima/Dropbox/Fantasy Grounds/modules'  # mac

text = '''
Двести лет назад волшебник Таливар поселился здесь и построил башню в центре города, чтобы проводить свои мистические исследования. Дом Таливара был увенчан планарным маяком, который заманивал существ с других планов в здание и ловил их там. После таинственного исчезновения Таливара жители Лейлона решили оставить его башню и монстров в покое.
Магическая чума, божественное явление, исказившее магию Фаэруна, разрушила защиту башни. Запечатанные внутри существа были освобождены, чтобы атаковать Лейлон, и магия планарного маяка была перенаправлена обратно в материальный план, заставляя гуманоидов, которые смотрели на него, парализоваться. Лейлон был быстро захвачен и впоследствии покинут и оставался таким более века.
Первым делом солдаты Невервинтера в Лейлоне уничтожили планарный Маяк в доме Таливара. Маг Галлио Элибро теперь восстановил Маяк и начал свои собственные исследования в эфирном плане.

'''

if __name__ == '__main__':
    dist_folder = 'temp_dist'
    module_name = 'TempModule'
    only_assemble_files = False
    module_file_name = '%s.mod' % module_name
    index = 1
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
    print(f'Copying {module_file_name} to {fantasy_grounds_folder}')

    shutil.copy(module_file_name, fantasy_grounds_folder)
    print('Done')
