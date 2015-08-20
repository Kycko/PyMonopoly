# -*- coding: utf-8 -*-
import Globals, pygame
from TransparentText import AlphaText

class MenuItem():
    def __init__(self, text, type, group, number=None):
        self.type = type
        self.text = AlphaText(text, group, number)
        self.init_for_group(group)
    def init_for_group(self, group):
        self.tooltip = None
        if group[:4] == 'main':
            self.active_zone = self.text.rect.inflate(500-self.text.rect.w, 0)
    def render(self, highlighted_menuitem):
        self.text.render()
class Cursor():
    def __init__(self, keys, rects):
        self.keys = keys
        self.y_cords = [rect.y for rect in rects]
        size = (500, rects[0].h+6)
        self.x = rects[0].x-(size[0]-rects[0].w)/2
        self.change_pos(keys[0])
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.surf, (0, 0, 0, 150), pygame.Rect((0, 0), size), 0)
    def change_pos(self, key):
        self.active = self.keys.index(key)
        self.y = self.y_cords[self.active]-3
    def render(self):
        Globals.screen.blit(self.surf, (self.x, self.y))
