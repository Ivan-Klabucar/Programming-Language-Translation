def get_name(string):
    return string.split()[0]

class Node:
    def __init__(self, data):
        self.name = get_name(data)
        self.data = data
        self.children = []
        self.parent = None
        self.tablica_znakova = None
    
    def add_child(self, child):
        self.children.append(child)
        child.add_parent(self)
    
    def add_parent(self, parent):
        self.parent = parent
    
    def isProduction(self, production):
        production_list = production.split(' ')
        result = False
        if len(production_list) == len(self.children):
            result = True
            i = 0
            for x in production_list:
                if x != self.children[i].name:
                    result = False
                i += 1
        return result

    def get_idn_entry(self, idn):
        return self.tablica_znakova.idn_declared(idn)