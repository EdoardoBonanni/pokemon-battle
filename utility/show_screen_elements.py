import pygame
import pygame_gui
from pygame.locals import Color
from utility import utils


def draw_battle_description(BattleWindow, text):
    """
    Draw text on the screen.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param text: battle description text.
    :return:
    """
    if text != 'YOU WIN' and text != 'YOU LOSE':
        BattleWindow.battle_description = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render(text, False, (0, 0, 0))
        BattleWindow.screen.blit(BattleWindow.battle_description,
                                 (BattleWindow.screen_width * 0.04, BattleWindow.screen_height * 0.825))
    else:
        BattleWindow.battle_description = pygame.font.Font("fonts/VT323-Regular.ttf", 85).render(text, False, (0, 0, 0))
        BattleWindow.screen.blit(BattleWindow.battle_description,
                                 (BattleWindow.screen_width * 0.43, BattleWindow.screen_height * 0.84))


def draw_button_moves(BattleWindow):
    """
    Draw Pokemon moves buttons on the screen.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    button_width = BattleWindow.screen_width * 0.18
    button_height = BattleWindow.screen_height * 0.08
    BattleWindow.btn_move1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((BattleWindow.screen_width * 0.58, BattleWindow.screen_height * 0.81),
                                  (button_width, button_height)),
        text='move1',
        manager=BattleWindow.manager,
        object_id='#btn_move1')

    BattleWindow.btn_move2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((BattleWindow.screen_width * 0.78, BattleWindow.screen_height * 0.81),
                                  (button_width, button_height)),
        text='move2',
        manager=BattleWindow.manager,
        object_id='#btn_move2')
    BattleWindow.btn_move3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((BattleWindow.screen_width * 0.58, BattleWindow.screen_height * 0.90),
                                  (button_width, button_height)),
        text='move3',
        manager=BattleWindow.manager,
        object_id='#btn_move3')
    BattleWindow.btn_move4 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((BattleWindow.screen_width * 0.78, BattleWindow.screen_height * 0.90),
                                  (button_width, button_height)),
        text='move4',
        manager=BattleWindow.manager,
        object_id='#btn_move4')


def draw_pokemon(BattleWindow, pokemon_me, pokemon_enemy, show_type_img):
    """
    Draw Pokemon and all their attributes: name, moves, color buttons.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param pokemon_me: Pokemon me.
    :param pokemon_enemy: Pokemon enemy.
    :param show_type_img: choose if show Pokemon move type images.
    :return:
    """

    # Pokemon player me.
    # Move up/down several Pokemon on the screen for the correct position.
    if len(BattleWindow.move_up_back) == 0:
        BattleWindow.move_up_back = ['charizard', 'pidgeotto', 'fearow', 'arcanine', 'machamp', 'victreebel', 'dodrio',
                                     'articuno', 'kangaskhan', 'gyarados', 'dragonite', 'rapidash', 'onix']
    if len(BattleWindow.move_down_back) == 0:
        BattleWindow.move_down_back = ['bulbasaur', 'ivysaur', 'charmander', 'squirtle', 'caterpie', 'metapod',
                                       'kakuna',
                                       'weedle', 'starly', 'pidgey', 'rattata', 'spearow', 'ekans', 'pikachu',
                                       'sandshrew', 'sandslash', 'nidoran', 'nidorina', 'clefairy', 'vulpix',
                                       'jigglypuff',
                                       'oddish', 'gloom', 'paras', 'venonat',
                                       'diglett', 'dugtrio', 'meowth', 'psyduck', 'mankey', 'growlithe', 'poliwag',
                                       'poliwhirl', 'abra', 'bellsprout', 'geodude', 'graveler', 'slowpoke',
                                       'magnemite',
                                       'seel', 'grimer', 'shellder', 'krabby', 'voltorb', 'exeggcute', 'cubone',
                                       'marowak',
                                       'chansey', 'tangela', 'horsea', 'seadra', 'goldeen', 'seaking',
                                       'staryu', 'ditto', 'jolteon', 'omanyte', 'porygon', 'kabuto']

    if BattleWindow.pokemon_me_visible:
        pokemon_me_image = pygame.image.load(
            'img_pokemon_battle_png/' + pokemon_me.name.lower() + '_back.png').convert_alpha()
        pokemon_me_image = pygame.transform.scale(pokemon_me_image, (
            pokemon_me_image.get_width() * 5, pokemon_me_image.get_height() * 5))
        if pokemon_me.name.lower() in BattleWindow.move_up_back:
            BattleWindow.screen.blit(pokemon_me_image,
                                     (BattleWindow.screen_width * 0.04, BattleWindow.screen_height * 0.28))
        elif pokemon_me.name.lower() in BattleWindow.move_down_back:
            BattleWindow.screen.blit(pokemon_me_image,
                                     (BattleWindow.screen_width * 0.04, BattleWindow.screen_height * 0.39))
        else:
            BattleWindow.screen.blit(pokemon_me_image,
                                     (BattleWindow.screen_width * 0.04, BattleWindow.screen_height * 0.33))
    draw_types_pokemon_img(BattleWindow, pokemon_me.type1, pokemon_me.type2, True)
    draw_name_me = BattleWindow.font_name.render(pokemon_me.name, False, (0, 0, 0))
    BattleWindow.screen.blit(draw_name_me, (BattleWindow.screen_width * 0.67, BattleWindow.screen_height * 0.475))
    BattleWindow.btn_move1.set_text(
        str(pokemon_me.move1.name) + ' ' + str(pokemon_me.move1.pp_remain) + '/' + str(pokemon_me.move1.pp))
    BattleWindow.btn_move2.set_text(
        str(pokemon_me.move2.name) + ' ' + str(pokemon_me.move2.pp_remain) + '/' + str(pokemon_me.move2.pp))
    BattleWindow.btn_move3.set_text(
        str(pokemon_me.move3.name) + ' ' + str(pokemon_me.move3.pp_remain) + '/' + str(pokemon_me.move3.pp))
    BattleWindow.btn_move4.set_text(
        str(pokemon_me.move4.name) + ' ' + str(pokemon_me.move4.pp_remain) + '/' + str(pokemon_me.move4.pp))

    color_move1 = BattleWindow.color_mapping[pokemon_me.move1.type.lower()]
    BattleWindow.btn_move1.colours['normal_border'] = color_move1
    BattleWindow.btn_move1.colours['hovered_border'] = color_move1
    BattleWindow.btn_move1.rebuild()
    color_move2 = BattleWindow.color_mapping[pokemon_me.move2.type.lower()]
    BattleWindow.btn_move2.colours['normal_border'] = color_move2
    BattleWindow.btn_move2.colours['hovered_border'] = color_move2
    BattleWindow.btn_move2.rebuild()
    color_move3 = BattleWindow.color_mapping[pokemon_me.move3.type.lower()]
    BattleWindow.btn_move3.colours['normal_border'] = color_move3
    BattleWindow.btn_move3.colours['hovered_border'] = color_move3
    BattleWindow.btn_move3.rebuild()
    color_move4 = BattleWindow.color_mapping[pokemon_me.move4.type.lower()]
    BattleWindow.btn_move4.colours['normal_border'] = color_move4
    BattleWindow.btn_move4.colours['hovered_border'] = color_move4
    BattleWindow.btn_move4.rebuild()
    if show_type_img:
        draw_types_moves_img(BattleWindow, pokemon_me.move1.type,
                             (BattleWindow.screen_width * 0.645, BattleWindow.screen_height * 0.79))
        draw_types_moves_img(BattleWindow, pokemon_me.move2.type,
                             (BattleWindow.screen_width * 0.85, BattleWindow.screen_height * 0.79))
        draw_types_moves_img(BattleWindow, pokemon_me.move3.type,
                             (BattleWindow.screen_width * 0.645, BattleWindow.screen_height * 0.975))
        draw_types_moves_img(BattleWindow, pokemon_me.move4.type,
                             (BattleWindow.screen_width * 0.85, BattleWindow.screen_height * 0.975))

    # Pokemon player enemy.
    # Move up/down several Pokemon on the screen for the correct position.
    if len(BattleWindow.move_up) == 0:
        BattleWindow.move_up = ['charizard', 'pidgeot', 'arcanine', 'machoke', 'machamp', 'rapidash', 'onix',
                                'exeggutor',
                                'kangaskhan', 'lapras', 'articuno', 'mewtwo', 'nidoqueen', 'nidoking',
                                'wartortle', 'venusaur', 'ninetales', 'fearow', 'pidgeotto', 'persian', 'alakazam',
                                'slowbro', 'dodrio', 'dewgong', 'hitmonlee', 'rhydon', 'snorlax', 'dragonite',
                                'moltres', 'victreebel']
    if len(BattleWindow.move_down) == 0:
        BattleWindow.move_down = ['rattata', 'bulbasaur', 'sandshrew', 'paras', 'diglett', 'ditto', 'omanyte',
                                  'porygon',
                                  'nidoran', 'spearow', 'jigglypuff', 'paras', 'growlithe', 'abra', 'grimer',
                                  'krabby', 'exeggcute', 'cubone', 'kabuto']
    if BattleWindow.pokemon_enemy_visible:
        pokemon_enemy_image = pygame.image.load(
            'img_pokemon_battle_png/' + pokemon_enemy.name.lower() + '.png').convert_alpha()
        pokemon_enemy_image = pygame.transform.scale(pokemon_enemy_image, (
            pokemon_enemy_image.get_width() * 3, pokemon_enemy_image.get_height() * 3))
        if pokemon_enemy.name.lower() in BattleWindow.move_up:
            BattleWindow.screen.blit(pokemon_enemy_image,
                                     (BattleWindow.screen_width * 0.73, BattleWindow.screen_height * 0.015))
        elif pokemon_enemy.name.lower() in BattleWindow.move_down:
            BattleWindow.screen.blit(pokemon_enemy_image,
                                     (BattleWindow.screen_width * 0.73, BattleWindow.screen_height * 0.065))
        else:
            BattleWindow.screen.blit(pokemon_enemy_image,
                                     (BattleWindow.screen_width * 0.73, BattleWindow.screen_height * 0.045))
    draw_types_pokemon_img(BattleWindow, pokemon_enemy.type1, pokemon_enemy.type2, False)
    draw_name_enemy = BattleWindow.font_name.render(pokemon_enemy.name, False, (0, 0, 0))
    BattleWindow.screen.blit(draw_name_enemy, (BattleWindow.screen_width * 0.11, BattleWindow.screen_height * 0.08))


def draw_types_pokemon_img(BattleWindow, type1, type2, pokemon_me):
    """
    Draw on screen Pokemon types.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param type1: first Pokemon type.
    :param type2: second Pokemon type.
    :param pokemon_me: choose if me or enemy.
    :return:
    """
    type1_img = pygame.image.load('img/types/' + type1.lower() + '.png').convert_alpha()
    type1_img = pygame.transform.scale(type1_img, (type1_img.get_width() * 2, type1_img.get_height() * 2))
    if pokemon_me:
        BattleWindow.screen.blit(type1_img, (BattleWindow.screen_width * 0.86, BattleWindow.screen_height * 0.5))
    else:
        BattleWindow.screen.blit(type1_img, (BattleWindow.screen_width * 0.3, BattleWindow.screen_height * 0.105))
    if type2 != '':
        type2_img = pygame.image.load('img/types/' + type2.lower() + '.png').convert_alpha()
        type2_img = pygame.transform.scale(type2_img, (type2_img.get_width() * 2, type2_img.get_height() * 2))
        if pokemon_me:
            BattleWindow.screen.blit(type2_img, (BattleWindow.screen_width * 0.92, BattleWindow.screen_height * 0.5))
        else:
            BattleWindow.screen.blit(type2_img, (BattleWindow.screen_width * 0.36, BattleWindow.screen_height * 0.105))


def renderHPBar(BattleWindow, width, height, position, total_hp, actual_hp):
    """
    Draw Pokemon HP bar.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param width: HP bar width.
    :param height: HP bar height.
    :param position: HP bar position.
    :param total_hp: total Pokemon HP.
    :param actual_hp: actual Pokemon HP.
    :return:
    """
    percentage = float(actual_hp) / total_hp
    color = "green"
    if percentage < 0.5:
        color = "orange"
    if percentage < 0.2:
        color = "red"
    bar = pygame.Rect(position, (width * percentage, height))
    BattleWindow.screen.fill(Color(color), bar)


def draw_hp(BattleWindow, hp_me, hp_enemy):
    """
    Draw HP bar for Pokemon in game.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param hp_me: HP player me.
    :param hp_enemy: Hp player enemy.
    :return:
    """
    renderHPBar(BattleWindow, BattleWindow.hp_img_enemy.get_width() * 0.62,
                BattleWindow.hp_img_enemy.get_height() * 0.275,
                (BattleWindow.screen_width * 0.178, BattleWindow.screen_height * 0.16),
                BattleWindow.model.enemy.team[0].battleHP,
                hp_enemy)  # HP enemy.
    renderHPBar(BattleWindow, BattleWindow.hp_img_me.get_width() * 0.6, BattleWindow.hp_img_me.get_height() * 0.18,
                (BattleWindow.screen_width * 0.732, BattleWindow.screen_height * 0.552),
                BattleWindow.model.me.team[0].battleHP,
                hp_me)  # HP me.
    draw_hp_number = BattleWindow.font_hp.render(str(hp_me) + ' / ' + str(BattleWindow.model.me.team[0].battleHP),
                                                 False, (0, 0, 0))
    BattleWindow.screen.blit(draw_hp_number, (BattleWindow.screen_width * 0.75, BattleWindow.screen_height * 0.62))


def draw_types_moves_img(BattleWindow, type, position):
    """
    Draw Pokemon types moves.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param type: Pokemon move type.
    :param position: type position on screen.
    :return:
    """
    type_img = pygame.image.load('img/types/' + type.lower() + '.png').convert_alpha()
    type_img = pygame.transform.scale(type_img, (BattleWindow.screen_width * 0.042, BattleWindow.screen_height * 0.023))
    BattleWindow.screen.blit(type_img, position)


def draw_team_choice_menu(BattleWindow):
    """
    Draw the team choice menu on screen where the player can change Pokemon in battle.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 50)
    bg_team = pygame.image.load('img/bg_team.png').convert_alpha()
    bg_team = pygame.transform.scale(bg_team, (BattleWindow.screen_width, BattleWindow.screen_height))

    pokemon_list_menu_active, image_pokemon_active, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total = create_pokemon_inbattle_menu(
        BattleWindow, BattleWindow.model.me.team[0].name, BattleWindow.font_name,
        BattleWindow.model.me.team[0].battleHP_actual,
        BattleWindow.model.me.team[0].battleHP)
    pokemon_list_menu_deactive1, image_pokemon_deactive1, draw_pokemon_name1, draw_hp_number_actual1, draw_hp_number_total1 = create_pokemon_not_inbattle_menu(
        BattleWindow, BattleWindow.model.me.team[1].name, font_name, BattleWindow.model.me.team[1].battleHP_actual,
        BattleWindow.model.me.team[1].battleHP)
    pokemon_list_menu_deactive2, image_pokemon_deactive2, draw_pokemon_name2, draw_hp_number_actual2, draw_hp_number_total2 = create_pokemon_not_inbattle_menu(
        BattleWindow, BattleWindow.model.me.team[2].name, font_name, BattleWindow.model.me.team[2].battleHP_actual,
        BattleWindow.model.me.team[2].battleHP)
    pokemon_list_menu_deactive3, image_pokemon_deactive3, draw_pokemon_name3, draw_hp_number_actual3, draw_hp_number_total3 = create_pokemon_not_inbattle_menu(
        BattleWindow, BattleWindow.model.me.team[3].name, font_name, BattleWindow.model.me.team[3].battleHP_actual,
        BattleWindow.model.me.team[3].battleHP)
    pokemon_list_menu_deactive4, image_pokemon_deactive4, draw_pokemon_name4, draw_hp_number_actual4, draw_hp_number_total4 = create_pokemon_not_inbattle_menu(
        BattleWindow, BattleWindow.model.me.team[4].name, font_name, BattleWindow.model.me.team[4].battleHP_actual,
        BattleWindow.model.me.team[4].battleHP)
    pokemon_list_menu_deactive5, image_pokemon_deactive5, draw_pokemon_name5, draw_hp_number_actual5, draw_hp_number_total5 = create_pokemon_not_inbattle_menu(
        BattleWindow, BattleWindow.model.me.team[5].name, font_name, BattleWindow.model.me.team[5].battleHP_actual,
        BattleWindow.model.me.team[5].battleHP)

    text_description = pygame.font.Font("fonts/VT323-Regular.ttf", 80).render('Choose a Pokemon.', False, (0, 0, 0))
    text_exit = pygame.font.Font("fonts/VT323-Regular.ttf", 50).render('Exit', False, (255, 255, 255))
    BattleWindow.rect_pokemon_list_menu_active = move_rect(pokemon_list_menu_active,
                                                           -BattleWindow.screen_width * 0.02,
                                                           BattleWindow.screen_height * 0.08)
    BattleWindow.rect_pokemon_list_menu_deactive1 = move_rect(pokemon_list_menu_deactive1,
                                                              BattleWindow.screen_width * 0.352,
                                                              BattleWindow.screen_height * 0.023)
    BattleWindow.rect_pokemon_list_menu_deactive2 = move_rect(pokemon_list_menu_deactive2,
                                                              BattleWindow.screen_width * 0.352,
                                                              BattleWindow.screen_height * 0.18)
    BattleWindow.rect_pokemon_list_menu_deactive3 = move_rect(pokemon_list_menu_deactive3,
                                                              BattleWindow.screen_width * 0.352,
                                                              BattleWindow.screen_height * 0.335)
    BattleWindow.rect_pokemon_list_menu_deactive4 = move_rect(pokemon_list_menu_deactive4,
                                                              BattleWindow.screen_width * 0.352,
                                                              BattleWindow.screen_height * 0.49)
    BattleWindow.rect_pokemon_list_menu_deactive5 = move_rect(pokemon_list_menu_deactive5,
                                                              BattleWindow.screen_width * 0.352,
                                                              BattleWindow.screen_height * 0.645)
    BattleWindow.rect_text_exit = move_rect(text_exit, BattleWindow.screen_width * 0.855,
                                            BattleWindow.screen_height * 0.875)

    BattleWindow.screen.blit(bg_team, (0, 0))
    BattleWindow.screen.blit(pokemon_list_menu_active,
                             (-BattleWindow.screen_width * 0.02, BattleWindow.screen_height * 0.08))
    BattleWindow.screen.blit(image_pokemon_active,
                             (BattleWindow.screen_width * 0.03, BattleWindow.screen_height * 0.17))
    BattleWindow.screen.blit(draw_pokemon_name, (BattleWindow.screen_width * 0.173, BattleWindow.screen_height * 0.22))
    BattleWindow.screen.blit(draw_hp_number_actual,
                             (BattleWindow.screen_width * 0.195, BattleWindow.screen_height * 0.4))
    BattleWindow.screen.blit(draw_hp_number_total, (BattleWindow.screen_width * 0.28, BattleWindow.screen_height * 0.4))
    BattleWindow.screen.blit(pokemon_list_menu_deactive1,
                             (BattleWindow.screen_width * 0.352, BattleWindow.screen_height * 0.023))
    BattleWindow.screen.blit(image_pokemon_deactive1,
                             (BattleWindow.screen_width * 0.40, BattleWindow.screen_height * 0.056))
    BattleWindow.screen.blit(draw_pokemon_name1, (BattleWindow.screen_width * 0.54, BattleWindow.screen_height * 0.07))
    BattleWindow.screen.blit(draw_hp_number_actual1,
                             (BattleWindow.screen_width * 0.84, BattleWindow.screen_height * 0.13))
    BattleWindow.screen.blit(draw_hp_number_total1,
                             (BattleWindow.screen_width * 0.92, BattleWindow.screen_height * 0.13))
    BattleWindow.screen.blit(pokemon_list_menu_deactive2,
                             (BattleWindow.screen_width * 0.352, BattleWindow.screen_height * 0.18))
    BattleWindow.screen.blit(image_pokemon_deactive2,
                             (BattleWindow.screen_width * 0.40, BattleWindow.screen_height * 0.215))
    BattleWindow.screen.blit(draw_pokemon_name2, (BattleWindow.screen_width * 0.54, BattleWindow.screen_height * 0.225))
    BattleWindow.screen.blit(draw_hp_number_actual2,
                             (BattleWindow.screen_width * 0.84, BattleWindow.screen_height * 0.285))
    BattleWindow.screen.blit(draw_hp_number_total2,
                             (BattleWindow.screen_width * 0.92, BattleWindow.screen_height * 0.285))
    BattleWindow.screen.blit(pokemon_list_menu_deactive3,
                             (BattleWindow.screen_width * 0.352, BattleWindow.screen_height * 0.335))
    BattleWindow.screen.blit(image_pokemon_deactive3,
                             (BattleWindow.screen_width * 0.40, BattleWindow.screen_height * 0.37))
    BattleWindow.screen.blit(draw_pokemon_name3, (BattleWindow.screen_width * 0.54, BattleWindow.screen_height * 0.38))
    BattleWindow.screen.blit(draw_hp_number_actual3,
                             (BattleWindow.screen_width * 0.84, BattleWindow.screen_height * 0.44))
    BattleWindow.screen.blit(draw_hp_number_total3,
                             (BattleWindow.screen_width * 0.92, BattleWindow.screen_height * 0.44))
    BattleWindow.screen.blit(pokemon_list_menu_deactive4,
                             (BattleWindow.screen_width * 0.352, BattleWindow.screen_height * 0.49))
    BattleWindow.screen.blit(image_pokemon_deactive4,
                             (BattleWindow.screen_width * 0.40, BattleWindow.screen_height * 0.525))
    BattleWindow.screen.blit(draw_pokemon_name4, (BattleWindow.screen_width * 0.54, BattleWindow.screen_height * 0.535))
    BattleWindow.screen.blit(draw_hp_number_actual4,
                             (BattleWindow.screen_width * 0.84, BattleWindow.screen_height * 0.595))
    BattleWindow.screen.blit(draw_hp_number_total4,
                             (BattleWindow.screen_width * 0.92, BattleWindow.screen_height * 0.595))
    BattleWindow.screen.blit(pokemon_list_menu_deactive5,
                             (BattleWindow.screen_width * 0.352, BattleWindow.screen_height * 0.645))
    BattleWindow.screen.blit(image_pokemon_deactive5,
                             (BattleWindow.screen_width * 0.40, BattleWindow.screen_height * 0.68))
    BattleWindow.screen.blit(draw_pokemon_name5, (BattleWindow.screen_width * 0.54, BattleWindow.screen_height * 0.69))
    BattleWindow.screen.blit(draw_hp_number_actual5,
                             (BattleWindow.screen_width * 0.84, BattleWindow.screen_height * 0.75))
    BattleWindow.screen.blit(draw_hp_number_total5,
                             (BattleWindow.screen_width * 0.92, BattleWindow.screen_height * 0.75))
    BattleWindow.screen.blit(text_description, (BattleWindow.screen_width * 0.05, BattleWindow.screen_height * 0.87))
    BattleWindow.screen.blit(text_exit, (BattleWindow.screen_width * 0.855, BattleWindow.screen_height * 0.875))


def create_pokemon_not_inbattle_menu(BattleWindow, pokemon_name, font_name, hp_actual, hp_total):
    """
    Create Pokemon image with its name and actual HP for team Pokemon not in battle.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param pokemon_name: Pokemon name.
    :param font_name: font name.
    :param hp_actual: Pokemon HP actual.
    :param hp_total: Pokemon HP total.
    :return: Every Pokemon info to draw on screen.
    """
    pokemon_list_menu_deactive = pygame.image.load('img/pokemon_team.png').convert_alpha()
    pokemon_list_menu_deactive = pygame.transform.scale(pokemon_list_menu_deactive,
                                                        (BattleWindow.screen_width * 0.66,
                                                         BattleWindow.screen_height * 0.18))
    image_pokemon_deactive = pygame.image.load(
        'img_pokemon_battle_png/' + pokemon_name.lower() + '.png').convert_alpha()
    image_pokemon_deactive = pygame.transform.scale(image_pokemon_deactive,
                                                    (BattleWindow.screen_width * 0.13,
                                                     BattleWindow.screen_height * 0.13))
    draw_pokemon_name = font_name.render(pokemon_name, False, (255, 255, 255))
    draw_hp_number_actual = font_name.render(str(hp_actual), False, (255, 255, 255))
    draw_hp_number_total = font_name.render(str(hp_total), False, (255, 255, 255))
    return pokemon_list_menu_deactive, image_pokemon_deactive, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total


def create_pokemon_inbattle_menu(BattleWindow, pokemon_name, font_name, hp_actual, hp_total):
    """
    Create Pokemon image with its name and actual HP for Pokemon in battle.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param pokemon_name: Pokemon name.
    :param font_name: font name.
    :param hp_actual: Pokemon HP actual.
    :param hp_total: Pokemon HP total.
    :return: Every Pokemon info to draw on screen.
    """
    pokemon_list_menu_active = pygame.image.load('img/my_pokemon.png').convert_alpha()
    pokemon_list_menu_active = pygame.transform.scale(pokemon_list_menu_active,
                                                      (BattleWindow.screen_width * 0.4,
                                                       BattleWindow.screen_height * 0.42))
    image_pokemon_active = pygame.image.load(
        'img_pokemon_battle_png/' + pokemon_name.lower() + '.png').convert_alpha()
    image_pokemon_active = pygame.transform.scale(image_pokemon_active,
                                                  (BattleWindow.screen_width * 0.15, BattleWindow.screen_height * 0.15))
    draw_pokemon_name = font_name.render(pokemon_name, False, (255, 255, 255))
    draw_hp_number_actual = font_name.render(str(hp_actual), False, (255, 255, 255))
    draw_hp_number_total = font_name.render(str(hp_total), False, (255, 255, 255))
    return pokemon_list_menu_active, image_pokemon_active, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total


def draw_HP_pokemon_choice_menu(BattleWindow):
    """
    Draw Pokemon HP in choice menu.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    renderHPBar(BattleWindow, BattleWindow.screen_width * 0.209, BattleWindow.screen_height * 0.022,
                (BattleWindow.screen_width * 0.129, BattleWindow.screen_height * 0.373),
                BattleWindow.model.me.team[0].battleHP,
                BattleWindow.model.me.team[0].battleHP_actual)  # HP actual pokemon
    renderHPBar(BattleWindow, BattleWindow.screen_width * 0.2, BattleWindow.screen_height * 0.022,
                (BattleWindow.screen_width * 0.77, BattleWindow.screen_height * 0.095),
                BattleWindow.model.me.team[1].battleHP,
                BattleWindow.model.me.team[1].battleHP_actual)  # HP pokemon 1
    renderHPBar(BattleWindow, BattleWindow.screen_width * 0.2, BattleWindow.screen_height * 0.022,
                (BattleWindow.screen_width * 0.77, BattleWindow.screen_height * 0.252),
                BattleWindow.model.me.team[2].battleHP,
                BattleWindow.model.me.team[2].battleHP_actual)  # HP pokemon 2
    renderHPBar(BattleWindow, BattleWindow.screen_width * 0.2, BattleWindow.screen_height * 0.022,
                (BattleWindow.screen_width * 0.77, BattleWindow.screen_height * 0.408),
                BattleWindow.model.me.team[3].battleHP,
                BattleWindow.model.me.team[3].battleHP_actual)  # HP pokemon 3
    renderHPBar(BattleWindow, BattleWindow.screen_width * 0.2, BattleWindow.screen_height * 0.022,
                (BattleWindow.screen_width * 0.77, BattleWindow.screen_height * 0.563),
                BattleWindow.model.me.team[4].battleHP,
                BattleWindow.model.me.team[4].battleHP_actual)  # HP pokemon 4
    renderHPBar(BattleWindow, BattleWindow.screen_width * 0.2, BattleWindow.screen_height * 0.022,
                (BattleWindow.screen_width * 0.77, BattleWindow.screen_height * 0.718),
                BattleWindow.model.me.team[5].battleHP,
                BattleWindow.model.me.team[5].battleHP_actual)  # HP pokemon 5


def move_rect(surface, posx, posy):
    """
    Move render surface on screen.
    :param surface: surface to move.
    :param posx: new x coordinate.
    :param posy: new y coordinate.
    :return: Surface in new position.
    """
    play_game_rect = surface.get_rect()
    play_game_rect.x = posx
    play_game_rect.y = posy
    return play_game_rect


def hide_buttons(BattleWindow):
    """
    Hide buttons.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    BattleWindow.btn_change_pokemon.hide()
    BattleWindow.btn_quit.hide()
    BattleWindow.btn_move1.hide()
    BattleWindow.btn_move2.hide()
    BattleWindow.btn_move3.hide()
    BattleWindow.btn_move4.hide()


def exit_battle_operations(BattleWindow):
    """
    Necessary operations before exit from battle and close the game.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    utils.reset_team_stats(BattleWindow.model.me)
    utils.reset_team_stats(BattleWindow.model.enemy)
    BattleWindow.model.enemy.team = []
    BattleWindow.model.enemy.name = ''
    BattleWindow.run = False


def basic_events(BattleWindow):
    """
    Handle basic events as they happen
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            BattleWindow.run = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element.most_specific_combined_id == BattleWindow.btn_quit.most_specific_combined_id:
                BattleWindow.exit_battle = True
        BattleWindow.manager.process_events(event)


def update_manager_and_display(BattleWindow):
    """
    Update manager to display objects on screen.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :return:
    """
    time_delta = BattleWindow.clock.tick(BattleWindow.FPS) / 1000.0
    BattleWindow.manager.update(time_delta)

    BattleWindow.manager.draw_ui(BattleWindow.screen)
    pygame.display.update()


def wait(BattleWindow, wait, show_button, show_type_img):
    """
    It allows waiting for visualize animations on screen.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param wait: time to wait.
    :param show_button: choose if show/hide buttons.
    :param show_type_img: choose if show Pokemon move type images.
    :return:
    """
    k = 0
    while k < wait:
        BattleWindow.clock.tick(BattleWindow.FPS)
        basic_events(BattleWindow)

        BattleWindow.update_battle_window(show_button, show_type_img)
        draw_hp(BattleWindow, BattleWindow.model.me.team[0].battleHP_actual,
                                       BattleWindow.model.enemy.team[0].battleHP_actual)

        update_manager_and_display(BattleWindow)
        k += 1


def start_battle_animations(BattleWindow, trainer_me, trainer_enemy, show_button, show_type_img):
    """
    Show initials animations of battle.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param trainer_me: frames trainer me to show.
    :param trainer_enemy: frames trainer enemy to show.
    :param show_button: choose if show/hide buttons.
    :param show_type_img: choose if show Pokemon move type images.
    :return:
    """
    k = 0
    wait_frame = 30
    while k < wait_frame:
        BattleWindow.clock.tick(BattleWindow.FPS)
        basic_events(BattleWindow)

        BattleWindow.update_battle_window(show_button, show_type_img)
        draw_hp(BattleWindow, BattleWindow.model.me.team[0].battleHP_actual,
                                       BattleWindow.model.enemy.team[0].battleHP_actual)
        trainer_img = pygame.transform.scale(trainer_me[k // 6], (
            trainer_me[k // 6].get_width() * 4, trainer_me[k // 6].get_height() * 4)).convert_alpha()
        BattleWindow.screen.blit(trainer_img, (-BattleWindow.screen_width * 0.02, BattleWindow.screen_height * 0.445))
        trainer_img_enemy = pygame.transform.scale(trainer_enemy[k // 10], (
            trainer_enemy[k // 10].get_width() * 3, trainer_enemy[k // 10].get_height() * 3)).convert_alpha()
        BattleWindow.screen.blit(trainer_img_enemy,
                                 (BattleWindow.screen_width * 0.85, BattleWindow.screen_height * 0.04))

        update_manager_and_display(BattleWindow)
        k += 1


def pokeball_animations(BattleWindow, wait_frame, show_button, show_type_img, open_pokeball, pokemon_me, pokemon_enemy,
                        animation_me, animation_enemy):
    """
    Pokeball animations on screen.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param wait_frame: frame to wait to visualize animations.
    :param show_button: choose if show/hide buttons.
    :param show_type_img: choose if show Pokemon move type images.
    :param open_pokeball: choose if open pokeball animation or the close one.
    :param pokemon_me: Pokemon player me in game.
    :param pokemon_enemy: Pokemon player enemy in game.
    :param animation_me: choose if animation Player me.
    :param animation_enemy: choose if animation Player enemy.
    :return:
    """
    k = 0
    while k < wait_frame:
        BattleWindow.clock.tick(BattleWindow.FPS)
        basic_events(BattleWindow)

        BattleWindow.update_battle_window(show_button, show_type_img)
        draw_hp(BattleWindow, BattleWindow.model.me.team[0].battleHP_actual,
                                       BattleWindow.model.enemy.team[0].battleHP_actual)
        if animation_enemy:
            pokeball_type = pokemon_enemy.pokeball
            filename = utils.read_pokeball(open_pokeball, pokeball_type)
            pokeball_image_enemy = pygame.image.load('img/pokeballs/' + filename + '.png').convert_alpha()
            pokeball_image_enemy = pygame.transform.flip(pokeball_image_enemy, True, False)
            pokeball_image_enemy = pygame.transform.scale(pokeball_image_enemy, (
                pokeball_image_enemy.get_width() * 2, pokeball_image_enemy.get_height() * 2)).convert_alpha()
            if open_pokeball:
                BattleWindow.screen.blit(pokeball_image_enemy,
                                         (BattleWindow.screen_width * 0.82, BattleWindow.screen_height * 0.22))
            else:
                BattleWindow.screen.blit(pokeball_image_enemy,
                                         (BattleWindow.screen_width * 0.82, BattleWindow.screen_height * 0.23))

        if animation_me:
            pokeball_type = pokemon_me.pokeball
            filename = utils.read_pokeball(open_pokeball, pokeball_type)
            pokeball_image = pygame.image.load('img/pokeballs/' + filename + '.png').convert_alpha()
            pokeball_image = pygame.transform.scale(pokeball_image, (
                pokeball_image.get_width() * 3, pokeball_image.get_height() * 3)).convert_alpha()
            BattleWindow.screen.blit(pokeball_image,
                                     (BattleWindow.screen_width * 0.22, BattleWindow.screen_height * 0.68))

        update_manager_and_display(BattleWindow)
        k += 1


def explosion_animations(BattleWindow, show_button, show_type_img, animation_pokemon_me):
    """
    Explosion animations on Pokemon when a another Pokemon attack.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param show_button: choose if show/hide buttons.
    :param show_type_img: choose if show Pokemon move type images.
    :param animation_pokemon_me: choose if visualize animation on Pokemon player me or enemy.
    :return:
    """
    k = 0
    wait_frame = 39
    while k < wait_frame:
        BattleWindow.clock.tick(BattleWindow.FPS)
        basic_events(BattleWindow)

        BattleWindow.update_battle_window(show_button, show_type_img)
        draw_hp(BattleWindow, BattleWindow.model.me.team[0].battleHP_actual,
                                       BattleWindow.model.enemy.team[0].battleHP_actual)
        if animation_pokemon_me:
            explosion = pygame.transform.scale(BattleWindow.explosion_sheet[k], (
                BattleWindow.explosion_sheet[k].get_width() * 1.5,
                BattleWindow.explosion_sheet[k].get_height() * 1.5)).convert_alpha()
            BattleWindow.screen.blit(explosion, (BattleWindow.screen_width * 0.15, BattleWindow.screen_height * 0.58))
        else:
            BattleWindow.screen.blit(BattleWindow.explosion_sheet[k],
                                     (BattleWindow.screen_width * 0.79, BattleWindow.screen_height * 0.15))

        update_manager_and_display(BattleWindow)
        k += 1


def reduce_hp_bar(BattleWindow, show_button, show_type_img, player_attacker, reduced_hp):
    """
    Animation to reduce HP bar of a Pokemon.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param show_button: choose if show/hide buttons.
    :param show_type_img: choose if show Pokemon move type images.
    :param player_attacker: choose if get HP player me or enemy.
    :param reduced_hp: attack damage received.
    :return:
    """
    if player_attacker:
        actual_hp = BattleWindow.model.enemy.team[0].battleHP_actual
    else:
        actual_hp = BattleWindow.model.me.team[0].battleHP_actual
    k = 0
    reduced_hp = abs(reduced_hp)
    while k < reduced_hp:
        BattleWindow.clock.tick(BattleWindow.FPS)
        basic_events(BattleWindow)

        BattleWindow.update_battle_window(show_button, show_type_img)
        if player_attacker:
            draw_hp(BattleWindow, BattleWindow.model.me.team[0].battleHP_actual,
                                           actual_hp + reduced_hp - k)
        else:
            draw_hp(BattleWindow, actual_hp + reduced_hp - k,
                                           BattleWindow.model.enemy.team[0].battleHP_actual)
        update_manager_and_display(BattleWindow)
        k += 1
