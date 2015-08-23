# -*- coding: utf-8 -*-
import Globals
from GlobalFuncs import change_color_alpha, slight_animation_count_pos
from pygame import draw, image, Rect, Surface

class Sprite():
    def __init__(self, pos, file):
        self.x, self.y = pos
        self.new_y = self.y
        self.bitmap = image.load(file)
    def render(self):
        self.x, self.y = slight_animation_count_pos((self.x, self.new_y), (self.x, self.y), 10)
        Globals.screen.blit(self.bitmap, (self.x, self.y))
class Line():
    def __init__(self, obj, type, width):
        self.color = change_color_alpha(obj.color, 5)
        if type == 'bottom':
            self.pos = obj.rect.bottomleft
            self.new_y = obj.new_y + obj.rect.h
        self.rect = Rect((0, 0), (obj.rect.w, width))
        self.surf = Surface(self.rect.size)
    def render(self):
        if self.color.a != 255:
            self.color.a += 10
            draw.rect(self.surf, self.color, self.rect, 0)
        self.pos = slight_animation_count_pos((self.pos[0], self.new_y), self.pos, 10)
        Globals.screen.blit(self.surf, self.pos)
