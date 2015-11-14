# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha

class GameField():
    def __init__(self):
        self.cells = tuple([FieldCell(i) for i in range(40)])
    def render(self):
        for cell in self.cells:
            cell.render()
class FieldCell():
    def __init__(self, number):
        if not number % 10:
            size = (80, 80)
            x = (Globals.RESOLUTION[0]-600)/2+int(number in (0, 30))*521
            y = 70+int(number in (0, 10))*521
        elif (number // 10) % 2:
            size = (80, 49)
            if number // 30:
                x = (Globals.RESOLUTION[0]-600)/2+521
                y = 101+(number % 10)*49
            else:
                x = (Globals.RESOLUTION[0]-600)/2
                y = 101+(10-number % 10)*49
        else:
            size = (49, 80)
            if number // 20:
                x = (Globals.RESOLUTION[0]-600)/2+31+(number % 10)*49
                y = 70
            else:
                x = (Globals.RESOLUTION[0]-600)/2+31+(10-number % 10)*49
                y = 591
        self.pos = (x, y)
        self.rect = pygame.Rect((0, 0), size)
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.change_color(Globals.COLORS['black'])
    def change_color(self, color):
        pygame.draw.rect(self.surf, change_color_alpha(color, 104), self.rect, 0)
    def render(self):
        Globals.screen.blit(self.surf, self.pos)
