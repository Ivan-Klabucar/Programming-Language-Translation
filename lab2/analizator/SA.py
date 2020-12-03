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
        self.stack = ['bottom of stack']

        f = sys.stdin
        x = f.readline().strip()
        while x:
            self.uniform_symbols.append(x)
            x = f.readline().strip()
        print(self.uniform_symbols)
        self.uniform_symbols.reverse()
    
    def get_next_symb(self):
        if self.uniform_symbols:
            return self.uniform_symbols.pop()
        else:
            return '#end_of_file#'

    def analyze(self):
        next_symb = self.get_next_symb()


if __name__ == '__main__':
    sa = SA('config')
    sa.analyze()