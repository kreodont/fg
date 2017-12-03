from Monster import Monster
import os
import shutil
from FgXml import FgXml
dist_folder = './dist'
fantasy_grounds_folder = 'C:/Users/Dima/Dropbox/Fantasy Grounds/modules'


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
    for the_file in os.listdir(dist_folder):
        file_path = os.path.join(dist_folder, the_file)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def build_xml():
    root = FgXml('root', {'version': "3.3", 'release': "8|CoreRPG:3"})


if __name__ == '__main__':
    print(build_xml())
    # Monster.load_from_file()
    # monsters_dict = Monster.filter({'name': 'Аа'})
    # purge_dist_folder()  # Deleting everything from dist folder
    # create_definition_xml()
    # shutil.copy('thumbnail.png', dist_folder + '/thumbnail.png')
    # os.mkdir('%s/tokens' % dist_folder)
    # os.mkdir('%s/images' % dist_folder)
    # aarakokra = list(monsters_dict.values())[0]
    # print(aarakokra.find_image())
    # print(aarakokra.find_token())
    # print([m.text for m in monsters_dict.values()])
