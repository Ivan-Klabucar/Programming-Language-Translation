from Node import Node

class IDN(Node):
    def __init__(self, data):
        super().__init__(data)
        self.ime = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]

class BROJ(Node):
    def __init__(self, data):
        super().__init__(data)
        self.vrijednost = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]
    
    def is_valid(self):
        if self.vrijednost < −2147483648 or self.vrijednost >  2147483647:
            return False
        else:
            return True

class ZNAK(Node):
    def __init__(self, data):
        super().__init__(data)
        self.znak = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]
    
    def is_valid(self):
        # implementirat provjeru po 4.3.2 !!!!!
        return True

class NIZ_ZNAKOVA(Node):
    def __init__(self, data):
        super().__init__(data)
        self.string = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]
    
    def is_valid(self):
        # implementirat provjeru po 4.3.2 !!!!!
        return True

class L_ZAGRADA(Node):
    def __init__(self, data):
        super().__init__(data)
        self.zagrada = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]

class D_ZAGRADA(Node):
    def __init__(self, data):
        super().__init__(data)
        self.zagrada = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]