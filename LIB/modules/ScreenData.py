# -*- coding: utf-8 -*-
import Globals, pygame
from MenuItems import MainCursor, MenuItem
from sys import exit as SYSEXIT

class MainScreen():
    def __init__(self, type):
        if type == 'main_main':
            self.menuitems = {'new_game'    : MenuItem(Globals.TRANSLATION[0], 'main_new_game', 'main_main', 0),
                              'settings'    : MenuItem(Globals.TRANSLATION[1], 'main_settings', 'main_main', 1),
                              'stats'       : MenuItem(Globals.TRANSLATION[2], 'main_stats', 'main_main', 2),
                              'exit'        : MenuItem(Globals.TRANSLATION[3], 'main_sysexit', 'main_main', 3)}
            self.pics = {'background'       : Globals.PICS['background']}
        self.cursor = MainCursor(self.menuitems, type)
    def mainloop(self):
        while True:
            cur_key = self.check_mouse_pos(pygame.mouse.get_pos())
            self.render(cur_key)
            self.events(cur_key)
    def check_mouse_pos(self, mp):
        key = self.find_hovering_menuitem(mp)
        if key != self.cursor.active_key and key in self.cursor.keys:
            self.cursor.change_pos(key)
        return key
    def find_hovering_menuitem(self, mp):
        for key in self.menuitems.keys():
            if self.menuitems[key].active_zone.collidepoint(mp):
                return key
        return None
    def render(self, cur_key):
        for pic in self.pics.values():
            pic.render()
        if self.cursor:
            self.cursor.render()
        for key in self.menuitems.keys():
            self.menuitems[key].render(cur_key == key)
        Globals.window.blit(Globals.screen, (0, 0))
        pygame.display.flip()
    def events(self, cur_key):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and cur_key:
                self.action_call(cur_key)
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_DOWN) and self.cursor:
                    self.cursor.keypress(e.key)
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.cursor:
                    self.action_call(self.cursor.active_key)
                elif e.key == pygame.K_ESCAPE:
                    self.menuitems['exit'].action()
                else:
                    for key in self.menuitems.keys():
                        if self.menuitems[key].group[:4] != 'main' and e.key == self.menuitems[key].HOTKEY:
                            self.action_call(key)
            elif e.type == pygame.QUIT:
                SYSEXIT()
    def action_call(self, key):
        type = self.menuitems[key].action()
        if type:
            print(type)
