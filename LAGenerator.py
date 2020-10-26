from AutomatonDefBuilder import *
from RegDefUnpacker import *
import pickle


class LexicalAnalyzerGenerator:
    def __init__(self):
        self.reg_def_processor = RegDefUnpacker()
        self.states = []
        self.lex_unit_names = []
        self.start_state = ''
        self.state_map = {}
        self.rule_map = {}

    def generate(self, input_file):
        f = open(input_file, 'r')
        definitions = True
        line = ''
        while definitions:
            line = f.readline().strip()
            if line.find('%X') == 0:  # redak sa stanjima
                definitions = False
                continue
            self.reg_def_processor.unpack(line)
        self.states = line[3:].split(' ')
        self.start_state = self.states[0]
        for state in self.states:
            self.state_map.update({state: []})
        self.lex_unit_names = f.readline().strip()[3:].split(' ')
        automata = open('./analizator/automati.txt', 'a')
        rule_num = 0
        params = ('-', False, '', -1)
        actions = False
        curr_state = ''
        for line in f:
            line = line.strip()
            if not actions:
                if line[0] == '{':
                    actions = True
                else:
                    cloven = line.split('>')
                    curr_state = cloven[0][1:]
                    regEx = self.reg_def_processor.purify(cloven[1])
                    self.state_map[curr_state].append(rule_num)
                    params[2] == curr_state
                    automata.write("%A," + str(rule_num) + "%D\n")
                    automaton_def = AutomatonDefBuilder(regEx, rule_num)
                    automata.write(automaton_def.getAutomatonDefinition())
                    automata.write("%E\n")
            else:
                if line == '-':
                    continue
                elif line.find('NOVI_REDAK') == 0:
                    params[1] = True
                elif line.find('UDJI_U_STANJE') == 0:
                    cloven = line.split(' ')
                    params[2] = cloven[1]
                elif line.find('VRATI_SE') == 0:
                    cloven = line.split(' ')
                    params[3] = cloven[1]
                if line == '}':
                actions = False
                self.rule_map.update({rule_num: params})
                params = ('-', False, '', -1)
                rule_num+=1



#
# with open('UlaznaDatoteka.txt', 'r') as file:
#     input_lines = [line.strip() for line in file]
#
# regDefs = ""
# while (input_lines[0][0:2] != "%X"):
#     regDefs += input_lines[0]
#     input_lines.pop(0)
#
# print(regDefs)
