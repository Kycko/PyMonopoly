# -*- coding: utf-8 -*-
import Globals
import GlobalFuncs
from pygame import draw, Rect, Surface

class Player():
    def __init__(self, name, color, human):
        self.name = name
        self.color = color
        self.human = human
        self.cur_field = 0
        self.game_piece = Surface((16, 16))
        draw.rect(self.game_piece, self.color, Rect((0, 0), (16, 16)))
        draw.rect(self.game_piece, Globals.COLORS['black'], Rect((0, 0), (16, 16)), 1)
        self.game_piece.blit(Globals.FONTS['ubuntu_11'].render(self.name[0], True, Globals.COLORS['black']), (4, 1))
        self.speed_limit = 50
    def initialize_coords(self, number):
        self.game_piece_order = 0
        for i in range(number):
            self.game_piece_order += int(Globals.PLAYERS[i].cur_field == self.cur_field)
        self.coords = self.count_coords()
        self.new_coords = self.coords
    def count_coords(self):
        gamefield = Globals.main_scr.objects['gamefield']
        cell = gamefield.cells[self.cur_field]
        x = cell.pos[0]+(self.game_piece_order%3)*15+gamefield.pos[0]
        y = cell.pos[1]+gamefield.pos[1]
        if self.cur_field <= 10:
            y += int(self.cur_field <= 10)*cell.rect.h-((self.game_piece_order//3)+1)*15-1
        else:
            y += ((self.game_piece_order//3))*15
        if cell.group in (7, 8):
            x += 19
        return (x, y)
    def change_new_pos(self, offset):
        self.new_coords = GlobalFuncs.count_new_pos(self.new_coords, offset)
    def move_forward(self, points):
        self.cur_field += points
        if self.cur_field > 39:
            self.cur_field -= 40
            self.money += Globals.main_scr.objects['gamefield'].cells[0].buy_cost
            Globals.main_scr.labels['money_player'+str(Globals.TEMP_VARS['cur_turn'])].update_text(str(self.money))
        self.game_piece_order = self.count_players_on_one_field()
        self.new_coords = self.count_coords()
    def count_players_on_one_field(self):
        busy = []
        for player in Globals.PLAYERS:
            if player.name != self.name and player.cur_field == self.cur_field:
                busy.append(player.game_piece_order)
        for i in range(6):
            if i not in busy:
                return i
    def render(self):
        self.coords = GlobalFuncs.slight_animation_count_pos(self.new_coords, self.coords, 10, self.speed_limit)
        Globals.screen.blit(self.game_piece, self.coords)
