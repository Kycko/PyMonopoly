# -*- coding: utf-8 -*-
import Globals, pygame
from GlobalFuncs import change_color_alpha, count_new_pos, slight_animation_count_pos

class SpriteTemplate():
    def change_new_pos(self, offset):
        self.new_pos = count_new_pos(self.new_pos, offset)
    def render(self):
        self.pos = slight_animation_count_pos(self.new_pos, self.pos, 10, self.speed_limit)
        Globals.screen.blit(self.surf, self.pos)
class Sprite(SpriteTemplate):
    def __init__(self, pos, file, speed_limit=None):
        self.init_pos = pos
        self.pos = pos
        self.new_pos = pos
        self.speed_limit = speed_limit
        self.surf = pygame.image.load(file)
class Line(SpriteTemplate):
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
        self.speed_limit = None
    def render(self):
        if self.color.a != 255:
            self.color.a += 10
            pygame.draw.rect(self.surf, self.color, self.rect, 0)
        SpriteTemplate.render(self)
