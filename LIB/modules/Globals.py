# -*- coding: utf-8 -*-
import pygame
from GlobalFuncs import change_volume, check_files, check_user_monitor, read_settings, read_translation, switch_sound_state
from ScreenData import MainScreen
from Sprite import Sprite

#--- Initialize python modules
pygame.display.init()
pygame.font.init()
pygame.mixer.init()
#--- Game version and resolution
VERSION = '0.4-dev'
AVAIL_RESOLUTIONS = check_user_monitor()
#RESOLUTION = (AVAIL_RESOLUTIONS[0][0], AVAIL_RESOLUTIONS[1][0]) --- commented out just for debugging
RESOLUTION = (1200, 700)
#--- Colors, directories, files, fonts, pictures and languages
COLORS = {'black'               : pygame.Color('black'),
          'grey'                : pygame.Color('grey'),
          'red'                 : pygame.Color('red'),
          'white'               : pygame.Color('white')}

DIRS = {'LIB'                   : 'LIB/',
        'settings'              : 'settings/'}
DIRS['fonts'] = DIRS['LIB'] + 'fonts/'
DIRS['images'] = DIRS['LIB'] + 'images/'
DIRS['images_etc'] = DIRS['images'] + 'etc/'
DIRS['sounds'] = DIRS['LIB'] + 'sounds/'
DIRS['translations'] = DIRS['LIB'] + 'translations/'

FILES = {'font_ubuntu'          : DIRS['fonts'] + 'Ubuntu-M.ttf',
         'last_game_settings'   : DIRS['settings'] + 'last_game_settings',
         'settings'             : DIRS['settings'] + 'settings',
         'stats'                : DIRS['settings'] + 'stats'}

FONTS = {'ubuntu_bigger'        : pygame.font.Font(FILES['font_ubuntu'], 32),
         'ubuntu_big'           : pygame.font.Font(FILES['font_ubuntu'], 24),
         'ubuntu_small'         : pygame.font.Font(FILES['font_ubuntu'], 16)}

PICS = {'appicon'               : DIRS['images'] + 'appicon.png',
        'background'            : Sprite(((RESOLUTION[0]-1820)/2, -130), DIRS['images'] + 'background.jpg'),
        'logo'                  : Sprite((RESOLUTION[0]/3, 100), DIRS['images_etc'] + 'logo.png')}

SOUNDS = {'music'               : pygame.mixer.music.load(DIRS['sounds'] + 'music.ogg'),
          'button-pressed'      : pygame.mixer.Sound(DIRS['sounds'] + 'button-pressed.wav')}

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
#--- Various important settings
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
change_volume(SETTINGS['volume'])
switch_sound_state('music', not SETTINGS['music'])
#--- Create MainScreen object
main_scr = MainScreen()
