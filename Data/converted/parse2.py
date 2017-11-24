from xml.etree import ElementTree as etree

def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.getchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d

tree = etree.parse("tmp.xml")
print etree_to_dict(tree.getroot())

