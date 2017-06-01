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
def read_cells_rent_costs():
    if Globals.TEMP_VARS['cur_game']:
        return {1   : (100, 1000, 3000, 9000, 20000),
                2   : (400, 1500, 6000, 18000, 45000),
                4   : (600, 2000, 8000, 20000, 50000),
                6   : (700, 3000, 9000, 25000, 55000),
                7   : (800, 4000, 10000, 30000, 60000),
                9   : (1200, 5000, 15000, 35000, 65000),
                11  : (1500, 6000, 20000, 40000, 70000),
                12  : (2000, 6500, 21000, 42000, 75000),
                14  : (2100, 7000, 22000, 45000, 80000),
                16  : (2200, 7500, 25000, 50000, 81000),
                17  : (2300, 8000, 26000, 55000, 85000),
                19  : (2400, 8500, 27000, 60000, 86000),
                21  : (2500, 9000, 28000, 61000, 90000),
                23  : (3000, 9500, 29000, 65000, 95000),
                24  : (3200, 10000, 30000, 70000, 100000),
                26  : (3500, 11000, 31000, 75000, 110000),
                28  : (3600, 12000, 35000, 80000, 120000),
                29  : (3800, 13000, 36000, 85000, 125000),
                31  : (3900, 14000, 34000, 90000, 130000),
                33  : (4000, 15000, 40000, 95000, 135000),
                34  : (4100, 16000, 45000, 100000, 150000),
                36  : (4400, 17000, 50000, 120000, 170000),
                38  : (4500, 18000, 60000, 140000, 180000),
                39  : (5000, 20000, 75000, 150000, 200000)}
    else:
        return {1   : (2, 10, 30, 90, 160, 250),
                3   : (4, 20, 60, 180, 320, 450),
                5   : (25, 50, 100, 200),
                6   : (6, 30, 90, 270, 400, 550),
                8   : (6, 30, 90, 270, 400, 550),
                9   : (8, 40, 100, 300, 450, 600),
                11  : (10, 50, 150, 450, 625, 750),
                12  : ('x4', 'x10'),
                13  : (10, 50, 150, 450, 625, 750),
                14  : (12, 60, 180, 500, 700, 900),
                15  : (25, 50, 100, 200),
                16  : (14, 70, 200, 550, 750, 950),
                18  : (14, 70, 200, 550, 750, 950),
                19  : (16, 80, 220, 600, 800, 1000),
                21  : (18, 90, 250, 700, 875, 1050),
                23  : (18, 90, 250, 700, 875, 1050),
                24  : (20, 100, 300, 750, 925, 1100),
                25  : (25, 50, 100, 200),
                26  : (22, 110, 330, 800, 975, 1150),
                27  : (22, 110, 330, 800, 975, 1150),
                28  : ('x4', 'x10'),
                29  : (24, 120, 360, 850, 1025, 1200),
                31  : (26, 130, 390, 900, 1100, 1275),
                32  : (26, 130, 390, 900, 1100, 1275),
                34  : (28, 150, 450, 1000, 1200, 1400),
                35  : (25, 50, 100, 200),
                37  : (35, 175, 500, 1100, 1300, 1500),
                39  : (50, 200, 600, 1400, 1700, 2000)}
def read_cells_build_costs():
    if Globals.TEMP_VARS['cur_game']:
        return (5000, 5000, 10000, 10000, 15000, 15000, 20000, 20000)
    else:
        return (50, 50, 100, 100, 150, 150, 200, 200)
def make_chests_and_chances(type):
    if type == 'chests':
        if Globals.TEMP_VARS['cur_game']:
            return ['free_jail', 'goto 34', 'goto 12', 'goto 12', 'goto 39', 'income -1000', 'goto 6', 'income 20000', 'income 10000', 'income 10000', 'income 5000', 'income -1000', 'income 20000', 'take_chance', 'income -20000', 'income 10000', 'income 1000', 'goto_forward -3', 'income -5000', 'goto 14', 'income 20000', 'goto_forward 2', 'income 20000', 'repair 5000 10000', 'goto 0', 'goto_jail', 'income -20000', 'goto 9', 'goto 39', 'income -5000', 'goto 24', 'income -1000', 'goto 4', 'goto_forward -3', 'income -5000', 'goto 14', 'income 10000', 'goto_forward 2', 'income 20000', 'repair 5000 10000', 'income 20000', 'goto_jail', 'income -20000', 'goto 9', 'income -20000', 'income -5000', 'goto 24', 'income -1000']
        else:
            return ['goto 0', 'repair 40 115', 'birthday 10', 'income 100', 'income 10', 'income -50', 'free_jail', 'goto_jail', 'income -50', 'income 100', 'income 50', 'income 20', 'income -100', 'income 200', 'income 25', 'income 100']
    else:
        if Globals.TEMP_VARS['cur_game']:
            return ['free_jail', 'goto 34', 'goto 12', 'goto 12', 'goto 39', 'income -1000', 'goto 6', 'goto 17', 'goto 19', 'goto 4', 'goto_forward 2', 'goto 0', 'goto 29', 'goto 28', 'goto 9', 'repair 5000 10000', 'income -5000', 'goto 24', 'goto_forward -3', 'income -1500', 'goto_jail', 'goto_forward 2', 'income 20000', 'repair 5000 10000', 'goto 0', 'goto_jail', 'income -20000', 'income -5000', 'goto 39', 'income -5000', 'goto 24', 'income -1000', 'free_jail', 'goto 34', 'goto 12', 'goto 12', 'goto 39', 'income -1000', 'goto 6', 'goto 17', 'goto 19', 'goto 4', 'goto_forward 2', 'goto 0', 'goto 29', 'goto 28', 'goto 9', 'repair 5000 10000']
        else:
            return ['goto_service', 'goto_forward -3', 'goto 0', 'goto_railroad', 'repair 25 100', 'goto 11', 'goto_jail', 'goto 39', 'goto_railroad', 'income 150', 'income -15', 'goto 5', 'goto 24', 'income 50', 'pay_each 50', 'free_jail']
