class AutomatonDefBuilder:
    def __init__(self, regEx, rule):
        self.regEx = regEx
        self.rule = rule
        self.num_of_states = 0
        self.transitions = ''
        self.states = ''
        self.validState = ''
        self.startState = ''

        lr, rr = self.pretvori(self.regEx)
        self.startState = self.makeStateString(lr)
        self.validState = self.makeStateString(rr)

    def makeStateString(self, num):
        #return "s{}_{}".format(num, self.rule)
        return "s{}".format(num)

    def add_state(self, num):
        optional = ','
        if self.states == '':
            optional = ''
        self.states += optional + self.makeStateString(num)

    def novo_stanje(self):
        self.num_of_states += 1
        self.add_state(self.num_of_states - 1)
        return self.num_of_states - 1

    def je_operator(self, izraz, i):
        br = 0
        while(i-1>=0 and izraz[i-1]=='\\'): 
            br = br + 1
            i = i - 1
        return (br%2 == 0)

    def pronadi_odgv_zatvorenu_zagradu(self, izraz, i):
        br_zagrada = 0
        i += 1
        while(i < len(izraz)):
            if izraz[i] == '(': 
                br_zagrada += 1
            elif izraz[i] == ')' and br_zagrada == 0:
                return i
            elif izraz[i] == ')' and br_zagrada > 0:
                br_zagrada -= 1
            i += 1

    def dodaj_epsilon_prijelaz(self, lijevo_stanje, desno_stanje):
        self.transitions += "{},$->{}\n".format(self.makeStateString(lijevo_stanje), self.makeStateString(desno_stanje))
    
    def dodaj_prijelaz(self, lijevo_stanje, desno_stanje, prijelazni_znak):
        self.transitions += "{},{}->{}\n".format(self.makeStateString(lijevo_stanje), prijelazni_znak, self.makeStateString(desno_stanje))


    def pretvori(self, izraz):
        izbori = []
        br_zagrada = 0
        ne_grupirani = 0
        for i in range(len(izraz)):
            if(izraz[i]=='(' and self.je_operator(izraz, i)):
                br_zagrada = br_zagrada + 1
            elif(izraz[i]==')' and self.je_operator(izraz, i)):
                br_zagrada = br_zagrada - 1
            elif(br_zagrada==0 and izraz[i]=='|' and self.je_operator(izraz, i)):
                izbori.append(izraz[ne_grupirani:i])
                ne_grupirani = i + 1
        if(ne_grupirani > 0 and ne_grupirani < len(izraz)):
            izbori.append(izraz[ne_grupirani:])
        

        lijevo_stanje = self.novo_stanje()
        desno_stanje = self.novo_stanje()
        if(ne_grupirani > 0 and ne_grupirani < len(izraz)):
            for i in range(len(izbori)):
                lr, rr = self.pretvori(izbori[i])
                self.dodaj_epsilon_prijelaz(lijevo_stanje, lr)
                self.dodaj_epsilon_prijelaz(rr, desno_stanje)
        else:
            prefiksirano = False
            zadnje_stanje = lijevo_stanje
            for i in range(len(izraz)):
                if prefiksirano:
                    prefiksirano = False
                    prijelazni_znak = ''
                    if izraz[i] == 't':
                        prijelazni_znak = '\t'
                    elif izraz[i] == 'n':
                        prijelazni_znak = '\n'
                    elif izraz[i] == '_':
                        prijelazni_znak = ' '
                    else:
                        prijelazni_znak = izraz[i]
                    
                    a = self.novo_stanje()
                    b = self.novo_stanje()
                    self.dodaj_prijelaz(a, b, prijelazni_znak)
                else:
                    if izraz[i] == '\\':
                        prefiksirano = True
                        continue

                    if izraz[i] != '(':
                        a = self.novo_stanje()
                        b = self.novo_stanje()
                        if izraz[i] == '$':
                            self.dodaj_epsilon_prijelaz(a, b)
                        else:
                            self.dodaj_prijelaz(a, b, izraz[i])
                    else:
                        j = self.pronadi_odgv_zatvorenu_zagradu(izraz, i)
                        lr, rr = self.pretvori(izraz[i+1:j])
                        a = lr
                        b = rr
                        i = j

                if (i+1<len(izraz)) and (izraz[i+1]=='*'):
                    x = a
                    y = b
                    a = self.novo_stanje()
                    b = self.novo_stanje()
                    self.dodaj_epsilon_prijelaz(a, x)
                    self.dodaj_epsilon_prijelaz(y, b)
                    self.dodaj_epsilon_prijelaz(a, b)
                    self.dodaj_epsilon_prijelaz(y, x)
                    i = i+1
                self.dodaj_epsilon_prijelaz(zadnje_stanje, a)
                zadnje_stanje = b
            self.dodaj_epsilon_prijelaz(zadnje_stanje, desno_stanje)
        return lijevo_stanje, desno_stanje

    def getAutomatonDefinition(self):
        result = self.states + '\n' + self.validState + '\n' + self.startState + '\n' + self.transitions
        print(result)
        return result




x = AutomatonDefBuilder('aab', 1)
x.getAutomatonDefinition()