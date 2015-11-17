# -*- coding: utf-8 -*-
import Globals

def make_groups():
    if Globals.TEMP_VARS['cur_game']:
        return ('start', 1, 1, 'income', 1, 'chance', 2, 2, 'chest', 2, 'jail', 3, 3, 'income', 3, 'chance', 4, 4, 'chest', 4, 'skip', 5, 'tax', 5, 5, 'chance', 6, 'chest', 6, 6, 'gotojail', 7, 'income', 7, 7, 'chance', 8, 'chest', 8, 8)
    else:
        return ('start', 1, 'chest', 1, 'tax', 'railroad', 2, 'chance', 2, 2, 'jail', 3, 'service', 3, 3, 'railroad', 4, 'chest', 4, 4, 'skip', 5, 'chance', 5, 5, 'railroad', 6, 6, 'service', 6, 'gotojail', 7, 7, 'chest', 7, 'railroad', 'chance', 8, 'tax', 8)
def make_group_symbols():
    font = Globals.FONTS['ubuntu_16']
    color = Globals.COLORS['black']
    if Globals.TEMP_VARS['cur_game']:
        return (font.render('$', True, color),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                font.render('#', True, color),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                font.render('->#', True, color),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None)
    else:
        return (font.render('$', True, color),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                font.render('#', True, color),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                font.render('->#', True, color),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None)
def make_group_colors():
    if Globals.TEMP_VARS['cur_game']:
        return ('light_brown', 'light_blue', 'magenta', 'light_red', 'red', 'yellow', 'light_green', 'white')
    else:
        return ('brown45', 'sky_blue', 'deep_magenta', 'orange', 'red27', 'deep_yellow', 'deep_green', 'light_blue')
