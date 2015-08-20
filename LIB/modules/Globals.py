# -*- coding: utf-8 -*-
import pygame
from GlobalFuncs import check_files, check_user_monitor, read_settings, read_translation
from ScreenData import MainScreen
from Sprite import Sprite

#--- Initialize python modules
pygame.display.init()
pygame.font.init()
#--- Game version and resolution
VERSION = '0.1-dev'
AVAIL_RESOLUTIONS = check_user_monitor()
RESOLUTION = (AVAIL_RESOLUTIONS[0][0], AVAIL_RESOLUTIONS[1][0])
#--- Directories, files, fonts, pictures and languages
DIRS = {'LIB'                   : 'LIB/',
        'settings'              : 'settings/'}
DIRS['fonts'] = DIRS['LIB'] + 'fonts/'
DIRS['images'] = DIRS['LIB'] + 'images/'
DIRS['translations'] = DIRS['LIB'] + 'translations/'

FILES = {'font_ubuntu'          : DIRS['fonts'] + 'Ubuntu-M.ttf',
         'last_game_settings'   : DIRS['settings'] + 'last_game_settings',
         'settings'             : DIRS['settings'] + 'settings',
         'stats'                : DIRS['settings'] + 'stats'}

FONTS = {'ubuntu_big'           : pygame.font.Font(FILES['font_ubuntu'], 24)}

PICS = {'appicon'               : DIRS['images'] + 'appicon.png',
        'background'            : Sprite(((RESOLUTION[0]-1820)/2, -130), DIRS['images'] + 'background.jpg')}

LANGUAGES = (('en', u'English'),
             ('ru', u'Русский'))
#--- Restore files, read settings and translation
check_files()
SETTINGS = read_settings()
TRANSLATION = read_translation(SETTINGS['language'])
#--- Create main window
pygame.display.set_icon(pygame.image.load(PICS['appicon']))
window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('PyMonopoly. Version: ' + VERSION)
screen = pygame.Surface(RESOLUTION)
main_scr = MainScreen()
