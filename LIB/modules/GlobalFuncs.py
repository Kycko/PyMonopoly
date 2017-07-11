# -*- coding: utf-8 -*-
import Globals
from datetime import datetime
from locale import getdefaultlocale
from os import listdir, mkdir
from Players import Player
from pygame import Color, display, mixer
from random import randrange
from sys import exit as SYSEXIT

#--- Common
def change_color_alpha(color, alpha):
    color -= Globals.COLORS['black']
    color.a = alpha
    return color
def check_substring_in_dict_keys(dict, string):
    for key in dict.keys():
        if string in key:
            return key
def clear_TEMP_VARS(exception):
    for key in Globals.TEMP_VARS.keys():
        if key not in exception:
            Globals.TEMP_VARS.pop(key)
def count_new_pos(old, offset):
    return tuple([old[i]+offset[i] for i in range(2)])
def change_volume(volume, write_to_file=False):
    mixer.music.set_volume(volume)
    Globals.SOUNDS['button-pressed'].set_volume(volume)
    Globals.SETTINGS['volume'] = volume
    if write_to_file:
        save_settings()
def switch_sound_state(object, current, write_to_file=False):
    if object == 'music':
        if current:
            mixer.music.fadeout(2000)
        else:
            mixer.music.play(-1)
    Globals.SETTINGS[object] = not current
    if write_to_file:
        save_settings()
def play_click_sound():
    if Globals.SETTINGS['sounds']:
        Globals.SOUNDS['button-pressed'].play()
def slight_animation_count_pos(new, current, speed, limitation=None):
    if new != current:
        current = list(current)
        for axis in range(2):
            if new[axis] != current[axis]:
                diff = (new[axis] - current[axis])/speed
                if abs(diff) < 0.1:
                    diff = 1
                elif limitation and abs(diff) > limitation:
                    if diff < 0:
                        diff = -limitation
                    else:
                        diff = limitation
                current[axis] += diff
    return tuple(current)
def read_file(file):
    list = open(file, 'r')
    array = list.readlines()
    list.close()
    return map(lambda x: x.decode('UTF').strip('\n'), array)
def write_to_file(file, data, method='w'):
    list = open(file, method)
    list.writelines(map(lambda x: x.encode('UTF'), data))
    list.close()
#--- Game related
def add_new_player(human):
    Globals.PLAYERS.append(Player(Globals.TEMP_VARS['avail_names'].pop(randrange(len(Globals.TEMP_VARS['avail_names']))),
                                  Globals.TEMP_VARS['avail_colors'].pop(randrange(len(Globals.TEMP_VARS['avail_colors']))),
                                  human))
def create_players_list():
    Globals.PLAYERS = [Player(Globals.SETTINGS['pl_name'], Globals.SETTINGS['pl_color'], True)]
def rm_player(name):
    for i in range(len(Globals.PLAYERS)):
        if name == Globals.PLAYERS[i].name:
            if 'pay_birthday' in Globals.TEMP_VARS.keys():
                for y in range(len(Globals.PLAYERS)):
                    if y == Globals.TEMP_VARS['cur_turn'] and i < y:
                        Globals.TEMP_VARS['cur_turn'] -=1
            Globals.PLAYERS.pop(i)
            return True
def get_gamename():
    return ('monopoly', 'manager')[Globals.TEMP_VARS['cur_game']]
def check_if_anybody_can_trade():
    for player in Globals.PLAYERS:
        if player.free_jail_cards:
            return True
    for cell in Globals.main_scr.objects['gamefield'].cells:
        if cell.owner:
            return True
def check_if_player_can_trade(player):
    return bool(player.free_jail_cards) or check_if_player_owns_fieldcells(player.name)
def check_if_player_owns_fieldcells(player_name):
    for cell in Globals.main_scr.objects['gamefield'].cells:
        if cell.owner == player_name:
            return True
def find_player_obj_by_name(name, return_DUEL_rival=False):
    for player in Globals.PLAYERS:
        if (return_DUEL_rival and player.name != name) or (not return_DUEL_rival and player.name == name):
            return player
def check_group_monopoly(group):
    fieldcells = Globals.main_scr.objects['gamefield'].cells
    if group == 'railroad':
        numbers = [i for i in range(5, 36, 10)]
    elif group == 'service':
        numbers = [12, 28]
    else:
        numbers = [i for i in range((group-1)*5+1, group*5) if fieldcells[i].group == group]
    owners = [fieldcells[i].owner for i in numbers]
    if owners.count(owners[0]) == len(owners):
        Globals.main_scr.objects['gamefield'].groups_monopolies[group] = owners[0]
    else:
        Globals.main_scr.objects['gamefield'].groups_monopolies[group] = ''
    if group in ('railroad', 'service'):
        mortragers = [fieldcells[i].owner for i in numbers if fieldcells[i].buildings < 0]
        for i in numbers:
            if fieldcells[i].buildings > -1:
                fieldcells[i].buildings = owners.count(fieldcells[i].owner) - 1 - mortragers.count(fieldcells[i].owner)
    return numbers
def check_cur_prop_management():
    if 'auction' in Globals.TEMP_VARS.keys():
        return Globals.TEMP_VARS['auction']['order'][0]
    elif 'bankruptcy_RECIPIENT' in Globals.TEMP_VARS.keys():
        return Globals.TEMP_VARS['bankruptcy_RECIPIENT']
    elif 'pay_birthday' in Globals.TEMP_VARS.keys():
        return Globals.TEMP_VARS['pay_birthday'][0]
    else:
        return Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
def prop_manage_pictures():
    return (u'●○➊➋➌➍❖          ', u'●○➊➋➌❖          ')[Globals.TEMP_VARS['cur_game']]
def check_bankrupt(player, money=None):
    PROP = count_player_funds(player)
    if money: return PROP < money
    else: return PROP < Globals.TEMP_VARS['MUST_PAY']
def count_player_funds(player):
    PROP = player.money
    for cell in Globals.main_scr.objects['gamefield'].cells:
        if cell.owner == player.name and cell.buildings != -1:
            PROP += cell.buy_cost / 2
            if cell.group not in ('railroad', 'service'):
                PROP += cell.buildings * cell.build_cost / 2
    return PROP
#--- Hardware related
def check_user_monitor(x, y):
    if display.Info().current_w-70 < x or display.Info().current_h-60 < y:
        print("Your monitor has too small resolution! We can't provide a good interface for it :(")
        SYSEXIT()
    else:
        return (x, y)
#--- Statistics, settings and translations
def check_files():
    try:
        mkdir(Globals.DIRS['settings'])
    except:
        print('config dir exists')
    DB = listdir(Globals.DIRS['settings'])
    for FILE in ('stats', 'settings', 'last_game_settings'):
        if (FILE not in DB) or (FILE == 'settings' and not len(read_file(Globals.FILES['settings'])) == 12):
            create_init_file(FILE)
def create_init_file(type):
    if type == 'stats':
        data = ['0\n' if x<3 else 'None 0 01.01.01 0\n' for x in range(10)]
        data = data + data
    elif type == 'settings':
        color = Globals.PLAYERS_COLORS[2]
        locale = getdefaultlocale()[0][:2]
        if locale not in (listdir(Globals.DIRS['translations'])):
            locale = 'en'
        data = (locale+'\n', 'Player 1\n', str(color.r)+'\n', str(color.g)+'\n', str(color.b)+'\n', '1\n', '1\n', '1\n', '1\n', '1.0\n', '1\n', '1\n')
    elif type == 'last_game_settings':
        data = ("human\n", "AI\n")
    write_to_file(Globals.FILES[type], data)
def read_settings():
    SETTINGS = read_file(Globals.FILES['settings'])
    return {'language'      : SETTINGS[0],
            'pl_name'       : SETTINGS[1],
            'pl_color'      : Color(int(SETTINGS[2]), int(SETTINGS[3]), int(SETTINGS[4])),
            'fav_game'      : int(SETTINGS[5]),
            'hotkeys'       : bool(int(SETTINGS[6])),
            'music'         : bool(int(SETTINGS[7])),
            'sounds'        : bool(int(SETTINGS[8])),
            'volume'        : float(SETTINGS[9]),
            'build_style'   : bool(int(SETTINGS[10])),
            'block'         : bool(int(SETTINGS[11]))}
def save_settings():
    array = [Globals.SETTINGS['language'] + '\n',
             Globals.SETTINGS['pl_name'] + '\n',
             str(Globals.SETTINGS['pl_color'][0]) + '\n',
             str(Globals.SETTINGS['pl_color'][1]) + '\n',
             str(Globals.SETTINGS['pl_color'][2]) + '\n',
             str(Globals.SETTINGS['fav_game']) + '\n',
             str(int(Globals.SETTINGS['hotkeys'])) + '\n',
             str(int(Globals.SETTINGS['music'])) + '\n',
             str(int(Globals.SETTINGS['sounds'])) + '\n',
             str(Globals.SETTINGS['volume']) + '\n',
             str(int(Globals.SETTINGS['build_style'])) + '\n',
             str(int(Globals.SETTINGS['block'])) + '\n']
    write_to_file(Globals.FILES['settings'], array)
def choose_next_language():
    avail_languages = listdir(Globals.DIRS['translations'])
    avail_languages.sort()
    index = avail_languages.index(Globals.SETTINGS['language']) + 1
    if index == len(avail_languages):
        index = 0
    Globals.SETTINGS['language'] = avail_languages[index]
    Globals.TRANSLATION = read_translation(Globals.SETTINGS['language'])
def read_translation(lang):
    return read_file(Globals.DIRS['translations'] + lang + '/main')
def read_stats(game):
    array = read_file(Globals.FILES['stats'])
    #--- 0: monopoly, 10: manager
    line = 10*game
    for i in range(line, line+10):
        if i < line+3:
            array[i] = int(array[i])
        else:
            temp = array[i].split()
            while len(temp) > 4:
                temp[0] += ' ' + temp[1]
                temp.pop(1)
            array[i] = {'name'      : temp[0],
                        'score'     : int(temp[1]),
                        'date'      : temp[2],
                        'recent'    : bool(int(temp[3]))}
    return array[line:line+10]
def write_stats():
    new_result = count_player_funds(Globals.PLAYERS[0])
    cur_stats = read_stats(Globals.TEMP_VARS['cur_game'])
    new_place = find_place_for_new_stats(cur_stats, new_result)
    cur_stats[1] += 1 * Globals.PLAYERS[0].human
    cur_stats[2] += new_result
    if new_place:
        for i in range(3, 10):
            cur_stats[i]['recent'] = False
        DATA = {'name'      : Globals.PLAYERS[0].name,
                'score'     : new_result,
                'date'      : datetime.now().strftime("%d.%m.%y"),
                'recent'    : True}
        cur_stats.pop()
        cur_stats.insert(new_place, DATA)
    save_stats_to_file(cur_stats)
def add_one_game():
    cur_stats = read_stats(Globals.TEMP_VARS['cur_game'])
    cur_stats[0] += 1
    save_stats_to_file(cur_stats)
def save_stats_to_file(cur_stats):
    array = read_file(Globals.FILES['stats'])
    line = 10*Globals.TEMP_VARS['cur_game']
    CHANGED = range(line, line + 10)
    for i in range(20):
        if i in CHANGED:
            if i % 10 < 3:
                array[i] = str(cur_stats[i % 10])
            else:
                array[i] = cur_stats[i%10]['name']+' '+str(cur_stats[i%10]['score'])+' '+cur_stats[i%10]['date']+' '+str(int(cur_stats[i%10]['recent']))
        array[i] += '\n'
    write_to_file(Globals.FILES['stats'], array)
def find_place_for_new_stats(cur_stats, new_result):
    for i in range(3, 10):
        if new_result >= cur_stats[i]['score']:
            return i
def save_last_game_settings():
    data = [('AI\n', 'human\n')[Globals.PLAYERS[i].human] for i in range(1, len(Globals.PLAYERS))]
    write_to_file(Globals.FILES['last_game_settings'], data)
def read_onboard_text():
    directory = Globals.DIRS['translations']+Globals.SETTINGS['language']+'/'+get_gamename()+'/'
    data = {}
    for type in ('fieldnames', 'onboard'):
        raw = read_file(directory + type)
        data[type] = {}
        for string in raw:
            string = string.split(':')
            data[type][int(string[0])] = string[1]
    data['rentlabels'] = read_file(directory + 'rentlabels')
    return data
def read_gamelog_translation():
    return read_file(Globals.DIRS['translations'] + Globals.SETTINGS['language'] + '/gamelog_messages')
def read_chests_and_chances_translation(type):
    return read_file(Globals.DIRS['translations'] + Globals.SETTINGS['language'] + '/' + get_gamename() + '/' + type)
