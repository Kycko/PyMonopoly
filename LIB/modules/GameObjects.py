# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha, slight_animation_count_pos

class GameField():
    def __init__(self):
        self.cells = tuple([FieldCell(i) for i in range(40)])
        self.move((-1820, 0))
    def move(self, offset):
        for cell in self.cells:
            cell.change_new_pos(offset)
    def render(self):
        for cell in self.cells:
            cell.render()
class FieldCell():
    def __init__(self, number):
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
        self.rect = pygame.Rect((0, 0), size)
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.change_color(Globals.COLORS['black'])
    def change_new_pos(self, offset):
        self.new_pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])
    def change_color(self, color):
        pygame.draw.rect(self.surf, change_color_alpha(color, 104), self.rect, 0)
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10, 50)
        Globals.screen.blit(self.surf, self.pos)
