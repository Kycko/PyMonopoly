# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha, play_click_sound, read_translation, slight_animation_count_pos, switch_sound_state
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
        if self.group == 'stats_switch':
            self.cursor = OwnCursor('light_green', self.active_zone)
            self.HOTKEYS = (pygame.K_LEFT, pygame.K_RIGHT)
            self.tooltip = Tooltip(u'HOTKEYS: ← →', 'top', self.text)
        else:
            self.tooltip = None
    def move_text(self):
        self.text.move_text()
        self.make_active_zone()
        if self.group[:4] != 'main':
            self.cursor.rect = self.active_zone.copy()
            self.tooltip.move_text(self.text.rect)
    def update_text(self, text):
        self.text.update_text(text)
        self.make_active_zone()
    def make_active_zone(self):
        if self.group[:4] == 'main':
            if self.text.x == 'center':
                self.active_zone = self.text.rect.inflate(500-self.text.rect.w, 6)
            else:
                self.active_zone = self.text.rect.move(-150, -3)
                self.active_zone.size = (500, self.text.rect.h+6)
        else:
            self.active_zone = self.text.rect.inflate(6, 6)
    def group_checkings(self, state):
        if self.text.new_y != self.text.y:
            self.move_text()
        if self.group[:4] != 'main':
            self.cursor.render(state)
            self.tooltip.render(state)
    def render(self, state):
        if self.text.AV:
            self.group_checkings(state)
            self.text.render(True)
    def action(self):
        play_click_sound()
        if self.type == 'main_sysexit':
            SYSEXIT()
        elif self.type in ('main_settings_music', 'main_settings_sounds'):
            switch_sound_state(self.type[14:], Globals.SETTINGS[self.type[14:]])
        elif self.type == 'main_settings_language':
            Globals.SETTINGS['language'] = int(not(Globals.SETTINGS['language']))
            Globals.TRANSLATION = read_translation(Globals.SETTINGS['language'])
        return self.type
class Tooltip():
    def __init__(self, text, type, obj):
        self.type = type
        self.rect = pygame.Rect((0, 0), Globals.FONTS['ume_smaller'].size(text))
        self.move_text(obj.rect)
        self.text = Globals.FONTS['ume_smaller'].render(text, True, Globals.COLORS['grey'])
    def move_text(self, rect):
        x = rect.x + (rect.w - self.rect.w)/2 - 15
        y = rect.y - self.rect.h - 5
        self.rect.topleft = (x, y)
    def render(self, state):
        if state:
            Globals.screen.blit(self.text, self.rect.topleft)
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
        first_rect = self.screen_switched(menuitems, type)
        Cursor.__init__(self, 0, first_rect)
    def screen_switched(self, menuitems, type):
        self.make_keys(type)
        first_rect = self.update_cords(menuitems)
        self.change_pos(self.keys[0])
        return first_rect
    def make_keys(self, type):
        if type == 'main_main':
            self.keys = ['new_game', 'settings', 'stats', 'exit']
        elif type == 'main_stats':
            self.keys = ['exit']
        elif type == 'main_settings':
            self.keys = ['language', 'music', 'sounds', 'exit']
    def update_cords(self, menuitems):
        rects = [menuitems[key].active_zone for key in self.keys]
        self.cords = [rect.topleft for rect in rects]
        return rects[0]
    def keypress(self, KEY):
        if KEY == pygame.K_DOWN:
            self.change_pos(self.keys[-len(self.keys) + self.active_num + 1])
        else:
            self.change_pos(self.keys[self.active_num - 1])
    def change_pos(self, key):
        self.active_key = key
        self.active_num = self.keys.index(key)
        self.change_new_cords()
    def change_new_cords(self):
        self.new_cords = self.cords[self.active_num]
    def render(self, menuitems):
        if menuitems[self.keys[0]].active_zone.topleft != self.cords[0]:
            self.update_cords(menuitems)
            self.change_new_cords()
        self.rect.topleft = slight_animation_count_pos(self.new_cords, self.rect.topleft, 5)
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
