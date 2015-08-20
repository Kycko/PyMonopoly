# -*- coding: utf-8 -*-
import Globals
from pygame import Color, Rect, Surface

class AlphaText():
    def __init__(self, text, group, number=None):
        self.alpha = 0
        self.init_for_group(text, group, number)
        self.anticolor = Color('white') - self.color
        self.update_text(text)
    def init_for_group(self, text, group, number):
        if group == 'main_main':
            self.AV = True
            self.font = Globals.FONTS['ubuntu_big']
            self.color = Color('white')
            self.x = Globals.RESOLUTION[0]/4
            self.y = Globals.RESOLUTION[1]/3+50*number
    def update_text(self, text):
        size = self.font.size(text)
        xpos = self.find_xpos(size)
        self.rect = Rect((xpos, self.y), size)
        self.text = self.font.render(text, True, self.color)
    def find_xpos(self, size):
        if self.x == 'center':
            return Globals.RESOLUTION[0]/2 - size[0]/2
        elif self.x == 'right':
            return Globals.RESOLUTION[0] - size[0] - self.x_offset
        else:
            return self.x
    def set_alpha(self):
        if self.alpha != 255:
            self.alpha += 5
        if self.alpha != 255:
            surf = Surface(self.rect.size)
            surf.fill(self.anticolor)
            surf.set_colorkey(self.anticolor)
            surf.blit(self.text, (0, 0))
            surf.set_alpha(self.alpha)
            return surf
        else:
            return self.text
    def render(self):
        Globals.screen.blit(self.set_alpha(), self.rect.topleft)
