import os
import shutil
from FgXml import FgXml
import zipfile
import pickle
from fg_translations import translate_to_iso_codes

dist_folder = 'story_dist'
# module_name = 'Tomb'
only_assemble_files = False
# module_file_name = '%s.mod' % module_name
# fantasy_grounds_folder = 'C:/Users/Dima/Dropbox/Fantasy Grounds/modules' # win
fantasy_grounds_folder = '/Users/dima/Dropbox/Fantasy Grounds/modules'  # mac


def create_definition_xml(name, distribution_folder, author='Kreodont'):
    xml_text = '''<?xml version="1.0" encoding="iso-8859-1"?>
<root version="3.3" release="8|CoreRPG:3">
    <name>%s</name>
    <category>Rus</category>
    <author>%s</author>
    <ruleset>5E</ruleset>
</root>''' % (name, author)
    with open('%s/definition.xml' % distribution_folder, 'w') as output_file:
        output_file.write(xml_text)


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

def build_xml(module_name):
    root = FgXml(module_name)
    root.append_under('root', 'library')
    root.append_under('library', 'russian_bestiary')
    root.append_under('russian_bestiary', 'categoryname', {'type': 'string'}, value='Rus')
    root.append_under('russian_bestiary', 'name', {'type': 'string'}, value='russian_bestiary')

    root.append_under('russian_bestiary', 'entries')
    root.append_under('entries', 'imagewindow')
    root.append_under('imagewindow', 'librarylink', {'type': "windowreference"})
    root.append_under('imagewindow', 'name', {'type': "string"}, value='Images &#38; Maps')
    root.append_under('librarylink', 'class', value='referenceindexsorted')
    root.append_under('librarylink', 'recordname', value='lists.imagewindow@%s' % module_name)
    root.append_under('entries', 'npc')
    root.append_under('npc', 'name', {'type': "string"}, value='Story')
    root.append_under('npc', 'librarylink', {'type': "windowreference"})
    root.append_under('npc -> librarylink', 'class', value='referenceindexsorted')
    root.append_under('npc -> librarylink', 'recordname', value='lists.npc@%s' % module_name)

    root.append_under('root', 'lists')
    root.append_under('lists', 'imagewindow')
    root.append_under('lists -> imagewindow', 'name', {'type': "string"}, value='Images &#38; Maps')
    root.append_under('lists -> imagewindow', 'index')
    root.append_under('lists', 'npc')
    root.append_under('lists -> npc', 'name', {'type': "string"}, value='Story')
    root.append_under('lists -> npc', 'index')

    root.append_under('root', 'reference')
    root.append_under('reference', 'imagedata')
    root.append_under('imagedata', 'category', {"name": "RUNPC", "baseicon": "0", "decalicon": "0"})
    root.append_under('reference', 'npcdata')
    root.append_under('npcdata', 'category', {"name": "Ru", "baseicon": "0", "decalicon": "0"})
    return root

if __name__ == '__main__':
    module_name = 'Tomb'
    module_file_name = '%s.mod' % module_name
    if only_assemble_files:
        zip_file = zipfile.ZipFile(module_file_name, 'w', zipfile.ZIP_DEFLATED)
        zipdir(dist_folder, zip_file)
        zip_file.close()
        shutil.copy(module_file_name, fantasy_grounds_folder)
        exit(0)

    purge_dist_folder()
    create_definition_xml(module_name, dist_folder)
    xml = build_xml(module_name)
    index = 14

    total_text = ''
    total_name = module_name
    with open('stories.obj', 'rb') as stories_file:
        stories = [pickle.loads(stories_file.read()), ]
        print(stories)
        for story in stories:
            print(f'Story length: {len(story)}')
            story_name = module_name
            story_text = story
            total_text += story_text
            # if len(story_text) < 150:
            #     continue
        story_index = 'id-%s' % str(index).zfill(5)
        xml.append_under('npc -> index', '%s' % story_index)
        xml.append_under('npc -> index -> %s' % story_index, 'listlink', {"type": "windowreference"})
        xml.append_under('npc -> index -> %s -> listlink' % story_index, 'class', value='encounter')
        xml.append_under('npc -> index -> %s -> listlink' % story_index, 'recordname', value='reference.npcdata.%s@%s' % (story_index, xml.module_name))
        xml.append_under('npc -> index -> %s' % story_index, 'name', {"type": "string"}, value=str(index).zfill(5) + ' ' + translate_to_iso_codes(total_name))
        xml.append_under('npcdata -> category', '%s' % story_index)
        story_path = 'npcdata -> category -> %s' % story_index
        xml.append_under(story_path, 'name', {'type': "string"}, value=translate_to_iso_codes(total_name))
        xml.append_under(story_path, 'text', {'type': "formattedtext"}, value=translate_to_iso_codes(total_text))
        index += 1

    with open('%s/common.xml' % dist_folder, 'w+') as common_xml:
        common_xml.write(str(xml))
        common_xml.close()

    zip_file = zipfile.ZipFile(module_file_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dist_folder, zip_file)
    zip_file.close()
    print(f'Copying {module_file_name} to {fantasy_grounds_folder}')

    shutil.copy(module_file_name, fantasy_grounds_folder)
    print('Done')

