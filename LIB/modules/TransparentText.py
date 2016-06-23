# -*- coding: utf-8 -*-
import Globals
from GlobalFuncs import slight_animation_count_pos
from pygame import Rect, Surface

class AlphaText():
    def __init__(self, text, group, number=0):
        self.group = group
        self.init_for_group(number)
        self.anticolor = Globals.COLORS['white'] - self.color
        self.update_text(text)
        self.init_new_pos()
    def init_for_group(self, number):
        #--- Fonts
        if 'SELECTOR' in self.group:
            self.font = Globals.FONTS['ume_16']
        elif self.group == 'step_indicator':
            self.font = Globals.FONTS['ume_8']
        elif self.group in ('target_cell_owner', 'target_cell_info') or 'gamelog_message' in self.group:
            self.font = Globals.FONTS['ubuntu_13']
        elif self.group in ('from_game_return_to_menu', 'show_menu', 'pl_info_tab'):
            self.font = Globals.FONTS['ume_32']
        elif self.group == 'ingame_dices':
            self.font = Globals.FONTS['dejavu_72']
        elif self.group[:4] in ('inga', 'main') or self.group in ('stats_game_name', 'main_settings_left_MI', 'main_settings_player', 'target_cell_name'):
            self.font = Globals.FONTS['ubuntu_24']
        elif self.group == 'stats_common':
            self.font = Globals.FONTS['ubuntu_20']
        elif self.group in ('APPVERSION', 'authors', 'stats_switch', 'stats_bests', 'settings_left', 'volume_in_game_lbl') or 'stats_table' in self.group or 'ERROR' in self.group:
            self.font = Globals.FONTS['ubuntu_16']
        elif self.group == 'music_and_sound_switches':
            self.font = Globals.FONTS['ume_16']
        elif self.group == 'stats_latest':
            self.font = Globals.FONTS['ume_12']
        elif self.group in ('newgame_playertype', 'pl_money_info'):
            self.font = Globals.FONTS['ubuntu_11']
        else:
            self.font = Globals.FONTS['ubuntu_32']
        #--- Colors
        if self.group == 'target_cell_owner':
            self.color = Globals.main_scr.objects['gamefield'].cells[Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field].color
        elif 'gamelog_message' in self.group:
            self.choose_switch_color(self.group)
        elif self.group in ('authors', 'stats_switch', 'from_game_return_to_menu', 'show_menu', 'pl_money_info'):
            self.color = Globals.COLORS['grey']
        elif 'volume_SELECTOR' in self.group:
            self.choose_selector_color('volume', number)
        elif self.group == 'main_new_total_SELECTOR':
            self.choose_selector_color('new_settings_total', number)
        elif self.group == 'main_new_humans_SELECTOR':
            self.choose_selector_color('new_settings_humans', number)
        elif self.group == 'music_and_sound_switches':
            self.choose_switch_color(('music', 'sounds')[number])
        elif self.group == 'pl_info_tab':
            self.color = Globals.PLAYERS[number].color
        elif self.group == 'main_new_playerlist':
            self.color = Globals.PLAYERS[number].color
        elif self.group == 'main_settings_player_color_SELECTOR':
            self.color = Globals.PLAYERS_COLORS[number]
        elif self.group == 'main_settings_player':
            self.color = Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].color
        elif 'ERROR' in self.group:
            self.color = Globals.COLORS['light_red']
        else:
            self.color = Globals.COLORS['white']
        #--- Position
        if self.group[:16] == 'gamelog_message_':
            self.x = 0
            self.rect = Rect((0, 0+18*number), (0, 0))
        elif self.group == 'onboard_select_cell':
            self.x = Globals.TEMP_VARS['cells_rects'][number].x
            self.rect = Globals.TEMP_VARS['cells_rects'][number]
        elif self.group == 'step_indicator':
            if number in range(11)+range(20, 31):
                self.x = Globals.TEMP_VARS['cells_rects'][number].centerx - 4
            elif number in range(11, 20):
                self.x = 283
            elif number in range(31, 40):
                self.x = 910
            if number in range(11):
                self.rect = Rect((0, 679), (0, 0))
            elif number in range(11, 20)+range(31, 40):
                self.rect = Rect((0, Globals.TEMP_VARS['cells_rects'][number].centery - 6), (0, 0))
            elif number in range(20, 31):
                self.rect = Rect((0, 55), (0, 0))
        elif self.group in ('ingame_main', 'ingame_dices'):
            self.x = 'center'
            self.x_offset = 0
            self.rect = Rect((0, 360+35*number), (0, 0))
        elif self.group[:12] == 'target_cell_':
            self.x = 'center'
            self.x_offset = 0
            self.rect = Rect((0, 430+35*number-5*(number-1)), (0, 0))
        elif self.group == 'ingame_start':
            self.x = 'center'
            self.x_offset = 1820
            self.rect = Rect((0, 400+35*number), (0, 0))
        elif self.group == 'main_main':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/4
            self.rect = Rect((0, Globals.RESOLUTION[1]/2+50+35*number), (0, 0))
        elif self.group == 'stats_common':
            self.x = Globals.RESOLUTION[0]/7
            self.rect = Rect((0, 320 + 25 * number), (0, 0))
        elif 'exit' in self.group or self.group == 'main_stats':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/6
            self.rect = Rect((0, Globals.RESOLUTION[1]+50-35*number), (0, 0))
        elif self.group == 'stats_game_name':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3-50
            self.rect = Rect((0, 280), (0, 0))
        elif self.group == 'stats_switch':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3+85
            self.rect = Rect((0, 280), (0, 0))
        elif 'stats_table' in self.group:
            self.x = Globals.RESOLUTION[0]/7 + 150*int(self.group[len(self.group)-1])
            self.rect = Rect((0, 365 + 20*number), (0, 0))
        elif self.group == 'from_game_return_to_menu':
            self.x = Globals.RESOLUTION[0] - 42
            self.rect = Rect((0, -95), (0, 0))
        elif self.group == 'show_menu':
            self.x = Globals.RESOLUTION[0] - 42
            self.rect = Rect((0, 6), (0, 0))
        elif self.group == 'main_settings_volume_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.rect = Rect((0, 623), (0, 0))
        elif self.group == 'main_settings_player_color_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.rect = Rect((0, 458), (0, 0))
        elif self.group == 'main_new_humans_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.rect = Rect((0, 403), (0, 0))
        elif self.group == 'main_new_total_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.rect = Rect((0, 348), (0, 0))
        elif self.group == 'main_new_playerlist':
            self.x = Globals.RESOLUTION[0]/4 - 50
            self.rect = Rect((0, 452 + 30*number), (0, 0))
        elif self.group == 'settings_left':
            self.x = Globals.RESOLUTION[0]/5 - 80
            self.rect = Rect((0, 320 + 55*number), (0, 0))
        elif self.group == 'newgame_playertype':
            self.x = Globals.RESOLUTION[0]/4 - 48 + Globals.FONTS['ubuntu_24'].size(Globals.PLAYERS[number].name)[0]
            self.rect = Rect((0, 455 + 30*number), (0, 0))
        elif self.group == 'main_settings_left_MI':
            self.x = Globals.RESOLUTION[0]/4 - 50
            self.rect = Rect((0, 342 + 55*number), (0, 0))
        elif self.group == 'main_settings_player':
            self.x = Globals.RESOLUTION[0]/4 - 50
            self.rect = Rect((0, 397 + 35*number), (0, 0))
        elif self.group == 'stats_latest':
            self.x = Globals.RESOLUTION[0]/7 + 365
            self.rect = Rect((0, 365 + 20*number), (0, 0))
        elif self.group == 'stats_bests':
            self.x = Globals.RESOLUTION[0]/7 - 20
            self.rect = Rect((0, 400), (0, 0))
        elif self.group == 'pl_info_tab':
            self.x = Globals.RESOLUTION[0]+1780
            self.rect = Rect((0, Globals.RESOLUTION[1]-(len(Globals.PLAYERS)-number)*39), (0, 0))
        elif self.group == 'pl_money_info':
            self.x = 'right'
            self.x_offset = -1781
            self.rect = Rect((0, Globals.RESOLUTION[1]-(len(Globals.PLAYERS)-number)*40+23), (0, 0))
        elif self.group == 'in_game_volume_SELECTOR':
            self.x = Globals.main_scr.labels['volume_level'].rect.w+20+25*number
            self.rect = Rect((0, -92), (0, 0))
        elif self.group == 'music_and_sound_switches':
            self.x = Globals.main_scr.labels['sounds'].rect.w+28
            self.rect = Rect((0, 31*number-59), (0, 0))
        elif self.group == 'volume_in_game':
            self.x = Globals.main_scr.labels['volume_level'].rect.w+15
            self.rect = Rect((0, -100), (0, 0))
        elif self.group == 'volume_in_game_lbl':
            self.x = 8
            self.rect = Rect((0, 32*number-94), (0, 0))
        elif self.group == 'ERROR_main':
            self.x = Globals.RESOLUTION[0]/2
            self.rect = Rect((0, Globals.RESOLUTION[1]/2), (0, 0))
        elif self.group == 'authors':
            self.x = 'right'
            self.x_offset = 10
            self.rect = Rect((0, Globals.RESOLUTION[1]-26-20*number), (0, 0))
        elif self.group == 'APPNAME':
            self.x = Globals.PICS['logo'].pos[0] + 110
            self.rect = Rect((0, Globals.PICS['logo'].pos[1] + 10), (0, 0))
        elif self.group == 'APPVERSION':
            self.x = Globals.PICS['logo'].pos[0] + 112
            self.rect = Rect((0, Globals.PICS['logo'].pos[1] + 50), (0, 0))
        temp = ('in_game_volume_SELECTOR', 'music_and_sound_switches', 'volume_in_game', 'volume_in_game_lbl')
        if not Globals.SETTINGS['music'] and not Globals.SETTINGS['sounds'] and self.group in temp:
            self.rect.y -= 33
    def init_new_pos(self):
        if self.group[:12] == 'target_cell_':
            self.new_pos = (self.rect.x, self.rect.y - 70)
        elif self.group[:5] in ('main_', 'stats', 'setti', 'newga', 'ingam'):
            self.new_pos = (self.rect.x, self.rect.y - 100)
        elif 'ERROR' in self.group:
            self.new_pos = (self.rect.x + 25, self.rect.y - 50)
        else:
            self.new_pos = self.rect.topleft
        self.speed_limit = 50
    def change_new_pos(self, offset):
        self.new_pos = (self.new_pos[0] + offset[0], self.new_pos[1] + offset[1])
    def change_color(self, color):
        self.color = color
        self.RErender()
    def choose_selector_color(self, type, num):
        if type == 'volume':
            state = num < Globals.SETTINGS['volume']*10
        elif type == 'new_settings_total':
            state = num < len(Globals.PLAYERS)
        elif type == 'new_settings_humans':
            state = Globals.PLAYERS[num].human
        if state:
            self.color = Globals.COLORS['white']
        else:
            self.color = Globals.COLORS['grey63']
    def choose_switch_color(self, type):
        if type in ('music', 'sounds'):
            if Globals.SETTINGS[type]:
                self.color = Globals.COLORS['deep_green']
            else:
                self.color = Globals.COLORS['light_red']
        elif type == 'gamelog_message_common':
            self.color = Globals.COLORS['grey22']
        elif type == 'gamelog_message_player_switched':
            self.color = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].color
    def RErender(self):
        if self.group == 'target_cell_name':
            self.font.set_underline(True)
        self.text = self.font.render(self.symbols, True, self.color)
        if self.group == 'target_cell_name':
            self.font.set_underline(False)
    def move_text(self):
        self.rect.topleft = slight_animation_count_pos(self.new_pos, self.rect.topleft, 10, self.speed_limit)
    def update_text(self, text, reset_alpha=True):
        self.symbols = text
        if self.group != 'onboard_select_cell':
            size = self.font.size(text)
            xpos = self.find_xpos(size)
            self.rect = Rect((xpos, self.rect.y), size)
        self.RErender()
        if reset_alpha:
            self.alpha = 5
    def find_xpos(self, size):
        if self.x == 'center':
            return Globals.RESOLUTION[0]/2 + self.x_offset - size[0]/2
        elif self.x == 'right':
            return Globals.RESOLUTION[0] - size[0] - self.x_offset
        else:
            return self.x
    def set_alpha(self):
        if self.alpha != 255:
            self.alpha += 10
        if self.alpha != 255:
            surf = Surface(self.rect.size)
            surf.fill(self.anticolor)
            surf.set_colorkey(self.anticolor)
            surf.blit(self.text, (0, 0))
            surf.set_alpha(self.alpha)
            return surf
        else:
            return self.text
    def render(self, MENU=False):
        if not MENU:
            self.move_text()
        Globals.screen.blit(self.set_alpha(), self.rect.topleft)
