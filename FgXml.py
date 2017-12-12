from xml.etree.ElementTree import Element, tostring, SubElement
import xml.dom.minidom


class FgXml(object):
    last_monster_number = 0
    last_picture_number = 0

    def __init__(self, module_name, name='root', attributes=None):
        if attributes is None:
            attributes = {'version': "3.3", 'release': "8|CoreRPG:3"}
        self.full_paths = {}
        self.module_name = module_name
        self.root = Element(name)
        for attribute_name, attribute_value in attributes.items():
            self.root.set(attribute_name, attribute_value)
        self.full_paths[name] = self.root

    def __repr__(self):
        xmlstr = xml.dom.minidom.parseString(tostring(self.root)).toprettyxml(indent="   ", encoding='iso-8859-1')
        return xmlstr.decode('utf-8', 'ignore').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')

    def find_in_full_path(self, path_part):
        matched_paths = []
        for full_path in self.full_paths:
            if full_path.endswith(path_part):
                matched_paths.append(full_path)

        return matched_paths

    def append_under(self, name_under, name_to_append, attributes=None, under_each=False, value=None):
        if not name_under:
            raise Exception('You should specify the tag name to append under')

        parents_full_paths = self.find_in_full_path(name_under)
        if not parents_full_paths:
            raise Exception('Cannot find element named "%s" to append "%s" under' % (name_under, name_to_append))

        if len(parents_full_paths) > 1 and not under_each:
            raise Exception('There are %s tags with name "%s": %s. To add under each, specify under_each=True' % (len(parents_full_paths), name_under, ', '.join(parents_full_paths)))

        if attributes is None:
            attributes = {}

        for parent_full_path in parents_full_paths:
            parent = self.full_paths[parent_full_path]
            element = SubElement(parent, name_to_append, attrib=attributes)
            if value is not None:
                element.text = value
            element_full_path = parent_full_path + ' -> ' + name_to_append
            if element_full_path in self.full_paths:
                raise Exception('Element %s already exists' % element_full_path)

            self.full_paths[element_full_path] = element


if __name__ == '__main__':
    test = FgXml('TestModule')
    test.append_under('root', 'library')
    test.append_under('library', 'rudnd5e2', {'static': 'true'})
    test.append_under('rudnd5e2', 'categoryname', {'type': 'string'}, value='Rus')
    test.append_under('rudnd5e2', 'entries')
    test.append_under('entries', 'imagewindow')
    print(test)
