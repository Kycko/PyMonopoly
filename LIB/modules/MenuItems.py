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
        self.init_for_group(number)
        self.init_for_type()
    def init_for_group(self, number):
        self.HOTKEYS = ()
        if self.group == 'onboard_select_cell':
            self.cursor = FieldCellCursor(self.active_zone)
            self.tooltip = Tooltip(number, 'fieldcells_info')
        elif self.group == 'pl_info_tab':
            self.cursor = OwnCursor('light_blue', self.active_zone)
            self.tooltip = Tooltip(Globals.PLAYERS[number].name, 'left', self.text, 'ubuntu_13')
        elif self.group == 'from_game_return_to_menu':
            self.cursor = OwnCursor('light_brown', self.active_zone)
            self.tooltip = Tooltip(u'HOTKEY: Escape', 'left', self.text)
            self.HOTKEYS = (pygame.K_ESCAPE)
        elif self.group == 'show_menu':
            self.cursor = OwnCursor('orange', self.active_zone)
            self.tooltip = Tooltip(u'HOTKEYS: PageDown, PageUp', 'downright', self.text)
            self.HOTKEYS = (pygame.K_PAGEDOWN, pygame.K_PAGEUP)
        elif self.group == 'show_prev_trades':
            self.cursor = OwnCursor('orange', self.active_zone)
            self.tooltip = Tooltip(u'HOTKEYS: Tab', 'left', self.text)
            self.HOTKEYS = (pygame.K_TAB, None)
        elif self.group == 'volume_in_game':
            self.cursor = OwnCursor('grey', self.active_zone)
            self.tooltip = None
        elif self.group == 'music_and_sound_switches':
            self.cursor = OwnCursor('light_blue', self.active_zone)
            self.tooltip = None
        elif self.group == 'stats_switch':
            self.cursor = OwnCursor('light_green', self.active_zone)
            self.tooltip = Tooltip(u'HOTKEYS: ← →', 'top', self.text)
        else:
            self.tooltip = None
    def init_for_type(self):
        #--- Hotkeys
        if self.type in ('main_settings_language', 'main_settings_hotkeys', 'main_settings_music', 'main_settings_sounds', 'main_settings_fav_game', 'stats_switch', 'main_new_game_switch'):
            self.HOTKEYS = (pygame.K_LEFT, pygame.K_RIGHT)
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
            if self.group not in ('onboard_select_cell', 'volume_in_game', 'music_and_sound_switches'):
                self.tooltip.move_text(self.text.rect)
    def change_new_pos(self, offset):
        self.text.new_pos = count_new_pos(self.text.new_pos, offset)
        if 'SELECTOR' in self.type:
            for item in self.selector.items:
                item.change_new_pos(offset)
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
        elif self.group == 'onboard_select_cell':
            self.active_zone = self.text.rect
        elif self.group in ('from_game_return_to_menu', 'show_menu', 'show_prev_trades', 'music_and_sound_switches'):
            self.active_zone = self.text.rect.inflate(20, 10)
        elif self.type == 'in_game_volume_SELECTOR':
            self.active_zone = self.text.rect
            self.active_zone.size = (251, 33)
        else:
            self.active_zone = self.text.rect.inflate(6, 6)
    def render(self, state):
        if self.text.new_pos != self.text.rect.topleft:
            self.move_text()
        if self.group[:4] not in ('main', 'inga'):
            self.cursor.render(state)
            if self.tooltip and ((Globals.SETTINGS['hotkeys'] and self.HOTKEYS) or (not self.HOTKEYS)) and not (self.group == 'onboard_select_cell' and Globals.main_scr.objects['gamefield'].pos[1] != 70):
                self.tooltip.render(state)
        if 'SELECTOR' in self.type:
            self.selector.render(state)
        else:
            self.text.render(True)
    def action(self, key):
        play_click_sound()
        if self.group == 'main_settings_exit':
            Globals.SETTINGS['pl_name'] = Globals.PLAYERS[0].name
            Globals.SETTINGS['pl_color'] = Globals.PLAYERS[0].color
            Globals.TEMP_VARS.pop('edit_player')
            save_settings()
        elif self.group == 'music_and_sound_switches':
            type = self.type[8:len(self.type)-7]
            switch_sound_state(type, Globals.SETTINGS[type], True)
            self.text.choose_switch_color(type)
            self.update_text((u'✖', u'✓')[int(Globals.SETTINGS[type])])
            return self.group
        if 'SELECTOR' in self.type:
            return self.selector.action()
        elif self.type == 'ingame_start_game' and self.text.rect.topleft != self.text.new_pos:
            return None
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
        elif self.type == 'main_settings_fav_game':
            Globals.SETTINGS['fav_game'] = int(not(Globals.SETTINGS['fav_game']))
            self.update_text(u'‹ '+Globals.TRANSLATION[5+int(Globals.SETTINGS['fav_game'])]+u' ›')
            return None
        elif self.type == 'main_settings_language':
            choose_next_language()
        elif self.type == 'onboard_select_cell' or 'pl_info_tab' in self.type:
            return None
        return self.type
class Tooltip():
    def __init__(self, text, type, obj=None, font='ume_12'):
        self.type = type
        if type == 'fieldcells_info':
            self.number = text
            self.NAME = Globals.TEMP_VARS['onboard_text']['fieldnames'][text]
            self.rect = pygame.Rect((10, Globals.RESOLUTION[1]-188), (280, 188))
            self.RErender()
        else:
            self.rect = pygame.Rect((0, 0), Globals.FONTS[font].size(text))
            self.move_text(obj.rect)
            self.text = Globals.FONTS[font].render(text, True, Globals.COLORS['grey'])
    def RErender(self, cell_state=0):
        CELL = Globals.main_scr.objects['gamefield'].cells[self.number]
        NAME = self.NAME
        if not cell_state and CELL.owner:
            NAME += Globals.TRANSLATION[96]
        NAME = Globals.FONTS['ubuntu_16'].render(NAME, True, Globals.COLORS['grey22'])
        self.text = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.text.blit(NAME, (0, 0))
        #--- Font and color
        font = Globals.FONTS['ubuntu_13']
        #--- Render elements
        ##--- Jail info
        if self.number == 10:
            line = 0
            jailcards = []
            for player in Globals.PLAYERS:
                if player.cur_field == 10:
                    line += 1
                    if player.exit_jail_attempts != None:
                        temp = '- ' + player.name + Globals.TRANSLATION[53] + str(player.exit_jail_attempts) + ')'
                        color = Globals.COLORS['light_green']
                    else:
                        temp = '- ' + player.name + Globals.TRANSLATION[52]
                        color = Globals.COLORS['grey22']
                    self.text.blit(font.render(temp, True, color), (0, 18*line))
                for i in player.free_jail_cards:
                    jailcards.append(player)
            if jailcards:
                for player in jailcards:
                    line += 1
                    self.text.blit(font.render(Globals.TRANSLATION[56] + player.name, True, player.color), (0, 18*line))
        else:
            ##--- Buy cost
            if self.number != 20:
                color = self.choose_color(0, cell_state + bool(CELL.owner))
                if CELL.owner:
                    text = Globals.TRANSLATION[97]
                    price = str(CELL.build_cost)
                else:
                    text = Globals.TRANSLATION[37]
                    price = str(CELL.buy_cost)
                self.text.blit(font.render(text, True, color), (0, 18))
                self.text.blit(font.render(price, True, color), (font.size(text+' ')[0], 18))
            ##--- Rentlabels
            if CELL.group in range(1, 9) + ['railroad', 'service']:
                start_string = 6
                if CELL.group == 'railroad':
                    count = 4
                elif CELL.group == 'service':
                    count = 2
                else:
                    count = 6 - Globals.TEMP_VARS['cur_game']
                    start_string = 0
                for i in range(count):
                    color = self.choose_color(i+1, cell_state)
                    self.text.blit(font.render((Globals.TEMP_VARS['rentlabels'][i+start_string]), True, color), (0, 45+i*15))
                    if cell_state == 1 and i == 0 and CELL.group not in (None, 'railroad') and Globals.main_scr.objects['gamefield'].groups_monopolies[CELL.group]:
                        string = '(x2) ' + str(2 * CELL.rent_costs[i])
                    else:
                        string = str(CELL.rent_costs[i])
                    self.text.blit(font.render(string, True, color), (180-font.size(string)[0], 45+i*15))
                for i in range(2):
                    color = self.choose_color(i, 2 + CELL.buildings)
                    self.text.blit(font.render(Globals.TRANSLATION[38+i], True, color), (0, 60+(count+i)*15))
                    string = str(int((CELL.buy_cost/2)+((CELL.buy_cost/2)*0.1*i)))
                    self.text.blit(font.render(string, True, color), (180-font.size(string)[0], 60+(count+i)*15))
    def choose_color(self, cur, needed):
        if cur == needed:
            return Globals.COLORS['light_green']
        else:
            return Globals.COLORS['grey22']
    def move_text(self, rect):
        if self.type == 'top':
            x = rect.x + (rect.w - self.rect.w)/2 - 15
            y = rect.y - self.rect.h - 5
        elif self.type == 'left':
            x = rect.x - self.rect.w - 15
            y = rect.y + (rect.h - self.rect.h)/2
        elif self.type == 'downright':
            x = rect.right - self.rect.w
            y = rect.bottom + 15
        self.rect.topleft = (x, y)
    def render(self, state):
        if state:
            Globals.screen.blit(self.text, self.rect.topleft)
class MenuSelector():
    def __init__(self, type):
        self.type = type
        itemcount_start = 0
        if 'volume_SELECTOR' in type:
            itemcount_end = 10
            self.active = int(Globals.SETTINGS['volume'] * 10 - 1)
        elif type == 'main_settings_player_color_SELECTOR':
            itemcount_end = len(Globals.PLAYERS_COLORS)
            if Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].color in Globals.PLAYERS_COLORS:
                self.active = Globals.PLAYERS_COLORS.index(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].color)
            else:
                self.active = 0
        elif type == 'main_new_total_SELECTOR':
            itemcount_start = 1
            itemcount_end = 6
            self.active = len(Globals.PLAYERS) - 2
        elif type == 'main_new_humans_SELECTOR':
            itemcount_end = len(Globals.PLAYERS)
            for i in range(len(Globals.PLAYERS)):
                if Globals.PLAYERS[i].human:
                    self.active = i
        elif type == 'cell_state_SELECTOR':
            num = int(Globals.main_scr.labels['property_management_input_ready'].symbols)
            gamefield = Globals.main_scr.objects['gamefield']
            group = gamefield.cells[num].group
            itemcount_end = 2 + (5 - int(Globals.TEMP_VARS['cur_game'])) * (group in range(9)) * bool(gamefield.groups_monopolies[group])
            self.active = gamefield.cells[num].buildings + 1
        self.items = [AlphaText(u'●', type, i) for i in range(itemcount_start, itemcount_end)]
        self.cursor_inflate = (10, 16)
        self.rects = [pygame.Rect(item.rect.inflate(self.cursor_inflate)) for item in self.items]
        self.cursor = SelectorCursor(self.rects[self.active])
        if type == 'in_game_volume_SELECTOR':
            self.cursor.new_cords = self.rects[self.active].topleft
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
        if 'volume_SELECTOR' in self.type:
            change_volume(float(self.active+1)/10, self.type == 'in_game_volume_SELECTOR')
            for i in range(len(self.items)):
                self.items[i].choose_selector_color('volume', i)
                self.items[i].RErender()
        elif self.type == 'main_settings_player_color_SELECTOR':
            Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].color = Globals.PLAYERS_COLORS[self.active]
            return self.type
        elif self.type == 'main_new_humans_SELECTOR':
            for i in range(1, len(Globals.PLAYERS)):
                status = i <= self.active
                if (status and not Globals.PLAYERS[i].human) or (not status and Globals.PLAYERS[i].human):
                    Globals.PLAYERS[i].human = not Globals.PLAYERS[i].human
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
        if type == 'ingame_continue':
            self.keys_generator(('ingame_continue', 'trade', 'manage_property'))
        elif type == 'ingame_end_turn':
            self.keys_generator(('end_turn', 'trade', 'manage_property'))
        elif type == 'ingame_buy_or_auction':
            self.keys_generator(('buy_a_cell', 'cell_to_an_auction', 'trade', 'manage_property'))
        elif type == 'auction_next_player':
            self.keys_generator(('auction_up_bet', 'trade', 'manage_property', 'auction_refuse'))
        elif type == 'ingame_push_to_auction':
            self.keys = ['ingame_push_to_auction_accept', 'return']
        elif type == 'property_management':
            self.keys = ['return']
        elif type == 'choose_player_to_trade':
            self.keys_generator(['choose_player_to_trade_' + player.name for player in Globals.PLAYERS] + ['return'])
        elif type == 'trading_main_menu':
            array = ['trading_input_fields', 'trading_input_offer_money', 'trading_input_ask_for_money', 'trading_offer_free_jail', 'trading_ask_for_free_jail']
            for key in ('offer', 'ask_for'):
                array += ['trading_' + key + '_free_jail' + str(i) for i in range(3)]
            array += ['accept_ALL', 'return']
            self.keys_generator(array)
        elif type == 'ingame_trading_ACCEPT_DECLINE':
            self.keys = ['ingame_trading_ACCEPT_ALL', 'return']
        elif type == 'trading_input':
            self.keys = ['return']
        elif type == 'main_main':
            self.keys = ['new_game', 'settings', 'stats', 'exit']
        elif type == 'ingame_main':
            self.keys_generator(('roll_the_dice', 'pay_money_to_exit_jail', 'use_card_to_exit_jail', 'trade', 'manage_property'))
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
    def keys_generator(self, keys):
        self.keys = [key for key in keys if key in Globals.main_scr.menuitems.keys()]
    def add_rm_keys(self, add, key, index=None, cords=None):
        if add:
            self.keys.insert(index, key)
            self.cords.insert(index, cords)
        else:
            index = self.keys.index(key)
            self.keys.pop(index)
            self.cords.pop(index)
        if key in ('accept', 'state_selector'):
            self.change_pos(('return', key)[add])
        # elif key == 'accept_ALL' and not add:
        #     self.change_pos('return')
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
        Cursor.__init__(self, 50, rect)
    def render(self, state):
        if state:
            if self.u_length < self.rect.w/2-15:
                self.u_length += 2
                self.draw_rect()
                pygame.draw.line(self.surf, self.u_color, (self.rect.w/2-self.u_length, self.rect.h-1), (self.rect.w/2+self.u_length, self.rect.h-1), 1)
            Cursor.render(self)
        elif self.u_length:
            self.u_length = 0
class FieldCellCursor(Cursor):
    def __init__(self, rect):
        Cursor.__init__(self, 104, rect)
        self.draw_rect()
    def render(self, state):
        if state:
            Cursor.render(self)
class CurTurnHighlighter(Cursor):
    def __init__(self, menuitems):
        self.verts = [menuitems['player_'+Globals.PLAYERS[i].name].active_zone[1] for i in range(len(Globals.PLAYERS))]
        Cursor.__init__(self, 80, pygame.Rect((menuitems['player_'+Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].name].active_zone[0]-162, self.verts[0]), (200, 39)))
        self.draw_rect()
        self.surf.blit(Globals.FONTS['ubuntu_11'].render(Globals.TRANSLATION[40], True, Globals.COLORS['grey']), (2, 0))
        self.new_cords = (self.rect.x-1820, self.rect.y)
    def change_new_pos(self, offset):
        self.new_cords = count_new_pos(self.new_cords, offset)
    def move(self):
        self.new_cords = (self.new_cords[0], self.verts[Globals.TEMP_VARS['cur_turn']])
    def render(self):
        self.rect.topleft = slight_animation_count_pos(self.new_cords, self.rect.topleft, 10, 50)
        Cursor.render(self)
