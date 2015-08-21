# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha
from sys import exit as SYSEXIT
from TransparentText import AlphaText

#--- Menuitems
class MenuItem():
    def __init__(self, text, type, group, number=None):
        self.type = type
        self.group = group
        self.text = AlphaText(text, group, number)
        self.init_for_group()
    def init_for_group(self):
        self.tooltip = None
        if self.group[:4] == 'main':
            self.active_zone = self.text.rect.inflate(500-self.text.rect.w, 6)
        elif self.group == 'somegroup':
            self.active_zone = self.text.rect.inflate(50, 6)
            self.cursor = OwnCursor(self.group, self.active_zone)
            self.HOTKEY = 'somehotkey'
    def render(self, state):
        if self.text.AV:
            if self.group[:4] != 'main':
                self.cursor.render(state)
            self.text.render()
    def action(self):
        if self.type == 'main_sysexit':
            SYSEXIT()
        else:
            return self.type
#--- Cursor TEMPLATE
class Cursor():
    def __init__(self, alpha, rect):
        self.x = rect.x
        self.size = rect.size
        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surf_color = change_color_alpha(Globals.COLORS['black'], alpha)
        self.count_u_length()
    def count_u_length(self):
        self.init_u_length = self.size[0]/2-3
        while self.init_u_length > 0:
            self.init_u_length -= self.u_growth
    def render(self):
        if self.u_length != self.size[0]/2-3:
            self.u_length += self.u_growth
            if self.surf_color.a != 104:
                self.surf_color.a += 8
            pygame.draw.rect(self.surf, self.surf_color, pygame.Rect((0, 0), self.size), 0)
            pygame.draw.line(self.surf, Globals.COLORS[self.u_color], (self.size[0]/2-self.u_length, self.size[1]-1), (self.size[0]/2+self.u_length, self.size[1]-1), 1)
        Globals.screen.blit(self.surf, (self.x, self.y))
#--- Cursors
class MainCursor(Cursor):
    def __init__(self, menuitems, type):
        self.init_for_type(type)
        self.u_growth = 20
        rects = [menuitems[key].active_zone for key in self.keys]
        Cursor.__init__(self, 0, rects[0])
        self.y_cords = [rect.y for rect in rects]
        self.change_pos(self.keys[0])
    def init_for_type(self, type):
        if type == 'main_main':
            self.keys = ['new_game', 'settings', 'stats', 'exit']
            self.u_colors = ['green200', 'yellow', 'yellow', 'red']
    def keypress(self, KEY):
        if KEY == pygame.K_DOWN:
            self.change_pos(self.keys[-len(self.keys) + self.active_num + 1])
        else:
            self.change_pos(self.keys[self.active_num - 1])
    def change_pos(self, key):
        self.active_key = key
        self.active_num = self.keys.index(key)
        self.y = self.y_cords[self.active_num]
        self.u_color = self.u_colors[self.active_num]
        self.u_length = self.init_u_length
class OwnCursor(Cursor):
    def __init__(self, type, rect):
        if type == 'a':
            self.u_color = 'yellow'
            self.y = rect.y
            self.u_growth = 5
        Cursor.__init__(self, 104, rect)
        self.u_length = self.init_u_length
    def render(self, state):
        if state:
            Cursor.render(self)
        elif self.u_length != self.init_u_length:
            self.u_length = self.init_u_length
