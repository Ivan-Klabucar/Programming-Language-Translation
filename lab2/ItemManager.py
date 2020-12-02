class ItemManager:
    def __init__(self, terminal, nonterminal):
        self.curr_production = 0  # Counter for determining production priority
        self.grammar = dict()  # Storing productions (nonterminal symbol : list of right sides of productions)
        self.empty = set()  # Set of empty nonterminal symbols
        self.begins = {'$': set()}  # Dictionary of beginning symbols for nonterminal and terminal symbols
        self.nonterminal = set()  # Set of nonterminal symbols in the given grammar
        self.terminal = set()  # Set of terminal symbols in the given grammar
        self.first = None  # Beginning nonterminal symbol
        self.populate_terminal(terminal)
        self.populate_nonterminal(nonterminal)

    # item_tuple = (lijeva strana produkcije, desna strana produkcije kao string reprezentacija liste,
    # string reprezentacija seta završnih simbola, index tockice, redni broj odgovarajuce produkcije)
    # novo pocetno stanje: <S'>
    # simbol za kraj niza: %EOF%

    # External use: loading terminal symbols and filling the reflexive closure of the 'begins' relation
    def populate_terminal(self, terminal):  # input format: list of terminal symbols(strings)
        self.terminal.update(set(terminal))
        for symbol in terminal:
            self.begins[symbol] = set([symbol])

    # External use: loading nonterminal symbols and filling the reflexive closure of the 'begins' relation
    def populate_nonterminal(self, nonterminal):  # input format: list of nonterminal symbols(strings)
        self.nonterminal.update(set(nonterminal))
        self.first = nonterminal[0]
        for symbol in nonterminal:
            self.begins[symbol] = set([symbol])

    # External use: adding production to grammar
    def add_production(self, left, right):  # input format: left = nonterminal symbol(string), right = stripped input string as given in input file
        self.grammar.setdefault(left, [])
        self.grammar[left].append((self.curr_production, right.split(" ")))
        self.curr_production += 1

    # Internal use: determining shallow emptiness of a list of symbols
    def is_empty(self, series):  # input format: list of symbols(strings)
        verdict = True
        for symbol in series:
            if symbol not in self.empty and symbol != '$':
                verdict = False
                break
        return verdict

    def populate_empty(self):  # External use: filling set of empty symbols
        found = True
        while found:
            found = False
            for production_set in self.grammar.items():
                if production_set[0] not in self.empty:
                    for production in production_set[1]:
                        if self.is_empty(production[1]):
                            self.empty.add(production_set[0])
                            found = True
                            break
        return

    def begins_terminal(self, series):  # Internal use: finding terminal symbols that start a given list of symbols
        ret = set()
        if series == ['$']:
            return ret
        for symbol in series:
            ret.update(set(filter(lambda t: t in self.terminal, self.begins[symbol])))
            if symbol not in self.empty:
                break
        return ret

    def begins_shallow(self, series):  # Internal use: determining shallow beginning symbols of a list of symbols
        ret = set()
        if series == ['$']:
            return ret
        for symbol in series:
            ret.add(symbol)
            if symbol not in self.empty:
                break
        return ret

    def populate_begins_shallow(self):  # Internal use: shallow filling of reflexive and transitive closure of the 'begins' relation
        for production_set in self.grammar.items():
            for production in production_set[1]:
                self.begins[production_set[0]].update(self.begins_shallow(production[1]))

    def populate_begins(self):  # External use: complete filling of reflexive and transitive closure of the 'begins' relation
        self.populate_begins_shallow()
        changed = True
        while changed:
            changed = False
            for symbol in self.nonterminal:
                start_iteration = set(self.begins[symbol])
                for start in start_iteration:
                    if not self.begins[symbol].issuperset(self.begins[start]):
                        self.begins[symbol].update(self.begins[start])
                        changed = True

    def transitions(self, item_tuple):  # External use: calculating next items and respective epsilon and regular transitions
        epsilon_transitions = []
        transition = ()
        curr_nonterminal = item_tuple[0]
        production = eval(item_tuple[1])
        curr_finish_set = eval(item_tuple[2])
        curr_position = item_tuple[3]
        curr_priority = item_tuple[4]
        if curr_position != len(production):
            transition = (production[curr_position],
                          (curr_nonterminal, repr(production), repr(curr_finish_set), curr_position + 1, curr_priority))
            if production[curr_position] in self.nonterminal:
                next_finish_set = set()
                for next_production in self.grammar[production[curr_position]]:
                    if curr_position + 1 == len(production):
                        next_finish_set.update(curr_finish_set)
                    else:
                        next_finish_set.update(self.begins_terminal(production[curr_position + 1:]))
                        if self.is_empty(production[curr_position + 1:]):
                            next_finish_set.update(curr_finish_set)
                    if next_production[1] == ['$']:
                        epsilon_transitions.append(
                            (production[curr_position], repr([]), repr(next_finish_set), 0, next_production[0]))
                    else:
                        epsilon_transitions.append((production[curr_position], repr(next_production[1]),
                                                    repr(next_finish_set), 0, next_production[0]))
        return epsilon_transitions, transition

    def get_start_item(self):
        return ('<S\'>', repr([self.first]), repr(set(['%EOF%'])), 0, -1)

    @staticmethod
    def is_finishing_item(item):  # External use: determines whether an item should be reduced
        return item[3] == len(eval(item[1]))


if __name__ == '__main__':
    im = ItemManager(['a', 'b'], ['<S>', '<A>', '<B>'])
    im.add_production('<S>', '<A>')
    im.add_production('<A>', '<B> <A>')
    im.add_production('<A>', '$')
    im.add_production('<B>', 'a <B>')
    im.add_production('<B>', 'b')
    im.populate_empty()
    im.populate_begins()
    exit(0)
