# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import *
from sys import exit as SYSEXIT
from TransparentText import AlphaText

#--- Menuitems
class MenuItem():
    def __init__(self, text, type, group, number=0):
        self.type = type
        self.group = group
        self.text = AlphaText(text, group, number)
        self.make_active_zone()
        self.init_for_group()
        self.init_for_type()
    def init_for_group(self):
        if self.group in ('stats_switch', 'onboard_select_cell'):
            self.cursor = OwnCursor('light_green', self.active_zone)
            self.tooltip = Tooltip(u'HOTKEYS: ← →', 'top', self.text)
        else:
            self.tooltip = None
    def init_for_type(self):
        #--- Hotkeys
        if self.type in ('main_settings_language', 'main_settings_hotkeys', 'main_settings_music', 'main_settings_sounds', 'main_settings_fav_game', 'stats_switch', 'main_new_game_switch'):
            self.HOTKEYS = (pygame.K_LEFT, pygame.K_RIGHT)
        else:
            self.HOTKEYS = ()
        #--- Selector
        if 'SELECTOR' in self.type:
            self.selector = MenuSelector(self.type)
    def move_text(self):
        self.text.move_text()
        if 'SELECTOR' in self.type:
            self.selector.move_text()
        self.make_active_zone()
        if self.group[:4] not in ('main', 'inga'):
            self.cursor.rect = self.active_zone.copy()
            self.tooltip.move_text(self.text.rect)
    def update_text(self, text):
        self.text.update_text(text)
        self.make_active_zone()
    def make_active_zone(self):
        if self.group[:4] in ('main', 'inga'):
            if self.text.x == 'center':
                self.active_zone = self.text.rect.inflate(400-self.text.rect.w, 6)
            else:
                self.active_zone = self.text.rect.move(-100, -3)
                self.active_zone.size = (400, self.text.rect.h+6)
        else:
            self.active_zone = self.text.rect.inflate(6, 6)
    def group_checkings(self, state):
        if self.text.new_pos != self.text.rect.topleft:
            self.move_text()
        if self.group[:4] not in ('main', 'inga'):
            self.cursor.render(state)
            if Globals.SETTINGS['hotkeys']:
                self.tooltip.render(state)
        if 'SELECTOR' in self.type:
            self.selector.render(state)
        else:
            self.text.render(True)
    def render(self, state):
        if self.text.AV:
            self.group_checkings(state)
    def action(self, key):
        play_click_sound()
        if self.group == 'main_settings_exit':
            Globals.SETTINGS['pl_name'] = Globals.PLAYERS[0]['name']
            Globals.SETTINGS['pl_color'] = Globals.PLAYERS[0]['color']
            Globals.TEMP_VARS.pop('edit_player')
            save_settings()
        if 'SELECTOR' in self.type:
            return self.selector.action()
        elif self.type == 'main_sysexit':
            SYSEXIT()
        elif self.type in ('main_settings_music', 'main_settings_sounds', 'main_settings_hotkeys'):
            if self.type in ('main_settings_music', 'main_settings_sounds'):
                switch_sound_state(self.type[14:], Globals.SETTINGS[self.type[14:]])
            else:
                Globals.SETTINGS['hotkeys'] = not Globals.SETTINGS['hotkeys']
            self.update_text(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS[self.type[14:]])]+u' ›')
            return None
        elif self.type == 'game_start':
            if self.text.color == Globals.COLORS['white']:
                save_last_game_settings()
            else:
                return None
        elif self.type == 'main_new_game_switch':
            Globals.TEMP_VARS['cur_game'] = int(not(Globals.TEMP_VARS['cur_game']))
            self.update_text(u'‹ '+Globals.TRANSLATION[5+int(Globals.TEMP_VARS['cur_game'])]+u' ›')
            return None
        elif key != 'exit' and 'main_new_edit_player' in self.type:
            Globals.TEMP_VARS['edit_player'] = int(self.type[len(self.type)-1])
        elif self.type in ('main_settings_language', 'main_settings_fav_game'):
            Globals.SETTINGS[self.type[14:]] = int(not(Globals.SETTINGS[self.type[14:]]))
            if self.type == 'main_settings_fav_game':
                self.update_text(u'‹ '+Globals.TRANSLATION[5+int(Globals.SETTINGS['fav_game'])]+u' ›')
                return None
            else:
                Globals.TRANSLATION = read_translation(Globals.SETTINGS['language'])
        return self.type
class Tooltip():
    def __init__(self, text, type, obj):
        self.type = type
        self.rect = pygame.Rect((0, 0), Globals.FONTS['ume_12'].size(text))
        self.move_text(obj.rect)
        self.text = Globals.FONTS['ume_12'].render(text, True, Globals.COLORS['grey'])
    def move_text(self, rect):
        x = rect.x + (rect.w - self.rect.w)/2 - 15
        y = rect.y - self.rect.h - 5
        self.rect.topleft = (x, y)
    def render(self, state):
        if state:
            Globals.screen.blit(self.text, self.rect.topleft)
class MenuSelector():
    def __init__(self, type):
        self.type = type
        itemcount_start = 0
        if type == 'main_settings_volume_SELECTOR':
            itemcount_end = 10
            self.active = int(Globals.SETTINGS['volume'] * 10 - 1)
        elif type == 'main_settings_player_color_SELECTOR':
            itemcount_end = len(Globals.PLAYERS_COLORS)
            if Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['color'] in Globals.PLAYERS_COLORS:
                self.active = Globals.PLAYERS_COLORS.index(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['color'])
            else:
                self.active = 0
        elif type == 'main_new_total_SELECTOR':
            itemcount_start = 1
            itemcount_end = 6
            self.active = len(Globals.PLAYERS) - 2
        elif type == 'main_new_humans_SELECTOR':
            itemcount_end = len(Globals.PLAYERS)
            for i in range(len(Globals.PLAYERS)):
                if Globals.PLAYERS[i]['human']:
                    self.active = i
        self.items = [AlphaText(u'●', type, i) for i in range(itemcount_start, itemcount_end)]
        self.cursor_inflate = (10, 16)
        self.rects = [pygame.Rect(item.rect.inflate(self.cursor_inflate)) for item in self.items]
        self.cursor = SelectorCursor(self.rects[self.active])
    def keypress(self, KEY):
        if KEY == pygame.K_LEFT:
            self.active -= 1
            if self.active == -1:
                self.active = len(self.items) - 1
        else:
            self.active += 1
            if self.active == len(self.items):
                self.active = 0
        self.apply_new_active(self.active)
    def add_rm_items(self, add, new_length):
        if add:
            for i in range(len(self.items), new_length):
                self.items.append(AlphaText(u'●', self.type, i))
                self.items[i].rect.topleft = self.items[i].new_pos
                self.rects.append(pygame.Rect(self.items[i].rect.inflate(self.cursor_inflate)))
        else:
            self.items = self.items[:new_length]
            self.rects = self.rects[:new_length]
            if self.active >= new_length:
                self.apply_new_active(new_length - 1)
    def apply_new_active(self, active):
        self.active = active
        self.cursor.new_cords = self.rects[active].topleft
    def move_text(self):
        for i in range(len(self.items)):
            self.items[i].move_text()
            self.rects[i] = self.items[i].rect.inflate(self.cursor_inflate)
        self.cursor.new_cords = self.rects[self.active].topleft
    def render(self, state):
        if state:
            self.cursor.render()
        else:
            self.cursor.reset_alpha()
        for item in self.items:
            item.render(True)
    def action(self):
        if self.type == 'main_settings_volume_SELECTOR':
            change_volume(float(self.active+1)/10)
            for i in range(len(self.items)):
                self.items[i].choose_selector_color('volume', i)
                self.items[i].RErender()
        elif self.type == 'main_settings_player_color_SELECTOR':
            Globals.PLAYERS[Globals.TEMP_VARS['edit_player']]['color'] = Globals.PLAYERS_COLORS[self.active]
            return self.type
        elif self.type == 'main_new_humans_SELECTOR':
            for i in range(1, len(Globals.PLAYERS)):
                status = i <= self.active
                if (status and not Globals.PLAYERS[i]['human']) or (not status and Globals.PLAYERS[i]['human']):
                    Globals.PLAYERS[i]['human'] = not Globals.PLAYERS[i]['human']
                    self.items[i].choose_selector_color('new_settings_humans', i)
                    self.items[i].RErender()
            return self.type
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
class SelectorCursor(Cursor):
    def __init__(self, rect):
        Cursor.__init__(self, 0, rect)
        self.draw_rect()
    def reset_alpha(self):
        self.surf_color.a = 0
    def move(self):
        self.rect.topleft = slight_animation_count_pos(self.new_cords, self.rect.topleft, 5)
    def render(self):
        if self.new_cords != self.rect.topleft:
            self.move()
        if self.surf_color.a != 208:
            self.surf_color.a += 4
            self.draw_rect()
        Cursor.render(self)
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
        elif type in ('main_stats', 'main_settings_player_name'):
            self.keys = ['exit']
        elif type == 'main_settings':
            self.keys = ['language', 'player', 'hotkeys', 'music', 'sounds', 'volume', 'exit']
            if not Globals.SETTINGS['block']:
                self.keys.insert(6, 'fav_game')
        elif 'main_new_edit_player' in type or type == 'main_settings_player':
            self.keys = ['name', 'color', 'exit']
        elif type == 'main_new_game':
            self.keys = ['total', 'humans', 'start', 'exit']
            for i in range(len(Globals.PLAYERS)):
                self.keys.insert(len(self.keys)-2, 'player'+str(i))
            if not Globals.SETTINGS['block']:
                self.keys.insert(0, 'game')
        elif type == 'game_start':
            self.keys = ['start_game', 'exit']
    def add_rm_keys(self, add, key, index=None, cords=None):
        if add:
            self.keys.insert(index, key)
            self.cords.insert(index, cords)
        else:
            index = self.keys.index(key)
            self.keys.pop(index)
            self.cords.pop(index)
    def update_cords(self, menuitems):
        rects = [menuitems[key].active_zone for key in self.keys]
        self.cords = [rect.topleft for rect in rects]
        return rects[0]
    def keypress(self, KEY):
        if KEY == pygame.K_DOWN:
            self.change_pos(self.keys[self.active_num - len(self.keys) + 1])
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
        self.rect.topleft = slight_animation_count_pos(self.new_cords, self.rect.topleft, 5, 15)
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
