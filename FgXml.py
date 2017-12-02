from xml.etree.ElementTree import Element, tostring, SubElement
import xml.dom.minidom


class FgXml(object):
    def __init__(self, name, attributes=None):
        self.existing_names = {}
        self.root = Element(name)
        self.existing_names[name] = 1
        for attribute_name, attribute_value in attributes.items():
            self.root.set(attribute_name, attribute_value)

    def __repr__(self):
        xmlstr = xml.dom.minidom.parseString(tostring(self.root)).toprettyxml(indent="   ", encoding='iso-8859-1')
        return xmlstr.decode('utf-8')

    def append_under(self, name_to_append, name_under, attributes=None, under_each=False):
        if name_under not in self.existing_names:
            raise Exception('Cannot find element named "%s" to append "%s" under' % (name_under, name_to_append))

        if attributes is None:
            attributes = {}

        SubElement(self.root, name_to_append, attrib=attributes)

if __name__ == '__main__':
    test = FgXml('root', {'version': "3.3", 'release': "8|CoreRPG:3"})
    test.append_under('library', 'root')
    print(test)