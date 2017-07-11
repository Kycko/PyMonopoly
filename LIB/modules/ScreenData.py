# -*- coding: utf-8 -*-
import FieldCellsData, GameMechanics, Globals, pygame, random
from GameObjects import GameField, GameLog, PropManageSummary, TradeSummary
from GlobalFuncs import *
from MenuItems import AuctionPlayerHighlighter, CurTurnHighlighter, MainCursor, MenuItem
from Sprite import *
from TransparentText import AlphaText
from sys import exit as SYSEXIT

class MainScreen():
    #--- Common
    def __init__(self):
        self.switch_screen('main_main', None)
    def switch_screen(self, type, key):
        # self.DEBUGGER_show_TEMP_VARS_keys()
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
                               'authors'    : AlphaText('Anthony Samartsev & Michael Mozhaev, 2014-2017', 'authors', 1)}
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
                                        'authors'    : AlphaText('Anthony Samartsev & Michael Mozhaev, 2014-2016', 'authors', 1)})
                    for key in ('authors', 'resources'):
                        self.labels[key].rect.x -= 1820
                    for key in ('APPNAME', 'APPVERSION'):
                        self.labels[key].change_new_pos((1820, 0))
                    for cell in self.objects['gamefield'].cells:
                        cell.step_indicator.change_new_pos((1820, 0))
                        cell.a_little_number.change_new_pos((1820, 0))
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
            self.make_obj_for_enter_name('name_MI')
        elif type == 'main_new_game':
            self.init_avail_colors_and_names()
            if key == 'exit':
                Globals.TEMP_VARS.pop('edit_player')
                self.clear_labels(('APPNAME', 'APPVERSION', 'resources', 'authors'))
            else:
                self.move_APPINFO((300, 0))
                Globals.TEMP_VARS['cur_game'] = Globals.SETTINGS['fav_game']
                Globals.TEMP_VARS['build_style'] = Globals.SETTINGS['build_style']
                LGS = read_file(Globals.FILES['last_game_settings'])
                for string in LGS:
                    add_new_player(string == 'human')
            self.menuitems = {'uniform_build'   : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.TEMP_VARS['build_style'])]+u' ›', 'main_new_uniform_build', 'main_settings_left_MI', 0),
                              'total'           : MenuItem('', 'main_new_total_SELECTOR', 'main_settings_left_MI', 1),
                              'humans'          : MenuItem('', 'main_new_humans_SELECTOR', 'main_settings_left_MI', 2),
                              'start'           : MenuItem(Globals.TRANSLATION[33], 'game_start', 'main_settings_player_exit', 1),
                              'exit'            : MenuItem(Globals.TRANSLATION[11], 'main_main', 'main_settings_player_exit')}
            self.labels.update({'uniform_build' : AlphaText(Globals.TRANSLATION[98], 'settings_left', 0),
                                'total'         : AlphaText(Globals.TRANSLATION[28], 'settings_left', 1),
                                'inactive_MI'   : AlphaText(u'●', 'main_new_total_SELECTOR', 0),
                                'humans'        : AlphaText(Globals.TRANSLATION[30], 'settings_left', 2),
                                'players'       : AlphaText(Globals.TRANSLATION[31], 'settings_left', 3)})
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
            Globals.TEMP_VARS['bank_property'] = ([32, 12], [26, 12])[Globals.TEMP_VARS['cur_game']]
            self.menuitems = {'start_game'      : MenuItem(Globals.TRANSLATION[34], 'ingame_start_game', 'ingame_start', 0),
                              'exit'            : MenuItem(Globals.TRANSLATION[35], 'main_main', 'ingame_start', 1)}
            self.objects = {'gamefield' : GameField()}
            for i in range(len(Globals.PLAYERS)):
                Globals.PLAYERS[i].initialize_coords(i)
                Globals.PLAYERS[i].money = (1500, 20000)[Globals.TEMP_VARS['cur_game']]
                self.menuitems.update({'player_'+Globals.PLAYERS[i].name    : MenuItem(u'●', 'pl_info_tab_'+Globals.PLAYERS[i].name, 'pl_info_tab', i)})
                self.labels.update({'money_player_'+Globals.PLAYERS[i].name : AlphaText(str(Globals.PLAYERS[i].money), 'pl_money_info', i)})
            self.labels.update({'bank_property1'    : AlphaText(Globals.TRANSLATION[104], 'bank_property1'),
                                'bank_property2'    : AlphaText(u'●', 'bank_property2'),
                                'bank_property3'    : AlphaText(str(Globals.TEMP_VARS['bank_property'][0]), 'bank_property3'),
                                'bank_property4'    : AlphaText(u'❖', 'bank_property4'),
                                'bank_property5'    : AlphaText(str(Globals.TEMP_VARS['bank_property'][1]), 'bank_property5')})
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
                    self.input_handling(e, 'name_MI', 15)
                elif self.labels and 'property_management_input' in self.labels.keys():
                    self.input_handling(e, 'property_management_input', 2)
                elif self.labels and check_substring_in_dict_keys(self.labels, 'trading_input'):
                    label_key = check_substring_in_dict_keys(self.labels, 'trading_input')
                    if label_key == 'trading_input_fields':
                        max_length = 2
                    elif label_key == 'trading_input_auction_bet':
                        max_length = len(str(Globals.TEMP_VARS['auction']['order'][0].money))
                    else:
                        trader = ('trader', 'tradingwith')['ask_for' in label_key]
                        max_length = len(str(Globals.TEMP_VARS['trading'][trader]['info'].money))
                    self.input_handling(e, label_key, max_length)
                elif self.cursor and e.key in self.menuitems[self.cursor.active_key].HOTKEYS:
                    self.action_call(self.cursor.active_key)
                else:
                    for key in self.menuitems.keys():
                        if self.menuitems[key].type[:4] != 'main' and e.key in self.menuitems[key].HOTKEYS:
                            self.action_call(key)
            elif e.type == pygame.QUIT:
                SYSEXIT()
    def input_handling(self, e, KEY, max_length):
        if e.key == pygame.K_BACKSPACE:
            self.labels[KEY].update_text(self.labels[KEY].symbols[:len(self.labels[KEY].symbols)-1], False)
        elif len(self.labels[KEY].symbols) < max_length and (KEY == 'name_MI' or e.unicode in ''.join([str(i) for i in range(10)])):
            self.labels[KEY].update_text(self.labels[KEY].symbols + e.unicode, False)
        if 'property_management_input' in self.labels.keys() or check_substring_in_dict_keys(self.labels, 'trading_input'):
            self.create_trading_input_spec_objects(KEY)
        self.make_obj_for_enter_name(KEY)
    #--- Menu actions
    def action_call(self, key):
        # self.DEBUGGER_show_TEMP_VARS_keys()
        if Globals.TRANSLATION[100] in self.menuitems[key].text.symbols and ((key == 'ingame_continue') or (key == 'roll_the_dice' and 'pay_birthday' in self.menuitems['roll_the_dice'].type)):
            CELLS = self.objects['gamefield'].cells
            CUR = check_cur_prop_management()
            self.objects['game_log'].add_message('bankrupt_player')
            self.objects['cur_turn_highlighter'].rm_player(CUR.name)
            MON = 0
            Globals.TEMP_VARS['bankruptcy_fields_changing'] = []
            for cell in CELLS:
                if cell.owner == CUR.name:
                    Globals.TEMP_VARS['bankruptcy_fields_changing'].append(cell.number)
                    if cell.buildings > 0 and cell.group not in ('railroad', 'service'):
                        MON += cell.buildings * cell.build_cost / 2
                        Globals.TEMP_VARS['bank_property'][0] += cell.buildings
                        if cell.buildings == 5 - Globals.TEMP_VARS['cur_game']:
                            Globals.TEMP_VARS['bank_property'][0] -= 1
                            Globals.TEMP_VARS['bank_property'][1] += 1
                        cell.buildings = 0
            self.upd_bank_property_lbl()
            self.change_player_money(CUR, MON)
            if self.menuitems[key].type == 'ingame_continue_PAY_RENT' or 'pay_birthday' in self.menuitems[key].type:
                if self.menuitems[key].type == 'ingame_continue_PAY_RENT':
                    for i in range(len(Globals.PLAYERS)):
                        if Globals.PLAYERS[i].name == CELLS[CUR.cur_field].owner:
                            Globals.TEMP_VARS['bankruptcy_RECIPIENT'] = Globals.PLAYERS[i]
                else:
                    Globals.TEMP_VARS['bankruptcy_RECIPIENT'] = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
                self.change_player_money(Globals.TEMP_VARS['bankruptcy_RECIPIENT'], CUR.money)
                if CUR.free_jail_cards:
                    for i in range(len(CUR.free_jail_cards)):
                        Globals.TEMP_VARS['bankruptcy_RECIPIENT'].free_jail_cards.append(CUR.free_jail_cards.pop(0))
            else:
                if CUR.free_jail_cards:
                    for i in range(len(CUR.free_jail_cards)):
                        vid = CUR.free_jail_cards.pop(0)
                        self.objects['gamefield'].chests_and_chances[vid+'s'].append(Globals.TEMP_VARS['free_jail_obj'])
            self.menuitems['fieldcell_10'].tooltip.RErender()
            rm_player(CUR.name)
            self.menuitems['player_' + CUR.name].update_text(u'✖')
            self.labels['money_player_' + CUR.name].update_text('game over')
            type = self.menuitems[key].type
            if type in ('ingame_continue_chest', 'ingame_continue_chance'):
                obj = self.objects['gamefield'].chests_and_chances[type[16:] + 's']
                obj.append(obj.pop(0))
            elif 'pay_birthday' in type:
                Globals.TEMP_VARS['pay_birthday'].pop(0)
            temp_var = Globals.TEMP_VARS['bankruptcy_fields_changing']
            if temp_var and 'bankruptcy_RECIPIENT' in Globals.TEMP_VARS.keys():
                Globals.TEMP_VARS['RErender_groups'] = []
                del_list = []
                for field in temp_var:
                    cell = self.objects['gamefield'].cells[field]
                    if not cell.buildings or (cell.group in ('railroad', 'service') and cell.buildings != -1):
                        del_list.append(field)
                        self.change_owner_for_a_cell(Globals.TEMP_VARS['bankruptcy_RECIPIENT'], cell)
                        Globals.TEMP_VARS['RErender_groups'].append(cell.group)
                for field in del_list:
                    temp_var.remove(field)
                if Globals.TEMP_VARS['RErender_groups']:
                    self.objects['gamefield'].RErender_fieldcell_groups()
                else:
                    Globals.TEMP_VARS.pop('RErender_groups')
                self.bankruptcy_fields_buyout(key)
            else:
                self.disable_central_labels()
                self.disable_step_indicators()
                self.next_bankruptcy_field()
            # for player in Globals.PLAYERS:
            #     print(player.name)
            # print('')
        elif not self.error_msg_money_limits(key):
            type = self.menuitems[key].action(key)
            if type in ('roll_the_dice', 'roll_the_dice_to_exit_jail'):
                self.labels['dices'] = GameMechanics.roll_the_dice()
                player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
                points = Globals.TEMP_VARS['dice1'] + Globals.TEMP_VARS['dice2']
                if type == 'roll_the_dice_to_exit_jail' and Globals.TEMP_VARS['dice1'] != Globals.TEMP_VARS['dice2']:
                    if 'error' in self.labels.keys():
                        self.labels.pop('error')
                    self.clear_main_menu_entries()
                    player.exit_jail_attempts -= 1
                    self.objects['game_log'].add_message('roll_the_dice_to_exit_jail')
                    self.labels['target_cell_owner'] = AlphaText(Globals.TRANSLATION[54] + str(player.exit_jail_attempts), 'target_cell_owner', 1)
                    self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49], 'ingame_continue_doesnt_exit_jail', 'ingame_main', 5)
                    self.cursor.screen_switched(self.menuitems, 'ingame_continue')
                    self.menuitems['fieldcell_10'].tooltip.RErender()
                else:
                    if Globals.TEMP_VARS['dice1'] == Globals.TEMP_VARS['dice2']:
                        Globals.TEMP_VARS['double_dices_count'] += 1
                    if Globals.TEMP_VARS['double_dices_count'] == 3:
                        self.player_on_a_new_cell(self.objects['gamefield'].cells[30])
                    else:
                        for i in range(player.cur_field + 1, player.cur_field + points + 1):
                            self.objects['gamefield'].cells[i-40].step_indicator.change_color(player.color)
                            self.objects['gamefield'].cells[i-40].step_indicator_visible = True
                        player.move_forward(points)
                        if player.cur_field - points == 10:
                            self.menuitems['fieldcell_10'].tooltip.RErender()
                        self.player_on_a_new_cell(self.objects['gamefield'].cells[player.cur_field])
                        self.objects['game_log'].add_message('roll_the_dice')
            elif type == 'ingame_end_turn':
                player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
                if player.cur_field != 10:
                    player.exit_jail_attempts = None
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
                self.menuitems['fieldcell_10'].tooltip.RErender()
                self.objects['game_log'].add_message(type)
                self.new_turn()
            elif type == 'ingame_buy_a_cell':
                player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
                self.change_owner_for_a_cell(player)
                self.change_player_money(player, -Globals.TEMP_VARS['MUST_PAY'])
                self.objects['game_log'].add_message(type)
                self.ask_to_end_turn()
            elif type == 'ingame_cell_to_an_auction':
                self.show_or_rm_error_msg(False, 99, 'ERROR_ingame', 'accept')
                self.save_step_indicators_state()
                self.clear_main_menu_entries()
                self.disable_central_labels()
                self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[81], 'target_cell_info')
                self.menuitems['ingame_push_to_auction_accept'] = MenuItem(Globals.TRANSLATION[82], 'ingame_push_to_auction_accept', 'ingame_main', 4)
                self.menuitems['return'] = MenuItem(Globals.TRANSLATION[64], 'return_player_on_a_new_cell', 'ingame_main', 5)
                self.cursor.screen_switched(self.menuitems, 'ingame_push_to_auction')
            elif type == 'ingame_push_to_auction_accept':
                if Globals.TEMP_VARS['cur_turn'] == len(Globals.PLAYERS)-1:
                    temp_range = range(len(Globals.PLAYERS))
                elif Globals.TEMP_VARS['cur_turn']:
                    temp_range = range(Globals.TEMP_VARS['cur_turn']+1, len(Globals.PLAYERS)) + range(Globals.TEMP_VARS['cur_turn']+1)
                else:
                    temp_range = range(Globals.TEMP_VARS['cur_turn']+1, len(Globals.PLAYERS)) + [0]
                field = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field
                Globals.TEMP_VARS['auction'] = {'bet'       : 0,
                                                'field'     : self.objects['gamefield'].cells[field],
                                                'order'     : [Globals.PLAYERS[i] for i in temp_range],
                                                'player'    : None}
                Globals.TEMP_VARS['auction']['field'].step_indicator.change_color(Globals.COLORS['white'])
                Globals.TEMP_VARS['auction']['field'].step_indicator_visible = True
                self.auction_next_player()
            elif type in ('ingame_continue_tax', 'ingame_continue_income'):
                self.objects['game_log'].add_message(type)
                self.change_player_money(Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']], Globals.TEMP_VARS['MUST_PAY'])
                self.ask_to_end_turn()
            elif type == 'ingame_continue_PAY_RENT':
                if 'double_rails' in Globals.TEMP_VARS.keys():
                    Globals.TEMP_VARS.pop('double_rails')
                cur_turn = Globals.TEMP_VARS['cur_turn']
                player = Globals.PLAYERS[cur_turn]
                cell = self.objects['gamefield'].cells[player.cur_field]
                self.change_player_money(player, -Globals.TEMP_VARS['MUST_PAY'])
                if 'cur_field_owner' in Globals.TEMP_VARS.keys():
                    Globals.TEMP_VARS['xxx'] = cell.owner
                    cell.owner = Globals.TEMP_VARS.pop('cur_field_owner')
                for i in range(len(Globals.PLAYERS)):
                    if Globals.PLAYERS[i].name == cell.owner:
                        self.change_player_money(Globals.PLAYERS[i], Globals.TEMP_VARS['MUST_PAY'])
                if 'xxx' in Globals.TEMP_VARS.keys():
                    cell.owner = Globals.TEMP_VARS.pop('xxx')
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
                    if Globals.TEMP_VARS['repair_cost_SAVE']:
                        Globals.TEMP_VARS['MUST_PAY'] = - Globals.TEMP_VARS.pop('repair_cost_SAVE')
                        self.change_player_money(player, Globals.TEMP_VARS['MUST_PAY'])
                        self.objects['game_log'].add_message('chest_income')
                    else:
                        Globals.TEMP_VARS.pop('repair_cost_SAVE')
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
            elif type == 'enter_the_property_management':
                Globals.TEMP_VARS['bank_property_back'] = [Globals.TEMP_VARS['bank_property'][i] for i in range(2)]
                self.show_or_rm_error_msg(False, 99, 'ERROR_ingame', 'accept')
                if 'prev_trade' in self.labels.keys():
                    self.labels.pop('prev_trade')
                if 'trade_summary' in self.objects.keys():
                    self.objects.pop('trade_summary')
                if 'pay_birthday' not in Globals.TEMP_VARS.keys():
                    self.disable_central_labels()
                Globals.TEMP_VARS['property'] = {}
                player = check_cur_prop_management()
                for cell in self.objects['gamefield'].cells:
                    if cell.owner == player.name:
                        Globals.TEMP_VARS['property'][cell.number] = cell.buildings
                Globals.TEMP_VARS['prop_manage_CHANGED'] = {'TOTAL' : 0}
                self.objects['prop_manage_summary'] = PropManageSummary()
                self.entering_property_menu()
                self.clear_main_menu_entries(('return'))
                self.objects['gamefield'].render_cell_numbers('prop_manage')
                self.labels['target_cell_trading_info'] = AlphaText(Globals.TRANSLATION[69], 'target_cell_info', -3)
                self.labels['property_management_input'] = AlphaText('', 'ingame_main', 1)
                self.make_obj_for_enter_name('property_management_input')
                self.cursor.screen_switched(self.menuitems, 'property_management')
            elif type == 'property_management_input_ACCEPT' and self.menuitems['accept'].text.color == Globals.COLORS['white']:
                num = int(self.labels['property_management_input'].symbols)
                self.create_prop_management_cell_state_objects(self.objects['gamefield'].cells[num])
            elif type == 'prop_management_ACCEPT_ALL':
                temp_var = Globals.TEMP_VARS['prop_manage_CHANGED']
                house_count = 0
                for key in temp_var.keys():
                    if key != 'TOTAL':
                        house_count += temp_var[key][3]
                bank_prop_fault = False
                for i in range(2):
                    if Globals.TEMP_VARS['bank_property'][i] < 0:
                        bank_prop_fault = True
                curplayer = check_cur_prop_management()
                if house_count + curplayer.build_ability > 3:
                    self.show_or_rm_error_msg(True, 103, 'ERROR_ingame', 'accept_all_prop_management')
                elif bank_prop_fault:
                    self.show_or_rm_error_msg(True, 105, 'ERROR_ingame', 'accept_all_prop_management')
                else:
                    curplayer.build_ability += house_count
                    for i in range(1, 40):
                        if i in temp_var.keys():
                            if temp_var[i][0] < 0 or temp_var[i][1] < 0:
                                self.objects['game_log'].add_message('prop_manage_mortrage_'+str(i))
                            if self.objects['gamefield'].cells[i].group not in ('railroad', 'service'):
                                if temp_var[i][1] > temp_var[i][0] and temp_var[i][1] > 0:
                                    self.objects['game_log'].add_message('prop_manage_build_'+str(i))
                                elif temp_var[i][0] > temp_var[i][1] and temp_var[i][0] > 0:
                                    self.objects['game_log'].add_message('prop_manage_debuild_'+str(i))
                    for cell in self.objects['gamefield'].cells:
                        cell.a_little_number_visible = False
                    temp = check_substring_in_dict_keys(self.labels, 'property_management_input')
                    if temp: self.labels.pop(temp)
                    for key in ('property_management_input',
                                'property_management_input_ready',
                                'target_cell_trading_info',
                                'target_cell_trading_subinfo'):
                        if key in self.labels.keys():
                            self.labels.pop(key)
                    self.change_player_money(check_cur_prop_management(), temp_var['TOTAL'])
                    if 'prop_manage_summary' in self.objects.keys():
                        self.objects.pop('prop_manage_summary')
                    if 'bank_property_back' in Globals.TEMP_VARS.keys():
                        Globals.TEMP_VARS.pop('bank_property_back')
                    self.return_to_game_from_trading(self.menuitems['return'].type)
            elif type == 'cell_state_SELECTOR':
                CELL = int(self.labels['property_management_input_ready'].symbols)
                cell_obj = self.objects['gamefield'].cells[CELL]
                old_buildings = cell_obj.buildings
                new_buildings = self.menuitems[key].selector.active - 1
                if old_buildings != new_buildings:
                    Globals.TEMP_VARS['RErender_groups'] = [cell_obj.group]
                    cell_obj.buildings = new_buildings
                    TEMP = [cell_obj.number]            # cell numbers to RErender
                    if Globals.TEMP_VARS['build_style']:
                        for cell in self.objects['gamefield'].cells:
                            if cell.group not in ('railroad', 'service') and cell.group in Globals.TEMP_VARS['RErender_groups'] and cell.number != cell_obj.number:
                                while cell.buildings not in range(new_buildings-1, new_buildings+2):
                                    cell.buildings += 1 - 2*int(new_buildings < old_buildings)
                                    TEMP.append(cell.number)
                    for i in TEMP:
                        self.menuitems['fieldcell_'+str(i)].tooltip.RErender(self.objects['gamefield'].cells[i].buildings+1)
                    self.objects['gamefield'].RErender_fieldcell_groups()
                    self.recheck_prop_management_money_changes()
                self.return_into_prop_manage_choose_field()
            elif type and 'enter_the_trade_menu' in type:
                self.show_or_rm_error_msg(False, 99, 'ERROR_ingame', 'accept')
                if 'prev_trade' in self.labels.keys():
                    self.labels.pop('prev_trade')
                if 'cur_field_owner' not in Globals.TEMP_VARS.keys() and 'ingame_bankruptcy_10' not in self.menuitems.keys():
                    Globals.TEMP_VARS['cur_field_owner'] = self.objects['gamefield'].cells[Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field].owner
                if 'pay_birthday' not in Globals.TEMP_VARS.keys():
                    self.disable_central_labels()
                if type == 'enter_the_trade_menu' or len(Globals.PLAYERS) == 2:
                    self.entering_property_menu()
                    Globals.TEMP_VARS['trading'] = {}
                    self.make_trading_TEMP_VARS('trader')
                    self.objects['trade_summary'] = TradeSummary()
                if type == 'enter_the_trade_menu':
                    if 'pay_birthday' not in Globals.TEMP_VARS.keys():
                        self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[63], 'target_cell_info', -3)
                    self.clear_main_menu_entries(('return'))
                    temp_var = Globals.TEMP_VARS['trading']['trader']
                    counter = 0
                    for i in range(len(Globals.PLAYERS)):
                        if Globals.PLAYERS[i].name != temp_var['info'].name:
                            trader = check_if_player_can_trade(temp_var['info'])
                            trading_with = check_if_player_can_trade(Globals.PLAYERS[i])
                            if trader or trading_with:
                                counter += 1
                                self.menuitems['choose_player_to_trade_'+Globals.PLAYERS[i].name] = MenuItem(Globals.PLAYERS[i].name, 'enter_the_trade_menu_'+Globals.PLAYERS[i].name, 'ingame_enter_the_trade_menu_'+Globals.PLAYERS[i].name, counter)
                    self.cursor.screen_switched(self.menuitems, 'choose_player_to_trade')
                else:
                    self.make_trading_TEMP_VARS('tradingwith', type[21:])
                    self.objects['trade_summary'].make_person_texts('tradingwith')
                    self.show_main_trading_menu()
            elif type and type[:7] == 'return_':
                if 'error' in self.labels.keys():
                    self.labels.pop('error')
                check_trading = check_substring_in_dict_keys(self.labels, 'trading_input')
                if check_trading in ('trading_input_fields', 'trading_input_offer_money', 'trading_input_ask_for_money'):
                    self.return_into_main_trading_menu(check_trading)
                elif 'state_selector' in self.menuitems.keys():
                    self.return_into_prop_manage_choose_field()
                else:
                    if 'trade_summary' in self.objects.keys():
                        self.objects.pop('trade_summary')
                        if 'prev_trade' in self.labels.keys(): self.labels.pop('prev_trade')
                    elif 'prop_manage_summary' in self.objects.keys():
                        self.objects.pop('prop_manage_summary')
                    if 'auction' in Globals.TEMP_VARS.keys():
                        self.disable_step_indicators()
                        key = 'target_cell_trading_info'
                        if key in self.labels.keys(): self.labels.pop(key)
                        key = 'text_cursor'
                        self.cancel_prop_manage()
                        for key in ('trading', 'property', 'prop_manage_CHANGED'):
                            if key in Globals.TEMP_VARS.keys():
                                Globals.TEMP_VARS.pop(key)
                        self.return_to_auction_main('return_auction_main')
                    else:
                        self.return_to_game_from_trading(type)
            elif type in ('trading_input_fields', 'trading_input_offer_money', 'trading_input_ask_for_money', 'trading_input_auction_bet'):
                if type == 'trading_input_auction_bet':
                    self.labels.pop('target_cell_info')
                    self.menuitems['return'] = MenuItem(Globals.TRANSLATION[64], 'return_auction_main', 'ingame_main', 6)
                self.clear_main_menu_entries(('return'))
                if 'error' in self.labels.keys():
                    self.labels.pop('error')
                if type == 'trading_input_fields':
                    self.objects['gamefield'].render_cell_numbers('trade')
                if 'money' in type:
                    text = Globals.TRANSLATION[71]
                elif 'fields' in type:
                    text = Globals.TRANSLATION[69]
                else:
                    temp_var = Globals.TEMP_VARS['auction']
                    text = Globals.TRANSLATION[83].replace('%', temp_var['order'][0].name).replace('@', temp_var['field'].NAME)
                self.labels['target_cell_trading_info'] = AlphaText(text, 'target_cell_info', -3)
                self.labels[type] = AlphaText('', 'ingame_main', 1)
                self.make_obj_for_enter_name(type)
                self.cursor.screen_switched(self.menuitems, 'trading_input')
            elif type == 'trading_input_fields_ACCEPT' and self.menuitems['accept'].text.color == Globals.COLORS['white']:
                cell_num = int(self.labels['trading_input_fields'].symbols)
                cell_obj = self.objects['gamefield'].cells[cell_num]
                if self.objects['trade_summary'].add_rm_fields(cell_obj):
                    self.labels['trading_input_fields'].update_text('')
                    self.make_obj_for_enter_name('trading_input_fields')
                    self.create_trading_input_spec_objects('trading_input_fields')
                else:
                    if cell_obj.owner not in (Globals.TEMP_VARS['trading']['trader']['info'].name, Globals.TEMP_VARS['trading']['tradingwith']['info'].name):
                        NUM = 74
                    else:
                        NUM = 106
                    self.show_or_rm_error_msg(True, NUM, 'ERROR_ingame', 'accept')
            elif type in ('trading_input_offer_money_ACCEPT', 'trading_input_ask_for_money_ACCEPT') and self.menuitems['accept'].text.color == Globals.COLORS['white']:
                player = ('tradingwith', 'trader')['offer' in type]
                money_lbl = check_substring_in_dict_keys(self.labels, 'trading_input')
                self.objects['trade_summary'].add_rm_money(player, int(self.labels[money_lbl].symbols))
                self.return_into_main_trading_menu(money_lbl)
            elif type == 'trading_input_auction_bet_ACCEPT' and self.menuitems['accept'].text.color == Globals.COLORS['white']:
                temp_var = Globals.TEMP_VARS['auction']
                new_bet = int(self.labels['trading_input_auction_bet'].symbols)
                if new_bet > temp_var['bet']:
                    temp_var['bet'] = int(self.labels['trading_input_auction_bet'].symbols)
                    temp_var['player'] = Globals.TEMP_VARS['auction']['order'][0]
                    temp_var['order'].append(temp_var['order'].pop(0))
                    text = Globals.TRANSLATION[86] + str(temp_var['bet']) + ' (' + temp_var['player'].name + ')'
                    self.labels['auction_cur_bet'] = AlphaText(text, 'auction_cur_bet')
                    self.return_to_auction_main('return_auction_main')
                else:
                    self.show_or_rm_error_msg(True, 91, 'ERROR_ingame', 'accept')
            elif type == 'auction_refuse':
                if 'error' in self.labels.keys():
                    self.labels.pop('error')
                Globals.TEMP_VARS['auction']['order'].pop(0)
                self.auction_next_player()
            elif type and 'ingame_bankruptcy' in type:
                RECIPIENT = Globals.TEMP_VARS['bankruptcy_RECIPIENT']
                temp_var = Globals.TEMP_VARS['bankruptcy_fields_changing']
                CELL = self.objects['gamefield'].cells[temp_var[0]]
                MON = CELL.buy_cost / 20
                MON = -MON
                if type == 'ingame_bankruptcy_110':
                    MON -= CELL.buy_cost / 2
                    CELL.buildings = 0
                    self.objects['game_log'].add_message('bankruptcy_field_110')
                else:
                    self.objects['game_log'].add_message('bankruptcy_field_10')
                self.change_player_money(RECIPIENT, MON)
                self.change_owner_for_a_cell(RECIPIENT, CELL)
                Globals.TEMP_VARS['RErender_groups'] = [CELL.group]
                self.objects['gamefield'].RErender_fieldcell_groups()
                temp_var.pop(0)
                CELL.step_indicator_visible = False
                if temp_var:
                    if 'error' in self.labels.keys():
                        self.labels.pop('error')
                    CELL = self.objects['gamefield'].cells[temp_var[0]]
                    CELL.step_indicator_visible = True
                    self.labels['target_cell_info'].update_text(CELL.NAME)
                    self.menuitems['ingame_bankruptcy_10'].update_text(Globals.TRANSLATION[101]+str(CELL.buy_cost/20))
                    self.menuitems['ingame_bankruptcy_110'].update_text(Globals.TRANSLATION[102]+str(int((CELL.buy_cost/2)*1.1)))
                else:
                    for key in ('bankruptcy_fields_changing', 'bankruptcy_RECIPIENT'):
                        Globals.TEMP_VARS.pop(key)
                    if 'pay_birthday' in Globals.TEMP_VARS.keys():
                        self.pay_birthday_next_player()
                    else:
                        self.change_player(True)
            elif type and 'onboard_select_cell' in type:
                if 'trading' in Globals.TEMP_VARS.keys() and 'tradingwith' in Globals.TEMP_VARS['trading'].keys():
                    cell_obj = self.objects['gamefield'].cells[int(type[20:])]
                    status = self.objects['trade_summary'].add_rm_fields(cell_obj)
                    if cell_obj.owner not in (Globals.TEMP_VARS['trading']['trader']['info'].name, Globals.TEMP_VARS['trading']['tradingwith']['info'].name):
                        NUM = 74
                    else:
                        NUM = 106
                    self.show_or_rm_error_msg(not status, NUM, 'ERROR_ingame', 'accept')
                    self.show_trading_OFFER_ALL_button(True)
                elif 'property' in Globals.TEMP_VARS.keys():
                    self.create_prop_management_cell_state_objects(self.objects['gamefield'].cells[int(type[20:])])
            elif type == 'ingame_trading_OFFER_ALL':
                self.clear_main_menu_entries('return')
                self.labels['target_cell_info'] = AlphaText(Globals.TEMP_VARS['trading']['tradingwith']['info'].name + Globals.TRANSLATION[77], 'trading_offer_request')
                self.menuitems['ingame_trading_ACCEPT_ALL'] = MenuItem(Globals.TRANSLATION[78], 'ingame_trading_ACCEPT_ALL', 'ingame_main', 3)
                temp_pos = self.menuitems['ingame_trading_ACCEPT_ALL'].text.new_pos
                self.menuitems['return'].text.update_text(Globals.TRANSLATION[79])
                upper_size = self.menuitems['ingame_trading_ACCEPT_ALL'].text.rect.w
                down_size = self.menuitems['return'].text.rect.w
                self.menuitems['return'].text.new_pos = (temp_pos[0] + (upper_size - down_size)/2, temp_pos[1] + 35)
                self.cursor.screen_switched(self.menuitems, 'ingame_trading_ACCEPT_DECLINE')
            elif type == 'ingame_trading_ACCEPT_ALL':
                self.swap_property_to_finish_trading()
                self.objects['gamefield'].RErender_fieldcell_groups()
                self.objects['game_log'].add_message(type)
                self.trade_history_append()
                self.return_to_game_from_trading(self.menuitems['return'].type)
            elif type == 'show_prev_trades':
                if not 'trading' in Globals.TEMP_VARS.keys():
                    if 'trade_summary' in self.objects.keys():
                        self.objects.pop('trade_summary')
                        self.labels.pop('prev_trade')
                    else:
                        self.objects['trade_summary'] = Globals.TEMP_VARS['prev_trade']
                        self.labels['prev_trade'] = AlphaText(Globals.TRANSLATION[80], 'last_trade_info')
            elif type and 'trading' in type and 'free_jail' in type:
                person = ('trader', 'tradingwith')['ask_for' in type]
                self.objects['trade_summary'].add_rm_jails(person, int(type[-1]))
                self.update_trading_jail_text_for_menuitem(person, int(type[-1]))
                person = ('trader', 'tradingwith')['ask_for' not in type]
                temp_var = Globals.TEMP_VARS['trading'][person]['jail']
                while temp_var:
                    num = temp_var[0]
                    self.objects['trade_summary'].add_rm_jails(person, num)
                    self.update_trading_jail_text_for_menuitem(person, num)
                self.show_trading_OFFER_ALL_button(True)
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
                    if 'money_player' not in lbl and 'bank_property' not in lbl:
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
                        self.menuitems['fieldcell_' + str(cell.number)] = MenuItem('', 'onboard_select_cell_' + str(cell.number), 'onboard_select_cell', cell.number)
                clear_TEMP_VARS(('build_style', 'cur_game', 'cur_turn', 'rentlabels', 'bank_property'))
                Globals.TEMP_VARS['double_dices_count'] = 0
                Globals.TEMP_VARS['take_chance_when_player_is_on_chest'] = False
                for player in Globals.PLAYERS:
                    player.speed_limit = 5
                add_one_game()
            elif type == 'show_menu':
                state = int(self.menuitems['show_menu'].text.symbols == u'↓')
                self.menuitems['show_menu'].update_text((u'↓', u'↑')[state])
                if not state:
                    state = -1
                objects_to_move = [self.pics['gamebackground'], self.objects['gamefield'], self.objects['game_log']]
                if 'trade_summary' in self.objects.keys():
                    objects_to_move += [self.objects['trade_summary']]
                elif 'prev_trade' in Globals.TEMP_VARS.keys():
                    Globals.TEMP_VARS['prev_trade'].change_new_pos((0, state*100))
                objects_to_move += [cell for cell in self.menuitems.values() if cell.group == 'onboard_select_cell']
                objects_to_move += [cell.step_indicator for cell in self.objects['gamefield'].cells]
                objects_to_move += [cell.a_little_number for cell in self.objects['gamefield'].cells]
                objects_to_move += [self.menuitems[key] for key in ('exit', 'show_menu', 'volume_level', 'music', 'sounds', 'show_prev_trades') if key in self.menuitems.keys()]
                objects_to_move += [self.labels[key] for key in ('volume_level', 'music', 'sounds', 'prev_trade') if key in self.labels.keys()]
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
            elif type == 'ingame_winner':
                if Globals.PLAYERS[0].human:
                    write_stats()
                self.switch_screen('main_main', 'exit')
                self.cursor.screen_switched(self.menuitems, 'main_main')
            elif type:
                self.switch_screen(type, key)
                self.cursor.screen_switched(self.menuitems, type)
    def return_to_game_from_trading(self, type):
        self.restore_step_indicators_state()
        self.cancel_prop_manage()
        for key in ('trading', 'property', 'prop_manage_CHANGED'):
            if key in Globals.TEMP_VARS.keys():
                Globals.TEMP_VARS.pop(key)
        if 'auction' in Globals.TEMP_VARS.keys():
            temp_var = Globals.TEMP_VARS['auction']
            if not (len(temp_var['order']) > 1 or (len(temp_var['order']) and not temp_var['bet'])):
                Globals.TEMP_VARS.pop('auction')
        if 'text_cursor' in self.objects.keys():
            self.objects.pop('text_cursor')
        if type != 'return_player_on_a_new_cell' and 'cur_field_owner' in Globals.TEMP_VARS:
            Globals.TEMP_VARS.pop('cur_field_owner')
        if type == 'return_end_turn':
            self.ask_to_end_turn()
        elif type == 'return_bankruptcy_buyout':
            self.clear_main_menu_entries()
            self.disable_central_labels()
            self.disable_step_indicators()
            CELL = self.objects['gamefield'].cells[Globals.TEMP_VARS['bankruptcy_fields_changing'][0]]
            CELL.step_indicator_visible = True
            self.labels['target_cell_trading_info'] = AlphaText(Globals.TRANSLATION[89].replace('%', Globals.TEMP_VARS['bankruptcy_RECIPIENT'].name), 'target_cell_bankrupt_buyout', -2)
            self.labels['target_cell_info'] = AlphaText(CELL.NAME, 'target_cell_info', -1)
            self.menuitems['ingame_bankruptcy_10'] = MenuItem(Globals.TRANSLATION[101]+str(CELL.buy_cost/20), 'ingame_bankruptcy_10', 'ingame_main', 3)
            self.menuitems['ingame_bankruptcy_110'] = MenuItem(Globals.TRANSLATION[102]+str(int((CELL.buy_cost/2)*1.1)), 'ingame_bankruptcy_110', 'ingame_main', 4)
            self.show_property_management_menuitems(5)
            self.cursor.screen_switched(self.menuitems, 'bankruptcy_buyout')
        elif type == 'return_pay_birthday':
            if 'target_cell_trading_info' in self.labels.keys():
                self.labels.pop('target_cell_trading_info')
            self.pay_birthday_next_player()
        elif type == 'return_new_turn':
            self.new_turn()
        elif type == 'return_player_on_a_new_cell':
            player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
            if player.cur_field == 10 and player.exit_jail_attempts != None:
                self.new_turn()
            else:
                self.disable_central_labels()
                self.labels['dices'] = GameMechanics.show_dices_picture()
                field_num = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field
                cell = self.objects['gamefield'].cells[field_num]
                if cell.owner and 'cur_field_owner' in Globals.TEMP_VARS.keys() and Globals.TEMP_VARS['cur_field_owner'] != cell.owner:
                    Globals.TEMP_VARS['xxx'] = cell.owner
                    cell.owner = Globals.TEMP_VARS['cur_field_owner']
                if 'auction' in Globals.TEMP_VARS.keys():
                    self.labels.pop('dices')
                    self.auction_next_player()
                else: self.player_on_a_new_cell(self.objects['gamefield'].cells[field_num])
                if 'xxx' in Globals.TEMP_VARS.keys():
                    cell.owner = Globals.TEMP_VARS.pop('xxx')
    def return_to_auction_main(self, type):
        if type == 'return_auction_main':
            Globals.TEMP_VARS['auction']['field'].step_indicator.change_color(Globals.COLORS['white'])
            Globals.TEMP_VARS['auction']['field'].step_indicator_visible = True
            for key in ('target_cell_trading_info', 'trading_input_auction_bet'):
                if key in self.labels.keys(): self.labels.pop(key)
            if 'text_cursor' in self.objects.keys(): self.objects.pop('text_cursor')
        self.auction_next_player()
    def return_into_prop_manage_choose_field(self):
        self.labels['property_management_input'] = self.labels.pop('property_management_input_ready')
        self.labels['property_management_input'].update_text('', True)
        self.labels.pop('target_cell_trading_subinfo')
        self.make_obj_for_enter_name('property_management_input')
        self.cursor.add_rm_keys(False, 'state_selector')
        self.menuitems.pop('state_selector')
        KEY = 'accept_all_prop_management'
        CHANGES = self.check_if_there_are_prop_management_changes()
        if not KEY in self.menuitems.keys() and CHANGES:
            self.menuitems[KEY] = MenuItem(Globals.TRANSLATION[13], 'prop_management_ACCEPT_ALL', 'ingame_main', 7)
            self.cursor.add_rm_keys(True, KEY, 0, self.menuitems[KEY].active_zone.move(0, self.menuitems[KEY].text.new_pos[1] - self.menuitems[KEY].text.rect.y).topleft)
        elif KEY in self.menuitems.keys() and not CHANGES:
            self.menuitems.pop(KEY)
            self.cursor.add_rm_keys(False, KEY)
        if KEY in self.menuitems.keys():
            temp_var = Globals.TEMP_VARS['prop_manage_CHANGED']
            house_count = 0
            for key in temp_var.keys():
                if key != 'TOTAL':
                    house_count += temp_var[key][3]
            bank_prop_fault = False
            for i in range(2):
                if Globals.TEMP_VARS['bank_property'][i] < 0:
                    bank_prop_fault = True
            curplayer = check_cur_prop_management()
            if bank_prop_fault or house_count + curplayer.build_ability > 3:
                self.menuitems['accept_all_prop_management'].text.change_color(Globals.COLORS['grey63'])
            else:
                self.menuitems['accept_all_prop_management'].text.change_color(Globals.COLORS['white'])
    def entering_property_menu(self):
        self.save_step_indicators_state()
        if 'pay_birthday' in Globals.TEMP_VARS.keys():
            self.labels['target_cell_info'].change_new_pos((0, -80))
        self.make_return_button_for_property_management()
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
            if key[:12] in ('dices', 'target_cell_', 'auction_cur_'):
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
    def cancel_prop_manage(self):
        temp = check_substring_in_dict_keys(self.labels, 'property_management_input')
        if temp:
            self.labels.pop(temp)
            Globals.TEMP_VARS['RErender_groups'] = []
            for cell in self.objects['gamefield'].cells:
                cell.a_little_number_visible = False
                if cell.number in Globals.TEMP_VARS['property'].keys() and cell.buildings != Globals.TEMP_VARS['property'][cell.number]:
                    cell.buildings = Globals.TEMP_VARS['property'][cell.number]
                    if cell.group not in Globals.TEMP_VARS['RErender_groups']:
                        Globals.TEMP_VARS['RErender_groups'].append(cell.group)
            self.RErender_fieldcell_tooltips_by_groups()
            self.objects['gamefield'].RErender_fieldcell_groups()
            Globals.TEMP_VARS['bank_property'] = Globals.TEMP_VARS.pop('bank_property_back')
            self.upd_bank_property_lbl()
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
                            'profit'    : AlphaText(Globals.TRANSLATION[10] + str(data[2]), 'stats_common', 2),
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
                          'build_style' : MenuItem(u'‹ '+Globals.TRANSLATION[18-int(Globals.SETTINGS['build_style'])]+u' ›', 'main_settings_build_style', 'main_settings_left_MI', 6),
                          'exit'        : MenuItem(Globals.TRANSLATION[13], 'main_main', 'main_settings_exit')}
        self.labels.update({'language'      : AlphaText(Globals.TRANSLATION[14], 'settings_left', 0),
                            'player'        : AlphaText(Globals.TRANSLATION[20], 'settings_left', 1),
                            'hotkeys'       : AlphaText(Globals.TRANSLATION[25], 'settings_left', 2),
                            'music'         : AlphaText(Globals.TRANSLATION[15], 'settings_left', 3),
                            'sounds'        : AlphaText(Globals.TRANSLATION[16], 'settings_left', 4),
                            'volume'        : AlphaText(Globals.TRANSLATION[19], 'settings_left', 5),
                            'build_style'   : AlphaText(Globals.TRANSLATION[98], 'settings_left', 6)})
        if not Globals.SETTINGS['block']:
            self.menuitems.update({'fav_game'   : MenuItem(u'‹ '+Globals.TRANSLATION[5+int(Globals.SETTINGS['fav_game'])]+u' ›', 'main_settings_fav_game', 'main_settings_left_MI', 7)})
            self.labels.update({'fav_game'      : AlphaText(Globals.TRANSLATION[26], 'settings_left', 7)})
    def make_obj_for_enter_name(self, key):
        self.objects['text_cursor'] = Line(self.labels[key], 'right', 2, Globals.COLORS['white'])
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
            obj = self.objects['gamefield'].chests_and_chances[group][0]
            text = obj.text
            if obj.type == 'income' and obj.modifier[0] < 0:
                Globals.TEMP_VARS['MUST_PAY'] = -obj.modifier[0]
            elif obj.type == 'pay_each':
                Globals.TEMP_VARS['MUST_PAY'] = obj.modifier[0] * (len(Globals.PLAYERS)-1)
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
        if 'save_step_indicators_state' in Globals.TEMP_VARS.keys():
            for i in Globals.TEMP_VARS['save_step_indicators_state']:
                self.objects['gamefield'].cells[i].step_indicator_visible = True
            Globals.TEMP_VARS.pop('save_step_indicators_state')
        else:
            self.objects['gamefield'].cells[Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].cur_field].step_indicator_visible = True
    def show_property_management_menuitems(self, number, condition=True):
        if condition:
            trader_name = self.trader_for_cur_player_or_for_birthday().name
            if check_if_anybody_can_trade():
                if len(Globals.PLAYERS) == 2:
                    type = 'enter_the_trade_menu_' + find_player_obj_by_name(trader_name, True).name
                else:
                    type = 'enter_the_trade_menu'
                self.menuitems['trade'] = MenuItem(Globals.TRANSLATION[44], type, 'ingame_main', number)
            if check_if_player_owns_fieldcells(trader_name):
                self.menuitems['manage_property'] = MenuItem(Globals.TRANSLATION[62], 'enter_the_property_management', 'ingame_main', number+1)
    def make_return_button_for_property_management(self):
        if 'end_turn' in self.menuitems.keys():
            back_type = 'return_end_turn'
        elif 'bankruptcy_RECIPIENT' in Globals.TEMP_VARS.keys():
            back_type = 'return_bankruptcy_buyout'
        elif 'pay_birthday' in Globals.TEMP_VARS.keys():
            back_type = 'return_pay_birthday'
        elif 'roll_the_dice' in self.menuitems.keys():
            back_type = 'return_new_turn'
        else:
            back_type = 'return_player_on_a_new_cell'
        self.menuitems['return'] = MenuItem(Globals.TRANSLATION[(64, 93)['property' in Globals.TEMP_VARS.keys()]], back_type, 'ingame_main', 8)
    def show_main_trading_menu(self):
        if 'target_cell_trading_info' in self.labels.keys():
            self.labels.pop('target_cell_trading_info')
        self.clear_main_menu_entries(('return'))
        temp_var = Globals.TEMP_VARS['trading']
        counter = 0
        trader = check_if_player_owns_fieldcells(temp_var['trader']['info'].name)
        trading_with = check_if_player_owns_fieldcells(temp_var['tradingwith']['info'].name)
        if trader or trading_with:
            counter += 1
            self.menuitems['trading_input_fields'] = MenuItem(Globals.TRANSLATION[65], 'trading_input_fields', 'ingame_main', counter)
        for i in range(2):
            counter += 1
            operation = ('trading_input_offer_money', 'trading_input_ask_for_money')[i]
            self.menuitems[operation] = MenuItem(Globals.TRANSLATION[(66, 67)[i]], operation, 'ingame_main', counter)
        for key in ('trader', 'tradingwith'):
            for i in range(len(temp_var[key]['info'].free_jail_cards)):
                counter += 1
                text, operation = self.generate_trading_jail_text_for_menuitem(key, i)
                self.menuitems[operation + str(i)] = MenuItem(text, operation + str(i), 'ingame_main_trading_jails_' + key, counter)
        self.show_trading_OFFER_ALL_button()
        self.cursor.screen_switched(self.menuitems, 'trading_main_menu')
    def show_trading_OFFER_ALL_button(self, cursor_key_just_add=False):
        if self.check_trading_accept_ability('trader') and self.check_trading_accept_ability('tradingwith') and 'text_cursor' not in self.objects.keys():
            if 'accept_ALL' not in self.menuitems.keys():
                self.menuitems['accept_ALL'] = MenuItem(Globals.TRANSLATION[76], 'ingame_trading_OFFER_ALL', 'ingame_main', 7)
                if cursor_key_just_add:
                    self.cursor.add_rm_keys(True, 'accept_ALL', len(self.cursor.keys) - 1, self.menuitems['accept_ALL'].active_zone.move(0, self.menuitems['accept_ALL'].text.new_pos[1] - self.menuitems['accept_ALL'].text.rect.y).topleft)
        elif 'accept_ALL' in self.menuitems.keys():
            self.menuitems.pop('accept_ALL')
            self.cursor.add_rm_keys(False, 'accept_ALL')
    def generate_trading_jail_text_for_menuitem(self, key, i):
        operation = ('trading_offer_free_jail', 'trading_ask_for_free_jail')[key == 'tradingwith']
        text = Globals.TRANSLATION[70].split('/')
        return text[i in Globals.TEMP_VARS['trading'][key]['jail']].capitalize() + Globals.TRANSLATION[68], operation
    def update_trading_jail_text_for_menuitem(self, key, i):
        text, operation = self.generate_trading_jail_text_for_menuitem(key, i)
        self.menuitems[operation + str(i)].update_text(text)
    def create_trading_input_spec_objects(self, KEY):
        self.check_error(('trading_input', 'property_management_input')['property' in Globals.TEMP_VARS.keys()])
        if not self.labels[KEY].symbols and 'accept' in self.menuitems.keys():
            self.menuitems.pop('accept')
            self.cursor.add_rm_keys(False, 'accept')
        if self.labels[KEY].symbols and ('trading_input' in KEY or KEY == 'property_management_input') and 'accept' not in self.menuitems.keys():
            if KEY in ('trading_input_auction_bet', 'property_management_input'):
                MInum = 5
                text = Globals.TRANSLATION[(90, 92)[KEY == 'property_management_input']]
            else:
                MInum = 7
                text = Globals.TRANSLATION[70]
                if 'money' in KEY:
                    text = text.split('/')[0]
            self.menuitems['accept'] = MenuItem(text, KEY + '_ACCEPT', 'ingame_main', MInum)
            self.cursor.add_rm_keys(True, 'accept', 0, self.menuitems['accept'].active_zone.move(0, self.menuitems['accept'].text.new_pos[1] - self.menuitems['accept'].text.rect.y).topleft)
    def return_into_main_trading_menu(self, label_key):
        for cell in self.objects['gamefield'].cells:
            cell.a_little_number_visible = False
        self.objects.pop('text_cursor')
        self.labels.pop(label_key)
        self.show_main_trading_menu()
    def make_trading_TEMP_VARS(self, key, player=None):
        if key == 'trader':
            Globals.TEMP_VARS['trading'][key] = {'info' : self.trader_for_cur_player_or_for_birthday()}
        else:
            Globals.TEMP_VARS['trading'][key] = {'info' : find_player_obj_by_name(player)}
        Globals.TEMP_VARS['trading'][key].update({'fields' : [], 'money' : 0, 'jail' : []})
    def trade_history_append(self):
        Globals.TEMP_VARS['prev_trade'] = self.objects.pop('trade_summary')
        temp_var = Globals.TEMP_VARS['prev_trade']
        temp_var.pos = (temp_var.pos[0], temp_var.pos[1] + 20)
        temp_var.new_pos = (temp_var.new_pos[0], temp_var.new_pos[1] + 20)
        if not 'show_prev_trades' in self.menuitems.keys():
            self.menuitems['show_prev_trades'] = MenuItem(u'♼', 'show_prev_trades', 'show_prev_trades', 1)
    def create_prop_management_cell_state_objects(self, CELL):
        player = check_cur_prop_management()
        if CELL.owner == player.name:
            if 'error' in self.labels.keys(): self.labels.pop('error')
            if 'text_cursor' in self.objects.keys(): self.objects.pop('text_cursor')
            if 'property_management_input' in self.labels.keys():
                self.labels['property_management_input_ready'] = self.labels.pop('property_management_input')
            self.labels['property_management_input_ready'].update_text(str(CELL.number))
            self.labels['target_cell_trading_subinfo'] = AlphaText(Globals.TRANSLATION[95], 'target_cell_info', -1)
            if 'accept' in self.menuitems.keys():
                self.menuitems.pop('accept')
                self.cursor.add_rm_keys(False, 'accept')
            self.menuitems['state_selector'] = MenuItem('', 'cell_state_SELECTOR', 'ingame_main', 3)
            if 'state_selector' in self.cursor.keys:
                self.cursor.add_rm_keys(False, 'state_selector')
            self.cursor.add_rm_keys(True, 'state_selector', 0, self.menuitems['state_selector'].active_zone.move(0, self.menuitems['state_selector'].text.new_pos[1] - self.menuitems['state_selector'].text.rect.y).topleft)
        else:
            if 'state_selector' in self.menuitems.keys():
                self.return_into_prop_manage_choose_field()
            self.show_or_rm_error_msg(True, 94, 'ERROR_ingame', 'accept')
    def upd_bank_property_lbl(self):
        for i in range(2):
            lbl = self.labels['bank_property' + str(3 + 2*(i))]
            pic_lbl = self.labels['bank_property' + str(2 + 2*(i))]
            lbl.x = lbl.new_pos[0]
            if Globals.TEMP_VARS['bank_property'][i] > 3:
                lbl.color = Globals.COLORS['white']
                pic_lbl.change_color(Globals.COLORS['white'])
            elif Globals.TEMP_VARS['bank_property'][i] > 0:
                lbl.color = Globals.COLORS['orange']
                pic_lbl.change_color(Globals.COLORS['orange'])
            else:
                lbl.color = Globals.COLORS['red27']
                pic_lbl.change_color(Globals.COLORS['red27'])
            lbl.update_text(str(Globals.TEMP_VARS['bank_property'][i]))
    #--- Various verifications
    def check_error(self, type):
        if type == 'main_new_game':
            status = self.check_doubles_for_players()
            data = (32, 'ERROR_main', 'start')
            if status and 'error' not in self.labels.keys():
                self.show_or_rm_error_msg(True, data[0], data[1], data[2])
            elif not status and 'error' in self.labels.keys():
                self.show_or_rm_error_msg(False, data[0], data[1], data[2])
        elif type == 'trading_input':
            temp = check_substring_in_dict_keys(self.labels, 'trading_input')
            data = (72 + ('money' in temp or 'auction' in temp), 'ERROR_ingame', 'accept')
            if 'fields' in temp:
                MAX = 39
            elif 'auction' in temp:
                MAX = Globals.TEMP_VARS['auction']['order'][0].money
            else:
                trader = ('trader', 'tradingwith')['ask_for' in temp]
                MAX = Globals.TEMP_VARS['trading'][trader]['info'].money
        elif type == 'property_management_input':
            temp = type
            data = (72, 'ERROR_ingame', 'accept')
            MAX = 39
        if type in ('trading_input', 'property_management_input'):
            obj = self.labels[temp].symbols
            if obj and int(obj) > MAX:
                self.show_or_rm_error_msg(True, data[0], data[1], data[2])
            elif (obj and int(obj) <= MAX and 'error' in self.labels.keys()) or (not obj and 'error' in self.labels.keys()):
                self.show_or_rm_error_msg(False, data[0], data[1], data[2])
    def show_or_rm_error_msg(self, SHOW, lbl_translation_num, lbl_type, menuitem_key):
        if SHOW:
            self.labels['error'] = AlphaText(Globals.TRANSLATION[lbl_translation_num], lbl_type, int('trading_input_fields' in self.menuitems.keys()))
        elif 'error' in self.labels.keys():
            self.labels.pop('error')
        if menuitem_key in self.menuitems.keys():
            self.menuitems[menuitem_key].text.color = Globals.COLORS[('white', 'grey63')[SHOW]]
            self.menuitems[menuitem_key].text.RErender()
    def error_msg_money_limits(self, key):
        if key == 'accept_all_prop_management':
            condition = self.objects['prop_manage_summary'].text['total'].color == Globals.COLORS['light_red']
        else:
            condition = self.cursor and self.cursor.uCOLOR == 'red27' and self.cursor.uCondition and key in ('buy_a_cell', 'ingame_continue', 'auction_up_bet', 'pay_money_to_exit_jail', 'roll_the_dice', 'ingame_bankruptcy_10', 'ingame_bankruptcy_110')
        if condition: self.show_or_rm_error_msg(True, 99, 'ERROR_ingame', 'accept')
        return condition
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
                if cell.owner == player and not (cell.group in ('railroad', 'service') and cell.buildings == -1):
                    data.append(cell)
        self.objects['gamefield'].groups_monopolies[group] = ('', player)[counter == len(data)]
        return data
    def trader_for_cur_player_or_for_birthday(self):
        if 'pay_birthday' in Globals.TEMP_VARS.keys():
            return Globals.TEMP_VARS['pay_birthday'][0]
        elif 'auction' in Globals.TEMP_VARS.keys():
            return Globals.TEMP_VARS['auction']['order'][0]
        elif 'bankruptcy_RECIPIENT' in Globals.TEMP_VARS.keys():
            return Globals.TEMP_VARS['bankruptcy_RECIPIENT']
        else:
            return Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
    def check_trading_accept_ability(self, player):
        for key in ('fields', 'money', 'jail'):
            if Globals.TEMP_VARS['trading'][player][key]:
                return True
    def check_if_there_are_prop_management_changes(self):
        for i in Globals.TEMP_VARS['property'].keys():
            if Globals.TEMP_VARS['property'][i] != self.objects['gamefield'].cells[i].buildings:
                return True
    def RErender_fieldcell_tooltips_by_groups(self):
        for cell in self.objects['gamefield'].cells:
            if cell.group in Globals.TEMP_VARS['RErender_groups']:
                self.menuitems['fieldcell_' + str(cell.number)].tooltip.RErender()
    def recheck_prop_management_money_changes(self):
        Globals.TEMP_VARS['prop_manage_CHANGED'] = {}
        temp_var = Globals.TEMP_VARS['prop_manage_CHANGED']
        temp_var['TOTAL'] = 0
        BANKprop = [0, 0]
        for i in Globals.TEMP_VARS['property'].keys():
            CELL = self.objects['gamefield'].cells[i]
            old_buildings = Globals.TEMP_VARS['property'][i]
            new_buildings = CELL.buildings
            CELL.step_indicator.change_color(check_cur_prop_management().color)
            CELL.step_indicator_visible = old_buildings != new_buildings
            if old_buildings != new_buildings:
                temp_var[i] = (old_buildings, new_buildings)
                MONEY = 0
                house_count = 0
                if old_buildings < 0:
                    MONEY -= int((CELL.buy_cost / 2) * 1.1)
                    old_buildings = 0
                elif new_buildings < 0:
                    MONEY += CELL.buy_cost / 2
                    new_buildings = 0
                if CELL.group in range(9):
                    MONEY += (old_buildings - new_buildings) * CELL.build_cost / (1 + 1 * int(new_buildings < old_buildings))
                    if new_buildings > old_buildings:
                        house_count += new_buildings - old_buildings
                    if old_buildings == 5 - Globals.TEMP_VARS['cur_game']:
                        BANKprop[0] -= new_buildings
                        BANKprop[1] += 1
                    elif new_buildings == 5 - Globals.TEMP_VARS['cur_game']:
                        BANKprop[0] += old_buildings
                        BANKprop[1] -= 1
                    else:
                        BANKprop[0] += old_buildings - new_buildings
                temp_var[i] += tuple([MONEY, house_count])
                if not MONEY:
                    temp_var.pop(i)
                    CELL.step_indicator_visible = False
                temp_var['TOTAL'] += MONEY
        for i in range(2):
            Globals.TEMP_VARS['bank_property'][i] = Globals.TEMP_VARS['bank_property_back'][i] + BANKprop[i]
        self.upd_bank_property_lbl()
        self.objects['prop_manage_summary'].recheck()
        # self.DEBUGGER_prop_management_money_changes()
    #--- Game mechanics
    def ask_to_end_turn(self):
        self.disable_central_labels()
        player = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
        if Globals.TEMP_VARS['dice1'] != Globals.TEMP_VARS['dice2'] or player.exit_jail_attempts != None:
            self.show_step_indicator_under_player()
            self.clear_main_menu_entries()
            self.menuitems['end_turn'] = MenuItem(Globals.TRANSLATION[61], 'ingame_end_turn', 'ingame_main', 0)
            self.show_property_management_menuitems(1)
            self.cursor.screen_switched(self.menuitems, 'ingame_end_turn')
        else:
            self.new_turn()
    def change_player(self, bankrupt=None):
        if 'bankruptcy_RECIPIENT' in Globals.TEMP_VARS.keys():
            Globals.TEMP_VARS.pop('bankruptcy_RECIPIENT')
        GameMechanics.change_player(bankrupt)
        Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].build_ability = 0
        self.objects['cur_turn_highlighter'].move()
        if len(Globals.PLAYERS) > 1:
            self.objects['game_log'].add_message('change_player')
            self.new_turn()
        else:
            self.disable_central_labels()
            self.show_step_indicator_under_player()
            if self.cursor:
                self.clear_main_menu_entries()
            self.labels['target_cell_name'] = AlphaText(Globals.TRANSLATION[107] + Globals.PLAYERS[0].name, 'target_cell_name', 0)
            self.labels['target_cell_name'].change_color(Globals.PLAYERS[0].color)
            self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[109] + str(count_player_funds(Globals.PLAYERS[0])), 'target_cell_info', 2)
            self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[108], 'ingame_winner', 'ingame_main', 6)
            if self.cursor:
                self.cursor.screen_switched(self.menuitems, 'ingame_winner')
            else:
                self.cursor = MainCursor(self.menuitems, 'ingame_winner')
    def new_turn(self):
        # self.DEBUGGER_show_TEMP_VARS_keys()
        if 'cur_field_owner' in Globals.TEMP_VARS.keys():
            Globals.TEMP_VARS.pop('cur_field_owner')
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
        # self.DEBUGGER_chests_and_chances()
        PLAYER = Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']]
        self.clear_main_menu_entries()
        if cell.NAME:
            self.labels['target_cell_name'] = AlphaText(cell.NAME, 'target_cell_name', 0)
        if cell.group in ('jail', 'skip', 'gotojail', 'start', 'income', 'tax', 'chest', 'chance'):
            self.show_special_cell_info(cell)
            group = (cell.group, 'chance')[Globals.TEMP_VARS['take_chance_when_player_is_on_chest']]
            property_management_number = 6
            if group in ('chest', 'chance'):
                obj = self.objects['gamefield'].chests_and_chances[group + 's'][0]
                if obj.type == 'repair' and 'repair_cost_SAVE' not in Globals.TEMP_VARS.keys():
                    Globals.TEMP_VARS['repair_cost_SAVE'] = 0
                    for i in self.objects['gamefield'].cells:
                        if str(i.group) in ('12345678') and i.owner == PLAYER.name and i.buildings > 0:
                            if i.buildings == 5 - Globals.TEMP_VARS['cur_game']:
                                Globals.TEMP_VARS['repair_cost_SAVE'] += obj.modifier[1]
                            else:
                                Globals.TEMP_VARS['repair_cost_SAVE'] += i.buildings * obj.modifier[0]
                property_management_condition = (obj.type == 'income' and obj.modifier[0] < 0) or obj.type in ('pay_each', 'repair')
            else:
                property_management_condition = cell.group == 'tax'
            if group in ('chest', 'chance') and self.objects['gamefield'].chests_and_chances[group + 's'][0].type == 'goto_jail':
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49], 'ingame_continue_gotojail', 'ingame_main', 5)
                obj = self.objects['gamefield'].chests_and_chances[group + 's']
                obj.append(obj.pop(0))
            else:
                addition = ''
                if group in ('chest', 'chance') and self.objects['gamefield'].chests_and_chances[group + 's'][0].type == 'repair':
                    addition = ' ($' + str(Globals.TEMP_VARS['repair_cost_SAVE']) + ')'
                    Globals.TEMP_VARS['MUST_PAY'] = Globals.TEMP_VARS['repair_cost_SAVE']
                    if check_bankrupt(PLAYER):
                        addition += Globals.TRANSLATION[100]
                elif ((group == 'tax' and check_bankrupt(PLAYER, -Globals.TEMP_VARS['MUST_PAY']))
                      or (group in ('chest', 'chance')
                          and ((obj.type == 'income'
                                and obj.modifier[0] < 0
                                and check_bankrupt(PLAYER))
                               or (obj.type == 'pay_each'
                                   and check_bankrupt(PLAYER))))):
                    addition += Globals.TRANSLATION[100]
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49] + addition, 'ingame_continue_'+group, 'ingame_main', 5)
            Globals.TEMP_VARS['take_chance_when_player_is_on_chest'] = False
        else:
            if cell.owner:
                addition = ''
                text = Globals.TRANSLATION[45] + cell.owner
                if cell.buildings < 0 or cell.owner == PLAYER.name:
                    type = 'ingame_continue_NO'
                    if cell.buildings < 0:
                        self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[96], 'target_cell_info', 2)
                else:
                    type = 'ingame_continue_PAY_RENT'
                    if 'cur_field_owner' not in Globals.TEMP_VARS.keys():
                        if cell.group == 'service':
                            if cell.step_indicator_visible:
                                state = int(cell.rent_costs[cell.buildings][1:])
                            else:
                                state = 10
                            Globals.TEMP_VARS['MUST_PAY'] = (Globals.TEMP_VARS['dice1'] + Globals.TEMP_VARS['dice2']) * state
                        else:
                            Globals.TEMP_VARS['MUST_PAY'] = cell.rent_costs[cell.buildings]
                            if (not cell.buildings and self.objects['gamefield'].groups_monopolies[cell.group]) or (cell.group == 'railroad' and 'double_rails' in Globals.TEMP_VARS.keys()) or (cell.group == 'railroad' and not cell.step_indicator_visible and self.objects['gamefield'].chests_and_chances['chances'][0].type != 'goto' and self.objects['gamefield'].chests_and_chances['chances'][0].modifier != [5]):
                                Globals.TEMP_VARS['MUST_PAY'] = Globals.TEMP_VARS['MUST_PAY'] * 2
                                if cell.group == 'railroad':
                                    Globals.TEMP_VARS['double_rails'] = True
                    self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[50] + str(Globals.TEMP_VARS['MUST_PAY']), 'target_cell_info', 2)
                    if PLAYER.money < Globals.TEMP_VARS['MUST_PAY'] and check_bankrupt(PLAYER):
                        addition = Globals.TRANSLATION[100]
                self.menuitems['ingame_continue'] = MenuItem(Globals.TRANSLATION[49]+addition, type, 'ingame_main', 6)
            else:
                text = Globals.TRANSLATION[45] + Globals.TRANSLATION[46]
                Globals.TEMP_VARS['MUST_PAY'] = cell.buy_cost
                self.menuitems.update({'buy_a_cell'         : MenuItem(Globals.TRANSLATION[47] + str(cell.buy_cost)+')', 'ingame_buy_a_cell', 'ingame_main', 5),
                                       'cell_to_an_auction' : MenuItem(Globals.TRANSLATION[48], 'ingame_cell_to_an_auction', 'ingame_main', 6)})
            property_management_number = 7
            property_management_condition = not(cell.buildings < 0 or cell.owner == PLAYER.name)
            self.labels['target_cell_owner'] = AlphaText(text, 'target_cell_owner', 1)
        self.show_property_management_menuitems(property_management_number, property_management_condition)
        self.cursor.screen_switched(self.menuitems, ('ingame_buy_or_auction', 'ingame_continue')['ingame_continue' in self.menuitems.keys()])
    def change_owner_for_a_cell(self, player, cell=None):
        if not cell:
            cell = self.objects['gamefield'].cells[player.cur_field]
        if player:
            cell.owner = player.name
            cell.color = player.color
            cells = self.check_group_owners(cell.group, player.name)
        else:
            cell.owner = None
            cell.color = Globals.COLORS['grey22']
            cells = self.check_group_owners(cell.group, None)
        for group_cell in cells:
            if group_cell.group in ('service', 'railroad') and group_cell.buildings != -1:
                group_cell.buildings = len(cells) - 1
            self.objects['gamefield'].RErender_a_cell(group_cell.number)
            self.menuitems['fieldcell_'+str(group_cell.number)].tooltip.RErender(group_cell.buildings+1)
    def change_player_money(self, player, money):
        player.money += money
        self.labels['money_player_'+player.name].update_text(str(player.money))
    def pay_birthday_next_player(self):
        if Globals.TEMP_VARS['pay_birthday']:
            player = Globals.TEMP_VARS['pay_birthday'][0]
            text = Globals.TRANSLATION[58].replace('%', player.name)
            text = text.replace('^', str(Globals.TEMP_VARS['MUST_PAY']))
            text = text.replace('@', Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].name)
            self.labels['target_cell_info'] = AlphaText(text, 'birthday_info')
            self.clear_main_menu_entries()
            addition = ''
            if check_bankrupt(player):
                addition = Globals.TRANSLATION[100]
            self.menuitems.update({'roll_the_dice'  : MenuItem(Globals.TRANSLATION[55] + str(Globals.TEMP_VARS['MUST_PAY']) + addition, 'pay_birthday_'+player.name, 'ingame_main', 3)})
            self.show_property_management_menuitems(4)
            self.cursor.screen_switched(self.menuitems, 'ingame_main')
        else:
            Globals.TEMP_VARS.pop('pay_birthday')
            self.objects['game_log'].add_message('birthday')
            self.ask_to_end_turn()
    def auction_next_player(self):
        temp_var = Globals.TEMP_VARS['auction']
        if len(temp_var['order']) > 1 or (len(temp_var['order']) and not temp_var['bet']):
            self.labels['target_cell_info'] = AlphaText(Globals.TRANSLATION[89].replace('%', temp_var['order'][0].name), 'auction_info', -3)
            self.objects['auction_pl_highlighter'] = AuctionPlayerHighlighter()
            self.clear_main_menu_entries()
            self.show_property_management_menuitems(2)
            number = 2 + ('trade' in self.menuitems.keys()) + ('manage_property' in self.menuitems.keys())
            if temp_var['bet']:
                text = Globals.TRANSLATION[84]
                betstring = Globals.TRANSLATION[86] + str(temp_var['bet']) + ' (' + temp_var['player'].name + ')'
                if not 'auction_cur_bet' in self.labels.keys():
                    self.labels['auction_cur_bet'] = AlphaText(betstring, 'auction_cur_bet')
            else:
                text = Globals.TRANSLATION[88]
                if not 'auction_cur_bet' in self.labels.keys():
                    self.labels['auction_cur_bet'] = AlphaText(Globals.TRANSLATION[87], 'auction_cur_bet')
            self.menuitems.update({'auction_up_bet' : MenuItem(text, 'trading_input_auction_bet', 'ingame_main', 1),
                                   'auction_refuse' : MenuItem(Globals.TRANSLATION[85], 'auction_refuse', 'ingame_main', number)})
            self.cursor.screen_switched(self.menuitems, 'auction_next_player')
        else:
            self.objects.pop('auction_pl_highlighter')
            temp_var['field'].buildings = 0
            self.change_owner_for_a_cell(temp_var['player'], temp_var['field'])
            if temp_var['bet']:
                self.change_player_money(temp_var['player'], -temp_var['bet'])
            self.objects['game_log'].add_message('auction_end')
            if 'bankruptcy_fields_changing' in Globals.TEMP_VARS.keys():
                Globals.TEMP_VARS['bankruptcy_fields_changing'].pop(0)
                self.next_bankruptcy_field()
            else:
                type = ('return_end_turn', 'return_new_turn')[Globals.TEMP_VARS['dice1'] == Globals.TEMP_VARS['dice2'] and Globals.PLAYERS[Globals.TEMP_VARS['cur_turn']].exit_jail_attempts == None]
                self.return_to_game_from_trading(type)
    def swap_property_to_finish_trading(self):
        Globals.TEMP_VARS['RErender_groups'] = []
        for i in range(2):
            temp_keys = ('trader', 'tradingwith')
            change_from = Globals.TEMP_VARS['trading'][temp_keys[i]]
            change_to = Globals.TEMP_VARS['trading'][temp_keys[i-1]]
            for field in change_from['fields']:
                cell = self.objects['gamefield'].cells[field]
                if cell.group not in Globals.TEMP_VARS['RErender_groups']:
                    Globals.TEMP_VARS['RErender_groups'].append(cell.group)
                cell.owner = change_to['info'].name
                cell.color = change_to['info'].color
            if change_from['money']:
                self.change_player_money(change_from['info'], -change_from['money'])
                self.change_player_money(change_to['info'], change_from['money'])
            for i in range(len(change_from['jail'])):
                change_to['info'].free_jail_cards.append(change_from['info'].free_jail_cards.pop(0))
                self.menuitems['fieldcell_10'].tooltip.RErender()
    def bankruptcy_fields_buyout(self, key):
        temp_var = Globals.TEMP_VARS['bankruptcy_fields_changing']
        if temp_var and self.menuitems[key].type == 'ingame_continue_PAY_RENT' or 'pay_birthday' in self.menuitems[key].type:
            if len(Globals.PLAYERS) > 1:
                CELL = self.objects['gamefield'].cells[temp_var[0]]
                self.clear_main_menu_entries()
                self.disable_central_labels()
                self.disable_step_indicators()
                CELL.step_indicator_visible = True
                self.labels['target_cell_trading_info'] = AlphaText(Globals.TRANSLATION[89].replace('%', Globals.TEMP_VARS['bankruptcy_RECIPIENT'].name), 'target_cell_bankrupt_buyout', -2)
                self.labels['target_cell_info'] = AlphaText(CELL.NAME, 'target_cell_info', -1)
                self.menuitems['ingame_bankruptcy_10'] = MenuItem(Globals.TRANSLATION[101]+str(CELL.buy_cost/20), 'ingame_bankruptcy_10', 'ingame_main', 3)
                self.menuitems['ingame_bankruptcy_110'] = MenuItem(Globals.TRANSLATION[102]+str(int((CELL.buy_cost/2)*1.1)), 'ingame_bankruptcy_110', 'ingame_main', 4)
                self.show_property_management_menuitems(5)
                self.cursor.screen_switched(self.menuitems, 'bankruptcy_buyout')
            else:
                Globals.TEMP_VARS['RErender_groups'] = []
                for cell in temp_var:
                    CELL = self.objects['gamefield'].cells[cell]
                    self.change_player_money(Globals.TEMP_VARS['bankruptcy_RECIPIENT'], -CELL.buy_cost / 20)
                    if CELL.group not in Globals.TEMP_VARS['RErender_groups']:
                        Globals.TEMP_VARS['RErender_groups'].append(CELL.group)
                self.objects['gamefield'].RErender_fieldcell_groups()
                self.change_player(True)
        else:
            self.disable_central_labels()
            self.disable_step_indicators()
            self.next_bankruptcy_field()
    def next_bankruptcy_field(self):
        if len(Globals.PLAYERS) == 1:
            self.change_player(True)
        elif Globals.TEMP_VARS['bankruptcy_fields_changing']:
            field = Globals.TEMP_VARS['bankruptcy_fields_changing'][0]
            if Globals.TEMP_VARS['cur_turn'] == len(Globals.PLAYERS):
                temp_range = range(len(Globals.PLAYERS))
            elif Globals.TEMP_VARS['cur_turn']:
                temp_range = range(Globals.TEMP_VARS['cur_turn']+1, len(Globals.PLAYERS)) + range(Globals.TEMP_VARS['cur_turn']+1)
            else:
                temp_range = range(Globals.TEMP_VARS['cur_turn']+1, len(Globals.PLAYERS)) + [0]
            if 'auction_cur_bet' in self.labels.keys():
                self.labels.pop('auction_cur_bet')
            Globals.TEMP_VARS['auction'] = {'bet'       : 0,
                                            'field'     : self.objects['gamefield'].cells[field],
                                            'order'     : [Globals.PLAYERS[i] for i in temp_range],
                                            'player'    : None}
            Globals.TEMP_VARS['auction']['field'].step_indicator.change_color(Globals.COLORS['white'])
            Globals.TEMP_VARS['auction']['field'].step_indicator_visible = True
            self.auction_next_player()
        else:
            Globals.TEMP_VARS.pop('bankruptcy_fields_changing')
            if 'auction' in Globals.TEMP_VARS.keys():
                Globals.TEMP_VARS.pop('auction')
            if 'pay_birthday' in Globals.TEMP_VARS.keys():
                self.pay_birthday_next_player()
            else:
                self.change_player(True)
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
    def DEBUGGER_prop_management_money_changes(self):
        for i in Globals.TEMP_VARS['prop_manage_CHANGED'].keys():
            if i != 'TOTAL':
                print(str(i)+'   : '+str(Globals.TEMP_VARS['prop_manage_CHANGED'][i][0])+'   '+str(Globals.TEMP_VARS['prop_manage_CHANGED'][i][1])+'   '+str(Globals.TEMP_VARS['prop_manage_CHANGED'][i][2]))
        print('-----------------------------------------------')
        print(15*' ' + str(Globals.TEMP_VARS['prop_manage_CHANGED']['TOTAL']))
        print('')
