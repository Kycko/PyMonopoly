# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha, slight_animation_count_pos

class Sprite():
    def __init__(self, pos, file):
        self.pos = pos
        self.new_pos = pos
        self.bitmap = pygame.image.load(file)
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10)
        Globals.screen.blit(self.bitmap, self.pos)
class Line():
    def __init__(self, obj, type, width, color=None):
        if color:
            self.color = change_color_alpha(color, 5)
        else:
            self.color = change_color_alpha(obj.color, 5)
        if type == 'bottom':
            self.pos = obj.rect.bottomleft
            self.new_pos = (obj.new_pos[0], obj.new_pos[1] + obj.rect.h)
            self.rect = pygame.Rect((0, 0), (obj.rect.w, width))
        elif type == 'right':
            self.pos = obj.rect.topright
            self.new_pos = (obj.new_pos[0]+obj.rect.w, obj.new_pos[1])
            self.rect = pygame.Rect((0, 0), (width, obj.rect.h))
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
    def render(self):
        if self.color.a != 255:
            self.color.a += 10
            pygame.draw.rect(self.surf, self.color, self.rect, 0)
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10)
        Globals.screen.blit(self.surf, self.pos)
