from Node import Node

global const_init_list
global num

const_init_list = []
num = 0

def to_special(c):
    if c == 'n':
        return '\n'
    elif c == 't':
        return '\t'
    elif c == '0':
        return '\0'
    elif c == '\\':
        return '\\'
    elif c == '\'':
        return '\''
    elif c == '"':
        return '"'


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
        self.label = None

        global const_init_list
        global num
        if self.is_valid():
            self.label = f'CONST_{num}'
            const_init_list.append(f'{self.label}  DW %D {self.vrijednost}')
            num += 1

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
        self.label = None
        self.char = self.znak[1:-1]

        global const_init_list
        global num
        if self.is_valid():
            self.label = f'CONST_{num}'
            const_init_list.append(f'{self.label}  DW %D {ord(self.char)}')
            num += 1
    
    def is_valid(self):
        c = self.char
        if len(c) == 0: return False
        if len(c) == 1 and c[0] != '\\': return True
        if len(c) == 1 and c[0] == '\\': return False
        if len(c) > 2: return False
        if len(c) > 1 and c[0] != '\\': return False
        if c[0] == '\\' and c[1] not in ['t', 'n', '0', '\\', '\'', '"']: 
            return False
        else:
            self.char = to_special(c[1])
        return True

class NIZ_ZNAKOVA(Node):
    def __init__(self, data):
        super().__init__(data)
        self.string = data.split(' ')[2]
        self.br_linije = data.split(' ')[1]
        self.label = None
        self.str = self.string[1:-1]
        self.true_string = None

        global const_init_list
        global num
        if self.is_valid():
            self.label = f'CONST_{num}'
            num += 1
            result = f'{self.label}   DW %D'
            result += self.get_ords_with_commas()
            const_init_list.append(result)
    
    def is_valid(self):
        s = self.str
        i = 0
        escaped = False
        true_string = ''
        while i < len(s):
            if escaped:
                if s[i] not in ['t', 'n', '0', '\\', '\'', '"']: 
                    return False
                else:
                    true_string += to_special(s[i])
                escaped = False
            else:
                if s[i] == '\\': 
                    escaped = True
                else:
                    true_string += s[i]
            i += 1
        if escaped: return False
        self.true_string = true_string
        return True
    
    def get_ords_with_commas(self):
        result = ''
        for c in self.true_string:
                result += f' {ord(c)},'
        terminator = '\0'
        result += f' {ord(terminator)},'
        return result

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