from Monster import Monster
import os
import shutil
from FgXml import FgXml
import zipfile
dist_folder = './dist'
# fantasy_grounds_folder = 'C:/Users/Dima/Dropbox/Fantasy Grounds/modules'
fantasy_grounds_folder = '/Users/dima/Dropbox/Fantasy Grounds/modules'
module_file_name = 'Test2.mod'


def create_definition_xml(name='TestModule', author='Kreodont and Mr_Robot2'):
    xml_text = '''<?xml version="1.0" encoding="iso-8859-1"?>
<root version="3.3" release="8|CoreRPG:3">
    <name>%s</name>
    <category>Rus</category>
    <author>%s</author>
    <ruleset>5E</ruleset>
</root>''' % (name, author)
    with open('%s/definition.xml' % dist_folder, 'w') as f:
        f.write(xml_text)


def purge_dist_folder():
    if not os.path.isdir(dist_folder):
        os.makedirs(dist_folder)

    for the_file in os.listdir(dist_folder):
        file_path = os.path.join(dist_folder, the_file)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def zipdir(path, ziph, exceptions=()):
    for root, dirs, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f).replace('\\', '/')
            if full_path in exceptions:
                continue
            full_path_without_folder_name = '/'.join(full_path.split('/')[1:])
            if full_path_without_folder_name in exceptions:
                continue
            ziph.write(full_path, full_path_without_folder_name)


def build_xml():
    root = FgXml()
    root.append_under('root', 'library')
    root.append_under('library', 'rudnd5e2', {'static': 'true'})
    root.append_under('rudnd5e2', 'name', {'type': 'string'}, value='rudnd5e2')
    root.append_under('rudnd5e2', 'categoryname', {'type': 'string'}, value='Rus')
    root.append_under('rudnd5e2', 'entries')
    root.append_under('entries', 'imagewindow')
    root.append_under('imagewindow', 'librarylink', {'type': "windowreference"})
    root.append_under('imagewindow', 'name', {'type': "string"}, value='Images &#38; Maps')
    root.append_under('librarylink', 'class', value='referenceindexsorted')
    root.append_under('librarylink', 'recordname', value='lists.imagewindow@RuDnD5e2')
    root.append_under('entries', 'npc')
    root.append_under('npc', 'librarylink', {'type': "windowreference"})
    root.append_under('npc -> librarylink', 'class', value='referenceindexsorted')
    root.append_under('npc -> librarylink', 'recordname', value='lists.npc@RuDnD5e2')

    root.append_under('root', 'lists')
    root.append_under('lists', 'imagewindow')
    root.append_under('lists -> imagewindow', 'name', {'type': "string"}, value='Images &#38; Maps')
    root.append_under('lists -> imagewindow', 'index')
    root.append_under('lists', 'npc')
    root.append_under('lists -> npc', 'name', {'type': "string"}, value='NPCs')
    root.append_under('lists -> npc', 'index')

    root.append_under('root', 'reference', {'static': "true"})
    root.append_under('reference', 'imagedata')
    root.append_under('imagedata', 'category', {"name": "RUNPC", "baseicon": "0", "decalicon": "0"})
    root.append_under('reference', 'npcdata')
    root.append_under('npcdata', 'category', {"name": "Ru", "baseicon": "0", "decalicon": "0"})
    return root


if __name__ == '__main__':
    xml = build_xml()
    Monster.load_from_file()
    purge_dist_folder()  # Deleting everything from dist folder
    create_definition_xml()
    shutil.copy('thumbnail.png', dist_folder + '/thumbnail.png')
    os.mkdir('%s/tokens' % dist_folder)
    os.mkdir('%s/images' % dist_folder)
    monsters_dict = Monster.filter({'name': 'Аа'})
    aarakokra = list(monsters_dict.values())[0]
    image_file, token_file = aarakokra.append_to_xml(xml)
    if image_file:
        shutil.copy(image_file, '%s/%s' % (dist_folder, image_file))

    shutil.copy(token_file, '%s/%s' % (dist_folder, token_file))
    common_xml_text = str(xml)
    with open('%s/common.xml' % dist_folder, 'w') as common_xml:
        common_xml.write(common_xml_text)
        common_xml.close()

    zip_file = zipfile.ZipFile(module_file_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dist_folder, zip_file)
    shutil.copy(module_file_name, fantasy_grounds_folder)
    print(xml)
