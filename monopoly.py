#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import pygame
from sys import exit as SYSEXIT

class Sprite:
    def __init__(self, pos, file):
        self.x, self.y = pos
        self.bitmap = pygame.image.load(file)
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

pygame.display.init()
MAX_RESOLUTION = (pygame.display.Info().current_w-70, pygame.display.Info().current_h-60)
avail_x = [i for i in (1820, 1250, 1200) if i < MAX_RESOLUTION[0]]
avail_y = [i for i in (1000, 950, 700) if i < MAX_RESOLUTION[1]]
if avail_x and avail_y:
    AVAIL_RESOLUTIONS = (avail_x, avail_y)
else:
    print("Your monitor has too small resolution! We can't provide a good interface for it :(")
    SYSEXIT()
VERSION = '0.1-dev'
RESOLUTION = (AVAIL_RESOLUTIONS[0][0], AVAIL_RESOLUTIONS[1][0])
DIRS = {'LIB'           : 'LIB/'}
DIRS['images'] = DIRS['LIB'] + 'images/'
PICS = {'appicon'       : DIRS['images'] + 'appicon.png',
        'background'    : Sprite(((RESOLUTION[0]-1820)/2, -130), DIRS['images'] + 'background.jpg')}
pygame.display.set_icon(pygame.image.load(PICS['appicon']))
window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('PyMonopoly. Version: ' + VERSION)
screen = pygame.Surface(RESOLUTION)
PICS['background'].render()
window.blit(screen, (0, 0))
pygame.display.flip()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            SYSEXIT()
