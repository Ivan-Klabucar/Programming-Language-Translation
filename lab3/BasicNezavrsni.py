from Node import Node
from TablicaZnakova import TablicaZnakova, TabZnakEntry

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

class Deklaracija(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('<ime_tipa> <lista_init_deklaratora> TOCKAZAREZ'):
            if not self.children[0].provjeri(): return False
            if not self.children[1].provjeri(ntip=self.children[0].tip): return False
        return True

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

class Init_deklarator(Node):
    def __init__(self, data):
        super().__init__(data)
    
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
            # dovrsi provjeru pod 3.
        return True


class Izravni_deklarator(Node):
    def __init__(self, data):
        super().__init__(data)
        self.tip = None
        self.br_elem = None
    
    def provjeri(self, ntip):
        self.tablica_znakova = self.parent.tablica_znakova

        if self.isProduction('IDN'):
            if ntip == 'void' or self.children[0].ime in self.tablica_znakova:
                print("<izravni_deklarator> ::= IDN({},{})".format(self.children[0].br_linije, self.children[0].ime))
                return False
            lizraz = False
            if ntip in ['int', 'char']: lizraz = True
            self.tablica_znakova[self.children[0].ime] = TabZnakEntry(tip=ntip, lizraz=lizraz)
            self.tip = ntip
        elif self.isProduction('IDN L_UGL_ZAGRADA BROJ D_UGL_ZAGRADA'):
            if ntip == 'void' or self.children[0].ime in self.tablica_znakova or int(self.children[2].vrijednost) < 0 or int(self.children[2].vrijednost) > 1024:
                print("<izravni_deklarator> ::= IDN({},{}) L_UGL_ZAGRADA({},{}) BROJ({},{}) D_UGL_ZAGRADA({},{})".format(self.children[0].br_linije, self.children[0].ime, self.children[1].br_linije, self.children[1].val, self.children[2].br_linije, self.children[2].vrijednost, self.children[3].br_linije, self.children[3].val))
                return False
            idn_type = "niz({})".format(ntip)
            self.tablica_znakova[self.children[0].ime] = TabZnakEntry(tip=idn_type, lizraz=False)
            self.tip = idn_type
            self.br_elem = int(self.children[2].vrijednost)
        elif self.isProduction('IDN L_ZAGRADA KR_VOID D_ZAGRADA'):
            f_type = "funkcija(void -> {})".format(ntip)
            if self.children[0].ime in self.tablica_znakova and self.tablica_znakova[self.children[0].ime] != f_type:
                print("<izravni_deklarator> ::= IDN({},{}) L_ZAGRADA({},{}) KR_VOID({},{}) D_ZAGRADA({},{})".format(self.children[0].br_linije, self.children[0].ime, self.children[1].br_linije, self.children[1].val, self.children[2].br_linije, self.children[2].val, self.children[3].br_linije, self.children[3].val))
                return False
            if self.children[0].ime not in self.tablica_znakova: self.tablica_znakova[self.children[0].ime] = TabZnakEntry(tip=f_type, lizraz=False)
        elif self.isProduction('IDN L_ZAGRADA <lista_parametara> D_ZAGRADA'):
            if not self.children[2].provjeri(): return False
            f_type = "funkcija({} -> {})".format(self.children[2].tipovi, ntip)
            if self.children[0].ime in self.tablica_znakova and self.tablica_znakova[self.children[0].ime] != f_type:
                production = "<izravni_deklarator> ::= IDN({},{}) L_ZAGRADA({},{}) <lista_parametara> D_ZAGRADA({},{})"
                print(production.format(self.children[0].br_linije, self.children[0].ime, self.children[1].br_linije, self.children[1].val, self.children[2].br_linije, self.children[2].val))
                return False
            if self.children[0].ime not in self.tablica_znakova: self.tablica_znakova[self.children[0].ime] = TabZnakEntry(tip=f_type, lizraz=False)
        return True
