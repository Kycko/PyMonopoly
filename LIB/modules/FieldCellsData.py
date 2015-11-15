# -*- coding: utf-8 -*-

def choose_cell_group(number):
    if number == 0:
        return 'start'
    elif number == 10:
        return 'jail'
    elif number == 30:
        return 'gotojail'
def choose_group_symbol(group):
    if group == 'start':
        return '$'
    elif group == 'jail':
        return '#'
    elif group == 'gotojail':
        return '-> #'
