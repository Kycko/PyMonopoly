# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha, slight_animation_count_pos

class Sprite():
    def __init__(self, pos, file):
        self.x, self.y = pos
        self.new_y = self.y
        self.bitmap = pygame.image.load(file)
    def render(self):
        self.x, self.y = slight_animation_count_pos((self.x, self.new_y), (self.x, self.y), 10)
        Globals.screen.blit(self.bitmap, (self.x, self.y))
class Line():
    def __init__(self, obj, type, width):
        self.color = change_color_alpha(obj.color, 5)
        if type == 'bottom':
            self.pos = obj.rect.bottomleft
            self.new_y = obj.new_y + obj.rect.h
        self.rect = pygame.Rect((0, 0), (obj.rect.w, width))
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
    def render(self):
        if self.color.a != 255:
            self.color.a += 10
            pygame.draw.rect(self.surf, self.color, self.rect, 0)
        self.pos = slight_animation_count_pos((self.pos[0], self.new_y), self.pos, 10)
        Globals.screen.blit(self.surf, self.pos)
