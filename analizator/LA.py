import pickle
import EpNKA

class LexicalAnalyzer:
    def __init__(self, config_file_path, automata_dir):
        self.config_file_path = config_file_path  #file with analyzer states and corresponding automata indices and function parameters
        self.automata_dir = automata_dir  #directory with files containing definitions for every automaton
        self.automata = []  #automata at indices corresponding to their rule numbers
        self.curr_state = ""  #current analyzer state
        self.state_map = {}  #maps rule indices to analyzer states
        self.rule_map = {}  #maps rule parameters to indices
        self.line_cnt = 1  #counts lines in input document
        self.begin = 0  #index of first unanalyzed input symbol
        self.end = -1  #index of last analyzed input symbol
        self.last = -1  #index of last recognized input symbol
        self.curr_rule = -1  #last recognized rule number
        self.input = ""  #input file text

        self.configure()
        self.populate_automata()
        self.load_input()

    def configure(self):  #load confguration for this analyzer
        config_file = open(config_file_path, "rb")
        config = pickle.load(config_file)
        self.current_state = config[0]
        self.state_map = config[1]
        self.rule_map = config[2]
        config_file.close()

    def populate_automata(self):  #fill list of automata from given directory
        return

    def load_input(self):  #read from stdin into self.input
        return

    def apply_rule(self):
        params = self.rule_map[self.curr_rule]
        if(params[0] != "-"):
            self.output_symbol(params[0])
        if(params[1]):
            self.line_cnt += 1
        if(params[2] != -1):
            self.begin += params[2]
            self.end = self.begin - 1
        else:
            self.begin = self.last + 1
            self.end = self.last
        self.last = -1
        self.curr_rule = -1
        self.curr_state = params[3]

    def error_recovery(self):
        self.output_error()
        self.end = self.begin
        self.begin += 1


    def output_symbol(self, symbol):
        return

    def output_error(self):
        return

    def feed_automata(self):
        for index in self.state_map["curr_state"]:
            automata[index].giveSymb(self.input[self.end])

    def reset_automata(self):
        for automaton in self.automata:
            automaton.reset()

    def find_valid(self):
        for index in self.state_map["curr_state"]:
            if(automata[index].isValid()):
                self.curr_rule = index
                self.last = self.end
                return
        return

    def is_empty(self):
        all_empty = True
        for index in self.state_map["curr_state"]:
            all_empty = err_bool and (automata[index].current_states == {})
        return all_empty


    def analyze(self):
        while (self.begin < len(self.input)):
            self.end += 1
            self.feed_automata()
            if(self.is_empty()):
                if(self.last == -1):
                    self.error_recovery()
                else:
                    self.apply_rule()
            else:
                self.find_valid()
