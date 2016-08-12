# -*- coding: utf-8 -*-
import Globals, FieldCellsData, pygame
from GlobalFuncs import count_new_pos, slight_animation_count_pos, read_chests_and_chances_translation
from random import shuffle
from Sprite import Sprite
from TransparentText import AlphaText

class GameField():
    def __init__(self):
        group_symbols = FieldCellsData.make_group_symbols()
        group_colors = FieldCellsData.make_group_colors()
        self.cells = []
        Globals.TEMP_VARS['cells_rects'] = []
        self.surf = pygame.Surface((601, 601), pygame.SRCALPHA)
        self.groups_monopolies = {}
        for i in range(40):
            size, pos = self.count_size_and_pos(i)
            Globals.TEMP_VARS['cells_rects'].append(pygame.Rect((pos[0]+300, pos[1]+70), size))
            self.cells.append(FieldCell(group_symbols[Globals.TEMP_VARS['cells_groups'][i]],
                                        group_colors,
                                        i,
                                        size,
                                        pos))
            if self.cells[i].group not in self.groups_monopolies.keys():
                self.groups_monopolies[self.cells[i].group] = False
            self.RErender_a_cell(i)
        self.chests_and_chances = {}
        for type in ('chests', 'chances'):
            data = FieldCellsData.make_chests_and_chances(type)
            text = read_chests_and_chances_translation(type)
            self.chests_and_chances[type] = [ChestOrChance(data[i], text[i]) for i in range(len(data))]
        for type in ('chests', 'chances'):
            shuffle(self.chests_and_chances[type])
        self.pos = (2120, 70)
        self.new_pos = (2120, 70)
    def count_size_and_pos(self, num):
        if not num % 10:
            size = (80, 80)
            x = int(num in (0, 30))*521
            y = int(num in (0, 10))*521
        elif (num // 10) % 2:
            size = (80, 49)
            if num // 30:
                x = 521
                y = 31+(num % 10)*49
            else:
                x = 0
                y = 31+(10-num % 10)*49
        else:
            size = (49, 80)
            if num // 20:
                x = 31+(num % 10)*49
                y = 0
            else:
                x = 31+(10-num % 10)*49
                y = 521
        return size, (x, y)
    def change_new_pos(self, offset):
        self.new_pos = count_new_pos(self.new_pos, offset)
        for player in Globals.PLAYERS:
            player.change_new_pos(offset)
    def RErender_a_cell(self, num):
        self.cells[num].RErender(self.groups_monopolies[self.cells[num].group])
        self.surf.blit(self.cells[num].surf, self.cells[num].pos)
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10, 50)
        Globals.screen.blit(self.surf, self.pos)
        for cell in self.cells:
            if cell.step_indicator_visible:
                cell.step_indicator.render()
        for player in Globals.PLAYERS:
            player.render()
class FieldCell():
    def __init__(self, group_symbol, group_colors, number, size, pos):
        self.owner = None
        self.NAME = None
        self.buildings = 0
        if number in Globals.TEMP_VARS['onboard_text']['fieldnames'].keys():
            self.NAME = Globals.TEMP_VARS['onboard_text']['fieldnames'][number]
        #--- Onboard text
        self.number = number
        self.group = Globals.TEMP_VARS['cells_groups'][number]
        self.group_symbol = group_symbol
        if number in Globals.TEMP_VARS['cells_cost'].keys():
            self.buy_cost = Globals.TEMP_VARS['cells_cost'][number]
        else:
            self.buy_cost = None
        if number in Globals.TEMP_VARS['cells_rent_costs'].keys():
            self.rent_costs = Globals.TEMP_VARS['cells_rent_costs'][number]
        else:
            self.rent_costs = None
        if self.group in range(1, 9):
            self.group_color = group_colors[self.group-1]
        else:
            self.group_color = None
        if number in Globals.TEMP_VARS['onboard_text']['onboard'].keys():
            self.onboard_text = Globals.FONTS['ubuntu_16'].render(Globals.TEMP_VARS['onboard_text']['onboard'][number], True, Globals.COLORS['black'])
        else:
            self.onboard_text = None
        self.step_indicator = AlphaText(u'●', 'step_indicator', number)
        self.step_indicator_visible = False
        #--- Position, rect and surface
        self.pos = pos
        self.rect = pygame.Rect((0, 0), size)
        self.surf = pygame.Surface(size)
        self.color = Globals.COLORS['grey22']
    def RErender(self, monopolied_cell = False):
        #--- Background
        pygame.draw.rect(self.surf, self.color, self.rect, 0)
        #--- Group-specific color (for groups 1-8)
        if self.group_color:
            rect = self.rect.copy()
            if self.group in (1, 2):
                rect.h = 20
            elif self.group in (3, 4):
                rect.w = 20
                rect = rect.move(60, 0)
            elif self.group in (5, 6):
                rect.h = 20
                rect = rect.move(0, 60)
            elif self.group in (7, 8):
                rect.w = 20
            pygame.draw.rect(self.surf, Globals.COLORS[self.group_color], rect, 0)
            pygame.draw.rect(self.surf, Globals.COLORS['black'], rect, 1)
        #--- Border
        pygame.draw.rect(self.surf, Globals.COLORS['black'], self.rect, 1)
        #--- Onboard text
        if self.onboard_text:
            self.surf.blit(self.onboard_text, ((self.rect.w-self.onboard_text.get_width())/2, self.rect.h/4))
        #--- Cell-specific symbol
        if not self.number % 10:
            y = 35
        elif self.group in ('chance', 'chest', 'income', 'railroad', 'service', 'tax'):
            if (self.group == 'income' and self.number in (13, 32)) or (self.group == 'tax' and self.number == 38):
                y = -7
            else:
                y = (self.rect.h-self.group_symbol.get_height())/2
        elif self.group in (1, 2, 5, 6):
            y = 5 + int(self.group in (1, 2))*17
        else:
            y = 2
        if self.group in (3, 4, 7, 8):
            x = int(self.group in (7, 8))*20 + (60-self.group_symbol.get_width())/2
        else:
            x = (self.rect.w-self.group_symbol.get_width())/2
        self.surf.blit(self.group_symbol, (x, y))
        #--- Cell price
        if self.number not in (0, 10) and self.buy_cost:
            temp = self.buy_cost
            if self.owner:
                temp = self.rent_costs[self.buildings]
                if monopolied_cell and self.group in range(9):
                    temp = temp * 2
            pic = Globals.FONTS['ubuntu_11'].render(str(temp), True, Globals.COLORS['black'])
            x = self.rect.right-pic.get_width()-3
            if self.number in range(11, 20) and self.group not in ('railroad', 'service', 'income'):
                x -= 20
            y = self.rect.bottom-15
            if self.number in range(21, 30) and self.group not in ('railroad', 'service', 'tax'):
                y -= 20
            self.surf.blit(pic, (x, y))
class GameLog():
    def __init__(self):
        self.messages = [AlphaText(Globals.GAMELOG_TRANSLATION[0], 'gamelog_message_common', 0)]
        self.add_message('change_player')
        self.RErender()
        self.pos = (10, 170)
        self.new_pos = (10, 70)
    def add_message(self, type):
        if type in ('roll_the_dice', 'chest_goto'):
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[(2, 10)[type == 'chest_goto']].replace('%', str(Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field)), 'gamelog_message_common', len(self.messages)))
        elif type == 'change_player':
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[1].replace('%', Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].name), 'gamelog_message_player_switched', len(self.messages)))
        elif type in ('ingame_continue_tax', 'ingame_continue_income'):
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[3 + 10*(type[16:] == 'income')].replace('%', str(Globals.TEMP_VARS['MUST_PAY'])[(type[16:] == 'tax'):]), 'gamelog_message_common', len(self.messages)))
        elif type == 'ingame_continue_PAY_RENT':
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[4].replace('%', str(Globals.TEMP_VARS['MUST_PAY'])).replace('^', Globals.main_scr.objects['gamefield'].cells[Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field].owner), 'gamelog_message_common', len(self.messages)))
        elif type == 'ingame_buy_a_cell':
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[5].replace('%', str(Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field)).replace('^', str(Globals.TEMP_VARS['MUST_PAY'])), 'gamelog_message_common', len(self.messages)))
        elif type == 'ingame_continue_gotojail':
            text = Globals.main_scr.objects['gamefield'].cells[30].NAME
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[6].replace('%', text[text.index(' ')+1:]), 'gamelog_message_common', len(self.messages)))
        elif type == 'money_for_start_passing':
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[7].replace('%', str(Globals.main_scr.objects['gamefield'].cells[0].buy_cost)), 'gamelog_message_common', len(self.messages)))
        elif type == 'chest_income':
            self.messages.append(AlphaText('- ' + Globals.GAMELOG_TRANSLATION[(3, 7)[Globals.TEMP_VARS['MUST_PAY'] > 0]].split()[1] + ' $' + str(Globals.TEMP_VARS['MUST_PAY']).lstrip('-'), 'gamelog_message_common', len(self.messages)))
        elif type in ('chest_free_jail', 'use_card_to_exit_jail'):
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[9 + 5*(type == 'use_card_to_exit_jail')], 'gamelog_message_common', len(self.messages)))
        elif type == 'roll_the_dice_to_exit_jail':
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[8].replace('%', str(Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].exit_jail_attempts)), 'gamelog_message_common', len(self.messages)))
        elif type == 'pay_money_to_exit_jail':
            CELL = Globals.main_scr.objects['gamefield'].cells[10]
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[3].replace('%', str(CELL.buy_cost)) + ' (' + CELL.NAME + ')', 'gamelog_message_common', len(self.messages)))
        elif type in ('birthday', 'pay_each'):
            self.messages.append(AlphaText(Globals.GAMELOG_TRANSLATION[11 + (type == 'pay_each')].replace('%', str(Globals.TEMP_VARS['MUST_PAY'])), 'gamelog_message_common', len(self.messages)))
        if len(self.messages) > 24:
            count = len(self.messages) - 24
            for i in range(count):
                self.messages.pop(i)
            for message in self.messages:
                if message:
                    message.change_new_pos((0, -18*count))
    def change_new_pos(self, offset):
        self.new_pos = count_new_pos(self.new_pos, offset)
    def RErender(self):
        self.surf = pygame.Surface((280, 430), pygame.SRCALPHA)
        for message in self.messages:
            message.move_text()
            self.surf.blit(message.set_alpha(), message.rect.topleft)
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10, 50)
        if self.messages[-1].alpha != 255:
            self.RErender()
        Globals.screen.blit(self.surf, self.pos)
class ChestOrChance():
    def __init__(self, type, text):
        self.modifier = type.split()[1:]
        if self.modifier:
            for i in range(len(self.modifier)):
                self.modifier[i] = int(self.modifier[i])
        self.type = type.split()[0]
        self.text = text
