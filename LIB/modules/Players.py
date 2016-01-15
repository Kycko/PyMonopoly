# -*- coding: utf-8 -*-
import Globals
from pygame import draw, Rect, Surface

class Player():
    def __init__(self, name, color, human):
        self.name = name
        self.color = color
        self.human = human
        self.game_piece = Surface((16, 16))
        draw.rect(self.game_piece, self.color, Rect((0, 0), (16, 16)))
        draw.rect(self.game_piece, Globals.COLORS['black'], Rect((0, 0), (16, 16)), 1)
        self.game_piece.blit(Globals.FONTS['ubuntu_11'].render(self.name[0], True, Globals.COLORS['black']), (4, 1))
