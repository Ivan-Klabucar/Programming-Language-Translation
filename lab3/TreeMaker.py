import sys

def get_name(string):
    return string.split()[0]

class Node:
    def __init__(self, data):
        self.name = get_name(data)
        self.data = data
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        self.children.append(child)
        child.add_parent(self)
    
    def add_parent(self, parent):
        self.parent = parent

class Foo(Node):
    def __init__(self, data):
        super().__init__(data)

    def say(self):
        print("Foo: Hej hej decko ti gay")
    
class Boo(Node):
    def __init__(self, data):
        super().__init__(data)

    def say(self):
        print("Boo: Odjebi u skokovima")

class Default(Node):
    def __init__(self, data):
        super().__init__(data)

    def say(self):
        print("Default")


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

