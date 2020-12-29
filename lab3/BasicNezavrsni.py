from Node import Node
from TablicaZnakova import TablicaZnakova

class Prijevodna_jedinica(Node):
    def __init__(self, data):
        super().__init__(data)
    
    def provjeri(self):
        if self.parent == None:                   # Tablica znakova bi bila None samo u korijenu generativnog stabla, sve ostale prijevodne jedinice naslijedile bi tablicu znakova
            self.tablica_znakova = TablicaZnakova()
        else:
            self.tablica_znakova = self.parent.tablica_znakova
        
        if self.isProduction('<vanjska_deklaracija>'):
            self.children[0].provjeri()
        elif self.isProduction('<prijevodna_jedinica> <vanjska_deklaracija>'):
            self.children[0].provjeri()
            self.children[1].provjeri()
        # else:
        # Mislim da s ovim znakom nis ne moze poc po krivu ?
        # msm ne provjeravaju se nikakava pravila, a msm da sintaksna analiza garantira da uvijek da je aktualna jedna od ovih gore produkcija