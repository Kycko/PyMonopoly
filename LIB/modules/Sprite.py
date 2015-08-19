# -*- coding: utf-8 -*-
import Globals
from pygame import image

class Sprite:
    def __init__(self, pos, file):
        self.x, self.y = pos
        self.bitmap = image.load(file)
    def render(self):
        Globals.screen.blit(self.bitmap, (self.x, self.y))
