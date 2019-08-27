"""
Input: list of XML formatted strings
Output: Module file that can be imported to Fantasy Grounds
"""
import shutil
import os
import zipfile
from typing import List
from FgXml import FgXml
from fg_translations import translate_to_iso_codes
from parse_html import get_stories


def define_fg_folder(os_type: str) -> str:
    if os_type.strip().lower() == 'win':
        return 'C:/Users/Dima/Dropbox/Fantasy Grounds/modules'
    elif os_type.strip().lower() == 'mac':
        return '/Users/dima/Dropbox/Fantasy Grounds/modules'


def copy_mod_file_to_fg_folder(filename: str, destination_folder: str):
    shutil.copy(filename, destination_folder)


def create_dist_folder(folder_name: str):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    for the_file in os.listdir(folder_name):
        file_path = os.path.join(folder_name, the_file)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def zipdir(
        module_name: str,
        dist_folder_name: str,
        exclude_files: List[str] = (),
) -> str:
    zip_file = zipfile.ZipFile(f'{module_name}.mod', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dist_folder_name):
        for f in files:
            full_path = os.path.join(root, f).replace('\\', '/')
            if full_path in exclude_files:
                continue

            full_path_without_folder_name = '/'.join(full_path.split('/')[1:])
            if full_path_without_folder_name in exclude_files:
                continue
            zip_file.write(full_path, full_path_without_folder_name)

    return zip_file.filename


def create_definition_xml(
        module_name: str,
        dist_folder: str,
        author: str = 'Kreodont',
        ruleset: str = '5E',
) -> str:
    xml_text = '''<?xml version="1.0" encoding="iso-8859-1"?>
<root version="3.3" release="8|CoreRPG:3">
    <name>%s</name>
    <category>Rus</category>
    <author>%s</author>
    <ruleset>%s</ruleset>
</root>''' % (module_name, author, ruleset)
    with open('%s/definition.xml' % dist_folder, 'w') as output_file:
        output_file.write(xml_text)

    return f'{dist_folder}/definition.xml'


def create_common_xml(
        *, 
        module_name: str, 
        dist_folder: str, 
        stories_list: List[str],
) -> str:

    def build_xml_template(mod_name) -> FgXml:
        root = FgXml(mod_name)
        library_name = mod_name
        root.append_under('root', 'library')
        root.append_under('library', library_name)
        root.append_under(library_name, 'categoryname',
                          {'type': 'string'}, value='Rus')
        root.append_under(library_name, 'name', {'type': 'string'},
                          value=library_name)

        root.append_under(library_name, 'entries')
        root.append_under('entries', 'imagewindow')
        root.append_under('imagewindow', 'librarylink',
                          {'type': "windowreference"})
        root.append_under('imagewindow', 'name', {'type': "string"},
                          value='Images &#38; Maps')
        root.append_under('librarylink', 'class', value='referenceindexsorted')
        root.append_under('librarylink', 'recordname',
                          value='lists.imagewindow@%s' % mod_name)
        root.append_under('entries', 'npc')
        root.append_under('npc', 'name', {'type': "string"}, value='Story')
        root.append_under('npc', 'librarylink', {'type': "windowreference"})
        root.append_under('npc -> librarylink', 'class',
                          value='referenceindexsorted')
        root.append_under('npc -> librarylink', 'recordname',
                          value='lists.npc@%s' % mod_name)

        root.append_under('root', 'lists')
        root.append_under('lists', 'imagewindow')
        root.append_under('lists -> imagewindow', 'name', {'type': "string"},
                          value='Images &#38; Maps')
        root.append_under('lists -> imagewindow', 'index')
        root.append_under('lists', 'npc')
        root.append_under('lists -> npc', 'name', {'type': "string"},
                          value='Story')
        root.append_under('lists -> npc', 'index')

        root.append_under('root', 'reference')
        root.append_under('reference', 'imagedata')
        root.append_under('imagedata', 'category',
                          {"name": "RUNPC", "baseicon": "0", "decalicon": "0"})
        root.append_under('reference', 'npcdata')
        root.append_under('npcdata', 'category',
                          {"name": "Ru", "baseicon": "0", "decalicon": "0"})
        return root

    xml_template = build_xml_template(module_name)
    for story_number, story in enumerate(stories_list, 1):
        story_index = 'id-%s' % str(story_number).zfill(5)
        xml_template.append_under('npc -> index', '%s' % story_index)
        xml_template.append_under(
                'npc -> index -> %s' % story_index,
                'listlink',
                {"type": "windowreference"},
        )

        xml_template.append_under(
                'npc -> index -> %s -> listlink' % story_index,
                'class',
                value='encounter',
        )

        xml_template.append_under(
                'npc -> index -> %s -> listlink' % story_index,
                'recordname', value='reference.npcdata.%s@%s' % (
                    story_index,
                    module_name,
                ),
        )

        xml_template.append_under(
                'npc -> index -> %s' % story_index,
                'name',
                {"type": "string"},
                value=str(story_number).zfill(5) + ' ' + translate_to_iso_codes(
                        module_name),
        )

        xml_template.append_under('npcdata -> category', '%s' % story_index)
        story_path = 'npcdata -> category -> %s' % story_index
        xml_template.append_under(
                story_path,
                'name',
                {'type': "string"},
                value=translate_to_iso_codes(module_name),
        )

        xml_template.append_under(
                story_path,
                'text',
                {'type': "formattedtext"},
                value=translate_to_iso_codes(story),
        )

        print(story)

    with open('%s/common.xml' % dist_folder, 'w') as output_file:
        output_file.write(str(xml_template))

    return f'{dist_folder}/common.xml'


if __name__ == '__main__':
    module_name_ = 'tomb_rus'
    print(f'Module name: "{module_name_}"')
    dist_folder_name_ = f'{module_name_}_dist'
    print(f'Creating folder "{dist_folder_name_}"')
    create_dist_folder(dist_folder_name_)
    print('Creating definition.xml')
    create_definition_xml(module_name_, dist_folder_name_)
    print('Creating common.xml')
    create_common_xml(
            module_name=module_name_,
            dist_folder=dist_folder_name_,
            # stories_list=['xexexe'],
            stories_list=get_stories(module_name_, 600),
    )
    module_file_name = zipdir(module_name_, dist_folder_name_)
    print(f'Packed {dist_folder_name_} to {module_file_name}')
    destination_folder_ = define_fg_folder("mac")
    print(f'Copying {module_file_name} '
          f'to {destination_folder_}/{module_file_name}')
    copy_mod_file_to_fg_folder(module_file_name, destination_folder_)
    print('Done')
