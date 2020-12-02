from lab2.ItemManager import *
from lab2.EpNKA import *
from lab2.DKA import *
import pickle
import sys

class SyntaxAnalyzerGenerator:
    def __init__(self):
        self.item_manager = None  # Stores grammar and generates LR(1) items
        self.syn = []  # List of synchronisation symbols
        self.epNKA = EpNKA()  # Epsilon NFA that models transitions between various LR(1) items
        self.DKA = None  # DFA that models transitions between LR(1) parser states
        self.table = {}  # LR(1) parser table (state: (input symbol/nonterminal symbol: action))

    # item_tuple = (lijeva strana produkcije, desna strana produkcije kao string reprezentacija liste,
    # string reprezentacija seta završnih simbola, index tockice, redni broj odgovarajuce produkcije)
    # novo pocetno stanje: <S'>
    # simbol za kraj niza: %EOF%
    # formati akcija:
    #   ('P', stanje) - pomakni
    #   ('S', stanje) - stavi
    #   ('R', (lijeva strana produkcije, desna strana produkcije kao string reprezentacija liste, redni br. produkcije))

    def parse_input(self):  # Reading input definition of LR(1) parser and populating basic data structures
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

    def fill_epNKA(self):  # Generating items and linking them with their respective transitions
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
        self.epNKA.calculate_epsilon_neighborhoods()

    def generate_automata(self):
        # self.parse_input() Otkomentirati prilikom finalne predaje
        # self.fill_epNKA() Otkomentirati prilikom finalne predaje
        self.DKA = DKA(self.epNKA)

    def generate_table(self):  # Generates LR(1) table
        for state in self.DKA.states:
            self.table[state] = {}
            for transition in self.DKA.transitions[state].items():
                if transition[0] not in self.item_manager.nonterminal:
                    self.table[state].update({transition[0]:('P', transition[1])})
                else:
                    self.table[state].update({transition[0]:('S', transition[1])})
            for stavka in self.DKA.stavke[state]:
                if self.item_manager.is_finishing_item(stavka):
                    for symbol in eval(stavka[2]):
                        if self.table[state].get(symbol):
                            if self.table[state][symbol][0] == 'P':
                                print('Pomakni/Reduciraj proturječje:'
                                      'pomakni({})/reduciraj({}->{})\n'
                                      'Razrješeno u korist akcije pomakni'
                                      .format(self.table[state][symbol][1], stavka[0], stavka[1]),
                                      file=sys.stderr)
                                continue
                            elif self.table[state][symbol][0] == 'R':
                                if stavka[4] < self.table[state][symbol][1][2]:
                                    failed_reduction = self.table[state][symbol][1]
                                    self.table[state][symbol] = ('R', (stavka[0], stavka[1], stavka[4]))
                                    successful_reduction = self.table[state][symbol][1]
                                else:
                                    successful_reduction = self.table[state][symbol][1]
                                    failed_reduction = (stavka[0], stavka[1], stavka[4])
                                print('Pomakni/Reduciraj proturječje:'
                                      'reduciraj({}->{})/reduciraj({}->{})\n'
                                      'Razrješeno u korist prve navedene redukcije'
                                      .format(successful_reduction[0], successful_reduction[1], failed_reduction[0], failed_reduction[1]),
                                      file=sys.stderr)
                        else:
                            self.table[state].update({symbol:('R', (stavka[0], stavka[1], stavka[4]))})

    def generate(self):  # External use: the only method that should be used outside of this class, generates config file for SA
        self.generate_automata()
        self.generate_table()
        config = (self.syn, self.table)
        config_file = open('./analizator/config', 'wb')
        pickle.dump(config, config_file)  # Config file format: ([sync], {table})
        config_file.close()

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
    SAG.epNKA.print_everything()
    SAG.generate_automata()
    SAG.generate_table()
    SAG.generate()
    exit(0)
