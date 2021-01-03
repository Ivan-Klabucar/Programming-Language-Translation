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
        if int(self.vrijednost) < −2147483648 or int(self.vrijednost) >  2147483647:
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

class SimpleZavrsni(Node):
    def __init__(self, data):
        super().__init__(data)
        self.val = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]

class L_ZAGRADA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class D_ZAGRADA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class L_UGL_ZAGRADA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class D_UGL_ZAGRADA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_VOID(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_PRIDRUZI(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_CONST(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_CHAR(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_INT(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_INC(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_DEC(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class PLUS(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class MINUS(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_TILDA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_NEG(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)