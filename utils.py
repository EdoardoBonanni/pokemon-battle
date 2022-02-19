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
                     'dragon': pygame.Color(112, 56, 248), 'dark': pygame.Color(112, 88, 72),
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

def checks_2_turns_attack(battle_window, move_me, move_enemy):
    if battle_window.special_moves_me and battle_window.special_moves_enemy:
        check_attacks(battle_window, battle_window.special_moves_me, battle_window.special_moves_enemy)
    elif battle_window.special_moves_me:
        check_attacks(battle_window, battle_window.special_moves_me, move_enemy)
    elif battle_window.special_moves_enemy:
        check_attacks(battle_window, move_me, battle_window.special_moves_enemy)
    else:
        check_attacks(battle_window, move_me, move_enemy)

def check_attacks(battle_window, move_me, move_enemy):
    battle_window.pokemon_changed_not_fainted = False
    if move_me == None:
        # _ = attack(battle_window, battle_window.model.enemy, battle_window.model.me, move_enemy, False, battle_window.count_move_enemy, None, battle_window.count_move_me)
        attack_move, count_move, special_attack = determine_special_attack(battle_window, move_enemy, battle_window.model.enemy.team[0], battle_window.count_move_enemy, False)
        battle_window.count_move_enemy = count_move
        update_special_attack(battle_window, special_attack, move_enemy, False)
        if attack_move:
            second_pokemon_fainted, first_pokemon_fainted, count_move = attack(battle_window, battle_window.model.enemy, battle_window.model.me, move_enemy, False, battle_window.count_move_enemy, battle_window.special_moves_me, battle_window.count_move_me)
            reset_special_attack(battle_window, count_move, False)
    else:
        turn(battle_window, move_me, move_enemy)

def turn(battle_window, move_me, move_enemy):
    first_attack_me = determine_first_attacker(battle_window, move_me, move_enemy)
    first_pokemon_fainted = False
    second_pokemon_fainted = False
    if first_attack_me:
        attack_move, count_move, special_attack = determine_special_attack(battle_window, move_me, battle_window.model.me.team[0], battle_window.count_move_me, True)
        battle_window.count_move_me = count_move
        update_special_attack(battle_window, special_attack, move_me, True)
        if attack_move:
            first_pokemon_fainted, second_pokemon_fainted, count_move = attack(battle_window, battle_window.model.me, battle_window.model.enemy, move_me, True, battle_window.count_move_me, battle_window.special_moves_enemy, battle_window.count_move_enemy)
            reset_special_attack(battle_window, count_move, True)
        if not first_pokemon_fainted and not second_pokemon_fainted:
            attack_move, count_move, special_attack = determine_special_attack(battle_window, move_enemy, battle_window.model.enemy.team[0], battle_window.count_move_enemy, False)
            battle_window.count_move_enemy = count_move
            update_special_attack(battle_window, special_attack, move_enemy, False)
            if attack_move:
                second_pokemon_fainted, first_pokemon_fainted, count_move = attack(battle_window, battle_window.model.enemy, battle_window.model.me, move_enemy, False, battle_window.count_move_enemy, battle_window.special_moves_me, battle_window.count_move_me)
                reset_special_attack(battle_window, count_move, False)
        if first_pokemon_fainted:
            battle_window.count_move_me = 0
        if second_pokemon_fainted:
            battle_window.count_move_enemy = 0
    else:
        attack_move, count_move, special_attack = determine_special_attack(battle_window, move_enemy, battle_window.model.enemy.team[0], battle_window.count_move_enemy, False)
        battle_window.count_move_enemy = count_move
        update_special_attack(battle_window, special_attack, move_enemy, False)
        if attack_move:
            first_pokemon_fainted, second_pokemon_fainted, count_move = attack(battle_window, battle_window.model.enemy, battle_window.model.me, move_enemy, False, battle_window.count_move_enemy, battle_window.special_moves_me, battle_window.count_move_me)
            reset_special_attack(battle_window, count_move, False)
        if not first_pokemon_fainted and not second_pokemon_fainted:
            attack_move, count_move, special_attack = determine_special_attack(battle_window, move_me, battle_window.model.me.team[0], battle_window.count_move_me, True)
            battle_window.count_move_me = count_move
            update_special_attack(battle_window, special_attack, move_me, True)
            if attack_move:
                second_pokemon_fainted, first_pokemon_fainted, count_move = attack(battle_window, battle_window.model.me, battle_window.model.enemy, move_me, True, battle_window.count_move_me, battle_window.special_moves_enemy, battle_window.count_move_enemy)
                reset_special_attack(battle_window, count_move, True)
        if first_pokemon_fainted:
            battle_window.count_move_enemy = 0
        if second_pokemon_fainted:
            battle_window.count_move_me = 0

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

def determine_special_attack(battle_window, move, pokemon, count_move, player_me):
    attack_move = True
    special_attack = False
    update_appearance_pokemon(battle_window, player_me, True)
    if move.name.lower() == 'solarbeam' and count_move == 0:
        battle_window.description_battle = pokemon.name + ' absorbed light!'
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'fly' and count_move == 0:
        battle_window.description_battle = pokemon.name + ' flew up high!'
        update_appearance_pokemon(battle_window, player_me, False)
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'dig' and count_move == 0:
        battle_window.description_battle = pokemon.name + ' dug underground!'
        update_appearance_pokemon(battle_window, player_me, False)
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'hyper beam':
        if count_move == 0:
            count_move += 1
            special_attack = True
        else:
            battle_window.description_battle = pokemon.name + ' must recharge!'
            count_move = 0
            attack_move = False
    else:
        count_move = 0
    if not attack_move:
        battle_window.wait(30, False, False)
    return attack_move, count_move, special_attack

def determine_first_attacker(battle_window, move_me, move_enemy):
    if move_me.name == 'ExtremeSpeed' and move_enemy.name != 'ExtremeSpeed':
        first_attack_me = True
    elif move_enemy.name == 'ExtremeSpeed' and move_me.name != 'ExtremeSpeed':
        first_attack_me = False
    else:
        if move_me.name == 'Quick Attack' and move_enemy.name != 'Quick Attack':
            first_attack_me = True
        elif move_enemy.name == 'Quick Attack' and move_me.name != 'Quick Attack':
            first_attack_me = False
        else:
            if battle_window.model.me.team[0].battleSpeed >= battle_window.model.enemy.team[0].battleSpeed:
                first_attack_me = True
            else:
                first_attack_me = False
    return first_attack_me

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

def attack(battle_window, attacker, defender, move, player_attacker, count_move_attacker, special_moves_defender, count_move_defender):
    # attacker and defender can be self.me or self.enemy
    # This modifier is used in damage calculations; it takes into account type advantage and STAB bonus
    modifier = 1
    # Calculating Type advantages using "Type Advantages.csv" file
    for key in battle_window.model.type_advantages:
        # If the attacking and defending types match up, multiply the modifier by the damage multiplier from the list
        if battle_window.model.type_advantages[key][0] == move.type and battle_window.model.type_advantages[key][1] == defender.team[0].type1:
            modifier *= float(battle_window.model.type_advantages[key][2])

        # Didn't use elif; Just in case you get a 4x or 0.25x modifier based on double type
        if battle_window.model.type_advantages[key][0] == move.type and battle_window.model.type_advantages[key][1] == defender.team[0].type2:
            modifier *= float(battle_window.model.type_advantages[key][2])

    attacker_fainted = False
    defender_fainted = False
    always_miss_attack = False
    if special_moves_defender:
        if special_moves_defender.name.lower() == 'fly' and count_move_defender == 1:
            always_miss_attack = True
        elif special_moves_defender.name.lower() == 'dig' and count_move_defender == 1 and move.name.lower() != 'earthquake':
            always_miss_attack = True
        update_appearance_pokemon(battle_window, player_attacker, True)

    if move.kind != "Physical" and move.kind != 'Special':
        move_accuracy = 100
    else:
        move_accuracy = int(move.accuracy.replace('%', ''))
    prob = random.random() * 100
    if prob > move_accuracy or always_miss_attack:
        count_move_attacker = 0
        battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + ' but missed attack!'
        battle_window.wait(30, False, False)
    elif move.pp_remain <= 0:
        battle_window.description_battle = move.name + ' has no pp remain!'
        battle_window.wait(30, False, False)
    else:
        if modifier >= 2:
            effectiveness = 'super effective'
        elif modifier == 1:
            effectiveness = 'normal effective'
        elif modifier == 0:
            effectiveness = 'not effect'
        else:
            effectiveness = 'not very effective'

        # Calculating STAB (Same-type Attack Bonus)
        if move.type == attacker.team[0].type1:
            modifier *= attacker.team[0].STAB

        elif move.type == attacker.team[0].type2:
            modifier *= attacker.team[0].STAB

        # Damage formula also has a random element
        critic_value = random.uniform(0.85, 1.0)
        modifier *= critic_value

        # Appending the useMove function to the output
        if move.kind == "Physical" or move.kind == "Special":
            if effectiveness == 'normal effective':
                battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + '.'
                if special_moves_defender:
                    if special_moves_defender.name.lower() != 'dig' and count_move_defender != 1 and move.name.lower() != 'earthquake':
                        battle_window.explosion_animations(False, False, not player_attacker)
                    else:
                        battle_window.wait(30, False, False)
                else:
                    battle_window.explosion_animations(False, False, not player_attacker)
            elif effectiveness == 'not effect':
                battle_window.description_battle = move.name + ' has no effect on ' + defender.team[0].name + '.'
                battle_window.wait(30, False, False)
            else:
                battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + '. It\'s ' + effectiveness + '.'
                if special_moves_defender:
                    if special_moves_defender.name.lower() != 'dig' and count_move_defender != 1 and move.name.lower() != 'earthquake':
                        battle_window.explosion_animations(False, False, not player_attacker)
                    else:
                        battle_window.wait(30, False, False)
                else:
                    battle_window.explosion_animations(False, False, not player_attacker)
        else:
            battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + '.'
            battle_window.wait(30, False, False)

        if critic_value > 0.98 and (move.kind == "Physical" or move.kind == "Special"):
            battle_window.description_battle = 'A critical hit!'
            battle_window.wait(30, False, False)

        # ATK/DEF or SpATK/SpDEF or Status? Using the Pokemon damage formula
        # If the move is "Physical", the damage formula will take into account attack and defense
        level = 100
        if move.kind == "Physical":
            damage = int((((2*level) + 10)/250 * (attacker.team[0].battleATK/defender.team[0].battleDEF) * move.power + 2) * modifier)
            hp_lost = defender.team[0].loseHP(damage)
            if move.name == 'Bonemerang' or move.name == 'Double Kick':
                damage *= 2
                battle_window.description_battle = move.name + ' hits 2 times.'
                battle_window.explosion_animations(False, False, not player_attacker)
        # If the move is "Special", the damage formula will take into account special attack and special defense
        elif move.kind == "Special":
            damage = int((((2*level) + 10)/250 * (attacker.team[0].battleSpATK/defender.team[0].battleSpDEF) * move.power + 2) * modifier)
            hp_lost = defender.team[0].loseHP(damage)
            if move.name == 'Giga Drain':
                gain_hp = abs(hp_lost) // 2
                gain_hp = attacker.team[0].gainHP(gain_hp)
        # Stat Changing moves
        else:
            # If the move is stat-changing, it does 0 damage and the modifier is set to 1 (so it doesn't return super effective or not very effective)
            hp_lost = 0
            if move.kind == "a+":
                attacker.team[0].atkStage +=1
                attacker.team[0].battleATK = attacker.team[0].originalATK * statMod(attacker.team[0].atkStage)
                battle_window.description_battle = attacker.team[0].name + '\'s attack rose!'

            elif move.kind == "d+":
                attacker.team[0].defStage +=1
                attacker.team[0].battleDEF = attacker.team[0].originalDEF * statMod(attacker.team[0].defStage)
                battle_window.description_battle = attacker.team[0].name + '\'s defense rose!'

            elif move.kind == "sa+":
                attacker.team[0].spAtkStage +=1
                attacker.team[0].battleSpATK = attacker.team[0].originalSpATK * statMod(attacker.team[0].spAtkStage)
                battle_window.description_battle = attacker.team[0].name + '\'s special attack rose!'

            elif move.kind == "sd+":
                attacker.team[0].spDefStage +=1
                attacker.team[0].battleSpDef = attacker.team[0].originalSpDEF * statMod(attacker.team[0].spDefStage)
                battle_window.description_battle = attacker.team[0].name + '\'s special defense rose!'

            elif move.kind == "s+":
                attacker.team[0].speedStage +=1
                attacker.team[0].battleSpeed = attacker.team[0].originalSpeed * statMod(attacker.team[0].speedStage)
                battle_window.description_battle = attacker.team[0].name + '\'s speed rose!'

            elif move.kind == "a+sa+":
                attacker.team[0].atkStage +=1
                attacker.team[0].spAtkStage +=1
                attacker.team[0].battleATK = attacker.team[0].originalATK * statMod(attacker.team[0].atkStage)
                attacker.team[0].battleSpATK = attacker.team[0].originalSpATK * statMod(attacker.team[0].spAtkStage)
                battle_window.description_battle = attacker.team[0].name + '\'s attack and special attack rose!'

            elif move.kind == "a-":
                defender.team[0].atkStage -= 1
                defender.team[0].battleATK = defender.team[0].originalATK * statMod(defender.team[0].atkStage)
                battle_window.description_battle = defender.team[0].name + ' attacks fell!'

            elif move.kind == "d-":
                defender.team[0].defStage -=1
                defender.team[0].battleDEF = defender.team[0].originalDEF * statMod(defender.team[0].defStage)
                battle_window.description_battle = defender.team[0].name + '\'s defense fell!'

            elif move.kind == "sa-":
                defender.team[0].spAtkStage -=1
                defender.team[0].battleSpATK = defender.team[0].originalSpATK * statMod(defender.team[0].spAtkStage)
                battle_window.description_battle = defender.team[0].name + '\'s special attack fell!'

            elif move.kind == "sd-":
                defender.team[0].spDefStage -=1
                defender.team[0].battleSpDEF = defender.team[0].originalSpDEF * statMod(defender.team[0].spDefStage)
                battle_window.description_battle = defender.team[0].name + '\'s special defense fell!'

            elif move.kind == "s-":
                defender.team[0].speedStage -=1
                defender.team[0].battleSpeed = defender.team[0].originalSpeed * statMod(defender.team[0].speedStage)
                battle_window.description_battle = defender.team[0].name + '\'s speed fell!'

            if move.name == 'Synthesis' or move.name == 'Moonlight':
                gain_hp = attacker.team[0].battleHP // 2
                gain_hp = attacker.team[0].gainHP(gain_hp)
                battle_window.description_battle = attacker.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP.'

        if (move.kind == "Physical" or move.kind == 'Special') and hp_lost != 0:
            battle_window.reduce_hp_bar(False, False, player_attacker, hp_lost)
            if move.name == 'Giga Drain':
                battle_window.description_battle = attacker.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP and ' + defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            else:
                battle_window.description_battle = defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            battle_window.wait(20, False, False)
        else:
            battle_window.wait(30, False, False)
        if move.name == 'Selfdestruct':
            attacker.team[0].battleHP_actual = 0
            battle_window.wait(15, False, False)
        move.pp_remain -= 1
        if defender.team[0].battleHP_actual == 0:
            pokemon_fainted(battle_window, player_attacker, defender.team[0])
            defender_fainted = True
        if attacker.team[0].battleHP_actual == 0:
            pokemon_fainted(battle_window, not player_attacker, attacker.team[0])
            attacker_fainted = True
    return attacker_fainted, defender_fainted, count_move_attacker

def pokemon_fainted(battle_window, player_attacker, pokemon):
    if player_attacker:
        battle_window.description_battle = 'The foe\'s ' + pokemon.name + ' fainted!'
        battle_window.wait(30, False, False)
        index = battle_window.model.enemy.search_pokemon_alive()
        if index != -1:
            battle_window.model.enemy.swap_position(0, index)
            battle_window.description_battle = 'The foe chooses ' + battle_window.model.enemy.team[0].name + '.'
            battle_window.pokemon_enemy_visible = False
            battle_window.pokeball_animations(10, False, False, False, battle_window.model.me.team[0], battle_window.model.enemy.team[0], False, True)
            battle_window.pokeball_animations(10, False, False, True, battle_window.model.me.team[0], battle_window.model.enemy.team[0], False, True)
            battle_window.pokemon_enemy_visible = True
        else:
            battle_window.description_battle = 'YOU WIN.'
            battle_window.wait(30, False, False)
            battle_window.exit_battle = True
    else:
        battle_window.description_battle = pokemon.name + ' fainted!'
        battle_window.wait(30, False, False)
        index = battle_window.model.me.search_pokemon_alive()
        if index != -1:
            battle_window.change_pokemon_menu = True
            battle_window.pokemon_player_fainted = True
        else:
            battle_window.description_battle = 'YOU LOSE.'
            battle_window.wait(30, False, False)
            battle_window.exit_battle = True






































