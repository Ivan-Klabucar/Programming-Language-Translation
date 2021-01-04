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
        if int(self.vrijednost) < -2147483648 or int(self.vrijednost) >  2147483647:
            return False
        else:
            return True

class ZNAK(Node):
    def __init__(self, data):
        super().__init__(data)
        self.znak = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]
    
    def is_valid(self):
        c = self.znak[1:-1]
        if len(c) == 0: return False
        if len(c) == 1 and c[0] != '\\': return True
        if len(c) == 1 and c[0] == '\\': return False
        if len(c) > 1 and c[0] != '\\': return False
        if c[0] == '\\' and c[1] not in ['t', 'n', '0', '\\', '\'', '"']: return False
        return True

class NIZ_ZNAKOVA(Node):
    def __init__(self, data):
        super().__init__(data)
        self.string = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]
    
    def is_valid(self):
        s = self.string[1:-1]
        i = 0
        escaped = False
        while i < len(s):
            if escaped:
                if s[i] not in ['t', 'n', '0', '\\', '\'', '"']: return False
                escaped = False
            else:
                if s[i] == '\\': escaped = True
            i += 1
        if escaped: return False
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

class TOCKAZAREZ(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_IF(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_ELSE(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_WHILE(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_FOR(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_CONTINUE(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_BREAK(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class KR_RETURN(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_PUTA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_DIJELI(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_MOD(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_LT(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_LTE(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_GT(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_GTE(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_EQ(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_NEQ(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_I(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_ILI(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_BIN_I(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_BIN_ILI(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class OP_BIN_XILI(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class ZAREZ(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class L_VIT_ZAGRADA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)

class D_VIT_ZAGRADA(SimpleZavrsni):
    def __init__(self, data):
        super().__init__(data)