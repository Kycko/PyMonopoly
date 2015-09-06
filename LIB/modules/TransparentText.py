# -*- coding: utf-8 -*-
import Globals
from GlobalFuncs import slight_animation_count_pos
from pygame import Rect, Surface

class AlphaText():
    def __init__(self, text, group, number=None):
        self.init_for_group(group, number)
        self.anticolor = Globals.COLORS['white'] - self.color
        self.update_text(text)
    def init_for_group(self, group, number):
        self.AV = True
        #--- Fonts
        if group == 'main_settings_volume_SELECTOR':
            self.font = Globals.FONTS['ume_16']
        elif group[:4] == 'main' or group in ('stats_game_name', 'main_settings_left_MI'):
            self.font = Globals.FONTS['ubuntu_24']
        elif group == 'stats_common':
            self.font = Globals.FONTS['ubuntu_20']
        elif group in ('APPVERSION', 'authors', 'stats_switch', 'stats_bests', 'settings_left') or 'stats_table' in group:
            self.font = Globals.FONTS['ubuntu_16']
        elif group == 'stats_latest':
            self.font = Globals.FONTS['ume_12']
        else:
            self.font = Globals.FONTS['ubuntu_32']
        #--- Colors
        if group in ('authors', 'stats_switch'):
            self.color = Globals.COLORS['grey']
        else:
            self.color = Globals.COLORS['white']
        #--- Position
        if group == 'main_main':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/4
            self.y = Globals.RESOLUTION[1]/2+50+35*number
        elif group == 'stats_common':
            self.x = Globals.RESOLUTION[0]/7
            self.y = 320 + 25 * number
        elif group in ('main_stats', 'main_settings_exit'):
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/6
            self.y = Globals.RESOLUTION[1]+50
        elif group == 'stats_game_name':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3-50
            self.y = 280
        elif group == 'stats_switch':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3+85
            self.y = 280
        elif 'stats_table' in group:
            self.x = Globals.RESOLUTION[0]/7 + 150*int(group[len(group)-1])
            self.y = 365 + 20*number
        elif group == 'main_settings_volume_SELECTOR':
            self.x = Globals.RESOLUTION[0]/4 - 50 + 25*number
            self.y = 513
        elif group == 'settings_left':
            self.x = Globals.RESOLUTION[0]/5 - 80
            self.y = 320 + 55*number
        elif group == 'main_settings_left_MI':
            self.x = Globals.RESOLUTION[0]/4 - 50
            self.y = 342 + 55*number
        elif group == 'stats_latest':
            self.x = Globals.RESOLUTION[0]/7 + 365
            self.y = 365 + 20*number
        elif group == 'stats_bests':
            self.x = Globals.RESOLUTION[0]/7 - 20
            self.y = 400
        elif group == 'authors':
            self.x = 'right'
            self.x_offset = 10
            self.y = Globals.RESOLUTION[1]-26-20*number
        elif group == 'APPNAME':
            self.x = Globals.PICS['logo'].x + 110
            self.y = Globals.PICS['logo'].y + 10
        elif group == 'APPVERSION':
            self.x = Globals.PICS['logo'].x + 112
            self.y = Globals.PICS['logo'].y + 50
        if group[:5] in ('main_', 'stats', 'setti'):
            self.new_y = self.y - 100
        else:
            self.new_y = self.y
    def move_text(self):
        if self.new_y != self.y:
            self.x, self.y = slight_animation_count_pos((self.x, self.new_y), (self.x, self.y), 10)
            self.rect = Rect((self.rect.x, self.y), self.rect.size)
    def update_text(self, text):
        self.symbols = text
        size = self.font.size(text)
        xpos = self.find_xpos(size)
        self.rect = Rect((xpos, self.y), size)
        self.text = self.font.render(text, True, self.color)
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
