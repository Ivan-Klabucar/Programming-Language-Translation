import sys
from Node import Node, get_name
from BasicNezavrsni import *
from RabiNezavrsni import *
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
classes['<init_deklarator>'] = Init_deklarator
classes['<izravni_deklarator>'] = Izravni_deklarator
classes['L_UGL_ZAGRADA'] = L_UGL_ZAGRADA
classes['D_UGL_ZAGRADA'] = D_UGL_ZAGRADA
classes['KR_VOID'] = KR_VOID
classes['<inicijalizator>'] = Inicijalizator
classes['OP_PRIDRUZI'] = OP_PRIDRUZI
classes['<izraz_pridruzivanja>'] = Izraz_pridruzivanja
classes['<izraz>'] = Izraz
classes['<postfiks_izraz>'] = Postfiks_izraz
classes['<lista_argumenata>'] = Lista_argumenata
classes['<log_ili_izraz>'] = Log_ili_izraz
classes['<log_i_izraz>'] = Log_i_izraz
classes['<bin_ili_izraz>'] = Bin_ili_izraz
classes['<bin_xili_izraz>'] = Bin_xili_izraz
classes['<bin_i_izraz>'] = Bin_i_izraz
classes['<jednakosni_izraz>'] = Jednakosni_izraz
classes['<odnosni_izraz>'] = Odnosni_izraz
classes['<aditivni_izraz>'] = Aditivni_izraz
classes['<ime_tipa>'] = Ime_tipa
classes['<specifikator_tipa>'] = Specifikator_tipa
classes['KR_CONST'] = KR_CONST
classes['KR_CHAR'] = KR_CHAR
classes['KR_INT'] = KR_INT
classes['<cast_izraz>'] = Cast_izraz
classes['<unarni_izraz>'] = Unarni_izraz
classes['OP_INC'] = OP_INC
classes['OP_DEC'] = OP_DEC
classes['<unarni_operator>'] = Unarni_operator
classes['PLUS'] = PLUS
classes['MINUS'] = MINUS
classes['OP_TILDA'] = OP_TILDA
classes['OP_NEG'] = OP_NEG
classes['<multiplikativni_izraz>'] = Multiplikativni_izraz
classes['<slozena_naredba>'] = Slozena_naredba
classes['<lista_naredbi>'] = Lista_naredbi
classes['<lista_deklaracija>'] = Lista_deklaracija
classes['<naredba>'] = Naredba

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

