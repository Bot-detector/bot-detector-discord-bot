import random
import string
import re

def is_valid_rsn(rsn):
        return re.fullmatch('[\w\d _-]{1,12}', rsn)

def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def joinParams(params):
    return " ".join(params)

def plus_minus(var, compare):
    diff_control = '-'
    if (isinstance(var, float)):
        if (var > compare):
            diff_control = '+'
    if (isinstance(var, str)):
        if (str(var) == str(compare)):
            diff_control = '+'
    return diff_control