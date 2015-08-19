# -*- coding: utf-8 -*-
import pygame
from GlobalFuncs import check_user_monitor
from ScreenData import MainScreen
from Sprite import Sprite

#--- Initialize python modules
pygame.display.init()

#--- Game version and resolution
VERSION = '0.1-dev'
AVAIL_RESOLUTIONS = check_user_monitor()
RESOLUTION = (AVAIL_RESOLUTIONS[0][0], AVAIL_RESOLUTIONS[1][0])

#--- Directories and pictures
DIRS = {'LIB'           : 'LIB/'}
DIRS['images'] = DIRS['LIB'] + 'images/'

PICS = {'appicon'       : DIRS['images'] + 'appicon.png',
        'background'    : Sprite(((RESOLUTION[0]-1820)/2, -130), DIRS['images'] + 'background.jpg')}

#--- Create main window
pygame.display.set_icon(pygame.image.load(PICS['appicon']))
window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('PyMonopoly. Version: ' + VERSION)
screen = pygame.Surface(RESOLUTION)
main_scr = MainScreen()
