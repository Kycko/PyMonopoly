# -*- coding: utf-8 -*-
import Globals, pygame

class MainScreen():
    def __init__(self):
        self.pics = {'background'   : Globals.PICS['background']}
    def mainloop(self):
        while True:
            for pic in self.pics.values():
                pic.render()
            Globals.window.blit(Globals.screen, (0, 0))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    Globals.SYSEXIT()
