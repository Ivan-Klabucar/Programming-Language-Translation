class EpNKA:
    def __init__(self, rule, file_path):
        self.rule = rule  #automaton's rule number
        self.start = '' #starting state of automaton
        self.file_path = file_path #definition of automaton
        self.states = [] # all possible states that the automaton can be in
        self.validStates = [] # obvious
        self.transitions = {} # mapping of all possible transitions 
        self.epNeigh = {} # all epsilon neighborhoods 
        self.visited = {} # helper data structure for dfs, keeps track of visited nodes
        
        self.populate_data_structures()
        self.calculate_epsilon_neighborhoods()
        self.expand_transitions()

        self.current_states = self.epNeigh[self.start]
    
    def populate_data_structures(self): #bez 1. i 3. linije orginalnog ulaza iz utr labosa
        with open(self.file_path, 'r') as file:
            input_lines = [line.strip() for line in file]

        #inputting all the possible states
        i = 0
        for x in input_lines[0].split(","):
            self.states.append(x)
            self.transitions[x] = {}
            self.epNeigh[x] = set([x])
            self.visited[x] = False
            i += 1
        input_lines.pop(0)
        
        #inputting valid states
        for x in input_lines[0].split(","):
            self.validStates.append(x)
        input_lines.pop(0)
        
        #starting state
        self.start = input_lines[0]
        input_lines.pop(0)

        #inputting the transition function
        for x in input_lines:
            if(x == ''): continue
            fx = x.split("->")
            temp = []
            temp.extend(fx[0].split(","))
            temp.append(fx[1].split(","))
            if temp[2][0] == "#":
                temp[2] = []
            self.transitions[temp[0]][temp[1]] = set(temp[2])
            if temp[1] == '$':
                self.epNeigh[temp[0]].update(temp[2]) 



    def calculate_epsilon_neighborhoods(self):
        for w in self.states:
            self.ep_neighborhood(w)
    
    #function for finding epsilon neighborhoods of each state
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


    #use the epsilon neighborhoods to expand transitions to all possibilities 
    def expand_transitions(self):
        for x in self.states:
            for y in self.transitions[x]:
                temporary = set()
                for q in self.transitions[x][y]:
                    temporary.update(self.epNeigh[q])
                self.transitions[x][y].update(temporary)
    
    def giveSymb(self, symbol):
        accumulator = set()
        for x in self.current_states:
            accumulator.update(self.transitions[x].get(symbol, set()))
        self.current_states = accumulator
    
    def isValid(self):
        for x in self.current_states:
            if x in self.validStates:
                return True
        return False
    
    def reset(self):
        self.current_states = self.epNeigh[self.start]

def print_states_from_set(states_for_print, beginning = "|"):
    print(beginning, end="")
    if states_for_print:
        print(",".join(sorted(states_for_print)), end="")
    else:
        print("#", end='')

x = EpNKA(1, "def.txt")
sequences = []
sequences.extend([x.split(",") for x in input().split("|")])

for sequence in sequences:
    print_states_from_set(x.current_states, beginning='')
    for syb in sequence:
        x.giveSymb(syb)
        print_states_from_set(x.current_states)
    x.reset()

    print()

#testiranje se vrsi ovako: u def.txt stavi se definicija automata
#sintaksa za def.txt je opisana u kako_izgleda_def.txt
#ulaz.txt ima nizove znakova koje ocemo testirati sintaksa je <simbol>,<simbol>,....<simbol>|<simbol>,<simbol>,....<simbol>....
# | oznacava novi niz
#ispis ove datoteke je identican kao u labosu za utr prvi

