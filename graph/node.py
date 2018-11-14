class Node:
    def __init__(self, name, children):
        self.name = name
        self.children = children
        self.val = 0

    def show(self, level=0):
        print("%s%s val=%d:" % (level*"  ", self.name, self.val))
        for c in self.children:
            c.show(level + 1)


# flattens a graph into a dictionary
def flatten(graph, flattened):
    flattened.setdefault(graph.name, {'value': graph.val, 'children': []})
    for c in graph.children:
        if c.name not in flattened[graph.name]['children']:
            flatten(c, flattened)
        flattened[graph.name]['children'].append(c.name)
    return flattened


# rebuilds a graph from a flattened one
def recreate(flattened):
    new_nodes = {i: Node(i, []) for i in flattened.keys()}
    for key, values in flattened.items():
        new_nodes[key].children.extend([new_nodes[i] for i in values['children']])
        new_nodes[key].val = values['value']
    return new_nodes



