# -*- coding: utf-8 -*-
import Globals
from pygame import Color, display
from os import listdir
from sys import exit as SYSEXIT

#--- Common
def read_file(file):
    list = open(file, 'r')
    array = list.readlines()
    list.close()
    return map(lambda x: x.decode('UTF').strip('\n'), array)
def write_to_file(file, data, method='w'):
    list = open(file, method)
    list.writelines(map(lambda x: x.encode('UTF'), data))
    list.close()

#--- Hardware related
def check_user_monitor():
    MAX_RESOLUTION = (display.Info().current_w-70, display.Info().current_h-60)
    avail_x = [i for i in (1820, 1250, 1200) if i < MAX_RESOLUTION[0]]
    avail_y = [i for i in (1000, 950, 700) if i < MAX_RESOLUTION[1]]
    if avail_x and avail_y:
        return (avail_x, avail_y)
    else:
        print("Your monitor has too small resolution! We can't provide a good interface for it :(")
        SYSEXIT()

#--- Statistics, settings and translations
def check_files():
    DB = listdir(Globals.DIRS['settings'])
    for FILE in ('stats', 'settings', 'last_game_settings'):
        if FILE not in DB:
            create_init_file(FILE)
def create_init_file(type):
    if type == 'stats':
        data = ['0\n' if x<3 else 'None 0 01.01.01 black\n' for x in range(10)]
        data = ['0\n'] + data + ['1\n'] + data
    elif type == 'settings':
        data = ('0\n', 'Player 1\n', '215\n', '0\n', '0\n', '6\n', '1\n', '1\n', '1.0\n', '1\n')
    elif type == 'last_game_settings':
        data = ("3\n", "2\n")
    write_to_file(Globals.FILES[type], data)
def read_settings():
    SETTINGS = read_file(Globals.FILES['settings'])
    return {'language'          : int(SETTINGS[0]),
            'player_name'       : SETTINGS[1],
            'player_color'      : Color(int(SETTINGS[2]), int(SETTINGS[3]), int(SETTINGS[4])),
            'favourite_game'    : int(SETTINGS[5]),
            'music'             : bool(SETTINGS[6]),
            'sound_effects'     : bool(SETTINGS[7]),
            'volume'            : float(SETTINGS[8]),
            'game_block'        : bool(SETTINGS[9])}
def read_translation(lang):
    return read_file(Globals.DIRS['translations'] + Globals.LANGUAGES[lang][0] + '/main')
