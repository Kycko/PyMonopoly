# -*- coding: utf-8 -*-
import Globals
from random import randrange

def roll_the_dice():
    dice1 = randrange(6)
    dice2 = randrange(6)
    return 1+dice1, 1+dice2, u'⚀⚁⚂⚃⚄⚅'[dice1] + ' ' + u'⚀⚁⚂⚃⚄⚅'[dice2]
def change_player():
    Globals.TEMP_VARS['cur_turn'] += 1
    if Globals.TEMP_VARS['cur_turn'] == len(Globals.PLAYERS):
        Globals.TEMP_VARS['cur_turn'] = 0
