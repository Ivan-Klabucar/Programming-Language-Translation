# dict tablica bi izgledala ovako:
# {'neki_idn': TabZnakEntry1, 'neki_drugi_idn': TabZnak2 ...}
class TablicaZnakova:
    def __init__(self, parent=None):
        self.parent = parent
        self.tablica = dict()
    
    def add(self, key, entry):
        if key not in self.tablica:
            self.tablica[key] = entry
            return True
        return False
    
    def get(self, key, default=False):
        if key in self.tablica:
            return self.tablica[key]
        return default
        
    
# Po potrebi u ovu klasu dodavat razne atribute koji su potrebni
class TabZnakEntry:
    def __init__(self, tip):
        self.tip = tip          # npr. 'int' ili 'char'