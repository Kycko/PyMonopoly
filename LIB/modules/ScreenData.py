# -*- coding: utf-8 -*-
import FieldCellsData, GameMechanics, Globals, pygame, random
from GameObjects import GameField, GameLog, TradeSummary
from GlobalFuncs import *
from MenuItems import CurTurnHighlighter, MainCursor, MenuItem
from Sprite import *
from TransparentText import AlphaText
from sys import exit as SYSEXIT

class MainScreen():
    #--- Common
    def __init__(self):
        self.switch_screen('main_main', None)
    def switch_screen(self, type, key):
        if type in ('main_new_game', 'main_settings', 'main_stats') and 'gamebackground' in self.pics.keys():
            self.pics.pop('gamebackground')
            self.pics['order'].remove('gamebackground')
            self.objects = {}
            create_players_list()
        if type == 'main_main':
            if key != 'exit':
                self.pics = {'background'   : Sprite(((Globals.RESOLUTION[0]-1820)/2, -130), Globals.PICS['background'], 50),
                             'logo'         : Globals.PICS['logo'],
                             'order'        : ['background', 'logo']}
                self.labels = {'APPNAME'    : AlphaText('PyMonopoly', 'APPNAME'),
                               'APPVERSION' : AlphaText(Globals.TRANSLATION[4]+Globals.VERSION, 'APPVERSION'),
                               'resources'  : AlphaText('Thanks to: freemusicarchive.org, openclipart.org', 'authors', 0),
                               'authors'    : AlphaText('Anthony Samartsev & Michael Mozhaev, 2014-2016', 'authors', 1)}
                self.objects = {}
            else:
                if self.menuitems['exit'].group not in ('from_game_return_to_menu', 'ingame_start'):
                    create_players_list()
                if self.menuitems['exit'].group == 'from_game_return_to_menu':
                    for player in Globals.PLAYERS:
                        player.speed_limit = 50
                    self.pics.update({'background'  : Sprite((((Globals.RESOLUTION[0]-1820)/2)-1820, self.pics['gamebackground'].pos[1]), Globals.PICS['background'], 50),
                                      'logo'        : Globals.PICS['logo'],
                                      'order'       : ['background', 'gamebackground', 'logo']})
                    for key in ('background', 'gamebackground'):
                        self.pics[key].change_new_pos((1820, -130-self.pics[key].new_pos[1]))
                    self.pics['logo'].change_new_pos((1820, 0))
                    for obj in self.objects.values():
                        obj.change_new_pos((1820, 0))
                    self.labels.update({'APPNAME'    : AlphaText('PyMonopoly', 'APPNAME'),
                                        'APPVERSION' : AlphaText(Globals.TRANSLATION[4]+Globals.VERSION, 'APPVERSION'),
                                        'resources'  : AlphaText('Thanks to: freemusicarchive.org, openclipart.org', 'authors', 0),
                                        'authors'    : AlphaText('Anthony Samartsev & Michael Mozhaev, 2014-2015', 'authors', 1)})
                    for key in ('authors', 'resources'):
                        self.labels[key].rect.x -= 1820
                    for key in ('APPNAME', 'APPVERSION'):
                        self.labels[key].change_new_pos((1820, 0))
                    for cell in self.objects['gamefield'].cells:
                        cell.step_indicator.change_new_pos((1820, 0))
                elif self.menuitems['exit'].group == 'main_settings_player_exit':
                    self.move_APPINFO((-300, 0))
                elif self.menuitems['exit'].group == 'ingame_start':
                    self.pics['logo'].new_pos = (self.pics['logo'].new_pos[0]-300, self.pics['logo'].pos[1])
                    for key in ('APPNAME', 'APPVERSION'):
                        self.labels[key].new_pos = (self.labels[key].new_pos[0]-300, self.labels[key].new_pos[1])
                    for key in ('background', 'gamebackground', 'logo'):
                        self.pics[key].new_pos = (self.pics[key].new_pos[0] + 1820, self.pics[key].new_pos[1])
                    for label in self.labels.values():
                        label.new_pos = (label.new_pos[0] + 1820, label.new_pos[1])
                    for obj in self.objects.values():
                        obj.change_new_pos((1820, 0))
                else:
                    self.move_APPINFO((0, 50))
                    self.objects = {}
                Globals.TEMP_VARS.clear()
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.menuitems = {'new_game'    : MenuItem(Globals.TRANSLATION[0], 'main_new_game', 'main_main', 0),
                              'settings'    : MenuItem(Globals.TRANSLATION[1], 'main_settings', 'main_main', 1),
                              'stats'       : MenuItem(Globals.TRANSLATION[2], 'main_stats', 'main_main', 2),
                              'exit'        : MenuItem(Globals.TRANSLATION[3], 'main_sysexit', 'main_main', 3)}
            self.cursor = MainCursor(self.menuitems, 'main_main')
        elif type == 'main_stats':
            self.move_APPINFO((0, -50))
            self.menuitems = {'exit'        : MenuItem(Globals.TRANSLATION[11], 'main_main', 'main_stats')}
            if not Globals.SETTINGS['block']:
                self.menuitems['switch'] = MenuItem(Globals.TRANSLATION[12], 'stats_switch', 'stats_switch')
            self.make_stats_screen(Globals.TRANSLATION[6-Globals.SETTINGS['fav_game']])
        elif type == 'main_settings':
            if key != 'exit':
                self.move_APPINFO((0, -50))
                Globals.TEMP_VARS['edit_player'] = 0
            else:
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.make_settings_screen()
        elif 'main_new_edit_player' in type or type == 'main_settings_player':
            if key == 'exit':
                Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].name = self.labels['name_MI'].symbols
                self.objects = {}
            self.make_playersettings_screen()
            if 'main_new_edit_player' in type:
                self.menuitems.update({'exit'   : MenuItem(Globals.TRANSLATION[21], 'main_new_game', 'main_settings_player_exit')})
            else:
                self.menuitems.update({'exit'   : MenuItem(Globals.TRANSLATION[21], 'main_settings', 'main_settings_player_exit')})
        elif type == 'main_settings_player_name':
            if self.menuitems['exit'].type == 'main_new_game':
                type = 'main_new_edit_player'
            else:
                type = 'main_settings_player'
            self.menuitems = {'exit'        : MenuItem(Globals.TRANSLATION[21], type, 'main_settings_player_exit')}
            self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            self.labels.update({'name'      : AlphaText(Globals.TRANSLATION[24], 'settings_left', 1),
                                'name_MI'   : AlphaText(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].name, 'main_settings_player', 0)})
            self.make_obj_for_enter_name()
        elif type == 'main_new_game':
            self.init_avail_colors_and_names()
            if key == 'exit':
                Globals.TEMP_VARS.pop('edit_player')
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            else:
                self.move_APPINFO((300, 0))
                Globals.TEMP_VARS['cur_game'] = Globals.SETTINGS['fav_game']
                LGS = read_file(Globals.FILES['last_game_settings'])
                for string in LGS:
                    add_new_player(string == 'human')
            self.menuitems = {'total'           : MenuItem('', 'main_new_total_SELECTOR', 'main_settings_left_MI', 0),
                              'humans'          : MenuItem('', 'main_new_humans_SELECTOR', 'main_settings_left_MI', 1),
                              'start'           : MenuItem(Globals.TRANSLATION[33], 'game_start', 'main_settings_player_exit', 1),
                              'exit'            : MenuItem(Globals.TRANSLATION[11], 'main_main', 'main_settings_player_exit')}
            self.labels.update({'total'         : AlphaText(Globals.TRANSLATION[28], 'settings_left', 0),
                                'inactive_MI'   : AlphaText(u'●', 'main_new_total_SELECTOR', 0),
                                'humans'        : AlphaText(Globals.TRANSLATION[30], 'settings_left', 1),
                                'players'       : AlphaText(Globals.TRANSLATION[31], 'settings_left', 2)})
            if key == 'exit':
                self.check_error(type)
            for i in range(len(Globals.PLAYERS)):
                self.menuitems.update({'player'+str(i)  : MenuItem(Globals.PLAYERS[i].name, 'main_new_edit_player_'+str(i), 'main_new_playerlist', i)})
                if not Globals.PLAYERS[i].human:
                    self.labels.update({'player'+str(i) : AlphaText('AI', 'newgame_playertype', i)})
            if not Globals.SETTINGS['block']:
                self.menuitems.update({'game'   : MenuItem(u'‹ '+Globals.TRANSLATION[5+int(Globals.TEMP_VARS['cur_game'])]+u' ›', 'main_new_game_switch', 'main_settings_left_MI', -1)})
                self.labels.update({'game'      : AlphaText(Globals.TRANSLATION[27], 'settings_left', -1)})
        elif type == 'game_start':
            for key in ('avail_colors', 'avail_names'):
                Globals.TEMP_VARS.pop(key)
            random.shuffle(Globals.PLAYERS)
            Globals.TEMP_VARS['onboard_text'] = read_onboard_text()
            Globals.TEMP_VARS['rentlabels'] = Globals.TEMP_VARS['onboard_text']['rentlabels']
            Globals.TEMP_VARS['cells_cost'] = FieldCellsData.read_cells_costs()
            Globals.TEMP_VARS['cells_groups'] = FieldCellsData.make_groups()
            Globals.TEMP_VARS['cells_rent_costs'] = FieldCellsData.read_cells_rent_costs()
            Globals.TEMP_VARS['cur_turn'] = 0
            self.menuitems = {'start_game'      : MenuItem(Globals.TRANSLATION[34], 'ingame_start_game', 'ingame_start', 0),
                              'exit'            : MenuItem(Globals.TRANSLATION[35], 'main_main', 'ingame_start', 1)}
            self.objects = {'gamefield' : GameField()}
            for i in range(len(Globals.PLAYERS)):
                Globals.PLAYERS[i].initialize_coords(i)
                Globals.PLAYERS[i].money = (1500, 20000)[Globals.TEMP_VARS['cur_game']]
                self.menuitems.update({'player_'+Globals.PLAYERS[i].name    : MenuItem(u'●', 'pl_info_tab_'+Globals.PLAYERS[i].name, 'pl_info_tab', i)})
                self.labels.update({'money_player_'+Globals.PLAYERS[i].name : AlphaText(str(Globals.PLAYERS[i].money), 'pl_money_info', i)})
            self.objects['gamefield'].change_new_pos((-1820, 0))
            self.objects['cur_turn_highlighter'] = CurTurnHighlighter(self.menuitems)
            self.pics.update({'gamebackground'  : Sprite((self.pics['background'].pos[0]+1820, -130), Globals.PICS['background'], 50),
                              'order'           : ['background', 'gamebackground', 'logo']})
            for key in ('background', 'gamebackground', 'logo'):
                self.pics[key].new_pos = (self.pics[key].new_pos[0] - 1820, self.pics[key].new_pos[1])
            for label in self.labels.values():
                label.new_pos = (label.new_pos[0]-1820, label.new_pos[1])
            for item in self.menuitems.values():
                item.text.new_pos = (item.text.new_pos[0]-1820, item.text.new_pos[1])
                if 'SELECTOR' in item.type:
                    for dot in item.selector.items:
                        dot.new_pos = (dot.new_pos[0]-1820, dot.new_pos[1])
    def mainloop(self):
        while True:
            cur_key = self.check_mouse_pos(pygame.mouse.get_pos())
            self.render(cur_key)
            self.events(cur_key)
    def render(self, cur_key):
        for key in self.pics['order']:
            self.pics[key].render()
        for obj in self.objects.values():
            obj.render()
        if self.cursor:
            self.cursor.render(self.menuitems)
        for key in self.menuitems.keys():
            self.menuitems[key].render(cur_key == key or self.cursor and self.cursor.active_key == key)
        for label in self.labels.values():
            label.render()
        Globals.window.blit(Globals.screen, (0, 0))
        pygame.display.flip()
    #--- Mouse and keyboard events
    def check_mouse_pos(self, mp):
        key = self.find_hovering_menuitem(mp)
        if self.cursor and key != self.cursor.active_key and key in self.cursor.keys:
            self.cursor.change_pos(key)
        return key
    def find_hovering_menuitem(self, mp):
        for key in self.menuitems.keys():
            if self.menuitems[key].active_zone.collidepoint(mp):
                if 'SELECTOR' in self.menuitems[key].type:
                    for i in range(len(self.menuitems[key].selector.items)):
                        if self.menuitems[key].selector.rects[i].collidepoint(mp):
                            self.menuitems[key].selector.apply_new_active(i)
                return key
        return None
    def events(self, cur_key):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and cur_key:
                self.action_call(cur_key)
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_DOWN) and self.cursor:
                    self.cursor.keypress(e.key)
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.cursor:
                    self.action_call(self.cursor.active_key)
                elif e.key == pygame.K_ESCAPE:
                    actionKEY = ('exit', 'return')['return' in self.menuitems.keys()]
                    self.action_call(actionKEY)
                elif e.key in (pygame.K_LEFT, pygame.K_RIGHT) and self.menuitems and self.cursor and 'SELECTOR' in self.menuitems[self.cursor.active_key].type:
                    self.menuitems[self.cursor.active_key].selector.keypress(e.key)
                elif self.menuitems and ('main_new_edit_player' in self.menuitems['exit'].type or self.menuitems['exit'].type == 'main_settings_player'):
                    if e.key == pygame.K_BACKSPACE:
                        self.labels['name_MI'].update_text(self.labels['name_MI'].symbols[:len(self.labels['name_MI'].symbols)-1], False)
                    elif len(self.labels['name_MI'].symbols) < 15:
                        self.labels['name_MI'].update_text(self.labels['name_MI'].symbols + e.unicode, False)
                    self.make_obj_for_enter_name()
                elif self.cursor and e.key in self.menuitems[self.cursor.active_key].HOTKEYS:
                        self.action_call(self.cursor.active_key)
                else:
                    for key in self.menuitems.keys():
                        if self.menuitems[key].type[:4] != 'main' and e.key in self.menuitems[key].HOTKEYS:
                            self.action_call(key)
            elif e.type == pygame.QUIT:
                SYSEXIT()
    #--- Menu actions
    def action_call(self, key):
        type = self.menuitems[key].action(key)
        if type in ('roll_the_dice', 'roll_the_dice_to_exit_jail'):
            self.labels['dices'] = GameMechanics.roll_the_dice()
            player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
            points = Globals.TEMP_VARS['dice1'] + Globals.TEMP_VARS['dice2']
            if not (type == 'roll_the_dice_to_exit_jail' and Globals.TEMP_VARS['dice1'] != Globals.TEMP_VARS['dice2']):
                for i in range(player.cur_field + 1, player.cur_field + points + 1):
                    self.objects['gamefield'].cells[i-40].step_indicator.change_color(player.color)
                    self.objects['gamefield'].cells[i-40].step_indicator_visible = True
                player.move_forward(points)
                if player.cur_field - points == 10:
                    self.menuitems['fieldcell_10'].tooltip.RErender()
                self.player_on_a_new_cell(self.objects['gamefield'].cells[player.cur_field])
                self.objects['game_log'].add_message('roll_the_dice')
            else:
                self.clear_main_menu_entries()
                player.exit_jail_attempts -= 1
                self.objects['game_log'].add_message('roll_the_dice_to_exit_jail')
                self.labels['target_cell_owner'] = AlphaText(Globals.TRANSLATION[54] + str(player.exit_jail_attempts), 'target_cell_owner', 1)
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49], 'ingame_continue_doesnt_exit_jail', 'ingame_main', 5)
                self.cursor.screen_switched(self.menuitems, 'ingame_continue')
                self.menuitems['fieldcell_10'].tooltip.RErender()
        elif type == 'ingame_end_turn':
            self.change_player()
        elif type in ('pay_money_to_exit_jail', 'use_card_to_exit_jail'):
            player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
            CELL = self.objects['gamefield'].cells[10]
            if type == 'pay_money_to_exit_jail':
                self.change_player_money(player, -CELL.buy_cost)
            else:
                vid = player.free_jail_cards.pop(0)
                self.objects['gamefield'].chests_and_chances[vid+'s'].append(Globals.TEMP_VARS['free_jail_obj'])
            player.exit_jail_attempts = None
            CELL.RErender()
            self.menuitems['fieldcell_10'].tooltip.RErender()
            self.objects['game_log'].add_message(type)
            self.new_turn()
        elif type == 'ingame_buy_a_cell':
            player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
            self.change_owner_for_a_cell(player)
            self.change_player_money(player, -Globals.TEMP_VARS['MUST_PAY'])
            self.objects['game_log'].add_message(type)
            self.ask_to_end_turn()
        elif type in ('ingame_continue_tax', 'ingame_continue_income'):
            self.objects['game_log'].add_message(type)
            self.change_player_money(Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']], Globals.TEMP_VARS['MUST_PAY'])
            self.ask_to_end_turn()
        elif type == 'ingame_continue_PAY_RENT':
            cur_turn = Globals.TEMP_VARS['cur_turn']
            player = Globals.PLAYERS[cur_turn]
            cell = self.objects['gamefield'].cells[player.cur_field]
            self.change_player_money(player, -Globals.TEMP_VARS['MUST_PAY'])
            for i in range(len(Globals.PLAYERS)):
                if Globals.PLAYERS[i].name == cell.owner:
                    self.change_player_money(Globals.PLAYERS[i], Globals.TEMP_VARS['MUST_PAY'])
            self.objects['game_log'].add_message(type)
            self.ask_to_end_turn()
        elif type in ('ingame_continue_chest', 'ingame_continue_chance'):
            obj = self.objects['gamefield'].chests_and_chances[type[16:] + 's']
            player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
            if obj[0].type == 'income':
                Globals.TEMP_VARS['MUST_PAY'] = obj[0].modifier[0]
                self.change_player_money(player, Globals.TEMP_VARS['MUST_PAY'])
                self.objects['game_log'].add_message('chest_income')
                self.ask_to_end_turn()
            elif obj[0].type[:4] == 'goto':
                type = obj[0].type[5:]
                if not type:
                    player.move_to(obj[0].modifier[0])
                elif type == 'forward':
                    player.move_forward(obj[0].modifier[0])
                else:
                    player.move_to_chance(type)
                self.player_on_a_new_cell(self.objects['gamefield'].cells[player.cur_field])
                self.objects['game_log'].add_message('chest_goto')
            elif obj[0].type == 'free_jail':
                Globals.TEMP_VARS['free_jail_obj'] = obj.pop(0)
                player.free_jail_cards.append(type[16:])
                self.objects['game_log'].add_message('chest_free_jail')
                self.menuitems['fieldcell_10'].tooltip.RErender()
                self.ask_to_end_turn()
                return None
            elif obj[0].type == 'repair':
                self.ask_to_end_turn()
            elif obj[0].type == 'birthday':
                self.disable_central_labels()
                Globals.TEMP_VARS['pay_birthday'] = [i for i in Globals.PLAYERS if i.name != player.name]
                Globals.TEMP_VARS['MUST_PAY'] = obj[0].modifier[0]
                self.pay_birthday_next_player()
            elif obj[0].type == 'pay_each':
                Globals.TEMP_VARS['MUST_PAY'] = obj[0].modifier[0]
                for i in Globals.PLAYERS:
                    if i.name == player.name:
                        self.change_player_money(player, -obj[0].modifier[0] * (len(Globals.PLAYERS)-1))
                    else:
                        self.change_player_money(i, obj[0].modifier[0])
                self.objects['game_log'].add_message('pay_each')
                self.ask_to_end_turn()
            elif obj[0].type == 'take_chance':
                Globals.TEMP_VARS['take_chance_when_player_is_on_chest'] = True
                self.player_on_a_new_cell(self.objects['gamefield'].cells[player.cur_field])
            obj.append(obj.pop(0))
        elif type == 'ingame_continue_gotojail':
            player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
            player.move_to(10, False)
            player.exit_jail_attempts = 3
            self.menuitems['fieldcell_10'].tooltip.RErender()
            self.objects['game_log'].add_message(type)
            self.ask_to_end_turn()
        elif type and 'enter_the_trade_menu' in type:
            if 'pay_birthday' not in Globals.TEMP_VARS.keys():
                self.disable_central_labels()
            if type == 'enter_the_trade_menu' or len(Globals.PLAYERS) == 2:
                self.save_step_indicators_state()
                Globals.TEMP_VARS['trading'] = {}
                Globals.TEMP_VARS['trading']['trader'] = {}
                temp_var = Globals.TEMP_VARS['trading']['trader']
                if 'pay_birthday' in Globals.TEMP_VARS.keys():
                    self.labels['target_cell_info'].change_new_pos((0, -80))
                temp_var['info'] = self.trader_for_cur_player_or_for_birthday()
                self.objects['trade_summary'] = TradeSummary()
                if 'end_turn' in self.menuitems.keys():
                    back_type = 'end_turn'
                elif 'pay_birthday' in Globals.TEMP_VARS.keys():
                    back_type = 'pay_birthday'
                elif 'roll_the_dice' in self.menuitems.keys():
                    back_type = 'new_turn'
                else:
                    back_type = 'player_on_a_new_cell'
                self.menuitems['return'] = MenuItem(Globals.TRANSLATION[64], 'return_' + back_type, 'ingame_main', 8)
            if type == 'enter_the_trade_menu':
                if 'pay_birthday' not in Globals.TEMP_VARS.keys():
                    self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[63], 'target_cell_info', -3)
                self.clear_main_menu_entries(('return'))
                counter = 0
                for i in range(len(Globals.PLAYERS)):
                    if Globals.PLAYERS[i].name != temp_var['info'].name:
                        trader = check_if_player_can_trade(temp_var['info'])
                        trading_with = check_if_player_can_trade(Globals.PLAYERS[i])
                        if trader or trading_with:
                            counter += 1
                            self.menuitems['choose_player_to_trade_'+Globals.PLAYERS[i].name] = MenuItem(Globals.PLAYERS[i].name, 'enter_the_trade_menu_'+Globals.PLAYERS[i].name, 'ingame_enter_the_trade_menu_'+Globals.PLAYERS[i].name, counter)
            else:
                Globals.TEMP_VARS['trading']['tradingwith'] = {}
                Globals.TEMP_VARS['trading']['tradingwith']['info'] = find_player_obj_by_name(type[21:])
                self.objects['trade_summary'].init_second()
                self.clear_main_menu_entries(('return'))
                temp_var = Globals.TEMP_VARS['trading']
                counter = 0
                trader = check_if_player_owns_fieldcells(temp_var['trader']['info'].name)
                trading_with = check_if_player_owns_fieldcells(temp_var['tradingwith']['info'].name)
                if trader or trading_with:
                    counter += 1
                    self.menuitems['trading_choose_fields'] = MenuItem(Globals.TRANSLATION[65], 'trading_choose_fields', 'ingame_main', counter)
                for i in range(2):
                    counter += 1
                    operation = ('trading_offer_money', 'trading_ask_for_money')[i]
                    self.menuitems[operation] = MenuItem(Globals.TRANSLATION[(66, 67)[i]], operation, 'ingame_main', counter)
                for key in ('trader', 'tradingwith'):
                    if temp_var[key]['info'].free_jail_cards:
                        counter += 1
                        operation = ('trading_offer_free_jail', 'trading_ask_for_free_jail')[key == 'tradingwith']
                        self.menuitems[operation] = MenuItem(Globals.TRANSLATION[(68, 69)[key == 'tradingwith']] + str(len(temp_var[key]['info'].free_jail_cards)) + ')', operation, 'ingame_main', counter)
            self.cursor.screen_switched(self.menuitems, ('trading_main_menu', 'choose_player_to_trade')[type == 'enter_the_trade_menu'])
        elif type and type[:7] == 'return_':
            self.restore_step_indicators_state()
            self.objects.pop('trade_summary')
            Globals.TEMP_VARS.pop('trading')
            if type == 'return_end_turn':
                self.ask_to_end_turn()
            elif type == 'return_pay_birthday':
                self.pay_birthday_next_player()
            elif type == 'return_new_turn':
                self.new_turn()
            elif type == 'return_player_on_a_new_cell':
                self.disable_central_labels()
                self.labels['dices'] = GameMechanics.show_dices_picture()
                field_num = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field
                self.player_on_a_new_cell(self.objects['gamefield'].cells[field_num])
        elif type and 'pay_birthday' in type:
            self.change_player_money(Globals.TEMP_VARS['pay_birthday'][0], -Globals.TEMP_VARS['MUST_PAY'])
            self.change_player_money(Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']], Globals.TEMP_VARS['MUST_PAY'])
            Globals.TEMP_VARS['pay_birthday'].pop(0)
            self.pay_birthday_next_player()
        elif type == 'stats_switch':
            self.make_stats_screen(self.labels['game_name'].symbols)
        elif type == 'main_settings_language':
            self.labels['APPVERSION'].update_text(Globals.TRANSLATION[4]+Globals.VERSION)
            self.make_settings_screen()
        elif type == 'main_settings_player_color_SELECTOR':
            self.menuitems['name'].text.color = Globals.PLAYERS_COLORS[self.menuitems['color'].selector.active]
            self.menuitems['name'].text.RErender()
        elif type and ('main_new_edit_player' in type or type == 'main_settings_player') and key == 'exit' and not self.labels['name_MI'].symbols:
            if 'error' not in self.labels.keys():
                self.labels.update({'error' : AlphaText(Globals.TRANSLATION[29], 'ERROR_main')})
        elif type == 'main_new_total_SELECTOR':
            old = len(Globals.PLAYERS)
            new = self.menuitems[key].selector.active + 2
            if old != new:
                tempModifier = int(new > old)
                for i in range(old, new, (new-old)/abs(new-old)):
                    dictkey = 'player'+str(i-1+tempModifier)
                    if new < old:
                        self.cursor.add_rm_keys(False, dictkey)
                        self.menuitems.pop(dictkey)
                        if not Globals.PLAYERS[i-1].human:
                            self.labels.pop(dictkey)
                        selector_color = 'grey63'
                    elif new > old:
                        add_new_player(False)
                        self.menuitems.update({dictkey  : MenuItem(Globals.PLAYERS[i].name, 'main_new_edit_player_'+str(i), 'main_new_playerlist', i)})
                        self.labels.update({dictkey     : AlphaText('AI', 'newgame_playertype', i)})
                        self.cursor.add_rm_keys(True, dictkey, len(self.cursor.keys)-2, self.menuitems[dictkey].active_zone.move(0, self.menuitems[dictkey].text.new_pos[1] - self.menuitems[dictkey].text.rect.y).topleft)
                        selector_color = 'white'
                    self.menuitems[key].selector.items[i-2+tempModifier].color = Globals.COLORS[selector_color]
                    self.menuitems[key].selector.items[i-2+tempModifier].RErender()
                if new < old:
                    Globals.PLAYERS = Globals.PLAYERS[:new]
                    self.init_avail_colors_and_names()
                    self.check_error('main_new_game')
                self.menuitems['humans'].selector.add_rm_items(new > old, new)
        elif type == 'main_new_humans_SELECTOR':
            for i in range(1, len(Globals.PLAYERS)):
                dictkey = 'player'+str(i)
                if Globals.PLAYERS[i].human and dictkey in self.labels.keys():
                    self.labels.pop(dictkey)
                elif not Globals.PLAYERS[i].human and dictkey not in self.labels.keys():
                    self.labels.update({dictkey  : AlphaText('AI', 'newgame_playertype', i)})
                    self.labels[dictkey].rect.topleft = self.labels[dictkey].new_pos
        elif type == 'ingame_start_game':
            Globals.GAMELOG_TRANSLATION = read_gamelog_translation()
            self.pics['logo'].pos = (self.pics['logo'].init_pos[0]-1820, self.pics['logo'].init_pos[1])
            self.pics['logo'].change_new_pos((-300, 0))
            for string in ('background', 'logo'):
                self.pics.pop(string)
                self.pics['order'].remove(string)
            for lbl in self.labels.keys():
                if 'money_player' not in lbl:
                    self.labels.pop(lbl)
            self.objects['game_log'] = GameLog()
            self.labels.update({'volume_level'  : AlphaText(Globals.TRANSLATION[41], 'volume_in_game_lbl', 0),
                                'music'         : AlphaText(Globals.TRANSLATION[15], 'volume_in_game_lbl', 1),
                                'sounds'        : AlphaText(Globals.TRANSLATION[42], 'volume_in_game_lbl', 2)})
            self.new_turn()
            self.menuitems.update({'exit'           : MenuItem(u'×', 'main_main', 'from_game_return_to_menu'),
                                   'show_menu'      : MenuItem(u'↓', 'show_menu', 'show_menu'),
                                   'volume_level'   : MenuItem('', 'in_game_volume_SELECTOR', 'volume_in_game'),
                                   'music'          : MenuItem((u'✖', u'✓')[int(Globals.SETTINGS['music'])], 'in_game_music_switch', 'music_and_sound_switches', 0),
                                   'sounds'         : MenuItem((u'✖', u'✓')[int(Globals.SETTINGS['sounds'])], 'in_game_sounds_switch', 'music_and_sound_switches', 1)})
            for cell in self.objects['gamefield'].cells:
                if cell.group in range(1, 9) + ['jail', 'railroad', 'service', 'skip']:
                    self.menuitems['fieldcell_' + str(cell.number)] = MenuItem('', 'onboard_select_cell', 'onboard_select_cell', cell.number)
            clear_TEMP_VARS(('cur_game', 'cur_turn', 'rentlabels'))
            Globals.TEMP_VARS['take_chance_when_player_is_on_chest'] = False
            for player in Globals.PLAYERS:
                player.speed_limit = 5
        elif type == 'show_menu':
            state = int(self.menuitems['show_menu'].text.symbols == u'↓')
            self.menuitems['show_menu'].update_text((u'↓', u'↑')[state])
            if not state:
                state = -1
            objects_to_move = [self.pics['gamebackground'], self.objects['gamefield'], self.objects['game_log']]
            if 'trade_summary' in self.objects.keys():
                objects_to_move += [self.objects['trade_summary']]
            objects_to_move += [cell for cell in self.menuitems.values() if cell.type == 'onboard_select_cell']
            objects_to_move += [cell.step_indicator for cell in self.objects['gamefield'].cells]
            objects_to_move += [self.menuitems[key] for key in ('exit', 'show_menu', 'volume_level', 'music', 'sounds')]
            objects_to_move += [self.labels[key] for key in ('volume_level', 'music', 'sounds')]
            for obj in objects_to_move:
                obj.change_new_pos((0, state*100))
        elif type == 'music_and_sound_switches':
            offset = None
            if not Globals.SETTINGS['music'] and not Globals.SETTINGS['sounds']:
                offset = (0, -33)
            elif self.labels['volume_level'].new_pos[1] < 0:
                offset = (0, 33)
            if offset:
                keys = ('volume_level', 'music', 'sounds')
                for obj in [self.labels[key] for key in keys] + [self.menuitems[key] for key in keys]:
                    obj.change_new_pos(offset)
        elif type == 'main_main' and 'show_menu' in self.menuitems.keys() and self.menuitems['show_menu'].text.symbols == u'↓':
            return None
        elif type and type[:16] == 'ingame_continue_':
            self.ask_to_end_turn()
        elif type:
            self.switch_screen(type, key)
            self.cursor.screen_switched(self.menuitems, type)
    #--- Cleaning and moving
    def clear_labels(self, exception):
        for key in self.labels.keys():
            if key not in exception:
                self.labels.pop(key)
    def clear_main_menu_entries(self, exception=()):
        for key in self.cursor.keys:
            if key not in exception:
                self.menuitems.pop(key)
    def disable_main_menu(self):
        self.clear_main_menu_entries()
        self.cursor = None
    def disable_central_labels(self):
        for key in self.labels.keys():
            if key[:12] in ('dices', 'target_cell_'):
                self.labels.pop(key)
    def disable_step_indicators(self):
        for cell in self.objects['gamefield'].cells:
            cell.step_indicator_visible = False
            cell.step_indicator.alpha = 5
    def save_step_indicators_state(self):
        Globals.TEMP_VARS['save_step_indicators_state'] = [cell.number for cell in self.objects['gamefield'].cells if cell.step_indicator_visible]
        self.disable_step_indicators()
    def move_APPINFO(self, offset):
        for obj in (self.pics['logo'], self.labels['APPNAME'], self.labels['APPVERSION']):
            obj.new_pos = count_new_pos(obj.new_pos, offset)
    #--- Creating specific objects
    def make_stats_screen(self, current):
        self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
        new = 6-Globals.TRANSLATION.index(current)
        data = read_stats(new)
        if data[1]:
            data[1] = str(data[1]) + ' ('+str(round(data[1]*100/data[0], 2))+' %)'
        self.labels.update({'game_name' : AlphaText(Globals.TRANSLATION[5+new], 'stats_game_name'),
                            'total'     : AlphaText(Globals.TRANSLATION[8] + str(data[0]), 'stats_common', 0),
                            'wins'      : AlphaText(Globals.TRANSLATION[9] + str(data[1]), 'stats_common', 1),
                            'profit'    : AlphaText(Globals.TRANSLATION[10] + '$ ' + str(data[2]), 'stats_common', 2),
                            'bestslbl'  : AlphaText(Globals.TRANSLATION[7], 'stats_bests', 3)})
        if data[3]['score']:
            for i in range(3, len(data)):
                if data[i]['score']:
                    self.labels.update({'bestname'+str(i-2)     : AlphaText(str(i-2)+'. '+data[i]['name'], 'stats_table_0', i),
                                        'bestscore'+str(i-2)    : AlphaText('  '*(10-len(str(data[i]['score'])))+str(data[i]['score']), 'stats_table_1', i),
                                        'bestdate'+str(i-2)     : AlphaText(data[i]['date'], 'stats_table_2', i)})
                    if data[i]['recent']:
                        self.labels.update({'bestrecent'        : AlphaText('latest', 'stats_latest', i)})
        else:
            self.labels.update({'message'                       : AlphaText(Globals.TRANSLATION[36], 'stats_table_0', 3)})
        self.objects = {'game_name_UL'  : Line(self.labels['game_name'], 'bottom', 2),
                        'bestslbl_UL'   : Line(self.labels['bestslbl'], 'bottom', 2)}
    def make_settings_screen(self):
        self.menuitems = {'language'    : MenuItem(u'‹ '+Globals.TRANSLATION[60]+u' ›', 'main_settings_language', 'main_settings_left_MI', 0),
                          'player'      : MenuItem(Globals.PLAYERS[0].name, 'main_settings_player', 'main_settings_player', 0),
                          'hotkeys'     : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['hotkeys'])]+u' ›', 'main_settings_hotkeys', 'main_settings_left_MI', 2),
                          'music'       : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['music'])]+u' ›', 'main_settings_music', 'main_settings_left_MI', 3),
                          'sounds'      : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['sounds'])]+u' ›', 'main_settings_sounds', 'main_settings_left_MI', 4),
                          'volume'      : MenuItem('', 'main_settings_volume_SELECTOR', 'main_settings_left_MI', 5),
                          'exit'        : MenuItem(Globals.TRANSLATION[13], 'main_main', 'main_settings_exit')}
        self.labels.update({'language'  : AlphaText(Globals.TRANSLATION[14], 'settings_left', 0),
                            'player'    : AlphaText(Globals.TRANSLATION[20], 'settings_left', 1),
                            'hotkeys'   : AlphaText(Globals.TRANSLATION[25], 'settings_left', 2),
                            'music'     : AlphaText(Globals.TRANSLATION[15], 'settings_left', 3),
                            'sounds'    : AlphaText(Globals.TRANSLATION[16], 'settings_left', 4),
                            'volume'    : AlphaText(Globals.TRANSLATION[19], 'settings_left', 5)})
        if not Globals.SETTINGS['block']:
            self.menuitems.update({'fav_game'   : MenuItem(u'‹ '+Globals.TRANSLATION[5+int(Globals.SETTINGS['fav_game'])]+u' ›', 'main_settings_fav_game', 'main_settings_left_MI', 6)})
            self.labels.update({'fav_game'      : AlphaText(Globals.TRANSLATION[26], 'settings_left', 6)})
    def make_obj_for_enter_name(self):
        self.objects = {'text_cursor'   : Line(self.labels['name_MI'], 'right', 2, Globals.COLORS['white'])}
    def make_playersettings_screen(self):
        self.menuitems = {'name'        : MenuItem(Globals.PLAYERS[Globals.TEMP_VARS['edit_player']].name, 'main_settings_player_name', 'main_settings_player', 0),
                          'color'       : MenuItem('', 'main_settings_player_color_SELECTOR', 'main_settings_left_MI', 2)}
        self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
        self.labels.update({'name'      : AlphaText(Globals.TRANSLATION[22], 'settings_left', 1),
                            'color'     : AlphaText(Globals.TRANSLATION[23], 'settings_left', 2)})
    def init_avail_colors_and_names(self):
        Globals.TEMP_VARS['avail_colors'] = list(Globals.PLAYERS_COLORS)
        Globals.TEMP_VARS['avail_names'] = read_file(Globals.DIRS['translations'] + Globals.SETTINGS['language'] + '/names')
        for player in Globals.PLAYERS:
            if player.color in Globals.TEMP_VARS['avail_colors']:
                Globals.TEMP_VARS['avail_colors'].remove(player.color)
            if player.name in Globals.TEMP_VARS['avail_names']:
                Globals.TEMP_VARS['avail_names'].remove(player.name)
    def show_special_cell_info(self, cell):
        if cell.group in ('tax', 'income'):
            text = Globals.TRANSLATION[50 + 9*(cell.group == 'income')] + str(cell.buy_cost)[(cell.group == 'tax'):]
            Globals.TEMP_VARS['MUST_PAY'] = cell.buy_cost
        elif cell.group in ('chest', 'chance'):
            if Globals.TEMP_VARS['take_chance_when_player_is_on_chest']:
                group = 'chances'
            else:
                group = cell.group + 's'
            text = self.objects['gamefield'].chests_and_chances[group][0].text
        elif cell.group == 'jail':
            text = Globals.TRANSLATION[51]
            self.menuitems['fieldcell_10'].tooltip.RErender()
        else:
            return None
        self.labels['target_cell_owner'] = AlphaText(text, 'target_cell_owner', 1)
    def show_step_indicator_under_player(self):
        self.disable_step_indicators()
        player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
        cell = self.objects['gamefield'].cells[player.cur_field]
        cell.step_indicator.change_color(player.color)
        cell.step_indicator_visible = True
    def restore_step_indicators_state(self):
        self.disable_step_indicators()
        for i in Globals.TEMP_VARS['save_step_indicators_state']:
            self.objects['gamefield'].cells[i].step_indicator_visible = True
        Globals.TEMP_VARS.pop('save_step_indicators_state')
    def show_property_management_menuitems(self, number, condition=True):
        if condition:
            trader_name = self.trader_for_cur_player_or_for_birthday()
            if check_if_anybody_can_trade():
                if len(Globals.PLAYERS) == 2:
                    type = 'enter_the_trade_menu_' + find_player_obj_by_name(trader_name, True).name
                else:
                    type = 'enter_the_trade_menu'
                self.menuitems['trade'] = MenuItem(Globals.TRANSLATION[44], type, 'ingame_main', number)
            if check_if_player_owns_fieldcells(trader_name):
                self.menuitems['manage_property'] = MenuItem(Globals.TRANSLATION[62], 'enter_the_property_management', 'ingame_main', number+1)
    #--- Various verifications
    def check_error(self, type):
        if type == 'main_new_game':
            status = self.check_doubles_for_players()
            if status and 'error' not in self.labels.keys():
                self.labels.update({'error' : AlphaText(Globals.TRANSLATION[32], 'ERROR_main')})
                self.menuitems['start'].text.color = Globals.COLORS['grey63']
                self.menuitems['start'].text.RErender()
            elif not status and 'error' in self.labels.keys():
                self.labels.pop('error')
                self.menuitems['start'].text.color = Globals.COLORS['white']
                self.menuitems['start'].text.RErender()
    def check_doubles_for_players(self):
        for i in range(len(Globals.PLAYERS)-1):
            for j in range(i+1, len(Globals.PLAYERS)):
                if Globals.PLAYERS[i].color == Globals.PLAYERS[j].color or Globals.PLAYERS[i].name == Globals.PLAYERS[j].name:
                    return True
    def check_group_owners(self, group, player):
        data = []
        counter = 0
        for cell in self.objects['gamefield'].cells:
            if cell.group == group:
                counter += 1
                if cell.owner == player:
                    data.append(cell)
        self.objects['gamefield'].groups_monopolies[group] = counter == len(data)
        return data
    def trader_for_cur_player_or_for_birthday(self):
        if 'pay_birthday' in Globals.TEMP_VARS:
            return Globals.TEMP_VARS['pay_birthday'][0]
        else:
            return Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
    #--- Game mechanics
    def ask_to_end_turn(self):
        self.disable_central_labels()
        player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
        if Globals.TEMP_VARS['dice1'] != Globals.TEMP_VARS['dice2'] or player.exit_jail_attempts != None:
            if player.cur_field != 10:
                player.exit_jail_attempts = None
            self.show_step_indicator_under_player()
            self.clear_main_menu_entries()
            self.menuitems['end_turn'] = MenuItem(Globals.TRANSLATION[61], 'ingame_end_turn', 'ingame_main', 0)
            self.show_property_management_menuitems(1)
            self.cursor.screen_switched(self.menuitems, 'ingame_end_turn')
        else:
            self.new_turn()
    def change_player(self):
        GameMechanics.change_player()
        self.objects['cur_turn_highlighter'].move()
        self.objects['game_log'].add_message('change_player')
        self.new_turn()
    def new_turn(self):
        # self.DEBUGGER_show_TEMP_VARS_keys()
        self.disable_central_labels()
        self.show_step_indicator_under_player()
        player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
        if player.human:
            if self.cursor:
                self.clear_main_menu_entries()
            if player.cur_field == 10 and player.exit_jail_attempts != None:
                self.menuitems['pay_money_to_exit_jail'] = MenuItem(Globals.TRANSLATION[55]+str(self.objects['gamefield'].cells[10].buy_cost), 'pay_money_to_exit_jail', 'ingame_main', int(player.exit_jail_attempts > 0))
                if player.exit_jail_attempts:
                    self.menuitems['roll_the_dice'] = MenuItem(Globals.TRANSLATION[43]+' ('+str(player.exit_jail_attempts)+')', 'roll_the_dice_to_exit_jail', 'ingame_main', 0)
                if player.free_jail_cards:
                    self.menuitems['use_card_to_exit_jail'] = MenuItem(Globals.TRANSLATION[57]+' ('+str(len(player.free_jail_cards))+')', 'use_card_to_exit_jail', 'ingame_main', 1+int(player.exit_jail_attempts > 0))
            else:
                self.menuitems['roll_the_dice'] = MenuItem(Globals.TRANSLATION[43], 'roll_the_dice', 'ingame_main', 0)
            number = len([key for key in ('pay_money_to_exit_jail', 'roll_the_dice', 'use_card_to_exit_jail') if key in self.menuitems.keys()])
            self.show_property_management_menuitems(number)
            if self.cursor:
                self.cursor.screen_switched(self.menuitems, 'ingame_main')
            else:
                self.cursor = MainCursor(self.menuitems, 'ingame_main')
        elif self.cursor:
            self.disable_main_menu()
    def player_on_a_new_cell(self, cell):
        self.DEBUGGER_chests_and_chances()
        self.clear_main_menu_entries()
        if cell.NAME:
            self.labels['target_cell_name'] = AlphaText(cell.NAME, 'target_cell_name', 0)
        if cell.group in ('jail', 'skip', 'gotojail', 'start', 'income', 'tax', 'chest', 'chance'):
            self.show_special_cell_info(cell)
            group = (cell.group, 'chance')[Globals.TEMP_VARS['take_chance_when_player_is_on_chest']]
            if group in ('chest', 'chance') and self.objects['gamefield'].chests_and_chances[group + 's'][0].type == 'goto_jail':
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49], 'ingame_continue_gotojail', 'ingame_main', 5)
                obj = self.objects['gamefield'].chests_and_chances[group + 's']
                obj.append(obj.pop(0))
            else:
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49], 'ingame_continue_'+group, 'ingame_main', 5)
            property_management_number = 6
            if cell.group in ('chest', 'chance'):
                obj = self.objects['gamefield'].chests_and_chances[cell.group + 's'][0]
                property_management_condition = (obj.type == 'income' and obj.modifier[0] < 0) or obj.type == 'pay_each'
            else:
                property_management_condition = cell.group == 'tax'
            Globals.TEMP_VARS['take_chance_when_player_is_on_chest'] = False
        else:
            if cell.owner:
                text = Globals.TRANSLATION[45] + cell.owner
                if cell.owner == Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].name:
                    type = 'ingame_continue_NO'
                else:
                    type = 'ingame_continue_PAY_RENT'
                    if cell.group == 'service':
                        if cell.step_indicator_visible:
                            state = int(cell.rent_costs[cell.buildings][1:])
                        else:
                            state = 10
                        Globals.TEMP_VARS['MUST_PAY'] = (Globals.TEMP_VARS['dice1'] + Globals.TEMP_VARS['dice2']) * state
                    else:
                        Globals.TEMP_VARS['MUST_PAY'] = cell.rent_costs[cell.buildings]
                        if (not cell.buildings and self.objects['gamefield'].groups_monopolies[cell.group]) or (cell.group == 'railroad' and not cell.step_indicator_visible):
                            Globals.TEMP_VARS['MUST_PAY'] = Globals.TEMP_VARS['MUST_PAY'] * 2
                    self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[50] + str(Globals.TEMP_VARS['MUST_PAY']), 'target_cell_info', 2)
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49], type, 'ingame_main', 6)
            else:
                text = Globals.TRANSLATION[45] + Globals.TRANSLATION[46]
                Globals.TEMP_VARS['MUST_PAY'] = cell.buy_cost
                self.menuitems.update({'buy_a_cell'         : MenuItem(Globals.TRANSLATION[47] + str(cell.buy_cost)+')', 'ingame_buy_a_cell', 'ingame_main', 5),
                                       'cell_to_an_auction' : MenuItem(Globals.TRANSLATION[48], 'ingame_cell_to_an_auction', 'ingame_main', 6)})
            property_management_number = 7
            property_management_condition = not(cell.owner == Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].name)
            self.labels['target_cell_owner'] = AlphaText(text, 'target_cell_owner', 1)
        self.show_property_management_menuitems(property_management_number, property_management_condition)
        self.cursor.screen_switched(self.menuitems, ('ingame_buy_or_auction', 'ingame_continue')['ingame_continue' in self.menuitems.keys()])
    def change_owner_for_a_cell(self, player):
        cell = self.objects['gamefield'].cells[player.cur_field]
        cell.owner = player.name
        cell.color = player.color
        cells = self.check_group_owners(cell.group, player.name)
        for group_cell in cells:
            if group_cell.group in ('service', 'railroad'):
                group_cell.buildings = len(cells) - 1
            self.objects['gamefield'].RErender_a_cell(group_cell.number)
            self.menuitems['fieldcell_'+str(group_cell.number)].tooltip.RErender(group_cell.buildings+1)
    def change_player_money(self, player, money):
        player.money += money
        self.labels['money_player_'+player.name].update_text(str(player.money))
    def pay_birthday_next_player(self):
        if Globals.TEMP_VARS['pay_birthday']:
            player_name = Globals.TEMP_VARS['pay_birthday'][0].name
            text = Globals.TRANSLATION[58].replace('%', player_name)
            text = text.replace('^', str(Globals.TEMP_VARS['MUST_PAY']))
            text = text.replace('@', Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].name)
            if 'return' in self.menuitems.keys():
                self.labels['target_cell_info'].change_new_pos((0, 80))
            else:
                self.labels['target_cell_info'] = AlphaText(text, 'birthday_info')
            self.clear_main_menu_entries()
            self.menuitems.update({'roll_the_dice'  : MenuItem(Globals.TRANSLATION[55]+str(Globals.TEMP_VARS['MUST_PAY']), 'pay_birthday_'+player_name, 'ingame_main', 3)})
            self.show_property_management_menuitems(4)
            self.cursor.screen_switched(self.menuitems, 'ingame_main')
        else:
            Globals.TEMP_VARS.pop('pay_birthday')
            self.objects['game_log'].add_message('birthday')
            self.ask_to_end_turn()
    #--- DEBUGGING
    def DEBUGGER_chests_and_chances(self):
        DEBUG = self.objects['gamefield'].chests_and_chances
        print('')
        for i in range(14, -1, -1):
            DEBUG_OUTPUT = ''
            for DEBUG_TYPE in ('chests', 'chances'):
                DEBUG_OUTPUT += DEBUG[DEBUG_TYPE][i].type
                DEBUG_OUTPUT += ' ' * (15-len(DEBUG[DEBUG_TYPE][i].type))
                if DEBUG[DEBUG_TYPE][i].modifier:
                    DEBUG_OUTPUT += str(DEBUG[DEBUG_TYPE][i].modifier[0])
                    DEBUG_OUTPUT += ' '*(8-len(str(DEBUG[DEBUG_TYPE][i].modifier[0])))
                else:
                    DEBUG_OUTPUT += 'NONE    '
                DEBUG_OUTPUT += '|   '
            DEBUG_OUTPUT += ('NEXT', str(i))[bool(i)]
            print(DEBUG_OUTPUT)
        print('---------------------------------------------------')
        print('CHESTS                     CHANCES')
    def DEBUGGER_show_TEMP_VARS_keys(self):
        for key in Globals.TEMP_VARS.keys():
            print(key)
        print('')
