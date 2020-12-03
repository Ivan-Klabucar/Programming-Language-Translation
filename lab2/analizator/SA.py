import pickle
import sys
from Tree import Tree, Node

class SA:
    def __init__(self, config_path):
        config_file = open(config_path, "rb")
        config = pickle.load(config_file)
        self.syn_symbols = config[0]
        self.table = config[1]
        self.uniform_symbols = []
        self.stack = ['bottom of stack', config[2]]
        self.next_uniform_row = None
        self.next_symb = None

        self.load_uniform_symbols()

    def load_uniform_symbols(self):
        f = sys.stdin
        x = f.readline().strip()
        while x:
            self.uniform_symbols.append(x)
            x = f.readline().strip()
        self.uniform_symbols.reverse()

    def get_next_uniform_row(self):
        if self.uniform_symbols:
            self.next_uniform_row = self.uniform_symbols.pop()
        else:
            self.next_uniform_row = '%EOF%'
        self.next_symb = self.symb_from_URow(self.next_uniform_row)

    def return_uniform_row(self, row):
        if row == '%EOF%':
            return
        else:
            self.uniform_symbols.append(row)
    
    def symb_from_URow(self, row):
        return row.split(' ')[0]
    
    def row_num_from_URow(self, row):
        return row.split(' ')[1]
    
    def raw_from_URow(self, row):
        return row.split(' ')[2]

    def print_expected_U_symbs(self):
        print("ocekivani uniformi znakovi:", file = sys.stderr, end="")
        for x in self.table[self.stack[-1]]:
            if x[0] != '<':
                print(" {},".format(x), file=sys.stderr, end="")
        print('', file = sys.stderr)
    
    def update_stack(self, next_state, node):
        self.stack.append(node)
        self.stack.append(next_state)

    def pomakni(self):
        next_state = self.table[self.stack[-1]][self.next_symb][1]
        self.update_stack(next_state, Node(self.next_uniform_row))

    def remove_production_from_stack(self, production_right_side_str, parent_node):
        production_right_side = eval(production_right_side_str)
        if not production_right_side:
            parent_node.add_child(Node('$'))
        while production_right_side:
            if self.symb_from_URow(self.stack[-2].data) == production_right_side.pop():
                parent_node.add_child(self.stack[-2])
                self.stack.pop()
                self.stack.pop()
            else:
                raise "krivi znakovi na stogu tijekom primjene produkcije"


    def reduciraj(self):
        self.return_uniform_row(self.next_uniform_row)
        parent = self.table[self.stack[-1]][self.next_symb][1][0]
        parent_node = Node(parent)
        self.remove_production_from_stack(self.table[self.stack[-1]][self.next_symb][1][1], parent_node)
        if self.table[self.stack[-1]][parent][0] == 'S':
            next_state = self.table[self.stack[-1]][parent][1]
            self.update_stack(next_state, parent_node)
        else:
            raise "kriva S akcija"
    
    def oporavak_od_greske(self):
        print("greska se dogodila u {}. retku".format(self.row_num_from_URow(self.next_uniform_row)), file = sys.stderr)
        self.print_expected_U_symbs()
        print("Ucitani uniformni znak: {}".format(self.next_symb), file = sys.stderr)
        print("znakovni prikaz: {}".format(self.raw_from_URow(self.next_uniform_row)), file = sys.stderr)
        while self.next_symb not in self.syn_symbols:
            self.get_next_uniform_row()
        self.return_uniform_row(self.next_uniform_row)
        while self.next_symb not in self.table[self.stack[-1]]:
            self.stack.pop()
            self.stack.pop()

    def analyze(self):
        while True:
            self.get_next_uniform_row()
            if self.next_symb in self.table[self.stack[-1]]:
                if self.table[self.stack[-1]][self.next_symb] == 'Prihvati':
                    return Tree(self.stack[-2])
                elif self.table[self.stack[-1]][self.next_symb][0] == 'P':
                    self.pomakni()
                elif self.table[self.stack[-1]][self.next_symb][0] == 'R':
                    self.reduciraj()
            else:
                self.oporavak_od_greske()
                

if __name__ == '__main__':
    sa = SA('config')
    tree = sa.analyze()
    tree.print_tree()