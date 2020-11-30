from lab2.ItemManager import *
import pickle
import sys

class SyntaxAnalyzerGenerator:
    def __init__(self):
        self.item_manager = None
        self.syn = []
        self.populate()


    def populate(self):
        f = sys.stdin
        line = f.readline().strip()
        nonterminal = line.split(' ')[1:]
        line = f.readline().strip()
        terminal = line.split(' ')[1:]
        line = f.readline().strip()
        syn = line.split(' ')[1:]
        self.syn.extend(syn)
        self.item_manager = ItemManager(terminal, nonterminal)
        curr_symbol = ''
        for line in f:
            if line[0] != ' ':
                curr_symbol = line.strip()
                continue
            else:
                self.item_manager.add_production(curr_symbol, line.strip())

