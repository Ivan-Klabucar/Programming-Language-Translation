from Node import Node
from TablicaZnakova import TablicaZnakova, TabZnakEntry
from HelperFunctions import *

class Izraz_pridruzivanja(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<log_ili_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        if self.isProduction('<postfiks_izraz> OP_PRIDRUZI <izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            if not self.children[0].lizraz:
                print('<izraz_pridruzivanja> ::= <postfiks_izraz> OP_PRIDRUZI({},{}) <izraz_pridruzivanja>'.format(self.children[1].br_linije, self.children[1].val))
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, self.children[0].tip):
                print('<izraz_pridruzivanja> ::= <postfiks_izraz> OP_PRIDRUZI({},{}) <izraz_pridruzivanja>'.format(self.children[1].br_linije, self.children[1].val))
                return False
            self.tip = self.children[0].tip
            self.lizraz = False
        return True
    
    def generate(self, outer=False):
        if outer:
            curr = self.children[0]
            while curr.children:
                curr = curr.children[0]
            if curr.name == "BROJ":
                return str(curr.vrijednost)
            elif curr.name == "ZNAK":
                return str(ord(curr.char))
            elif curr.name == "NIZ_ZNAKOVA":
                return curr.get_ords_with_commas()
            else:
                raise Exception(f"Somethin went wrong with global initialization in line: {curr.br_linije}") # FIX exception, ne string
        else:
            if self.isProduction('<log_ili_izraz>'):
                return self.children[0].generate()
            elif self.isProduction('<postfiks_izraz> OP_PRIDRUZI <izraz_pridruzivanja>'): # ovim se jos ne bi bavio
                return 'TREBA IMPLEMENTIRAT DO KRAJA Izraz_pridruzivanja'

class Izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<izraz> ZAREZ <izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            if not self.children[2].provjeri(): return False
            self.tip = self.children[2].tip
            self.lizraz = False
        return True

    def generate(self):
        try:
            if self.isProduction('<izraz_pridruzivanja>'):
                return self.children[0].generate()
            elif self.isProduction('<izraz> ZAREZ <izraz_pridruzivanja>'):
                return self.children[0].generate() + self.children[2].generate() # Treba provjerit mislim da bi se trebalo obrisat sta god je desni izraz stavio na stog ? TREBA IMPLEMENTIRAT
        except e:
            return 'Treba implementirat Izraz\n'

class Postfiks_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<postfiks_izraz> ::= <postfiks_izraz> L_UGL_ZAGRADA({},{}) <izraz> D_UGL_ZAGRADA({},{})'.format(self.children[1].br_linije, self.children[1].val, self.children[3].br_linije, self.children[3].val)
        print(production)

    def error_in_production2(self):
        production = '<postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA({},{}) D_ZAGRADA({},{})'.format(self.children[1].br_linije, self.children[1].val, self.children[2].br_linije, self.children[2].val)
        print(production)

    def error_in_production3(self):
        production = '<postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA({},{}) <lista_argumenata> D_ZAGRADA({},{})'.format(self.children[1].br_linije, self.children[1].val, self.children[3].br_linije, self.children[3].val)
        print(production)

    def error_in_production4(self):
        production = '<postfiks_izraz> ::= <postfiks_izraz> OP_INC({},{})'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def error_in_production5(self):
        production = '<postfiks_izraz> ::= <postfiks_izraz> OP_DEC({},{})'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<primarni_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<postfiks_izraz> L_UGL_ZAGRADA <izraz> D_UGL_ZAGRADA'):
            if not self.children[0].provjeri(): return False
            if not (is_seq(self.children[0].tip)[0] and is_X(is_seq(self.children[0].tip)[1])):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = is_seq(self.children[0].tip)[1]
            self.lizraz = not is_const(is_seq(self.children[0].tip)[1])[0]
        elif self.isProduction('<postfiks_izraz> L_ZAGRADA D_ZAGRADA'):
            if not self.children[0].provjeri(): return False
            if not is_param_void_func(self.children[0].tip):
                self.error_in_production2()
                return False
            self.tip = return_type(self.children[0].tip)
            self.lizraz = False
        elif self.isProduction('<postfiks_izraz> L_ZAGRADA <lista_argumenata> D_ZAGRADA'):
            if not self.children[0].provjeri(): return False
            if not self.children[2].provjeri(): return False
            if not (is_function(self.children[0].tip) and not is_param_void_func(self.children[0].tip) and len(self.children[2].tipovi) == len(param_types(self.children[0].tip)) and all([tilda(self.children[2].tipovi[x], param_types(self.children[0].tip)[x]) for x in range(len(self.children[2].tipovi))])):
                self.error_in_production3()
                return False
            self.tip = return_type(self.children[0].tip)
            self.lizraz = False
        elif self.isProduction('<postfiks_izraz> OP_INC'):
            if not self.children[0].provjeri(): return False
            if not (self.children[0].lizraz and tilda(self.children[0].tip,'int')):
                self.error_in_production4()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<postfiks_izraz> OP_DEC'):
            if not self.children[0].provjeri(): return False
            if not (self.children[0].lizraz and tilda(self.children[0].tip,'int')):
                self.error_in_production5()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<primarni_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<postfiks_izraz> L_UGL_ZAGRADA <izraz> D_UGL_ZAGRADA'):
            return 'TREBA IMPLEMENTIRAT Postfiks_izraz'
        elif self.isProduction('<postfiks_izraz> L_ZAGRADA D_ZAGRADA'):
            return 'TREBA IMPLEMENTIRAT Postfiks_izraz'
        elif self.isProduction('<postfiks_izraz> L_ZAGRADA <lista_argumenata> D_ZAGRADA'):
            return 'TREBA IMPLEMENTIRAT Postfiks_izraz'
        elif self.isProduction('<postfiks_izraz> OP_INC'):
            return 'TREBA IMPLEMENTIRAT Postfiks_izraz'
        elif self.isProduction('<postfiks_izraz> OP_DEC'):
            return 'TREBA IMPLEMENTIRAT Postfiks_izraz'

class Lista_argumenata(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tipovi = []
        self.lizraz = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            self.tipovi.append(self.children[0].tip)
        elif self.isProduction('<lista_argumenata> ZAREZ <izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            if not self.children[2].provjeri(): return False
            self.tipovi.extend(self.children[0].tipovi)
            self.tipovi.append(self.children[2].tip)
        return True

class Log_ili_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<log_ili_izraz> ::= <log_ili_izraz> OP_ILI({},{}) <log_i_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<log_i_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<log_ili_izraz> OP_ILI <log_i_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip,'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<log_i_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<log_ili_izraz> OP_ILI <log_i_izraz>'):
            return 'TREBA IMPLEMENTIRAT Log_ili_izraz'

class Log_i_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<log_i_izraz> ::= <log_i_izraz> OP_I({},{}) <bin_ili_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<bin_ili_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<log_i_izraz> OP_I <bin_ili_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip,'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<bin_ili_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<log_i_izraz> OP_I <bin_ili_izraz>'):
            return 'TREBA IMPLEMENTIRAT Log_i_izraz'


class Bin_ili_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<bin_ili_izraz> ::= <bin_ili_izraz> OP_BIN_ILI({},{}) <bin_xili_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<bin_xili_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<bin_ili_izraz> OP_BIN_ILI <bin_xili_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<bin_xili_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<bin_ili_izraz> OP_BIN_ILI <bin_xili_izraz>'):
            return 'TREBA IMPLEMENTIRAT Bin_ili_izraz'


class Bin_xili_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<bin_xili_izraz> ::= <bin_xili_izraz> OP_BIN_XILI({},{}) <bin_i_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<bin_i_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<bin_xili_izraz> OP_BIN_XILI <bin_i_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<bin_i_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<bin_xili_izraz> OP_BIN_XILI <bin_i_izraz>'):
            return 'TREBA IMPLEMENTIRAT Bin_xili_izraz'

class Bin_i_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<bin_i_izraz> ::= <bin_i_izraz> OP_BIN_I({},{}) <jednakosni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<jednakosni_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<bin_i_izraz> OP_BIN_I <jednakosni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<jednakosni_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<bin_i_izraz> OP_BIN_I <jednakosni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Bin_i_izraz'

class Jednakosni_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<jednakosni_izraz> ::= <jednakosni_izraz> OP_EQ({},{}) <odnosni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def error_in_production2(self):
        production = '<jednakosni_izraz> ::= <jednakosni_izraz> OP_NEQ({},{}) <odnosni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<odnosni_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<jednakosni_izraz> OP_EQ <odnosni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<jednakosni_izraz> OP_NEQ <odnosni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production2()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production2()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<odnosni_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<jednakosni_izraz> OP_EQ <odnosni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Jednakosni_izraz'
        elif self.isProduction('<jednakosni_izraz> OP_NEQ<odnosni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Jednakosni_izraz'


class Odnosni_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<odnosni_izraz> ::= <odnosni_izraz> OP_LT({},{}) <aditivni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def error_in_production2(self):
        production = '<odnosni_izraz> ::= <odnosni_izraz> OP_GT({},{}) <aditivni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def error_in_production3(self):
        production = '<odnosni_izraz> ::= <odnosni_izraz> OP_LTE({},{}) <aditivni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def error_in_production4(self):
        production = '<odnosni_izraz> ::= <odnosni_izraz> OP_GTE({},{}) <aditivni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<aditivni_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<odnosni_izraz> OP_LT <aditivni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<odnosni_izraz> OP_GT <aditivni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production2()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production2()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<odnosni_izraz> OP_LTE <aditivni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production3()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production3()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<odnosni_izraz> OP_GTE <aditivni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production4()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production4()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<aditivni_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<odnosni_izraz> OP_LT <aditivni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Odnosni_izraz'
        elif self.isProduction('<odnosni_izraz> OP_GT <aditivni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Odnosni_izraz'
        elif self.isProduction('<odnosni_izraz> OP_LTE <aditivni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Odnosni_izraz'
        elif self.isProduction('<odnosni_izraz> OP_GTE <aditivni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Odnosni_izraz'

class Aditivni_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<aditivni_izraz> ::= <aditivni_izraz> PLUS({},{}) <multiplikativni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def error_in_production2(self):
        production = '<aditivni_izraz> ::= <aditivni_izraz> MINUS({},{}) <multiplikativni_izraz>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<multiplikativni_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<aditivni_izraz> PLUS <multiplikativni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<aditivni_izraz> MINUS <multiplikativni_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_production2()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_production2()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<multiplikativni_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<aditivni_izraz> PLUS <multiplikativni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Aditivni_izraz'
        elif self.isProduction('<aditivni_izraz> MINUS <multiplikativni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Aditivni_izraz'


class Definicija_funkcije(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def error_in_production(self):
        production = '<definicija_funkcije> ::= <ime_tipa> IDN({},{}) L_ZAGRADA({},{}) KR_VOID({},{}) D_ZAGRADA({},{}) <slozena_naredba>'.format(self.children[1].br_linije, self.children[1].ime, self.children[2].br_linije, self.children[2].val, self.children[3].br_linije, self.children[3].val, self.children[4].br_linije, self.children[4].val)
        print(production)

    def error_in_production2(self):
        production = '<definicija_funkcije> ::= <ime_tipa> IDN({},{}) L_ZAGRADA({},{}) <lista_parametara> D_ZAGRADA({},{}) <slozena_naredba>'.format(self.children[1].br_linije, self.children[1].ime, self.children[2].br_linije, self.children[2].val, self.children[4].br_linije, self.children[4].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<ime_tipa> IDN L_ZAGRADA KR_VOID D_ZAGRADA <slozena_naredba>'):
            if not self.children[0].provjeri(): return False
            if is_const(self.children[0].tip)[0]:                                  #Implementirati metodu
                self.error_in_production()
                return False
            if self.tablica_znakova.function_defined(self.children[1].ime):
                self.error_in_production()
                return False
            global_idn = self.get_idn_entry(self.children[1].ime)
            if global_idn and global_idn.tip != 'funkcija(void -> {})'.format(self.children[0].tip):
                self.error_in_production()
                return False
            self.tablica_znakova.update(self.children[1].ime, TabZnakEntry(tip='funkcija(void -> {})'.format(self.children[0].tip), lizraz=False, defined=True))
            #print('Defined {}:{}'.format(self.children[1].ime, 'funkcija(void -> {})'.format(self.children[0].tip)))
            if not self.children[5].provjeri(imena=[], tipovi=[]): return False
        elif self.isProduction('<ime_tipa> IDN L_ZAGRADA <lista_parametara> D_ZAGRADA <slozena_naredba>'):
            if not self.children[0].provjeri(): return False
            if is_const(self.children[0].tip)[0]:                                  #Implementirati metodu
                self.error_in_production2()
                return False
            if self.tablica_znakova.function_defined(self.children[1].ime):
                self.error_in_production2()
                return False
            if not self.children[3].provjeri(): return False
            global_idn = self.get_idn_entry(self.children[1].ime)
            if global_idn and global_idn.tip != 'funkcija({} -> {})'.format(self.children[3].tipovi, self.children[0].tip):
                self.error_in_production2()
                return False
            self.tablica_znakova.update(self.children[1].ime, TabZnakEntry(tip='funkcija({} -> {})'.format(self.children[3].tipovi, self.children[0].tip), lizraz=False, defined=True))
            #print('Defined {}:{}'.format(self.children[1].ime, 'funkcija(void -> {})'.format(self.children[0].tip)))
            if not self.children[5].provjeri(imena=self.children[3].imena, tipovi=self.children[3].tipovi): return False                #Not rly sure kaj se od mene trazi tu, nije mijasan tekst tog uvjeta
        return True
    
    def generate(self):
        result = f'F_{self.children[1].ime}'
        imena = None
        if not self.isProduction('<ime_tipa> IDN L_ZAGRADA KR_VOID D_ZAGRADA <slozena_naredba>') and self.children[3].imena: imena = self.children[3].imena  # FIX za void funkcije bacalo error
        result += self.children[5].generate(imena=imena)
        return result



class Lista_parametara(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tipovi = []
        self.imena = []

    def error_in_production(self):
        production = '<lista_parametara> ::= <lista_parametara> ZAREZ({},{}) <deklaracija_parametra>'.format(self.children[1].br_linije, self.children[1].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<deklaracija_parametra>'):
            if not self.children[0].provjeri(): return True
            self.tipovi.append(self.children[0].tip)
            self.imena.append(self.children[0].ime)
        elif self.isProduction('<lista_parametara> ZAREZ <deklaracija_parametra>'):
            if not self.children[0].provjeri(): return False
            if not self.children[2].provjeri(): return False
            if self.children[2].ime in self.children[0].imena:
                self.error_in_production()
                return False
            self.tipovi.extend(self.children[0].tipovi)
            self.tipovi.append(self.children[2].tip)
            self.imena.extend(self.children[0].imena)
            self.imena.append(self.children[2].ime)
        return True


class Deklaracija_parametra(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.ime = None

    def error_in_production(self):
        production = '<deklaracija_parametra> ::= <ime_tipa> IDN({},{})'.format(self.children[1].br_linije, self.children[1].ime)
        print(production)

    def error_in_production2(self):
        production = '<deklaracija_parametra> ::= <ime_tipa> IDN({},{}) L_UGL_ZAGRADA({},{}) D_UGL_ZAGRADA({},{})'.format(self.children[1].br_linije, self.children[1].ime, self.children[2].br_linije, self.children[2].val, self.children[3].br_linije, self.children[3].val)
        print(production)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<ime_tipa> IDN'):
            if not self.children[0].provjeri(): return False
            if self.children[0].tip == 'void':
                self.error_in_production()
                return False
            self.tip = self.children[0].tip
            self.ime = self.children[1].ime
        elif self.isProduction('<ime_tipa> IDN L_UGL_ZAGRADA D_UGL_ZAGRADA'):
            if not self.children[0].provjeri(): return False
            if self.children[0].tip == 'void':
                self.error_in_production2()
                return False
            self.tip = 'niz({})'.format(self.children[0].tip)
            self.ime = self.children[1].ime
        return True


class Lista_izraza_pridruzivanja(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tipovi = []
        self.br_elem = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            self.tipovi.append(self.children[0].tip)
            self.br_elem = 1
        elif self.isProduction('<lista_izraza_pridruzivanja> ZAREZ <izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            if not self.children[2].provjeri(): return False
            self.tipovi.extend(self.children[0].tipovi)
            self.tipovi.append(self.children[2].tip)
            self.br_elem = self.children[0].br_elem + 1
        return True
    
    def generate(self, outer=False):
        if outer:
            if self.isProduction('<izraz_pridruzivanja>'):
                return self.children[0].generate(outer=outer)
            elif self.isProduction('<lista_izraza_pridruzivanja> ZAREZ <izraz_pridruzivanja>'):
                return self.children[0].generate(outer=outer) + ', ' + self.children[2].generate(outer=outer)
        else:
            if self.isProduction('<izraz_pridruzivanja>'):
                return self.children[0].generate(outer=outer)
            elif self.isProduction('<lista_izraza_pridruzivanja> ZAREZ <izraz_pridruzivanja>'):
                return self.children[2].generate(outer=outer) + self.children[0].generate(outer=outer) # ovo je namjerno stavljeno u obrnuti redosljed tako da prvi clan niza bude na manjoj adresi