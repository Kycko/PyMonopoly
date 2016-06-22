# -*- coding: utf-8 -*-
import Globals
from random import randrange

def roll_the_dice():
    Globals.TEMP_VARS['dice1'] = 1+randrange(6)
    Globals.TEMP_VARS['dice2'] = 1+randrange(6)
    return u' ⚀⚁⚂⚃⚄⚅'[Globals.TEMP_VARS['dice1']] + ' ' + u' ⚀⚁⚂⚃⚄⚅'[Globals.TEMP_VARS['dice2']]
def change_player():
    Globals.TEMP_VARS['cur_turn'] += 1
    if Globals.TEMP_VARS['cur_turn'] == len(Globals.PLAYERS):
        Globals.TEMP_VARS['cur_turn'] = 0
