# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha, slight_animation_count_pos
from sys import exit as SYSEXIT
from TransparentText import AlphaText

#--- Menuitems
class MenuItem():
    def __init__(self, text, type, group, number=None):
        self.type = type
        self.group = group
        self.text = AlphaText(text, group, number)
        self.make_active_zone()
        self.init_for_group()
    def init_for_group(self):
        self.tooltip = None
        if self.group == 'somegroup':
            self.cursor = OwnCursor('black', self.active_zone)
            self.HOTKEY = 'somehotkey'
    def update_text(self, text):
        self.text.update_text(text)
        self.make_active_zone()
    def make_active_zone(self):
        if self.group[:4] == 'main':
            self.active_zone = self.text.rect.inflate(500-self.text.rect.w, 6)
        elif self.group == 'somegroup':
            self.active_zone = self.text.rect.inflate(50, 6)
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
        self.rect = rect.copy()
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.surf_color = change_color_alpha(Globals.COLORS['black'], alpha)
    def draw_rect(self):
        pygame.draw.rect(self.surf, self.surf_color, ((0, 0), self.rect.size), 0)
    def render(self):
        Globals.screen.blit(self.surf, self.rect.topleft)
#--- Cursors
class MainCursor(Cursor):
    def __init__(self, menuitems, type):
        self.make_keys(type)
        rects = [menuitems[key].active_zone for key in self.keys]
        self.y_cords = [rect.y for rect in rects]
        self.change_pos(self.keys[0])
        Cursor.__init__(self, 0, rects[0])
    def make_keys(self, type):
        if type == 'main_main':
            self.keys = ['new_game', 'settings', 'stats', 'exit']
    def keypress(self, KEY):
        if KEY == pygame.K_DOWN:
            self.change_pos(self.keys[-len(self.keys) + self.active_num + 1])
        else:
            self.change_pos(self.keys[self.active_num - 1])
    def change_pos(self, key):
        self.active_key = key
        self.active_num = self.keys.index(key)
        self.new_y = self.y_cords[self.active_num]
    def render(self):
        self.rect.y = slight_animation_count_pos(self.new_y, self.rect.y)
        if self.surf_color.a != 104:
            self.surf_color.a += 8
            self.draw_rect()
        Cursor.render(self)
class OwnCursor(Cursor):
    def __init__(self, color, rect):
        self.u_color = Globals.COLORS[color]
        self.u_length = 0
        Cursor.__init__(self, 104, rect)
    def render(self, state):
        if state:
            if self.u_length < self.rect.w/2-25:
                self.u_length += 1
                self.draw_rect()
                pygame.draw.line(self.surf, self.u_color, (self.rect.w/2-self.u_length, self.rect.h-1), (self.rect.w/2+self.u_length, self.rect.h-1), 1)
            Cursor.render(self)
        elif self.u_length:
            self.u_length = 0
