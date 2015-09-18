# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import read_stats
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
            self.menuitems = {'new_game'    : MenuItem(Globals.TRANSLATION[0], 'main_new_game', 'main_main', 0),
                              'settings'    : MenuItem(Globals.TRANSLATION[1], 'main_settings', 'main_main', 1),
                              'stats'       : MenuItem(Globals.TRANSLATION[2], 'main_stats', 'main_main', 2),
                              'exit'        : MenuItem(Globals.TRANSLATION[3], 'main_sysexit', 'main_main', 3)}
            self.objects = {}
            if key != 'exit':
                self.pics = {'background'   : Globals.PICS['background'],
                             'logo'         : Globals.PICS['logo'],
                             'order'        : ['background', 'logo']}
                self.labels = {'APPNAME'    : AlphaText('PyMonopoly', 'APPNAME'),
                               'APPVERSION' : AlphaText(Globals.TRANSLATION[4]+Globals.VERSION, 'APPVERSION'),
                               'resources'  : AlphaText('Thanks to: freemusicarchive.org, openclipart.org', 'authors', 0),
                               'authors'    : AlphaText('Anthony Samartsev & Michael Mozhaev, 2014-2015', 'authors', 1)}
            else:
                self.move_APPINFO(50)
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
        elif type == 'main_stats':
            self.move_APPINFO(-50)
            self.menuitems = {'exit'        : MenuItem(Globals.TRANSLATION[11], 'main_main', 'main_stats')}
            if not Globals.SETTINGS['block']:
                self.menuitems['switch'] = MenuItem(Globals.TRANSLATION[12], 'stats_switch', 'stats_switch')
            self.make_stats_screen(Globals.TRANSLATION[6-Globals.SETTINGS['fav_game']])
        elif type == 'main_settings':
            if key != 'exit':
                self.move_APPINFO(-50)
                Globals.TEMP_VARS['edit_player'] = 0
            else:
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.make_settings_screen()
        elif type == 'main_settings_player':
            self.menuitems = {'name'        : MenuItem(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['name'], 'main_settings_player_name', 'main_settings_player', 0),
                              'color'       : MenuItem('', 'main_settings_player_color_SELECTOR', 'main_settings_left_MI', 2),
                              'exit'        : MenuItem(Globals.TRANSLATION[21], 'main_settings', 'main_settings_player_exit')}
            self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.labels.update({'name'      : AlphaText(Globals.TRANSLATION[22], 'settings_left', 1),
                                'color'     : AlphaText(Globals.TRANSLATION[23], 'settings_left', 2)})
        elif type == 'main_settings_player_name':
            self.menuitems = {'exit'        : MenuItem(Globals.TRANSLATION[21], 'main_settings_player', 'main_settings_player_exit')}
            self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.labels.update({'name'      : AlphaText(Globals.TRANSLATION[24], 'settings_left', 1),
                                'name_MI'   : AlphaText(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['name'], 'main_settings_player', 0)})
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
        for label in self.labels.values():
            label.render()
        for obj in self.objects.values():
            obj.render()
        if self.cursor:
            self.cursor.render(self.menuitems)
        for key in self.menuitems.keys():
            self.menuitems[key].render(cur_key == key or self.cursor and self.cursor.active_key == key)
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
                elif self.menuitems['exit'].type == 'main_settings_player':
                    if e.key == pygame.K_BACKSPACE:
                        self.labels['name_MI'].symbols = self.labels['name_MI'].symbols[:len(self.labels['name_MI'].symbols)-1]
                        self.labels['name_MI'].RErender()
                else:
                    for key in self.menuitems.keys():
                        if e.key in self.menuitems[key].HOTKEYS:
                            if self.menuitems[key].group[:4] == 'main':
                                self.action_call(self.cursor.active_key)
                            else:
                                self.action_call(key)
            elif e.type == pygame.QUIT:
                SYSEXIT()
    def action_call(self, key):
        type = self.menuitems[key].action()
        if type == 'stats_switch':
            self.make_stats_screen(self.labels['game_name'].symbols)
        elif type == 'main_settings_language':
            self.labels['APPVERSION'].update_text(Globals.TRANSLATION[4]+Globals.VERSION)
            self.make_settings_screen()
        elif type == 'main_settings_player_color_SELECTOR':
            self.menuitems['name'].text.color = Globals.PLAYERS_COLORS[self.menuitems['color'].selector.active]
            self.menuitems['name'].text.RErender()
        elif type:
            self.switch_screen(type, key)
            self.cursor.screen_switched(self.menuitems, type)
    def move_APPINFO(self, offset):
        self.pics['logo'].new_y += offset
        for key in ('APPNAME', 'APPVERSION'):
            self.labels[key].new_y += offset
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
                self.labels.update({'bestname'+str(i-2)     : AlphaText(str(i-2)+'. '+data[i]['name'], 'stats_table_0', i)})
                self.labels.update({'bestscore'+str(i-2)    : AlphaText('  '*(10-len(str(data[i]['score'])))+str(data[i]['score']), 'stats_table_1', i)})
                self.labels.update({'bestdate'+str(i-2)     : AlphaText(data[i]['date'], 'stats_table_2', i)})
                if data[i]['recent']:
                    self.labels.update({'bestrecent'        : AlphaText('latest', 'stats_latest', i)})
        self.objects = {'game_name_UL'  : Line(self.labels['game_name'], 'bottom', 2),
                        'bestslbl_UL'   : Line(self.labels['bestslbl'], 'bottom', 2)}
    def make_settings_screen(self):
        self.menuitems = {'language'    : MenuItem(u'‹ '+Globals.LANGUAGES[Globals.SETTINGS['language']][1]+u' ›', 'main_settings_language', 'main_settings_left_MI', 0),
                          'player'      : MenuItem(Globals.PLAYERS[0]['name'], 'main_settings_player', 'main_settings_player', 0),
                          'music'       : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['music'])]+u' ›', 'main_settings_music', 'main_settings_left_MI', 2),
                          'sounds'      : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['sounds'])]+u' ›', 'main_settings_sounds', 'main_settings_left_MI', 3),
                          'volume'      : MenuItem('', 'main_settings_volume_SELECTOR', 'main_settings_left_MI', 4),
                          'exit'        : MenuItem(Globals.TRANSLATION[13], 'main_main', 'main_settings_exit')}
        self.labels.update({'language'  : AlphaText(Globals.TRANSLATION[14], 'settings_left', 0),
                            'player'    : AlphaText(Globals.TRANSLATION[20], 'settings_left', 1),
                            'music'     : AlphaText(Globals.TRANSLATION[15], 'settings_left', 2),
                            'sounds'    : AlphaText(Globals.TRANSLATION[16], 'settings_left', 3),
                            'volume'    : AlphaText(Globals.TRANSLATION[19], 'settings_left', 4)})
