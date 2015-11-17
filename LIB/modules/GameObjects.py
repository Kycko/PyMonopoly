# -*- coding: utf-8 -*-
import Globals, FieldCellsData, pygame
from GlobalFuncs import read_onboard_text, slight_animation_count_pos

class GameField():
    def __init__(self):
        onboard_text = read_onboard_text()
        groups = FieldCellsData.make_groups()
        group_symbols = FieldCellsData.make_group_symbols()
        group_colors = FieldCellsData.make_group_colors()
        self.cells = []
        self.surf = pygame.Surface((601, 601), pygame.SRCALPHA)
        for i in range(40):
            size, pos = self.count_size_and_pos(i)
            self.cells.append(FieldCell(onboard_text, groups[i], group_symbols[groups[i]], group_colors, i, size, pos))
            self.change_color_for_a_cell(i, 'grey22')
        self.pos = (2120, 70)
        self.change_new_pos((-1820, 0))
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
        self.new_pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])
    def change_color_for_a_cell(self, num, color):
        self.cells[num].change_color(color)
        self.surf.blit(self.cells[num].surf, self.cells[num].pos)
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10, 50)
        Globals.screen.blit(self.surf, self.pos)
class FieldCell():
    def __init__(self, onboard_text, group, group_symbol, group_colors, number, size, pos):
        #--- Onboard text
        self.number = number
        self.group = group
        self.group_symbol = group_symbol
        if group in range(1, 9):
            self.group_color = group_colors[group-1]
        else:
            self.group_color = None
        if number in onboard_text.keys():
            self.onboard_text = Globals.FONTS['ubuntu_16'].render(onboard_text[number], True, Globals.COLORS['black'])
        else:
            self.onboard_text = None
        #--- Position, rect and surface
        self.pos = pos
        self.rect = pygame.Rect((0, 0), size)
        self.surf = pygame.Surface(size)
    def change_color(self, color):
        self.color = color
        self.RErender()
    def RErender(self):
        #--- Background
        pygame.draw.rect(self.surf, Globals.COLORS[self.color], self.rect, 0)
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
            if self.group == 'income' and self.number in (13, 32):
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
