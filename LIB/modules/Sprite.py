# -*- coding: utf-8 -*-
import Globals
from GlobalFuncs import slight_animation_count_pos
from pygame import image

class Sprite:
    def __init__(self, pos, file):
        self.x, self.y = pos
        self.new_y = self.y
        self.bitmap = image.load(file)
    def render(self):
        self.x, self.y = slight_animation_count_pos((self.x, self.new_y), (self.x, self.y), 10)
        Globals.screen.blit(self.bitmap, (self.x, self.y))
