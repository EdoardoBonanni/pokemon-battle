import pygame
import random
from Spritesheet.Spritesheet import Spritesheet
from models.Pokemon import Pokemon
from models.Move import Move
from utility import show_screen_elements


def create_color_mapping():
    """
    Function that map every Pokemon type in a color.
    :return: Dictionary created from mapping.
    """
    color_mapping = {'water': pygame.Color(104, 144, 240), 'steel': pygame.Color(184, 184, 208),
                     'rock': pygame.Color(184, 160, 56), 'psychic': pygame.Color(248, 88, 136),
                     'poison': pygame.Color(160, 64, 160), 'normal': pygame.Color(168, 168, 120),
                     'ice': pygame.Color(152, 216, 216), 'ground': pygame.Color(224, 192, 104),
                     'grass': pygame.Color(120, 200, 80), 'ghost': pygame.Color(112, 88, 152),
                     'flying': pygame.Color(168, 144, 240), 'fire': pygame.Color(240, 128, 48),
                     'fighting': pygame.Color(192, 48, 40), 'electric': pygame.Color(248, 208, 48),
                     'dragon': pygame.Color(112, 56, 248), 'dark': pygame.Color(112, 88, 72),
                     'bug': pygame.Color(168, 184, 32), 'null': pygame.Color(104, 160, 144)}
    return color_mapping


def readCSV_moves(filename):
    """
    Read CSV that contains all attributes for Pokemon moves.
    :param filename: Filename CSV.
    :return: Dictionary with all attributes for Pokemon moves.
    """
    dict_moves = {}
    fin = open(filename, 'r')
    for line in fin:
        line = line.strip()
        move_list = line.split(",")
        if any(map(str.isdigit, move_list[0])):
            id = move_list[0]
            name = move_list[1]
            description = move_list[2]
            type = move_list[3]
            kind = move_list[4]
            power = int(move_list[5])
            accuracy = move_list[6]
            pp = int(move_list[7])
            move = Move(id, name, description, type, kind, power, accuracy, pp)
            dict_moves[
                name.lower()] = move  # Creating dictionary with key = name and value is the move object.
    fin.close()
    return dict_moves


def readCSV_Pokemon(dict_moves, filename):
    """
    Read CSV that contains all attributes for Pokemon.
    :param dict_moves: Dictionary of Pokemon moves.
    :param filename: Filename CSV.
    :return: Dictionary of all Pokemon.
    """
    dict_Pokemon = {}
    fin = open(filename, 'r')
    for line in fin:
        line = line.strip()
        poke_list = line.split(",")
        if any(map(str.isdigit, poke_list[0])):
            id = poke_list[0]
            name = poke_list[1]
            type1 = poke_list[2]
            type2 = poke_list[3]
            hp = int(poke_list[4])
            atk = int(poke_list[5])
            defense = int(poke_list[6])
            spAtk = int(poke_list[7])
            spDef = int(poke_list[8])
            speed = int(poke_list[9])
            move1 = dict_moves[poke_list[10].lower()]
            move2 = dict_moves[poke_list[11].lower()]
            move3 = dict_moves[poke_list[12].lower()]
            move4 = dict_moves[poke_list[13].lower()]
            total = hp + atk + defense + spAtk + spDef + speed
            pokemon = Pokemon(id, name, type1, type2, hp, atk, defense, spAtk, spDef, speed, total, move1, move2, move3,
                              move4)
            dict_Pokemon[name] = pokemon  # Creating dictionary with key = name and value is the Pokemon object.
    fin.close()
    return dict_Pokemon


def read_type_advantages(filename):
    """
    Read from CSV type advantages among Pokemon.
    :param filename: Filename CSV.
    :return: Dictionary of type advantages.
    """
    type_advantages = {}
    fin = open(filename, 'r')
    for line in fin:
        line = line.strip()
        type_list = line.split(",")
        if any(map(str.isdigit, type_list[0])):
            type_advantages[(type_list[1], type_list[2])] = [type_list[1], type_list[2], type_list[
                3]]  # Creating dictionary with key = (type1, type2) and value the informations of type advantages.
    fin.close()
    return type_advantages


def statMod(stat_stage):
    """
    Stat modification function that will be called inside the attack function if the move alters the defending Pokemon's stats.
    :param statStage: Current stats stage.
    :return: The multiplier that affects the value of the in-battle stat.
    """
    multiplier = 1
    if stat_stage == 1:
        multiplier = 1.5
    elif stat_stage == -1:
        multiplier = 2 / 3
    elif stat_stage == 2:
        multiplier = 2
    elif stat_stage == -2:
        multiplier = 1 / 2
    elif stat_stage == 3:
        multiplier = 2.5
    elif stat_stage == -3:
        multiplier = 0.4
    elif stat_stage == 4:
        multiplier = 3
    elif stat_stage == -4:
        multiplier = 1 / 3
    elif stat_stage == 5:
        multiplier = 3.5
    elif stat_stage == -5:
        multiplier = 2 / 7
    elif stat_stage == 6:
        multiplier = 4
    elif stat_stage == -6:
        multiplier = 1 / 4
    return multiplier


def read_spritesheet_trainer_me(filename):
    """
    Read sprite-sheet for trainer animation (player me).
    :param filename: Filename json.
    :return: sequence of images.
    """
    my_spritesheet = Spritesheet(filename)
    rand = random.randint(0, 1)
    trainer = []
    if rand == 0:
        for i in range(5):
            trainer.append(my_spritesheet.parse_sprite('trainer' + str(i + 1) + '.png'))
    else:
        for i in range(5):
            trainer.append(my_spritesheet.parse_sprite('f_trainer' + str(i + 1) + '.png'))
    return trainer


def read_spritesheet_trainer_enemy(filename):
    """
    Read sprite-sheet for trainer animation (player enemy).
    :param filename: Filename json.
    :return: sequence of images.
    """
    my_spritesheet = Spritesheet(filename)
    rand = random.randint(0, 3)
    trainer = []
    if rand == 0:
        for i in range(3):
            trainer.append(my_spritesheet.parse_sprite('brook' + str(i + 1) + '.png'))
    elif rand == 1:
        for i in range(3):
            trainer.append(my_spritesheet.parse_sprite('giovanni' + str(i + 1) + '.png'))
    elif rand == 2:
        for i in range(3):
            trainer.append(my_spritesheet.parse_sprite('lance' + str(i + 1) + '.png'))
    else:
        for i in range(3):
            trainer.append(my_spritesheet.parse_sprite('misty' + str(i + 1) + '.png'))
    return trainer


def read_spritesheet_explosion(filename):
    """
    Read sprite-sheet for explosion animation.
    :param filename: Filename json.
    :return: sequence of images.
    """
    my_spritesheet = Spritesheet(filename)
    explosion = []
    for i in range(39):
        explosion.append(my_spritesheet.parse_sprite('explosion' + str(i + 1) + '.png'))
    return explosion


def read_pokeball(pokeball_open, pokeball_type):
    """
    Choose a random pokeball to visualize.
    :param pokeball_open: choose if pokeball is open or not.
    :param pokeball_type: it's the random value for pokeball choice.
    :return: pokeball filename to read.
    """
    if pokeball_open:
        open = '_open'
    else:
        open = ''
    if pokeball_type == 0:
        filename = 'pk' + open
    elif pokeball_type == 1:
        filename = 'pk_mega' + open
    elif pokeball_type == 2:
        filename = 'pk_ultra' + open
    else:
        filename = 'pk_master' + open
    return filename


def choose_enemy_move(BattleWindow):
    """
    Choose a random move for enemy Pokemon.
    :param BattleWindow: PyGame window.
    :return: the move selected.
    """
    if BattleWindow.model.enemy.team[0].move1.pp_remain <= 0 and BattleWindow.model.enemy.team[
        0].move2.pp_remain <= 0 and \
            BattleWindow.model.enemy.team[0].move3.pp_remain <= 0 and BattleWindow.model.enemy.team[
        0].move4.pp_remain <= 0:
        return BattleWindow.model.enemy.team[0].move1
    while True:
        # random_number = 4  # used for testing.
        random_number = random.randint(1, 4)
        if random_number == 1 and BattleWindow.model.enemy.team[0].move1.pp_remain > 0:
            return BattleWindow.model.enemy.team[0].move1
        elif random_number == 2 and BattleWindow.model.enemy.team[0].move2.pp_remain > 0:
            return BattleWindow.model.enemy.team[0].move2
        elif random_number == 3 and BattleWindow.model.enemy.team[0].move3.pp_remain > 0:
            return BattleWindow.model.enemy.team[0].move3
        elif random_number == 4 and BattleWindow.model.enemy.team[0].move4.pp_remain > 0:
            return BattleWindow.model.enemy.team[0].move4


def update_special_attack(BattleWindow, special_attack, move, player_me):
    """
    Update the values of special moves.
    :param BattleWindow: PyGame window.
    :param special_attack: choose if it is a special attack.
    :param move: Pokemon move.
    :param player_me: choose if it is Pokemon enemy or me.
    :return:
    """
    if player_me:
        if special_attack:
            BattleWindow.special_moves_me = move
        else:
            BattleWindow.special_moves_me = None
    else:
        if special_attack:
            BattleWindow.special_moves_enemy = move
        else:
            BattleWindow.special_moves_enemy = None


def reset_special_attack(BattleWindow, count_move, player_me):
    """
    Reset the values of special moves.
    :param BattleWindow: PyGame window.
    :param count_move: Counter of special move.
    :param player_me: choose if it is Pokemon enemy or me.
    :return:
    """
    if player_me:
        if count_move == 0:
            BattleWindow.special_moves_me = None
            BattleWindow.count_move_me = 0
    else:
        if count_move == 0:
            BattleWindow.special_moves_enemy = None
            BattleWindow.count_move_enemy = 0


def reset_stats(pokemon):
    """
    Reset Pokemon stats.
    :param pokemon: Pokemon.
    :return:
    """
    pokemon.battleATK = pokemon.originalATK
    pokemon.battleDEF = pokemon.originalDEF
    pokemon.battleSpATK = pokemon.originalSpATK
    pokemon.battleSpDEF = pokemon.originalSpDEF
    pokemon.battleSpeed = pokemon.originalSpeed
    pokemon.atkStage = 0
    pokemon.defStage = 0
    pokemon.spAtkStage = 0
    pokemon.spDefStage = 0
    pokemon.speedStage = 0


def reset_team_stats(player):
    """
    Reset Pokemon team stats.
    :param player: Player me or enemy.
    :return:
    """
    for pokemon in player.team:
        pokemon.battleHP_actual = pokemon.battleHP
        pokemon.move1.pp_remain = pokemon.move1.pp
        pokemon.move2.pp_remain = pokemon.move2.pp
        pokemon.move3.pp_remain = pokemon.move3.pp
        pokemon.move4.pp_remain = pokemon.move4.pp
        reset_stats(pokemon)


def update_appearance_pokemon(BattleWindow, player_attacker, value):
    """
    Update the appearance of Pokemon based on moves in the window.
    :param BattleWindow: PyGame window.
    :param player_attacker: Player me or enemy.
    :param value: choose if Pokemon is visible or not.
    :return:
    """
    if player_attacker:
        BattleWindow.pokemon_me_visible = value
    else:
        BattleWindow.pokemon_enemy_visible = value


def search_move_pokemon(pokemon, move_name):
    """
    Search a Pokemon move.
    :param pokemon: Pokemon.
    :param move_name: move name.
    :return: move selected.
    """
    if pokemon.move1.name == move_name:
        move = pokemon.move1
    elif pokemon.move2.name == move_name:
        move = pokemon.move2
    elif pokemon.move3.name == move_name:
        move = pokemon.move3
    else:
        move = pokemon.move4
    return move


def search_pokemon(pokemon_team, pokemon_name):
    """
    Search a Pokemon.
    :param pokemon_team: Pokemon team.
    :param pokemon_name: Pokemon name.
    :return: index of Pokemon selected or -1.
    """
    for i in range(len(pokemon_team)):
        if pokemon_team[i].name == pokemon_name:
            return i
    return -1


def determine_special_attack(BattleWindow, move, pokemon, count_move, player_me):
    """
    Determine the special move type of the Pokemon.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param move: Pokemon move.
    :param pokemon: Pokemon.
    :param count_move: counter of special move.
    :param player_me: check if player me or enemy.
    :return: [attack_move, count_move, special_attack] = check if it's an attack move, counter of special move and the special attack move.
    """
    attack_move = True
    special_attack = False
    update_appearance_pokemon(BattleWindow, player_me, True)
    if move.name.lower() == 'solarbeam' and count_move == 0:
        BattleWindow.description_battle = pokemon.name + ' absorbed light!'
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'fly' and count_move == 0:
        BattleWindow.description_battle = pokemon.name + ' flew up high!'
        update_appearance_pokemon(BattleWindow, player_me, False)
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'dig' and count_move == 0:
        BattleWindow.description_battle = pokemon.name + ' dug underground!'
        update_appearance_pokemon(BattleWindow, player_me, False)
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'hyper beam':
        if count_move == 0:
            count_move += 1
            special_attack = True
        else:
            BattleWindow.description_battle = pokemon.name + ' must recharge!'
            count_move = 0
            attack_move = False
    else:
        count_move = 0
    if not attack_move:
        show_screen_elements.wait(BattleWindow, 30, False, False)
    return attack_move, count_move, special_attack
