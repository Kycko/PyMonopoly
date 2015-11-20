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
def read_cells_costs():
    if Globals.TEMP_VARS['cur_game']:
        return {0   : 20000,
                1   : 5000,
                2   : 6000,
                3   : 20000,
                4   : 7000,
                6   : 9000,
                7   : 10000,
                9   : 11000,
                10  : 500,
                11  : 13000,
                12  : 14000,
                13  : 20000,
                14  : 15000,
                16  : 17000,
                17  : 18000,
                19  : 19000,
                21  : 21000,
                22  : -20000,
                23  : 22000,
                24  : 23000,
                26  : 25000,
                28  : 26000,
                29  : 27000,
                31  : 29000,
                32  : 20000,
                33  : 30000,
                34  : 31000,
                36  : 33000,
                38  : 34000,
                39  : 35000}
    else:
        return {0   : 200,
                1   : 60,
                3   : 60,
                4   : -200,
                5   : 200,
                6   : 100,
                8   : 100,
                9   : 120,
                10  : 50,
                11  : 140,
                12  : 150,
                13  : 140,
                14  : 160,
                15  : 200,
                16  : 180,
                18  : 180,
                19  : 200,
                21  : 220,
                23  : 220,
                24  : 240,
                25  : 200,
                26  : 260,
                27  : 260,
                28  : 150,
                29  : 280,
                31  : 300,
                32  : 300,
                34  : 320,
                35  : 200,
                37  : 350,
                38  : -100,
                39  : 400}
