# -*- coding: utf-8 -*-
import pygame
from GlobalFuncs import change_volume, check_files, check_user_monitor, create_players_list, read_settings, read_translation, switch_sound_state
from os.path import expanduser
from ScreenData import MainScreen
from Sprite import Sprite

#--- Initialize python modules
pygame.display.init()
pygame.font.init()
pygame.mixer.init()
#--- Game version and resolution
VERSION = '0.4-dev'
RESOLUTION = check_user_monitor(1200, 700)
#--- Colors, directories, files, fonts, pictures and languages
COLORS = {'black'               : pygame.Color('black'),
          'light_brown'         : pygame.Color(160, 78, 61),
          'light_blue'          : pygame.Color(15, 124, 164),
          'light_green'         : pygame.Color(126, 231, 85),
          'grey'                : pygame.Color('grey'),
          'grey63'              : pygame.Color(95, 95, 95),
          'magenta'             : pygame.Color('magenta'),
          'light_red'           : pygame.Color(231, 85, 85),
          'red'                 : pygame.Color(255, 30, 30),
          'white'               : pygame.Color('white'),
          'yellow'              : pygame.Color(228, 227, 17)}

PLAYERS_COLORS = (COLORS['light_blue'],
                  COLORS['magenta'],
                  COLORS['red'],
                  COLORS['light_green'],
                  COLORS['light_brown'],
                  COLORS['yellow'])

DIRS = {'LIB'                   : '/usr/lib/pymonopoly/',
        'settings'              : expanduser('~') + '/.config/pymonopoly/'}
DIRS['fonts'] = DIRS['LIB'] + 'fonts/'
DIRS['images'] = DIRS['LIB'] + 'images/'
DIRS['images_etc'] = DIRS['images'] + 'etc/'
DIRS['sounds'] = DIRS['LIB'] + 'sounds/'
DIRS['translations'] = DIRS['LIB'] + 'translations/'

FILES = {'font_ubuntu'          : DIRS['fonts'] + 'Ubuntu-M.ttf',
         'font_ume'             : DIRS['fonts'] + 'ume-ugo5.ttf',
         'last_game_settings'   : DIRS['settings'] + 'last_game_settings',
         'settings'             : DIRS['settings'] + 'settings',
         'stats'                : DIRS['settings'] + 'stats'}

FONTS = {'ubuntu_11'    : pygame.font.Font(FILES['font_ubuntu'], 11),
         'ubuntu_16'    : pygame.font.Font(FILES['font_ubuntu'], 16),
         'ubuntu_20'    : pygame.font.Font(FILES['font_ubuntu'], 20),
         'ubuntu_24'    : pygame.font.Font(FILES['font_ubuntu'], 24),
         'ubuntu_32'    : pygame.font.Font(FILES['font_ubuntu'], 32),
         'ume_12'       : pygame.font.Font(FILES['font_ume'], 12),
         'ume_16'       : pygame.font.Font(FILES['font_ume'], 16)}

PICS = {'appicon'               : DIRS['images'] + 'appicon.png',
        'background'            : Sprite(((RESOLUTION[0]-1820)/2, -130), DIRS['images'] + 'background.jpg'),
        'logo'                  : Sprite((RESOLUTION[0]/3, 120), DIRS['images_etc'] + 'logo.png')}

SOUNDS = {'music'               : pygame.mixer.music.load(DIRS['sounds'] + 'music.ogg'),
          'button-pressed'      : pygame.mixer.Sound(DIRS['sounds'] + 'button-pressed.wav')}

LANGUAGES = (('en', u'English'),
             ('ru', u'Русский'))

TEMP_VARS = {}
#--- Restore files, read settings and translation, create players list
check_files()
SETTINGS = read_settings()
TRANSLATION = read_translation(SETTINGS['language'])
create_players_list()
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
