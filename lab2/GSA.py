from ItemManager import *
import pickle
import sys

class SyntaxAnalyzerGenerator:
    def __init__(self):
        self.item_manager = None


    def populate(self):
        f = sys.stdin
        line = f.readline().strip()
        nonterminal = line.split(' ')[1:]
        line = f.readline().strip()
        terminal = line.split(' ')[1:]
        line = f.readline().strip()
        syn = line.split(' ')[1:]
        self.item_manager = ItemManager(terminal, nonterminal)
