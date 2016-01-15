# -*- coding: utf-8 -*-
import Globals
from pygame import draw, Rect, Surface

class Player():
    def __init__(self, name, color, human):
        self.name = name
        self.color = color
        self.human = human
        self.cur_field = 0
        self.game_piece = Surface((16, 16))
        draw.rect(self.game_piece, self.color, Rect((0, 0), (16, 16)))
        draw.rect(self.game_piece, Globals.COLORS['black'], Rect((0, 0), (16, 16)), 1)
