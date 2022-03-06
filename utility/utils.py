import pygame
import random
from Spritesheet.spritesheet import Spritesheet

def create_color_mapping():
    color_mapping = {'water': pygame.Color(104, 144, 240), 'steel': pygame.Color(184, 184, 208),
                     'rock': pygame.Color(184, 160, 56), 'psychic': pygame.Color(248, 88, 136),
                     'poison': pygame.Color(160, 64, 160), 'normal': pygame.Color(168, 168, 120),
                     'ice': pygame.Color(152, 216, 216), 'ground': pygame.Color(224, 192, 104),
                     'grass': pygame.Color(120, 200, 80), 'ghost': pygame.Color(112, 88, 152),
                     'flying': pygame.Color(168, 144, 240), 'fire': pygame.Color(240, 128, 48),
                     'fighting': pygame.Color(192, 48, 40), 'electric': pygame.Color(248, 208, 48),
                     'dragon': pygame.Color(112, 56, 248), 'dark': pygame.Color(80, 120, 136),
                     'bug': pygame.Color(168, 184, 32), 'null': pygame.Color(104, 160, 144)}
    return color_mapping

def read_type_advantages(filename):
    type_advantages = {}
    fin = open(filename, 'r')
    for line in fin:
        line = line.strip()
        type_list = line.split(",")
        if any(map(str.isdigit, type_list[0])):
            type_advantages[(type_list[1], type_list[2])] = [type_list[1], type_list[2], type_list[3]]  # Creating dicticionary with key = (type1, type2) and value the informations of type advantages
    fin.close()
    return type_advantages

# Stat modification function; will be called inside the attack function if the move alters the defending Pokemon's stats
# Takes the current statStage as input and returns a multiplier that will be used to calculate the new statStage
def statMod(statStage):
    multiplier = 1
    if statStage == 1:
        multiplier = 1.5
    elif statStage == -1:
        multiplier = 2/3
    elif statStage == 2:
        multiplier = 2
    elif statStage == -2:
        multiplier = 1/2
    elif statStage == 3:
        multiplier = 2.5
    elif statStage == -3:
        multiplier = 0.4
    elif statStage == 4:
        multiplier = 3
    elif statStage == -4:
        multiplier = 1/3
    elif statStage == 5:
        multiplier = 3.5
    elif statStage == -5:
        multiplier = 2/7
    elif statStage == 6:
        multiplier = 4
    elif statStage == -6:
        multiplier = 1/4
    return multiplier  # This multiplier affects the value of the in-battle stat

def read_spritesheet_trainer_me(filename):
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
    my_spritesheet = Spritesheet(filename)
    explosion = []
    for i in range(39):
        explosion.append(my_spritesheet.parse_sprite('explosion' + str(i + 1) + '.png'))
    return explosion

def read_pokeball(pokeball_open, pokeball_type):
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

def choose_enemy_move(battle_window):
    if battle_window.model.enemy.team[0].move1.pp_remain <= 0 and battle_window.model.enemy.team[0].move2.pp_remain <= 0 and \
        battle_window.model.enemy.team[0].move3.pp_remain <= 0 and battle_window.model.enemy.team[0].move4.pp_remain <= 0:
        return battle_window.model.enemy.team[0].move1
    while True:
        random_number = random.randint(1, 4)
        if random_number == 1 and battle_window.model.enemy.team[0].move1.pp_remain > 0:
            return battle_window.model.enemy.team[0].move1
        elif random_number == 2 and battle_window.model.enemy.team[0].move2.pp_remain > 0:
            return battle_window.model.enemy.team[0].move2
        elif random_number == 3 and battle_window.model.enemy.team[0].move3.pp_remain > 0:
            return battle_window.model.enemy.team[0].move3
        elif random_number == 4 and battle_window.model.enemy.team[0].move4.pp_remain > 0:
            return battle_window.model.enemy.team[0].move4
    # return battle_window.model.enemy.team[0].move4

def update_special_attack(battle_window, special_attack, move, player_me):
    if player_me:
        if special_attack:
            battle_window.special_moves_me = move
        else:
            battle_window.special_moves_me = None
    else:
        if special_attack:
            battle_window.special_moves_enemy = move
        else:
            battle_window.special_moves_enemy = None

def reset_special_attack(battle_window, count_move, player_me):
    if player_me:
        if count_move == 0:
            battle_window.special_moves_me = None
            battle_window.count_move_me = 0
    else:
        if count_move == 0:
            battle_window.special_moves_enemy = None
            battle_window.count_move_enemy = 0

def reset_stats(pokemon):
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
    for pokemon in player.team:
        pokemon.battleHP_actual = pokemon.battleHP
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

def update_appearance_pokemon(battle_window, player_attacker, value):
    if player_attacker:
        battle_window.pokemon_me_visible = value
    else:
        battle_window.pokemon_enemy_visible = value

def search_move_pokemon(pokemon, move_name):
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
    for i in range(len(pokemon_team)):
        if pokemon_team[i].name == pokemon_name:
            return i
    return -1