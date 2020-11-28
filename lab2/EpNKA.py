class EpNKA:
    def __init__(self):
        self.start = -1
        self.last_state = -1
        #self.states = [] # all possible states that the automaton can be in
        self.validStates = [] # obvious
        self.transitions = {} # mapping of all possible transitions 
        self.epNeigh = {} # all epsilon neighborhoods 
        self.visited = {} # helper data structure for dfs, keeps track of visited nodes
        self.alphabet = set()
        self.stavke = {}
    
    def set_starting_state(self, x):  # za vanjsku uporabu
        if x in self.transitions:
            self.start = x
        else:
            raise "starting state must be an existing state"
    
    def add_state(self, stavka): # za vanjsku uporabu
        self.last_state += 1
        new_state = self.last_state
        self.transitions[new_state] = {}
        self.epNeigh[new_state] = set([new_state])
        self.stavke[new_state] = stavka     # stavka moze biti bilo kakav objekt
        self.visited[new_state] = False
        return new_state
    
    def states_not_in_trans(self, from_state, to_state): 
        if from_state not in self.transitions or to_state not in self.transitions:
            raise "{} or {} not in transitions".format(from_state, to_state)

    def add_transition(self, from_state, symb, to_state): # za vanjsku uporabu
        self.states_not_in_trans(from_state, to_state)
        self.transitions[from_state].setdefault(symb, set())
        self.transitions[from_state][symb].add(to_state)
        self.alphabet.add(symb)
    
    def add_epsilon_transition(self, from_state, to_state): # za vanjsku uporabu
        self.states_not_in_trans(from_state, to_state)
        self.transitions[from_state].setdefault('epsilon', set())
        self.transitions[from_state]['epsilon'].add(to_state)
        self.epNeigh[from_state].add(to_state)

    def calculate_epsilon_neighborhoods(self): # za vanjsku uporabu
        for w in self.transitions:
            self.ep_neighborhood(w)
        self.expand_transitions()

    def ep_neighborhood(self, state):
        states_to_try = self.epNeigh[state]
        result = set()
        while states_to_try:
            x = states_to_try.pop()
            result.add(x)
            if self.visited[x]:
                result.update(self.epNeigh[x])
            else:
                for q in self.epNeigh[x]: 
                    if q not in result: states_to_try.add(q)
        self.visited[state] = True
        self.epNeigh[state].update(result)
    
    def expand_transitions(self):
        for x in self.transitions:
            for y in self.transitions[x]:
                accumulator = set()
                for q in self.transitions[x][y]:
                    accumulator.update(self.epNeigh[q])
                self.transitions[x][y].update(accumulator)

    def print_everything(self): # za vanjsku uporabu
        print("Starting state: {}".format(self.start))
        print("Transitions:")
        for state in self.transitions:
            print("{}:".format(state))
            for symb in self.transitions[state]:
                print("  {}:".format(symb), end="")
                for to_state in self.transitions[state][symb]:
                    print(" {},".format(to_state), end="")
                print()
            print("  epsilon neigh: {}".format(self.epNeigh[state]))
            print()


# automaton = EpNKA()

# automaton.add_state() # 0
# automaton.add_state() # 1
# automaton.add_state() # 2
# automaton.add_state() # 3
# automaton.add_state() # 4
# automaton.set_starting_state(0)

# automaton.add_transition(0, 'a', 1)
# automaton.add_transition(1, 'b', 2)
# automaton.add_transition(2, 'b', 2)
# automaton.add_transition(2, 'b', 3)
# automaton.add_epsilon_transition(3, 0)
# automaton.add_epsilon_transition(0, 4)

# automaton.calculate_epsilon_neighborhoods()

# automaton.print_everything()



