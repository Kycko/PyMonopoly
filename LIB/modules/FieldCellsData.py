# -*- coding: utf-8 -*-
import Globals

def make_groups():
    if Globals.TEMP_VARS['cur_game']:
        return ('start', 1, 1, 'income', 1, 'chance', 2, 2, 'chest', 2, 'jail', 3, 3, 'income', 3, 'chance', 4, 4, 'chest', 4, 'skip', 5, 'tax', 5, 5, 'chance', 6, 'chest', 6, 6, 'gotojail', 7, 'income', 7, 7, 'chance', 8, 'chest', 8, 8)
    else:
        return ('start', 1, 'chest', 1, 'tax', 'railroad', 2, 'chance', 2, 2, 'jail', 3, 'service', 3, 3, 'railroad', 4, 'chest', 4, 4, 'skip', 5, 'chance', 5, 5, 'railroad', 6, 6, 'service', 6, 'gotojail', 7, 7, 'chest', 7, 'railroad', 'chance', 8, 'tax', 8)
def make_group_symbols():
    return {'start'     : Globals.FONTS['ume_40'].render(u'☚', True, Globals.COLORS['black']),
            'jail'      : Globals.FONTS['ume_48'].render(u'▥', True, Globals.COLORS['black']),
            'skip'      : Globals.FONTS['ume_32'].render(u'♨', True, Globals.COLORS['black']),
            'gotojail'  : Globals.FONTS['ume_32'].render(u'⇙', True, Globals.COLORS['black']),
            'income'    : Globals.FONTS['ume_48'].render(u'☺', True, Globals.COLORS['dark_green']),
            'tax'       : Globals.FONTS['ume_48'].render(u'☹', True, Globals.COLORS['deep_red']),
            'chance'    : Globals.FONTS['ume_32'].render(u'✭', True, Globals.COLORS['black']),
            'chest'     : Globals.FONTS['ume_48'].render(u'✎', True, Globals.COLORS['black']),
            'railroad'  : Globals.FONTS['ume_32'].render(u'☍', True, Globals.COLORS['black']),
            'service'   : Globals.FONTS['ume_32'].render(u'♒', True, Globals.COLORS['black']),
            1           : Globals.FONTS['ume_32'].render(u'☂', True, Globals.COLORS['black']),
            2           : Globals.FONTS['ume_32'].render(u'✲', True, Globals.COLORS['black']),
            3           : Globals.FONTS['ume_32'].render(u'✆', True, Globals.COLORS['black']),
            4           : Globals.FONTS['ume_32'].render(u'✇', True, Globals.COLORS['black']),
            5           : Globals.FONTS['ume_32'].render(u'❖', True, Globals.COLORS['black']),
            6           : Globals.FONTS['ume_32'].render(u'✂', True, Globals.COLORS['black']),
            7           : Globals.FONTS['ume_32'].render(u'❃', True, Globals.COLORS['black']),
            8           : Globals.FONTS['ume_32'].render(u'☭', True, Globals.COLORS['black'])}
def make_group_colors():
    if Globals.TEMP_VARS['cur_game']:
        return ('deep_yellow', 'orange', 'pink', 'red27', 'light_green', 'deep_sky_blue', 'white', 'blue_magenta')
    else:
        return ('brown45', 'sky_blue', 'deep_magenta', 'orange', 'red27', 'deep_yellow', 'deep_green', 'light_blue')
