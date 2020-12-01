from lab2.ItemManager import *
from lab2.EpNKA import *
from lab2.DKA import *
import pickle
import sys

class SyntaxAnalyzerGenerator:
    def __init__(self):
        self.item_manager = None
        self.syn = []
        self.epNKA = EpNKA()
        self.DKA = None

    def parse_input(self):
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
        im.populate_empty()
        im.populate_begins()

    def fill_epNKA(self):
        todo = []
        todo.append(im.get_start_item())
        visited = set()
        while todo:
            curr_item = todo.pop()
            curr_item_state = self.epNKA.add_state(curr_item)
            if curr_item == im.get_start_item():
                self.epNKA.set_starting_state(curr_item_state)
            visited.add(curr_item_state)
            transitions = im.transitions(curr_item)
            for next_item in transitions[0]:
                next_item_state = self.epNKA.add_state(next_item)
                self.epNKA.add_epsilon_transition(curr_item_state, next_item_state)
                if next_item_state not in visited:
                    todo.append(next_item)
            if transitions[1]:
                next_item_state = self.epNKA.add_state(transitions[1][1])
                self.epNKA.add_transition(curr_item_state, transitions[1][0], next_item_state)
                if next_item_state not in visited:
                    todo.append(transitions[1][1])

    def generate_automata(self):
        self.parse_input()
        self.fill_epNKA()
        self.DKA = DKA(self.epNKA)

if __name__ == '__main__':
    im = ItemManager(['a','b'], ['<S>','<A>','<B>'])
    im.add_production('<S>','<A>')
    im.add_production('<A>','<B> <A>')
    im.add_production('<A>','$')
    im.add_production('<B>','a <B>')
    im.add_production('<B>','b')
    im.populate_empty()
    im.populate_begins()
    SAG = SyntaxAnalyzerGenerator()
    SAG.item_manager = im
    SAG.fill_epNKA()
    print(SAG.epNKA.print_everything())
    exit(0)
