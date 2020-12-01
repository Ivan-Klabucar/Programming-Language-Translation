from EpNKA import EpNKA
class DKA:
    def __init__(self, epNKA):
        self.states = []
        self.stavke = {}
        self.transitions = {}
        self.start = -1
        self.states_to_analyze = set()
        self.alphabet = epNKA.alphabet
        self.epNKA = epNKA
        self.analyzed = set()

        self.start = self.compound_state_string(epNKA.epNeigh[epNKA.start])
        self.states_to_analyze.add(self.start)

        self.build_from_epNKA()

    def compound_state_string(self, set_of_states):
        list_of_states = list(set_of_states)
        list_of_states.sort()
        list_of_states = [str(x) for x in list_of_states]
        return ','.join(list_of_states)

    def to_set_of_states(self, compound_string):
        if compound_string == '': return set()
        return set([int(x) for x in compound_string.split(',')])

    def add_state(self, state, state_set):
        self.states.append(state)
        self.transitions[state] = {}
        self.stavke[state] = set()
        for s in state_set:
            self.stavke[state].add(self.epNKA.stavke[s])
    
    def build_from_epNKA(self):
        while self.states_to_analyze:
            x = self.states_to_analyze.pop()
            x_set = self.to_set_of_states(x)
            self.add_state(x, x_set)
            self.analyzed.add(x)
            for symb in self.alphabet:
                accumulator = set()
                for y in x_set:
                    accumulator.update(self.epNKA.transitions[y].get(symb, set()))
                if accumulator == set(): continue
                accumulator_str = self.compound_state_string(accumulator)
                self.transitions[x][symb] = accumulator_str
                if accumulator_str not in self.analyzed:
                    self.states_to_analyze.add(accumulator_str)
    
    def print_everything(self): # za vanjsku uporabu
        print("Starting state: {}".format(self.start))
        print("States:")
        for state in self.transitions:
            print("{}:".format(state))
            for symb in self.transitions[state]:
                print("  {}: {}".format(symb, self.transitions[state][symb]))
            print("Stavke: ", end="")
            for stavka in self.stavke[state]:
                print("{} ".format(stavka), end="")
            print()
                
# enka = EpNKA()
#
# enka.add_state('stavka0') # 0   Stavka moze biti bilo sto sto je hashable
# enka.add_state('stavka1') # 1
# enka.add_state('stavka2') # 2
# enka.add_state('stavka3') # 3
# enka.add_state('stavka4') # 4
# enka.set_starting_state(0)
#
# enka.add_transition(0, 'a', 1)
# enka.add_transition(1, 'b', 2)
# enka.add_transition(2, 'b', 2)
# enka.add_transition(2, 'b', 3)
# enka.add_epsilon_transition(3, 0)
# enka.add_epsilon_transition(0, 4)
#
# enka.calculate_epsilon_neighborhoods()
#
# dka = DKA(enka)
# dka.print_everything()