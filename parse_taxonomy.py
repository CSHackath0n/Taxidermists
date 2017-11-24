import codecs
from treelib import Node, Tree

def parse_taxonomy_form_file(file_path):
    taxonomy_node_list = []
    with open(file_path, 'r') as f:
        for line in f:
            elements = line.strip().split(';')
            for node in elements:
                if node != '':
                    taxonomy_node_list.append((elements.index(node),node))
    return node_list_to_tree(taxonomy_node_list)

def node_list_to_tree(node_list):
    tree = Tree()
    parents = []
    node_tmp = node_list.pop(0)
    parent_node = tree.create_node(node_tmp[1])
    parents.append(parent_node)
    while node_list:
        if len(node_list) > 1:
            if node_list[0] == node_list[1]:
                node_list.pop(0)
                pass
        node_tmp = node_list.pop(0)
        if node_tmp[0] < len(parents):
            parents = parents[:node_tmp[0]]
        new_node = tree.create_node(node_tmp[1], parent=parents[len(parents)-1])
        parents.append(new_node)
    return tree

print(
        parse_taxonomy_form_file('Data/T0.csv').to_json()
)
