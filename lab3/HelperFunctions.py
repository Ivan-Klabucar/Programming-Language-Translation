def tilda(type1, type2):     # returns type1 ~ type2, needs implementing, has to support calls like tilda('int', 'T')
    return True

def return_type(function_type):
    return function_type.split('->')[1].strip().replace(')', '')

def is_void_func(function_type):
    return function_type.split('->')[1].strip().replace(')', '') == 'void'

def is_non_void_func(function_type):
    return

def param_types(function_type):
    return

def is_const(type):
    return True