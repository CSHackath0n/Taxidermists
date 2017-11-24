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

def tree_to_file(tree, file_path):
    res = list(flatten(tree_to_str(tree.get_node(tree.root), tree)))
    with open(file_path, 'w') as f:
        f.write('\n'.join(res)+'\n')

def tree_to_str(node, tree):
    res = ['' for i in range(tree.depth()+1)]
    res[tree.depth(node)] = node.tag
    return [';'.join(res)] + [tree_to_str(child, tree) for child in tree.children(node.identifier)]

def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i
