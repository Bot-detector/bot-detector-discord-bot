import random
import string
import re

def is_valid_rsn(rsn):
    return re.fullmatch('[\w\d _-]{1,12}', rsn)

def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def to_jagex_name(name: str) -> str:
    #Allow for special characters as the first character of RSNs
    jagex_name = name[0:1] + name[1:].replace('_', ' ').replace('-', ' ').strip()
    return jagex_name

def plus_minus(var, compare):
    diff_control = '-'
    if isinstance(var, float) and var > compare:
        diff_control = '+'

    if isinstance(var, str) and var == str(compare):
        diff_control = '+'

    return diff_control
