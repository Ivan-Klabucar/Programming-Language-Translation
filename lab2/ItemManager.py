class ItemManager:
    def __init__(self, nonterminal, terminal):
        self.grammar = dict()
        self.empty = set()
        self.begins = dict()
        self.nonterminal = set()
        self.terminal = set()
        self.first = None
        self.populate_terminal(terminal)
        self.populate_nonterminal(nonterminal)


    def populate_terminal(self, terminal):
        self.terminal.union(set(terminal))
        for symbol in terminal:
            self.begins[symbol] = set([symbol])

    def populate_nonterminal(self, nonterminal):
        self.nonterminal.union(set(nonterminal))
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

    def begins_single(self, series):
        ret = set()
        for i in range(len(series)):
            ret.add(series[i])
            if series[i] not in self.empty:
                break
        return ret

    def populate_begins_shallow(self):
        for production_set in self.grammar.items():
            for production in production_set[1]:
                self.begins[production_set[0]].add(self.begins_single(production))

    def populate_begins(self):
        self.populate_begins_shallow()
        changed = True
        while changed:
            changed = False
            for symbol in self.nonterminal:
                for start in self.begins[symbol]:
                    if not self.begins[symbol].superset(self.begins[start]):
                        self.begins[symbol].union(self.begins[start])
                        changed = True











if __name__ == '__main__':
    im = ItemManager()
    im.add_production("<A>", "$")
    im.add_production("<A>", "b")
    im.add_production("<B>", "<A>")
    im.add_production("<B>", "<C> b")
    im.add_production("<C>", "c")
    im.populate_empty()
    for elem in im.empty:
        print(elem)