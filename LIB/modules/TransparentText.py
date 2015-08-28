# -*- coding: utf-8 -*-
import Globals
from GlobalFuncs import slight_animation_count_pos
from pygame import Rect, Surface

class AlphaText():
    def __init__(self, text, group, number=None):
        self.alpha = 5
        self.symbols = text
        self.init_for_group(group, number)
        self.anticolor = Globals.COLORS['white'] - self.color
        self.update_text()
    def init_for_group(self, group, number):
        self.AV = True
        #--- Fonts
        if group[:4] == 'main' or group == 'stats_game_name':
            self.font = Globals.FONTS['ubuntu_big']
        elif group in ('stats_common', 'stats_bests'):
            self.font = Globals.FONTS['ubuntu_medium']
        elif group in ('APPVERSION', 'authors', 'stats_switch'):
            self.font = Globals.FONTS['ubuntu_small']
        else:
            self.font = Globals.FONTS['ubuntu_bigger']
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
        elif group == 'main_stats':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/6
            self.y = Globals.RESOLUTION[1]+50
        elif group == 'stats_game_name':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3-50
            self.y = 280
        elif group == 'stats_switch':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3+100
            self.y = 280
        elif group == 'stats_bests':
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/3-20
            self.y = 450
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
        if group[:5] in ('main_', 'stats'):
            self.new_y = self.y - 100
        else:
            self.new_y = self.y
    def move_text(self):
        if self.new_y != self.y:
            self.x, self.y = slight_animation_count_pos((self.x, self.new_y), (self.x, self.y), 10)
            self.rect = Rect((self.rect.x, self.y), self.rect.size)
    def update_text(self):
        size = self.font.size(self.symbols)
        xpos = self.find_xpos(size)
        self.rect = Rect((xpos, self.y), size)
        self.text = self.font.render(self.symbols, True, self.color)
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
