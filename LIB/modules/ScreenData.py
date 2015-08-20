# -*- coding: utf-8 -*-
import Globals, pygame
from MenuItems import Cursor, MenuItem
from sys import exit as SYSEXIT

class MainScreen():
    def __init__(self):
        self.menuitems = {'new_game'    : MenuItem(Globals.TRANSLATION[0], 'main_new_game', 'main_main', 0),
                          'settings'    : MenuItem(Globals.TRANSLATION[1], 'main_settings', 'main_main', 1),
                          'stats'       : MenuItem(Globals.TRANSLATION[2], 'main_stats', 'main_main', 2),
                          'exit'        : MenuItem(Globals.TRANSLATION[3], 'main_sysexit', 'main_main', 3)}
        self.pics = {'background'       : Globals.PICS['background']}
        self.create_cursor()
    def create_cursor(self):
        keys = ['new_game', 'settings', 'stats', 'exit']
        rects = [self.menuitems[key].text.rect for key in keys]
        self.cursor = Cursor(keys, rects)
    def mainloop(self):
        while True:
            key = self.check_mouse_pos(pygame.mouse.get_pos())
            self.render(key)
            self.events()
    def check_mouse_pos(self, mp):
        key = self.find_hovering_menuitem(mp)
        if key in self.cursor.keys:
            self.cursor.change_pos(key)
        return key
    def find_hovering_menuitem(self, mp):
        for key in self.menuitems.keys():
            if self.menuitems[key].active_zone.collidepoint(mp):
                return key
        return None
    def render(self, highlighted_menuitem):
        for pic in self.pics.values():
            pic.render()
        self.cursor.render()
        for item in self.menuitems.values():
            if item.text.AV:
                item.render(highlighted_menuitem)
        Globals.window.blit(Globals.screen, (0, 0))
        pygame.display.flip()
    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                SYSEXIT()
