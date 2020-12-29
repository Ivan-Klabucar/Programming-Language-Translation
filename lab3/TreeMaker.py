import sys
from Node import Node, get_name
from BasicNezavrsni import *
from Zavrsni import *
from Nebitni import *

def get_level(string):
    return len(string) - len(string.lstrip())

def append_node(stack, line):
    next_node = classes.get(get_name(line), Default)(line)
    stack[-1].add_child(next_node)
    stack.append(next_node)

def print_tree(node, indent):
    leading_space = ' ' * indent
    print("{}{}".format(leading_space, node.data))
    for x in node.children:
        print_tree(x, indent + 1)

global classes
classes = dict()
classes['<Foo>'] = Foo
classes['Boo'] = Boo

classes['<prijevodna_jedinica>'] = Prijevodna_jedinica
classes['<primarni_izraz>'] = Primarni_izraz
classes['IDN'] = IDN
classes['BROJ'] = BROJ
classes['ZNAK'] = ZNAK
classes['NIZ_ZNAKOVA'] = NIZ_ZNAKOVA
classes['L_ZAGRADA'] = L_ZAGRADA
classes['D_ZAGRADA'] = D_ZAGRADA
classes['<vanjska_deklaracija>'] = Vanjska_deklaracija
classes['<deklaracija>'] = Deklaracija
classes['<lista_init_deklaratora>'] = Lista_init_deklaratora

stack = []
level = 0
first = True
for line in sys.stdin:
    if first:
        line = line.strip()
        stack.append(classes.get(get_name(line), Default)(line))
        first = False
        continue

    if get_level(line) == level:
        stack.pop()
        line = line.strip()
        append_node(stack, line)
    elif get_level(line) == level + 1:
        level += 1
        line = line.strip()
        append_node(stack, line)
    elif get_level(line) < level:
        stack.pop()
        for i in range(level - get_level(line)):
            stack.pop()
        level = get_level(line)
        line = line.strip()
        append_node(stack, line)

root = stack[0]
print_tree(root, 0)
print("Parent of Boo 3 xyzzy: {}".format(root.children[0].children[1].parent.name))
# kad isprogramiramo sve te potrebne klase samo bi pokrenuli:
# root.provjeri()

