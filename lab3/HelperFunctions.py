def is_const(type): # Samo je li vanjski const
    retb = False
    retv = None
    elems = type.split('(')
    if elems[0] == 'const':
        retb = True
        retv = type[6:-1]
    return retb, retv

def is_T(type):
    return type in ['int','char']

def is_X(type):
    return is_T(type) or is_T(is_const(type)[1])

def is_seq(type):
    retb = False
    retv = None
    elems = type.split('(')
    if elems[0] == 'niz':
        retb = True
        retv = type[4:-1]
    return retb, retv

def is_function(type):
    elems = type.split('(')
    if elems[0] == 'funkcija':
        return True
    return False

def tilda(type1, type2): # returns type1 ~ type2, needs implementing, has to support calls like tilda('int', 'T')
    if type2 == 'T':
        return is_T(type1)
    if type2 == 'X':
        return is_X(type1)
    if type1 == type2:
        return True
    elif type1 == 'char' and type2 == 'int':
        return True
    elif is_const(type1)[0]:
        return tilda(is_const(type1)[1], type2)
    elif is_const(type2)[0]:
        return tilda(type1, is_const(type2)[1])
    elif is_seq(type1)[0] and not is_const(is_seq(type1)[1])[0] and is_seq(type2)[0] and not is_const(is_seq(type2)[1])[0]:
        return tilda(is_seq(type1)[1], is_seq(type2)[1])
    elif is_seq(type1)[0] and not is_const(is_seq(type1)[1])[0] and is_seq(type2)[0] and is_const(is_seq(type2)[1])[0]:
        return tilda(is_seq(type1)[1], is_const(is_seq(type2)[1])[1])
    elif is_seq(type1)[0] and is_const(is_seq(type1)[1])[0] and is_seq(type2)[0] and is_const(is_seq(type2)[1])[0]:
        return tilda(is_const(is_seq(type1)[1])[1], is_const(is_seq(type2)[1])[1])
    return False

def return_type(function_type):
    print("rtrn typ: {}".format(function_type))
    return function_type.split('->')[1].strip().replace(')', '')

def is_void_func(function_type):
    return function_type.split('->')[1].strip().replace(')', '') == 'void'

def param_types(function_type):
    return eval(function_type.split('->')[0].strip()[9:])