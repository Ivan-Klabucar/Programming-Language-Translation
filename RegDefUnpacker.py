class RegDefUnpacker:
    def __init__(self):
        self.library = {}

    def unpack(self, line):
        #lines = batch_def.splitlines()
        #for line in lines:
        def_list = line.split(' ')
        definition = def_list[0]
        regEx = def_list[1]
        regEx = self.purify(regEx)
        self.library.update({definition: regEx})

    def purify(self, regEx):
        for key in self.library:
            occurences = regEx.count(key)
            i = 0
            while occurences > 0:
                index_of_key = regEx.find(key, i)
                if not self.je_operator(regEx, index_of_key):
                    i = index_of_key + 1
                    occurences -= 1
                    continue
                regEx = regEx[:index_of_key] + '(' + self.library[key] + ')' + regEx[index_of_key+len(key):]
                occurences -= 1
        return regEx

    def je_operator(self, izraz, i):
        br = 0
        while i-1 >= 0 and izraz[i-1] == '\\':
            br = br + 1
            i = i - 1
        return br % 2 == 0

#Znam da je moj proces testiranja dosta rudimentaran al mi se nije dalo smisljat fensi nacine so ur gonna have to deal with it
a = RegDefUnpacker()
a.unpack('{oktalnaZnamenka} 0|1|2|3|4|5|6|7\n{dekadskaZnamenka} {oktalnaZnamenka}|8|9\n{hexZnamenka} a|b|c|d|e|f|{dekadskaZnamenka}|A|B|C|D|E|F\n')
print(a.library)
print("--------------------------------")
print(a.purify("ppppp|{oktalnaZnamenka}|{}|\{oktalnaZnamenka}|{oktalnaZnamenka}"))
