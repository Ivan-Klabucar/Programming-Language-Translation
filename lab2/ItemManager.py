class ItemManager:
    def __init__(self, terminal, nonterminal):
        self.grammar = dict()
        self.empty = set()
        self.begins = {'$':set()}
        self.nonterminal = set()
        self.terminal = set()
        self.first = None
        self.populate_terminal(terminal)
        self.populate_nonterminal(nonterminal)


    #item_tuple = (lijeva strana produkcije, desna strana produkcije kao string reprezentacija liste,
    # set završnih simbola, index tockice)
    # novo pocetno stanje: <S'>
    # simbol za kraj niza: %EOF%

    def populate_terminal(self, terminal):
        self.terminal.update(set(terminal))
        for symbol in terminal:
            self.begins[symbol] = set([symbol])

    def populate_nonterminal(self, nonterminal):
        self.nonterminal.update(set(nonterminal))
        self.first = nonterminal[0]
        for symbol in nonterminal:
            self.begins[symbol] = set([symbol])

    def add_production(self, left, right):
        self.grammar.setdefault(left, [])
        self.grammar[left].append(right.split(" "))


    def is_empty(self, series):
        verdict = True
        for symb in series:
            if symb not in self.empty and symb != '$':
                verdict = False
                break
        return verdict

    def populate_empty(self):
        found = True
        while found:
            found = False
            for production_set in self.grammar.items():
                if production_set[0] not in self.empty:
                    for production in production_set[1]:
                        if self.is_empty(production):
                            self.empty.add(production_set[0])
                            found = True
                            break
        return

    def begins_terminal(self, series):
        ret = set()
        if series == ['$']:
            return ret
        for symbol in series:
            ret.update(set(filter(lambda t: t in self.terminal, self.begins[symbol])))
            if not self.is_empty(symbol):
                break
        return ret


    def begins_shallow(self, series):
        ret = set()
        if series == ['$']:
            return ret
        for i in range(len(series)):
            ret.add(series[i])
            if series[i] not in self.empty:
                break
        return ret

    def populate_begins_shallow(self):
        for production_set in self.grammar.items():
            for production in production_set[1]:
                self.begins[production_set[0]].update(self.begins_shallow(production))

    def populate_begins(self):
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

    # item_tuple = (lijeva strana produkcije, desna strana produkcije kao string reprezentacija liste,
    # string reperezentacija seta završnih simbola, index tockice)
    def transitions(self, item_tuple):
        epsilon_transitions = []
        transition = ()
        curr_nonterminal = item_tuple[0]
        production = eval(item_tuple[1])
        curr_finish_set = eval(item_tuple[2])
        curr_position = item_tuple[3]
        if curr_position != len(production):
            transition = (production[curr_position], (curr_nonterminal, repr(production), repr(curr_finish_set), curr_position+1))
            if production[curr_position] in self.nonterminal:
                next_finish_set = set()
                for next_production in self.grammar[production[curr_position]]:
                    if curr_position + 1 == len(production):
                        next_finish_set.update(curr_finish_set)
                    else:
                        next_finish_set.update(self.begins_terminal(production[curr_position + 1:]))
                        if self.is_empty(production[curr_position+1:]):
                            next_finish_set.update(curr_finish_set)
                    if next_production == ['$']:
                        epsilon_transitions.append((production[curr_position], repr([]), repr(next_finish_set), 0))
                    else:
                        epsilon_transitions.append((production[curr_position], repr(next_production), repr(next_finish_set), 0))
        return epsilon_transitions, transition

    def get_start_item(self):
        return ('<S\'>', repr([self.first]), repr(set(['%EOF%'])), 0)



if __name__ == '__main__':
    im = ItemManager(['a','b'], ['<S>','<A>','<B>'])
    im.add_production('<S>','<A>')
    im.add_production('<A>','<B> <A>')
    im.add_production('<A>','$')
    im.add_production('<B>','a <B>')
    im.add_production('<B>','b')
    im.populate_empty()
    im.populate_begins()
    exit(0)