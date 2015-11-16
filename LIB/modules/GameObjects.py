# -*- coding: utf-8 -*-
import Globals, FieldCellsData
from GlobalFuncs import read_onboard_text, slight_animation_count_pos
from pygame import draw, Rect, Surface

class GameField():
    def __init__(self):
        onboard_text = read_onboard_text()
        groups = FieldCellsData.make_groups()
        group_symbols = FieldCellsData.make_group_symbols()
        group_colors = FieldCellsData.make_group_colors()
        self.cells = tuple([FieldCell(onboard_text, groups[i], group_symbols[i], group_colors, i) for i in range(40)])
        self.move((-1820, 0))
    def move(self, offset):
        for cell in self.cells:
            cell.change_new_pos(offset)
    def render(self):
        for cell in self.cells:
            cell.render()
class FieldCell():
    def __init__(self, onboard_text, group, group_symbol, group_colors, number):
        #--- Onboard text
        self.group = group
        self.group_symbol = group_symbol
        if group in range(1, 9):
            self.group_color = Globals.COLORS[group_colors[group-1]]
        else:
            self.group_color = None
        if number in onboard_text.keys():
            self.onboard_text = Globals.FONTS['ubuntu_16'].render(onboard_text[number], True, Globals.COLORS['black'])
        else:
            self.onboard_text = None
        #--- Size and position
        if not number % 10:
            size = (80, 80)
            x = 2120+int(number in (0, 30))*521
            y = 70+int(number in (0, 10))*521
        elif (number // 10) % 2:
            size = (80, 49)
            if number // 30:
                x = 2641
                y = 101+(number % 10)*49
            else:
                x = 2120
                y = 101+(10-number % 10)*49
        else:
            size = (49, 80)
            if number // 20:
                x = 2151+(number % 10)*49
                y = 70
            else:
                x = 2151+(10-number % 10)*49
                y = 591
        self.pos = (x, y)
        #--- Rect and surface
        self.rect = Rect((0, 0), size)
        self.surf = Surface(size)
        self.change_color(Globals.COLORS['grey22'])
        self.RErender()
    def change_new_pos(self, offset):
        self.new_pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])
    def change_color(self, color):
        self.color = color
    def RErender(self):
        draw.rect(self.surf, self.color, self.rect, 0)
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
            draw.rect(self.surf, self.group_color, rect, 0)
            draw.rect(self.surf, Globals.COLORS['black'], rect, 1)
        draw.rect(self.surf, Globals.COLORS['black'], self.rect, 1)
        objects = [obj for obj in (self.onboard_text, self.group_symbol) if obj]
        for i in range(len(objects)):
            self.surf.blit(objects[i], ((self.rect.w-objects[i].get_width())/2, self.rect.h/4+16*i))
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10, 50)
        Globals.screen.blit(self.surf, self.pos)
