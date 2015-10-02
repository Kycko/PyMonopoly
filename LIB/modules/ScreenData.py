# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import add_new_player, count_new_pos, create_players_list, read_file, read_stats
from MenuItems import MainCursor, MenuItem
from Sprite import Line
from TransparentText import AlphaText
from sys import exit as SYSEXIT

class MainScreen():
    def __init__(self):
        self.switch_screen('main_main', None)
        self.cursor = MainCursor(self.menuitems, 'main_main')
    def switch_screen(self, type, key):
        if type == 'main_main':
            if key != 'exit':
                self.pics = {'background'   : Globals.PICS['background'],
                             'logo'         : Globals.PICS['logo'],
                             'order'        : ['background', 'logo']}
                self.labels = {'APPNAME'    : AlphaText('PyMonopoly', 'APPNAME'),
                               'APPVERSION' : AlphaText(Globals.TRANSLATION[4]+Globals.VERSION, 'APPVERSION'),
                               'resources'  : AlphaText('Thanks to: freemusicarchive.org, openclipart.org', 'authors', 0),
                               'authors'    : AlphaText('Anthony Samartsev & Michael Mozhaev, 2014-2015', 'authors', 1)}
            else:
                if self.menuitems['exit'].group == 'main_settings_player_exit':
                    self.move_APPINFO((-300, 0))
                    Globals.TEMP_VARS.clear()
                    create_players_list()
                else:
                    self.move_APPINFO((0, 50))
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.menuitems = {'new_game'    : MenuItem(Globals.TRANSLATION[0], 'main_new_game', 'main_main', 0),
                              'settings'    : MenuItem(Globals.TRANSLATION[1], 'main_settings', 'main_main', 1),
                              'stats'       : MenuItem(Globals.TRANSLATION[2], 'main_stats', 'main_main', 2),
                              'exit'        : MenuItem(Globals.TRANSLATION[3], 'main_sysexit', 'main_main', 3)}
            self.objects = {}
        elif type == 'main_stats':
            self.move_APPINFO((0, -50))
            self.menuitems = {'exit'        : MenuItem(Globals.TRANSLATION[11], 'main_main', 'main_stats')}
            if not Globals.SETTINGS['block']:
                self.menuitems['switch'] = MenuItem(Globals.TRANSLATION[12], 'stats_switch', 'stats_switch')
            self.make_stats_screen(Globals.TRANSLATION[6-Globals.SETTINGS['fav_game']])
        elif type == 'main_settings':
            if key != 'exit':
                self.move_APPINFO((0, -50))
                Globals.TEMP_VARS['edit_player'] = 0
            else:
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.make_settings_screen()
        elif 'main_new_edit_player' in type or type == 'main_settings_player':
            if key == 'exit':
                Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['name'] = self.labels['name_MI'].symbols
                self.objects = {}
            self.make_playersettings_screen()
            if 'main_new_edit_player' in type:
                self.menuitems.update({'exit'   : MenuItem(Globals.TRANSLATION[21], 'main_new_game', 'main_settings_player_exit')})
            else:
                self.menuitems.update({'exit'   : MenuItem(Globals.TRANSLATION[21], 'main_settings', 'main_settings_player_exit')})
        elif type == 'main_settings_player_name':
            if self.menuitems['exit'].type == 'main_new_game':
                type = 'main_new_edit_player'
            else:
                type = 'main_settings_player'
            self.menuitems = {'exit'        : MenuItem(Globals.TRANSLATION[21], type, 'main_settings_player_exit')}
            self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.labels.update({'name'      : AlphaText(Globals.TRANSLATION[24], 'settings_left', 1),
                                'name_MI'   : AlphaText(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['name'], 'main_settings_player', 0)})
            self.make_obj_for_enter_name()
        elif type == 'main_new_game':
            if key == 'exit':
                Globals.TEMP_VARS.pop('edit_player')
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
                self.check_error(type)
            else:
                self.move_APPINFO((300, 0))
                Globals.TEMP_VARS['cur_game'] = Globals.SETTINGS['fav_game']
                self.init_avail_colors_and_names()
                LGS = read_file(Globals.FILES['last_game_settings'])
                for string in LGS:
                    add_new_player(string == 'human')
            self.menuitems = {'total'           : MenuItem('', 'main_new_total_SELECTOR', 'main_settings_left_MI', 1),
                              'humans'          : MenuItem('', 'main_new_humans_SELECTOR', 'main_settings_left_MI', 2),
                              'exit'            : MenuItem(Globals.TRANSLATION[11], 'main_main', 'main_settings_player_exit')}
            self.labels.update({'total'         : AlphaText(Globals.TRANSLATION[28], 'settings_left', 1),
                                'inactive_MI'   : AlphaText(u'●', 'main_new_total_SELECTOR', 0),
                                'humans'        : AlphaText(Globals.TRANSLATION[30], 'settings_left', 2),
                                'players'       : AlphaText(Globals.TRANSLATION[31], 'settings_left', 3)})
            for i in range(len(Globals.PLAYERS)):
                self.menuitems.update({'player'+str(i)  : MenuItem(Globals.PLAYERS[i]['name'], 'main_new_edit_player_'+str(i), 'main_new_playerlist', i)})
                if not Globals.PLAYERS[i]['human']:
                    self.labels.update({'playertype'+str(i) : AlphaText('AI', 'newgame_playertype', i)})
            if not Globals.SETTINGS['block']:
                self.menuitems.update({'game'   : MenuItem(u'‹ '+Globals.TRANSLATION[5+int(Globals.TEMP_VARS['cur_game'])]+u' ›', 'main_new_game_switch', 'main_settings_left_MI', 0)})
                self.labels.update({'game'      : AlphaText(Globals.TRANSLATION[27], 'settings_left', 0)})
    def clear_labels(self, exception):
        for key in self.labels.keys():
            if key not in exception:
                self.labels.pop(key)
    def mainloop(self):
        while True:
            cur_key = self.check_mouse_pos(pygame.mouse.get_pos())
            self.render(cur_key)
            self.events(cur_key)
    def check_mouse_pos(self, mp):
        key = self.find_hovering_menuitem(mp)
        if key != self.cursor.active_key and key in self.cursor.keys:
            self.cursor.change_pos(key)
        return key
    def find_hovering_menuitem(self, mp):
        for key in self.menuitems.keys():
            if self.menuitems[key].active_zone.collidepoint(mp):
                if 'SELECTOR' in self.menuitems[key].type:
                    for i in range(len(self.menuitems[key].selector.items)):
                        if self.menuitems[key].selector.rects[i].collidepoint(mp):
                            self.menuitems[key].selector.apply_new_active(i)
                return key
        return None
    def render(self, cur_key):
        for key in self.pics['order']:
            self.pics[key].render()
        for obj in self.objects.values():
            obj.render()
        if self.cursor:
            self.cursor.render(self.menuitems)
        for key in self.menuitems.keys():
            self.menuitems[key].render(cur_key == key or self.cursor and self.cursor.active_key == key)
        for label in self.labels.values():
            label.render()
        Globals.window.blit(Globals.screen, (0, 0))
        pygame.display.flip()
    def events(self, cur_key):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and cur_key:
                self.action_call(cur_key)
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_DOWN) and self.cursor:
                    self.cursor.keypress(e.key)
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.cursor:
                    self.action_call(self.cursor.active_key)
                elif e.key == pygame.K_ESCAPE:
                    self.action_call('exit')
                elif e.key in (pygame.K_LEFT, pygame.K_RIGHT) and 'SELECTOR' in self.menuitems[self.cursor.active_key].type:
                    self.menuitems[self.cursor.active_key].selector.keypress(e.key)
                elif 'main_new_edit_player' in self.menuitems['exit'].type or self.menuitems['exit'].type == 'main_settings_player':
                    if e.key == pygame.K_BACKSPACE:
                        self.labels['name_MI'].update_text(self.labels['name_MI'].symbols[:len(self.labels['name_MI'].symbols)-1], False)
                    elif len(self.labels['name_MI'].symbols) < 15:
                        self.labels['name_MI'].update_text(self.labels['name_MI'].symbols + e.unicode, False)
                    self.make_obj_for_enter_name()
                elif self.cursor and e.key in self.menuitems[self.cursor.active_key].HOTKEYS:
                        self.action_call(self.cursor.active_key)
                else:
                    for key in self.menuitems.keys():
                        if self.menuitems[key].type[:4] != 'main' and e.key in self.menuitems[key].HOTKEYS:
                            self.action_call(key)
            elif e.type == pygame.QUIT:
                SYSEXIT()
    def action_call(self, key):
        type = self.menuitems[key].action(key)
        if type == 'stats_switch':
            self.make_stats_screen(self.labels['game_name'].symbols)
        elif type == 'main_settings_language':
            self.labels['APPVERSION'].update_text(Globals.TRANSLATION[4]+Globals.VERSION)
            self.make_settings_screen()
        elif type == 'main_settings_player_color_SELECTOR':
            self.menuitems['name'].text.color = Globals.PLAYERS_COLORS[self.menuitems['color'].selector.active]
            self.menuitems['name'].text.RErender()
        elif type and ('main_new_edit_player' in type or type == 'main_settings_player') and key == 'exit' and not self.labels['name_MI'].symbols:
            if 'error' not in self.labels.keys():
                self.labels.update({'error' : AlphaText(Globals.TRANSLATION[29], 'ERROR_main')})
        elif type == 'main_new_total_SELECTOR':
            old = len(Globals.PLAYERS)
            new = self.menuitems[key].selector.active + 2
            if new < old:
                for i in range(new, old):
                    self.menuitems.pop('player'+str(i))
                    if not Globals.PLAYERS[i]['human']:
                        self.labels.pop('playertype'+str(i))
                    Globals.TEMP_VARS['avail_colors'].append(Globals.PLAYERS[i]['color'])
                    Globals.TEMP_VARS['avail_names'].append(Globals.PLAYERS[i]['name'])
                Globals.PLAYERS = Globals.PLAYERS[:new]
        elif type:
            self.switch_screen(type, key)
            self.cursor.screen_switched(self.menuitems, type)
    def move_APPINFO(self, offset):
        for obj in (self.pics['logo'], self.labels['APPNAME'], self.labels['APPVERSION']):
            obj.new_pos = count_new_pos(obj.new_pos, offset)
    def make_stats_screen(self, current):
        self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
        new = not(6-Globals.TRANSLATION.index(current))
        data = read_stats(new)
        if data[1]:
            data[1] = str(data[1]) + ' ('+str(round(data[1]*100/data[0], 2))+' %)'
        self.labels.update({'game_name' : AlphaText(Globals.TRANSLATION[6-new], 'stats_game_name'),
                            'total'     : AlphaText(Globals.TRANSLATION[8] + str(data[0]), 'stats_common', 0),
                            'wins'      : AlphaText(Globals.TRANSLATION[9] + str(data[1]), 'stats_common', 1),
                            'profit'    : AlphaText(Globals.TRANSLATION[10] + '$' + str(data[2]), 'stats_common', 2),
                            'bestslbl'  : AlphaText(Globals.TRANSLATION[7], 'stats_bests', 3)})
        for i in range(3, len(data)):
            if data[i]['score']:
                self.labels.update({'bestname'+str(i-2)     : AlphaText(str(i-2)+'. '+data[i]['name'], 'stats_table_0', i),
                                    'bestscore'+str(i-2)    : AlphaText('  '*(10-len(str(data[i]['score'])))+str(data[i]['score']), 'stats_table_1', i),
                                    'bestdate'+str(i-2)     : AlphaText(data[i]['date'], 'stats_table_2', i)})
                if data[i]['recent']:
                    self.labels.update({'bestrecent'        : AlphaText('latest', 'stats_latest', i)})
        self.objects = {'game_name_UL'  : Line(self.labels['game_name'], 'bottom', 2),
                        'bestslbl_UL'   : Line(self.labels['bestslbl'], 'bottom', 2)}
    def make_settings_screen(self):
        self.menuitems = {'language'    : MenuItem(u'‹ '+Globals.LANGUAGES[Globals.SETTINGS['language']][1]+u' ›', 'main_settings_language', 'main_settings_left_MI', 0),
                          'player'      : MenuItem(Globals.PLAYERS[0]['name'], 'main_settings_player', 'main_settings_player', 0),
                          'hotkeys'     : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['hotkeys'])]+u' ›', 'main_settings_hotkeys', 'main_settings_left_MI', 2),
                          'music'       : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['music'])]+u' ›', 'main_settings_music', 'main_settings_left_MI', 3),
                          'sounds'      : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['sounds'])]+u' ›', 'main_settings_sounds', 'main_settings_left_MI', 4),
                          'volume'      : MenuItem('', 'main_settings_volume_SELECTOR', 'main_settings_left_MI', 5),
                          'exit'        : MenuItem(Globals.TRANSLATION[13], 'main_main', 'main_settings_exit')}
        self.labels.update({'language'  : AlphaText(Globals.TRANSLATION[14], 'settings_left', 0),
                            'player'    : AlphaText(Globals.TRANSLATION[20], 'settings_left', 1),
                            'hotkeys'   : AlphaText(Globals.TRANSLATION[25], 'settings_left', 2),
                            'music'     : AlphaText(Globals.TRANSLATION[15], 'settings_left', 3),
                            'sounds'    : AlphaText(Globals.TRANSLATION[16], 'settings_left', 4),
                            'volume'    : AlphaText(Globals.TRANSLATION[19], 'settings_left', 5)})
        if not Globals.SETTINGS['block']:
            self.menuitems.update({'fav_game'   : MenuItem(u'‹ '+Globals.TRANSLATION[5+int(Globals.SETTINGS['fav_game'])]+u' ›', 'main_settings_fav_game', 'main_settings_left_MI', 6)})
            self.labels.update({'fav_game'      : AlphaText(Globals.TRANSLATION[26], 'settings_left', 6)})
    def make_obj_for_enter_name(self):
        self.objects = {'text_cursor'   : Line(self.labels['name_MI'], 'right', 2, Globals.COLORS['white'])}
    def make_playersettings_screen(self):
        self.menuitems = {'name'        : MenuItem(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['name'], 'main_settings_player_name', 'main_settings_player', 0),
                          'color'       : MenuItem('', 'main_settings_player_color_SELECTOR', 'main_settings_left_MI', 2)}
        self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
        self.labels.update({'name'      : AlphaText(Globals.TRANSLATION[22], 'settings_left', 1),
                            'color'     : AlphaText(Globals.TRANSLATION[23], 'settings_left', 2)})
    def init_avail_colors_and_names(self):
        Globals.TEMP_VARS['avail_colors'] = [color for color in Globals.PLAYERS_COLORS if color != Globals.PLAYERS[0]['color']]
        Globals.TEMP_VARS['avail_names'] = read_file(Globals.DIRS['translations'] + Globals.LANGUAGES[Globals.SETTINGS['language']][0] + '/names')
        if Globals.PLAYERS[0]['name'] in Globals.TEMP_VARS['avail_names']:
            Globals.TEMP_VARS['avail_names'].remove(Globals.PLAYERS[0]['name'])
    def check_error(self, type):
        if type == 'main_new_game':
            if self.check_doubles_for_players() and 'error' not in self.labels.keys():
                self.labels.update({'error' : AlphaText(Globals.TRANSLATION[32], 'ERROR_main')})
    def check_doubles_for_players(self):
        for i in range(len(Globals.PLAYERS)-1):
            for j in range(i+1, len(Globals.PLAYERS)):
                if Globals.PLAYERS[i]['color'] == Globals.PLAYERS[j]['color'] or Globals.PLAYERS[i]['name'] == Globals.PLAYERS[j]['name']:
                    return True
