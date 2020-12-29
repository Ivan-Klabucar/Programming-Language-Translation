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
            # do smh like:
            # self.children[0].provjeri(tablica_znakova=self.tablica_znakova)
            print('hej hej')
        elif self.isProduction('<prijevodna_jedinica> <vanjska_deklaracija>'):
            # do smh else like:
            # self.children[0].provjeri(tablica_znakova=self.tablica_znakova)
            # self.children[1].provjeri(tablica_znakova=self.tablica_znakova)
            print('nej nej')