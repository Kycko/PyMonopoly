# -*- coding: utf-8 -*-
import Globals
from pygame import Color, Rect, Surface

class AlphaText():
    def __init__(self, text, group, number=None):
        self.alpha = 5
        self.init_for_group(text, group, number)
        self.anticolor = Color('white') - self.color
        self.update_text(text)
    def init_for_group(self, text, group, number):
        self.AV = True
        if group == 'main_main':
            self.font = Globals.FONTS['ubuntu_big']
            self.color = Color('white')
            self.x = 'center'
            self.x_offset = -Globals.RESOLUTION[0]/4
            self.y = Globals.RESOLUTION[1]*0.45+35*number
        elif group == 'somegroup':
            self.font = 'somefont'
            self.color = 'somecolor'
            self.x = 0
            self.x_offset = 0
            self.y = 0
    def update_text(self, text):
        size = self.font.size(text)
        xpos = self.find_xpos(size)
        self.rect = Rect((xpos, self.y), size)
        self.text = self.font.render(text, True, self.color)
    def find_xpos(self, size):
        if self.x == 'center':
            return Globals.RESOLUTION[0]/2 + self.x_offset - size[0]/2
        elif self.x == 'right':
            return Globals.RESOLUTION[0] - size[0] - self.x_offset
        else:
            return self.x
    def set_alpha(self):
        if self.alpha != 255:
            self.alpha += 10
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
