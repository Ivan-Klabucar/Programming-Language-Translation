from Node import Node
from TablicaZnakova import TablicaZnakova, TabZnakEntry
from HelperFunctions import *

global loop_num
global cond_num

loop_num = 0
cond_num = 0

class OdmakWrapper:
    def __init__(self, odmak):
        self.val = odmak

class Prijevodna_jedinica(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self):
        if self.parent == None:                   # Tablica znakova bi bila None samo u korijenu generativnog stabla, sve ostale prijevodne jedinice naslijedile bi tablicu znakova
            self.tablica_znakova = TablicaZnakova()
        else:
            self.tablica_znakova = self.parent.tablica_znakova
        
        if self.isProduction('<vanjska_deklaracija>'):
            if not self.children[0].provjeri(): return False
        elif self.isProduction('<prijevodna_jedinica> <vanjska_deklaracija>'):
            if not self.children[0].provjeri(): return False
            if not self.children[1].provjeri(): return False
        return True
    
    def generate(self):
        result = ''
        if self.parent == None: 
            result = \
        """\
        MOVE 40000, R7 
        CALL F_main
        HALT\n"""

        if self.isProduction('<vanjska_deklaracija>'):
            result += self.children[0].generate()
        elif self.isProduction('<prijevodna_jedinica> <vanjska_deklaracija>'):
            result += self.children[0].generate()
            result += self.children[1].generate()

        return result

class Primarni_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('IDN'):
            idn_entry = self.get_idn_entry(self.children[0].ime)
            if idn_entry:
                self.tip = idn_entry.tip 
                self.lizraz = idn_entry.lizraz
            else:
                print("<primarni_izraz> ::= IDN({},{})".format(self.children[0].br_linije, self.children[0].ime))
                return False
        elif self.isProduction('BROJ'):
            if not self.children[0].is_valid(): 
                print("<primarni_izraz> ::= BROJ({},{})".format(self.children[0].br_linije, self.children[0].vrijednost))
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('ZNAK'):
            if not self.children[0].is_valid():
                print("<primarni_izraz> ::= ZNAK({},{})".format(self.children[0].br_linije, self.children[0].znak))
                return False
            self.tip = 'char'
            self.lizraz = False
        elif self.isProduction('NIZ_ZNAKOVA'):
            if not self.children[0].is_valid():
                print("<primarni_izraz> ::= NIZ_ZNAKOVA({},{})".format(self.children[0].br_linije, self.children[0].string))
                return False
            self.tip = 'niz(const(char))'
            self.lizraz = False
        elif self.isProduction('L_ZAGRADA <izraz> D_ZAGRADA'):
            if not self.children[1].provjeri(): return False
            self.tip = self.children[1].tip
            self.lizraz = self.children[1].lizraz
        return True
    
    def generate(self, for_assign=False):
        if self.isProduction('IDN'):
            idn_entry, level, is_global = self.tablica_znakova.get_idn_and_other_info(self.children[0].ime)
            result = ''
            if is_X(idn_entry.tip):
                if is_global and not for_assign:
                    result += f"""\
                LOAD R0, ({idn_entry.label})
                PUSH R0\n"""
                    return result
                
                if is_global and for_assign:
                    result += f"""\
                MOVE {idn_entry.label}, R0
                PUSH R0\n"""
                    return result
                
                if level > 0:
                    result += """\
                PUSH R5\n"""
                    cnt = level
                    while cnt > 0:
                        result += """\
                LOAD R5, (R5)\n"""
                        cnt -= 1
                
                if not for_assign: result += f"""\
                LOAD R0, (R5 + %D {idn_entry.odmak})\n"""
                else:
                    result += f"""\
                MOVE R5, R0
                ADD R0, %D {idn_entry.odmak}, R0\n"""
                
                if level > 0:
                    result += """\
                POP R5\n"""

                result += """\
                PUSH R0\n"""
                return result
            elif is_seq(idn_entry.tip):
                if is_global:
                    result += f"""\
                MOVE {idn_entry.label}, R0
                PUSH R0\n"""
                    return result
                
                if level > 0:
                    result += """\
                PUSH R5\n"""
                    cnt = level
                    while cnt > 0:
                        result += """\
                LOAD R5, (R5)\n"""
                        cnt -= 1
                
                result += f"""\
                MOVE R5, R0
                ADD  R0, %D {idn_entry.odmak}, R0\n"""
                
                if level > 0:
                    result += """\
                POP R5\n"""

                result += """\
                PUSH R0\n"""
                return result

        elif self.isProduction('BROJ') or self.isProduction('ZNAK'):
            result = f"""\
            LOAD R0, ({self.children[0].label})
            PUSH R0\n"""
            return result
        elif self.isProduction('NIZ_ZNAKOVA'):
            result = f"""\
            MOVE {self.children[0].label}, R0
            PUSH R0\n"""
            return result
        elif self.isProduction('L_ZAGRADA <izraz> D_ZAGRADA'):
            return self.children[1].generate() # for_assign=for_assign ?? kak sad ovo ide TREBA IMPLEMENTIRAT



class Vanjska_deklaracija(Node):
    def __init__(self, data):
        super().__init__(data)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<definicija_funkcije>'):
            if not self.children[0].provjeri(): return False
        elif self.isProduction('<deklaracija>'):
            if not self.children[0].provjeri(): return False
        
        return True
    
    def generate(self):
        result = ''
        if self.isProduction('<definicija_funkcije>'):
            result += self.children[0].generate()
        elif self.isProduction('<deklaracija>'):
            result += self.children[0].generate(outer=True)
        return result

class Deklaracija(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<ime_tipa> <lista_init_deklaratora> TOCKAZAREZ'):
            if not self.children[0].provjeri(): return False
            if not self.children[1].provjeri(ntip=self.children[0].tip): return False
        return True
    
    def generate(self, outer=False, odmak_w=None):
        return self.children[1].generate(outer=outer, odmak_w=odmak_w)



class Lista_init_deklaratora(Node):
    def __init__(self, data):
        super().__init__(data)

    def provjeri(self, ntip):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<init_deklarator>'):
            if not self.children[0].provjeri(ntip=ntip): return False
        elif self.isProduction('<lista_init_deklaratora> ZAREZ <init_deklarator>'):
            if not self.children[0].provjeri(ntip=ntip): return False
            if not self.children[2].provjeri(ntip=ntip): return False
        return True
    
    def generate(self, odmak_w=None, outer=False):
        if self.isProduction('<init_deklarator>'):
            return self.children[0].generate(outer=outer, odmak_w=odmak_w)
        elif self.isProduction('<lista_init_deklaratora> ZAREZ <init_deklarator>'):
            result = self.children[0].generate(outer=outer, odmak_w=odmak_w)
            result += self.children[2].generate(outer=outer, odmak_w=odmak_w)  # FIX bacalo error, quick and dirty fix Fixed ?
            return result


class Init_deklarator(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def error_in_production2(self):
        production = "<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI({},{}) <inicijalizator>"
        print(production.format(self.children[1].br_linije, self.children[1].val))
    
    def provjeri(self, ntip):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<izravni_deklarator>'):
            if not self.children[0].provjeri(ntip=ntip): return False
            if self.children[0].tip in ['const(int)', 'const(char)', 'niz(const(int))', 'niz(const(char))']:
                print("<init_deklarator> ::= <izravni_deklarator>")
                return False
        elif self.isProduction('<izravni_deklarator> OP_PRIDRUZI <inicijalizator>'):
            if not self.children[0].provjeri(ntip=ntip): return False
            if not self.children[2].provjeri(): return False
            
            if self.children[0].tip in ['int', 'char', 'const(int)', 'const(char)']:
                [retb, retv] = is_const(self.children[0].tip)
                correct_type = self.children[0].tip
                if retb: correct_type = retv
                if self.children[2].tip == None or not tilda(self.children[2].tip, correct_type):
                    self.error_in_production2()
                    return False
            elif self.children[0].tip in ['niz(int)', 'niz(char)', 'niz(const(int))', 'niz(const(char))']:
                if not self.children[2].br_elem or self.children[2].tipovi == None: 
                    self.error_in_production2()
                    return False
                if not self.children[0].br_elem or self.children[2].br_elem > self.children[0].br_elem:
                    self.error_in_production2()
                    return False
                error = False
                correct_type = is_seq(self.children[0].tip)[1]
                [retb, retv] = is_const(is_seq(self.children[0].tip)[1])
                if retb: correct_type = is_const(is_seq(self.children[0].tip)[1])[1]
                for x in self.children[2].tipovi:
                    if not tilda(x, correct_type): error = True
                if error:
                    self.error_in_production2()
                    return False
        
        return True
    
    def generate(self, outer=False, odmak_w=None):
        if outer:
            if self.isProduction('<izravni_deklarator>'):
                result = self.children[0].generate(outer=outer)
                if is_X(self.children[0].tip):
                    result += ' DW %D 0\n'
                elif is_seq(self.children[0].tip):
                    result += ' DW '
                    for i in range(self.children[0].br_elem):
                        result += '%D 0,'
                    result += '\n'
                return result
            elif self.isProduction('<izravni_deklarator> OP_PRIDRUZI <inicijalizator>'):
                result = self.children[0].generate(outer=outer)
                result += ' DW '
                result += self.children[2].generate(outer=outer) + '\n'
                return result
        else:
            if self.isProduction('<izravni_deklarator>'):
                if self.children[0].br_elem:
                    pomak = 4 * self.children[0].br_elem
                    odmak_w.val = odmak_w.val - pomak + 4
                    self.children[0].generate(odmak_w=odmak_w)
                    odmak_w.val -= 4
                    result = f"""\
            SUB R7, %D {pomak}, R7\n"""
                    return result
                else:
                    result = """\
            SUB R7, 4, R7\n"""
                    return result # FIX too many values to unpack old comment
            elif self.isProduction('<izravni_deklarator> OP_PRIDRUZI <inicijalizator>'):
                if self.children[0].br_elem:
                    pomak = 4 * self.children[0].br_elem
                    odmak_w.val = odmak_w.val - pomak + 4
                self.children[0].generate(odmak_w=odmak_w)
                odmak_w.val -= 4
                return self.children[2].generate()



class Izravni_deklarator(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.br_elem = None
    
    def provjeri(self, ntip):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('IDN'):
            if ntip == 'void' or self.children[0].ime in self.tablica_znakova.tablica:
                print("<izravni_deklarator> ::= IDN({},{})".format(self.children[0].br_linije, self.children[0].ime))
                return False
            lizraz = False
            if ntip in ['int', 'char']: lizraz = True
            self.tablica_znakova.add(key=self.children[0].ime, entry=TabZnakEntry(tip=ntip, lizraz=lizraz))
            self.tip = ntip
        elif self.isProduction('IDN L_UGL_ZAGRADA BROJ D_UGL_ZAGRADA'):
            if ntip == 'void' or self.children[0].ime in self.tablica_znakova.tablica or int(self.children[2].vrijednost) <= 0 or int(self.children[2].vrijednost) > 1024:
                print("<izravni_deklarator> ::= IDN({},{}) L_UGL_ZAGRADA({},{}) BROJ({},{}) D_UGL_ZAGRADA({},{})".format(self.children[0].br_linije, self.children[0].ime, self.children[1].br_linije, self.children[1].val, self.children[2].br_linije, self.children[2].vrijednost, self.children[3].br_linije, self.children[3].val))
                return False
            idn_type = "niz({})".format(ntip)
            self.tablica_znakova.add(self.children[0].ime, TabZnakEntry(tip=idn_type, lizraz=False))
            self.tip = idn_type
            self.br_elem = int(self.children[2].vrijednost)
        elif self.isProduction('IDN L_ZAGRADA KR_VOID D_ZAGRADA'):
            f_type = "funkcija(void -> {})".format(ntip)
            if self.children[0].ime in self.tablica_znakova.tablica and self.tablica_znakova.get(self.children[0].ime).tip != f_type:
                print("<izravni_deklarator> ::= IDN({},{}) L_ZAGRADA({},{}) KR_VOID({},{}) D_ZAGRADA({},{})".format(self.children[0].br_linije, self.children[0].ime, self.children[1].br_linije, self.children[1].val, self.children[2].br_linije, self.children[2].val, self.children[3].br_linije, self.children[3].val))
                return False
            if self.children[0].ime not in self.tablica_znakova.tablica: self.tablica_znakova.add(key=self.children[0].ime, entry=TabZnakEntry(tip=f_type, lizraz=False))
        elif self.isProduction('IDN L_ZAGRADA <lista_parametara> D_ZAGRADA'):
            if not self.children[2].provjeri(): return False
            f_type = "funkcija({} -> {})".format(self.children[2].tipovi, ntip)
            if self.children[0].ime in self.tablica_znakova.tablica and self.tablica_znakova.get(self.children[0].ime).tip != f_type:
                production = "<izravni_deklarator> ::= IDN({},{}) L_ZAGRADA({},{}) <lista_parametara> D_ZAGRADA({},{})"
                print(production.format(self.children[0].br_linije, self.children[0].ime, self.children[1].br_linije, self.children[1].val, self.children[3].br_linije, self.children[3].val))
                return False
            if self.children[0].ime not in self.tablica_znakova.tablica: self.tablica_znakova.add(key=self.children[0].ime, entry=TabZnakEntry(tip=f_type, lizraz=False))
        return True
    
    def generate(self, outer=False, odmak_w=None):
        if self.isProduction('IDN') or self.isProduction('IDN L_UGL_ZAGRADA BROJ D_UGL_ZAGRADA'):
            result = f'G_{self.children[0].ime}'
            entry = self.tablica_znakova.get(self.children[0].ime)
            entry.label = result
            if not outer and odmak_w != None: entry.odmak = odmak_w.val
            return result
        else:
            return ''

class Inicijalizator(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.br_elem = None
        self.tipovi = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<izraz_pridruzivanja>'):
            if not self.children[0].provjeri(): return False
            izraz_pridruzivanja_zavrsni = self.children[0].get_zavrsni()
            if len(izraz_pridruzivanja_zavrsni) == 1 and izraz_pridruzivanja_zavrsni[0].name == 'NIZ_ZNAKOVA':
                self.br_elem = len(izraz_pridruzivanja_zavrsni[0].true_string) + 1 # + 1 zbog '\0'
                self.tipovi = ['char'] * self.br_elem
            else:
                self.tip = self.children[0].tip
        elif self.isProduction('L_VIT_ZAGRADA <lista_izraza_pridruzivanja> D_VIT_ZAGRADA'):
            if not self.children[1].provjeri(): return False
            self.br_elem = self.children[1].br_elem
            self.tipovi = self.children[1].tipovi
        return True

    def generate(self, outer=False):
        if outer:
            if self.isProduction('<izraz_pridruzivanja>'):
                return self.children[0].generate(outer=outer)
            elif self.isProduction('L_VIT_ZAGRADA <lista_izraza_pridruzivanja> D_VIT_ZAGRADA'):
                return self.children[1].generate(outer=outer)
        else:
            if self.isProduction('<izraz_pridruzivanja>'):
                result = self.children[0].generate(outer=outer)
                izraz_pridruzivanja_zavrsni = self.children[0].get_zavrsni()
                if len(izraz_pridruzivanja_zavrsni) == 1 and izraz_pridruzivanja_zavrsni[0].name == 'NIZ_ZNAKOVA':
                    result += f"""\
                    POP R0
                    ADD R0, %D {(self.br_elem - 1) * 4}, R0\n"""
                    for i in range(self.br_elem):
                        result += """\
                    LOAD R1, (R0)
                    PUSH R1
                    SUB  R0, 4, R0\n"""
                return result
            elif self.isProduction('L_VIT_ZAGRADA <lista_izraza_pridruzivanja> D_VIT_ZAGRADA'):
                return self.children[1].generate(outer=outer)

class Ime_tipa(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<specifikator_tipa>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
        elif self.isProduction('KR_CONST <specifikator_tipa>'):
            if not self.children[1].provjeri(): return False
            if self.children[1].tip =='void':
                print('<ime_tipa> ::= KR_CONST({},{}) <specifikator_tipa>'.format(self.children[0].br_linije, self.children[0].val))
                return False
            self.tip = 'const({})'.format(self.children[1].tip)
        return True

class Specifikator_tipa(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
    
    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('KR_VOID'):
            self.tip = 'void'
        elif self.isProduction('KR_CHAR'):
            self.tip = 'char'
        elif self.isProduction('KR_INT'):
            self.tip = 'int'
        else:
            return False
        return True

class Cast_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None
    
    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<unarni_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('L_ZAGRADA <ime_tipa> D_ZAGRADA <cast_izraz>'):
            if not self.children[1].provjeri(): return False
            if not self.children[3].provjeri(): return False
            brojevni_tipovi = ['const(int)', 'const(char)', 'char', 'int']
            if self.children[1].tip not in brojevni_tipovi or self.children[3].tip not in brojevni_tipovi:  # not super duper sure abt this
                production = '<cast_izraz> ::= L_ZAGRADA({},{}) <ime_tipa> D_ZAGRADA({},{}) <cast_izraz>'
                print(production.format(self.children[0].br_linije, self.children[0].val, self.children[2].br_linije, self.children[2].val))
                return False
            self.tip = self.children[1].tip
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<unarni_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('L_ZAGRADA <ime_tipa> D_ZAGRADA <cast_izraz>'):
            return self.children[3].generate()

class Unarni_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None
    
    def error_in_production_2_or_3(self):
        production = ''
        if self.isProduction('OP_INC <unarni_izraz>'):
            production = '<unarni_izraz> ::= OP_INC({},{}) <unarni_izraz>'
        else:
            production = '<unarni_izraz> ::= OP_DEC({},{}) <unarni_izraz>'
        print(production.format(self.children[0].br_linije, self.children[0].val))

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<postfiks_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('OP_INC <unarni_izraz>') or self.isProduction('OP_DEC <unarni_izraz>'):
            if not self.children[1].provjeri(): return False
            if not self.children[1].lizraz or not tilda(self.children[1].tip, 'int'):
                self.error_in_production_2_or_3()
                return False
            self.tip = 'int'
            self.lizraz = False
        elif self.isProduction('<unarni_operator> <cast_izraz>'):
            if not self.children[1].provjeri(): return False
            if not tilda(self.children[1].tip, 'int'):
                print('<unarni_izraz> ::= <unarni_operator> <cast_izraz>')
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<postfiks_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('OP_INC <unarni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Unarni_izraz'
        elif self.isProduction('OP_DEC <unarni_izraz>'):
            return 'TREBA IMPLEMENTIRAT Unarni_izraz'
        elif self.isProduction('<unarni_operator> <cast_izraz>'):
            return 'TREBA IMPLEMENTIRAT Unarni_izraz'

class Unarni_operator(Node):
    def __init__(self, data):
        super().__init__(data)

class Multiplikativni_izraz(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.lizraz = None
    
    def error_in_group_2(self):
        production = ''
        if self.isProduction('<multiplikativni_izraz> OP_PUTA <cast_izraz>'):
            production = '<multiplikativni_izraz> ::= <multiplikativni_izraz> OP_PUTA({},{}) <cast_izraz>'
        elif self.isProduction('<multiplikativni_izraz> OP_DIJELI <cast_izraz>'):
            production = '<multiplikativni_izraz> ::= <multiplikativni_izraz> OP_DIJELI({},{}) <cast_izraz>'
        else:
            production = '<multiplikativni_izraz> ::= <multiplikativni_izraz> OP_MOD({},{}) <cast_izraz>'
        print(production.format(self.children[1].br_linije, self.children[1].val))

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<cast_izraz>'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
            self.lizraz = self.children[0].lizraz
        elif self.isProduction('<multiplikativni_izraz> OP_PUTA <cast_izraz>') or self.isProduction('<multiplikativni_izraz> OP_DIJELI <cast_izraz>') or self.isProduction('<multiplikativni_izraz> OP_MOD <cast_izraz>'):
            if not self.children[0].provjeri(): return False
            if not tilda(self.children[0].tip, 'int'):
                self.error_in_group_2()
                return False
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_in_group_2()
                return False
            self.tip = 'int'
            self.lizraz = False
        return True
    
    def generate(self):
        if self.isProduction('<cast_izraz>'):
            return self.children[0].generate()
        elif self.isProduction('<multiplikativni_izraz> OP_PUTA <cast_izraz>'):
            result = self.children[0].generate()
            result += self.children[2].generate()
            result += """\
            CALL MULTIPLY
            PUSH R6\n"""
            return result
        elif self.isProduction('<multiplikativni_izraz> OP_DIJELI <cast_izraz>'):
            result = self.children[0].generate()
            result += self.children[2].generate()
            result += """\
            CALL DIVIDE
            PUSH R6\n"""
            return result
        elif self.isProduction('<multiplikativni_izraz> OP_MOD <cast_izraz>'):
            result = self.children[0].generate()
            result += self.children[2].generate()
            result += """\
            CALL MOD
            PUSH R6\n"""
            return result

class Slozena_naredba(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self, imena=None, tipovi=None):
        self.tablica_znakova = TablicaZnakova(parent=self.parent.tablica_znakova)
        if imena and tipovi:
            for x in imena:
                lizraz = False
                curr_type = tipovi.pop(0)
                if curr_type in ['int', 'char']: lizraz = True
                self.tablica_znakova.add(key=x, entry=TabZnakEntry(tip=curr_type, lizraz=lizraz))

        if self.isProduction('L_VIT_ZAGRADA <lista_naredbi> D_VIT_ZAGRADA'):
            if not self.children[1].provjeri(new_tablica=self.tablica_znakova): return False
        elif self.isProduction('L_VIT_ZAGRADA <lista_deklaracija> <lista_naredbi> D_VIT_ZAGRADA'):
            if not self.children[1].provjeri(new_tablica=self.tablica_znakova): return False
            if not self.children[2].provjeri(new_tablica=self.tablica_znakova): return False
        return True
    
    def generate(self, imena=None, num = -1):
        if imena:
            i = 2
            for ime in imena.reverse():
                self.tablica_znakova.get(ime).odmak = i * 4
                i += 1

        result = """\
        PUSH R5
        MOVE R7, R5\n"""

        if self.isProduction('L_VIT_ZAGRADA <lista_naredbi> D_VIT_ZAGRADA'):
            result += self.children[1].generate(num)
        elif self.isProduction('L_VIT_ZAGRADA <lista_deklaracija> <lista_naredbi> D_VIT_ZAGRADA'):
            result += self.children[1].generate(odmak_w=OdmakWrapper(-4))
            result += self.children[2].generate(num)
        
        result += """\
        MOVE R5, R7
        POP  R5\n"""

        return result


class Lista_naredbi(Node):
    def __init__(self, data):
        super().__init__(data)

    def provjeri(self, new_tablica=None):
        if new_tablica:
            self.tablica_znakova = new_tablica
        else:
            self.tablica_znakova = self.parent.tablica_znakova
        
        if self.isProduction('<naredba>'):
            if not self.children[0].provjeri(): return False
        elif self.isProduction('<lista_naredbi> <naredba>'):
            if not self.children[0].provjeri(): return False
            if not self.children[1].provjeri(): return False
        return True
    
    def generate(self, num = -1):
        result = ''
        if self.isProduction('<naredba>'):
            result += self.children[0].generate(num)
        elif self.isProduction('<lista_naredbi> <naredba>'):
            result += self.children[0].generate(num)
            result += self.children[1].generate(num)
        return result

class Lista_deklaracija(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self, new_tablica=None):
        if new_tablica:
            self.tablica_znakova = new_tablica
        else:
            self.tablica_znakova = self.parent.tablica_znakova
        
        if self.isProduction('<deklaracija>'):
            if not self.children[0].provjeri(): return False
        elif self.isProduction('<lista_deklaracija> <deklaracija>'):
            if not self.children[0].provjeri(): return False
            if not self.children[1].provjeri(): return False
        return True
    
    def generate(self, odmak_w=None):
        result = ''
        if self.isProduction('<deklaracija>'):
            result += self.children[0].generate(odmak_w=odmak_w)
        elif self.isProduction('<lista_deklaracija> <deklaracija>'):
            result += self.children[0].generate(odmak_w=odmak_w)
            result += self.children[1].generate(odmak_w=odmak_w)
        return result

class Naredba(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<slozena_naredba>')  or  \
           self.isProduction('<izraz_naredba>')    or  \
           self.isProduction('<naredba_grananja>') or  \
           self.isProduction('<naredba_petlje>')   or  \
           self.isProduction('<naredba_skoka>'):
            
            if not self.children[0].provjeri(): return False
        return True

    def generate(self, num = -1):
        if not self.isProduction('<naredba_petlje>') and not self.isProduction('<izraz_naredba>'):
            return self.children[0].generate(num=num)
        else:
            return self.children[0].generate()

class Izraz_naredba(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
    
    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('TOCKAZAREZ'):
            self.tip = 'int'
        elif self.isProduction('<izraz> TOCKAZAREZ'):
            if not self.children[0].provjeri(): return False
            self.tip = self.children[0].tip
        return True

    def generate(self):
        if self.isProduction('TOCKAZAREZ'):
            return ''
        elif self.isProduction('<izraz> TOCKAZAREZ'):
            result = self.children[0].generate()
            result += """\
            ADD R7, 4, R7\n"""
            return result

class Naredba_grananja(Node):
    def __init__(self, data):
        super().__init__(data)

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('KR_IF L_ZAGRADA <izraz> D_ZAGRADA <naredba>'):
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                production = '<naredba_grananja> ::= KR_IF({},{}) L_ZAGRADA({},{}) <izraz> D_ZAGRADA({},{}) <naredba>'
                print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val, self.children[3].br_linije, self.children[3].val))
                return False
            if not self.children[4].provjeri(): return False
        elif self.isProduction('KR_IF L_ZAGRADA <izraz> D_ZAGRADA <naredba> KR_ELSE <naredba>'):
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                production = '<naredba_grananja> ::= KR_IF({},{}) L_ZAGRADA({},{}) <izraz> D_ZAGRADA({},{}) <naredba> KR_ELSE({},{}) <naredba>'
                print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val, self.children[3].br_linije, self.children[3].val, self.children[5].br_linije, self.children[5].val))
                return False
            if not self.children[4].provjeri(): return False
            if not self.children[6].provjeri(): return False
        return True

    def generate(self, num = -1):
        global cond_num
        result = ''
        local_num = cond_num
        cond_num += 1

        result = ''
        if self.isProduction('KR_IF L_ZAGRADA <izraz> D_ZAGRADA <naredba>'):
            result += f"""IF_{local_num}\n"""
            result += self.children[2].generate()
            result += f"""\
        POP R0
        CMP R0, 0
        JR_EQ ENDIF_{local_num}\n"""
            result += self.children[4].generate(num)
            result += f"""ENDIF_{local_num}\n"""
        elif self.isProduction('KR_IF L_ZAGRADA <izraz> D_ZAGRADA <naredba> KR_ELSE <naredba>'):
            result += f"""IF_{local_num}\n"""
            result += self.children[2].generate()
            result += f"""\
        POP R0
        CMP R0, 0
        JR_EQ ELSE_{local_num}\n"""
            result += self.children[4].generate(num)
            result +=f"""\
        JR ENDIF_{local_num}\n"""
            result += f"""ELSE_{local_num}\n"""
            result += self.children[6].generate(num)
            result += f"""ENDIF_{local_num}"""
        return result;


class Naredba_petlje(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def error_1(self):
        production = '<naredba_petlje> ::= KR_WHILE({},{}) L_ZAGRADA({},{}) <izraz> D_ZAGRADA({},{}) <naredba>'
        print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val, self.children[3].br_linije, self.children[3].val))

    def error_2(self):
        production = '<naredba_petlje> ::= KR_FOR({},{}) L_ZAGRADA({},{}) <izraz_naredba> <izraz_naredba> D_ZAGRADA({},{}) <naredba>'
        print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val, self.children[4].br_linije, self.children[4].val))

    def error_3(self):
        production = '<naredba_petlje> ::= KR_FOR({},{}) L_ZAGRADA({},{}) <izraz_naredba> <izraz_naredba> <izraz> D_ZAGRADA({},{}) <naredba>'
        print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val, self.children[5].br_linije, self.children[5].val))

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('KR_WHILE L_ZAGRADA <izraz> D_ZAGRADA <naredba>'):
            if not self.children[2].provjeri(): return False
            if not tilda(self.children[2].tip, 'int'):
                self.error_1()
                return False
            if not self.children[4].provjeri(): return False
        elif self.isProduction('KR_FOR L_ZAGRADA <izraz_naredba> <izraz_naredba> D_ZAGRADA <naredba>'):
            if not self.children[2].provjeri(): return False
            if not self.children[3].provjeri(): return False
            if not tilda(self.children[3].tip, 'int'):
                self.error_2()
                return False
            if not self.children[5].provjeri(): return False
        elif self.isProduction('KR_FOR L_ZAGRADA <izraz_naredba> <izraz_naredba> <izraz> D_ZAGRADA <naredba>'):
            if not self.children[2].provjeri(): return False
            if not self.children[3].provjeri(): return False
            if not tilda(self.children[3].tip, 'int'):
                self.error_3()
                return False
            if not self.children[4].provjeri(): return False
            if not self.children[6].provjeri(): return False
        return True

    def generate(self):
        global loop_num
        result = ''
        local_num = loop_num
        loop_num += 1

        if self.isProduction('KR_WHILE L_ZAGRADA <izraz> D_ZAGRADA <naredba>'):
            result += f"""LOOP_{local_num} \n"""
            result += self.children[2].generate()
            result += f"""\
             POP R0
             CMP R0, 0
             JR_EQ ENDLOOP_{local_num}\n"""
            result += self.children[4].generate(num = local_num)
            result += f"""INCLOOP_{local_num}\n"""
            result += f"""\
             JR LOOP_{local_num}
ENDLOOP_{local_num}\n"""
        elif self.isProduction('KR_FOR L_ZAGRADA <izraz_naredba> <izraz_naredba> D_ZAGRADA <naredba>'):
            result += self.children[2].generate()
            result += f"""LOOP_{local_num} \n"""
            if self.children[3].isProduction('<izraz> TOCKAZAREZ'):
                result += self.children[3].children[0].generate()
                result += f"""\
                 POP R0
                 CMP R0, 0
                 JR_EQ ENDLOOP_{local_num}\n"""
            result += self.children[5].generate(num = local_num)
            result += f"""INCLOOP_{local_num}\n"""
            result += f"""\
             JR LOOP_{local_num}
ENDLOOP_{local_num}\n"""
        elif self.isProduction('KR_FOR L_ZAGRADA <izraz_naredba> <izraz_naredba> <izraz> D_ZAGRADA <naredba>'):
            result += self.children[2].generate()
            result += f"""LOOP_{local_num} \n"""
            if self.children[3].isProduction('<izraz> TOCKAZAREZ'):
                result += self.children[3].children[0].generate()
                result += f"""\
            POP R0
            CMP R0, 0
            JR_EQ ENDLOOP_{local_num}\n"""
            result += self.children[6].generate(num = local_num)
            result += f"""INCLOOP_{local_num}\n"""
            result += self.children[4].generate()
            result += f"""\
            JR LOOP_{local_num}
ENDLOOP_{local_num}\n"""

        return result

class Naredba_skoka(Node):         # Ovo tu treb jos onak fkt iztestirat
    def __init__(self, data):
        super().__init__(data)
    
    def error_1(self):
        production = ''
        if self.isProduction('KR_BREAK TOCKAZAREZ'):
            production = '<naredba_skoka> ::= KR_BREAK({},{}) TOCKAZAREZ({},{})'
        else:
            production = '<naredba_skoka> ::= KR_CONTINUE({},{}) TOCKAZAREZ({},{})'
        print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val))

    def error_2(self):
        production = '<naredba_skoka> ::= KR_RETURN({},{}) TOCKAZAREZ({},{})'
        print(production.format(self.children[0].br_linije, self.children[0].val, self.children[1].br_linije, self.children[1].val))
    
    def error_3(self):
        production = '<naredba_skoka> ::= KR_RETURN({},{}) <izraz> TOCKAZAREZ({},{})'
        print(production.format(self.children[0].br_linije, self.children[0].val, self.children[2].br_linije, self.children[2].val))

    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('KR_BREAK TOCKAZAREZ') or self.isProduction('KR_CONTINUE TOCKAZAREZ'):
            curr = self.parent
            isInLoop = False
            while curr:
                if curr.name == '<naredba_petlje>':
                    isInLoop = True
                    break
                curr = curr.parent
            if not isInLoop:
                self.error_1()
                return False
        elif self.isProduction('KR_RETURN TOCKAZAREZ'):
            curr = self.parent
            isInVoidFunction = False
            while curr:
                if curr.name == '<definicija_funkcije>':
                    func_name = curr.children[1].ime
                    func_entry = curr.get_idn_entry(func_name)
                    if not func_entry: break
                    isInVoidFunction = is_void_func(func_entry.tip)
                    break
                curr = curr.parent
            if not isInVoidFunction:
                self.error_2()
                return False
        elif self.isProduction('KR_RETURN <izraz> TOCKAZAREZ'):
            if not self.children[1].provjeri(): return False
            curr = self.parent
            isInFuncOfCorrectType = False
            while curr:
                if curr.name == '<definicija_funkcije>':
                    func_name = curr.children[1].ime
                    func_entry = curr.get_idn_entry(func_name)
                    if not func_entry: break
                    isInFuncOfCorrectType = tilda(self.children[1].tip, return_type(func_entry.tip))
                    break
                curr = curr.parent
            if not isInFuncOfCorrectType:
                self.error_3()
                return False
        return True

    def generate(self, num = -1):
        result = ''

        if self.isProduction('KR_BREAK TOCKAZAREZ'):
            result += f"""\
        JR ENDLOOP_{num}"""
        elif self.isProduction('KR_CONTINUE TOCKAZAREZ'):
            result += f"""\
        JR INCLOOP_{num}"""
        elif self.isProduction('KR_RETURN TOCKAZAREZ'):
            result += """\
        MOVE R5, R7
        POP  R5
        RET\n"""
        elif self.isProduction('KR_RETURN <izraz> TOCKAZAREZ'):
            result += self.children[1].generate()
            result += """\
        POP R6
        MOVE R5, R7
        POP  R5
        RET\n"""
        return result






