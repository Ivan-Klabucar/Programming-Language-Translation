from collections import deque  

class Node:
    def __init__(self, data):
        self.data = data
        self.children = deque()
    
    # ova metoda dodaje djecu u poretku kakvom ce se pojavljivat u stogu
    # npr za produkciju S -> ABC
    # sa stoga ce se prvo skinu C pa B pa A
    # i tocno tim redom treba zvati add_child metodu
    def add_child(self, child): 
        self.children.appendleft(child)

class Tree:
    def __init__(self, root):
        self.root = root
    
    def print_subtree(self, node, level):
        indent = ' ' * level
        print('{}{}'.format(indent, node.data))
        for child in node.children:
            self.print_subtree(child, level + 1)
        
    def print_tree(self):
        self.print_subtree(self.root, 0)

# primjer printanja ovakvog stabla
# to je integracijski test 03
# <A>
#  <B>
#   $
#  <C>
#   c 1 c
#   a 2 a
#  c 3 c
root = Node('<A>')
bigB = Node('<B>')
bigC = Node('<C>')
leaf1 = Node('$')
leaf2 = Node('c 1 c')
leaf3 = Node('a 2 a')
leaf4 = Node('c 3 c')

root.add_child(leaf4)
root.add_child(bigC)
root.add_child(bigB)

bigB.add_child(leaf1)

bigC.add_child(leaf3)
bigC.add_child(leaf2)

tree = Tree(root)
tree.print_tree()
