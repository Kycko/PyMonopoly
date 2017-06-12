# -*- coding: utf-8 -*-
import Globals, TransparentText
from random import randrange

def roll_the_dice():
    for i in range(1, 3):
        Globals.TEMP_VARS['dice' + str(i)] = randrange(1, 7)
    return show_dices_picture()
def show_dices_picture():
    text = u' ⚀⚁⚂⚃⚄⚅'[Globals.TEMP_VARS['dice1']] + ' ' + u' ⚀⚁⚂⚃⚄⚅'[Globals.TEMP_VARS['dice2']]
    return TransparentText.AlphaText(text, 'ingame_dices')
def change_player(bankrupt=None):
    Globals.TEMP_VARS['double_dices_count'] = 0
    if not bankrupt:
        Globals.TEMP_VARS['cur_turn'] += 1
    if Globals.TEMP_VARS['cur_turn'] == len(Globals.PLAYERS):
        Globals.TEMP_VARS['cur_turn'] = 0
