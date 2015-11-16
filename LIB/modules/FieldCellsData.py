# -*- coding: utf-8 -*-
import Globals

def choose_cell_group(number):
    if number == 0:
        return 'start'
    elif number == 10:
        return 'jail'
    elif number == 30:
        return 'gotojail'
def choose_group_symbol(group):
    font = Globals.FONTS['ubuntu_16']
    color = Globals.COLORS['black']
    if group == 'start':
        return font.render('$', True, color)
    elif group == 'jail':
        return font.render('#', True, color)
    elif group == 'gotojail':
        return font.render('-> #', True, color)
