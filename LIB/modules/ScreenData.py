# -*- coding: utf-8 -*-
import Globals, pygame
from MenuItems import MenuItem
from sys import exit as SYSEXIT

class MainScreen():
    def __init__(self):
        self.menuitems = {'new_game'    : MenuItem(Globals.TRANSLATION[0], 'new_game', 'main_main', 0)}
        self.pics = {'background'       : Globals.PICS['background']}
    def mainloop(self):
        while True:
            for pic in self.pics.values():
                pic.render()
            for item in self.menuitems.values():
                item.text.render()
            Globals.window.blit(Globals.screen, (0, 0))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    SYSEXIT()
