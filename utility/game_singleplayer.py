from utility import utils, show_screen_elements
import random


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
        attack_move, count_move, special_attack = determine_special_attack(battle_window, move_enemy,
                                                                           battle_window.model.enemy.team[0],
                                                                           battle_window.count_move_enemy, False)
        battle_window.count_move_enemy = count_move
        utils.update_special_attack(battle_window, special_attack, move_enemy, False)
        if attack_move:
            second_pokemon_fainted, first_pokemon_fainted, count_move = attack(battle_window, battle_window.model.enemy,
                                                                               battle_window.model.me, move_enemy,
                                                                               False, battle_window.count_move_enemy,
                                                                               battle_window.special_moves_me,
                                                                               battle_window.count_move_me)
            utils.reset_special_attack(battle_window, count_move, False)
    else:
        turn(battle_window, move_me, move_enemy)


def turn(battle_window, move_me, move_enemy):
    first_attack_me = determine_first_attacker(battle_window, move_me, move_enemy)
    first_pokemon_fainted = False
    second_pokemon_fainted = False
    if first_attack_me:
        attack_move, count_move, special_attack = determine_special_attack(battle_window, move_me,
                                                                           battle_window.model.me.team[0],
                                                                           battle_window.count_move_me, True)
        battle_window.count_move_me = count_move
        utils.update_special_attack(battle_window, special_attack, move_me, True)
        if attack_move:
            first_pokemon_fainted, second_pokemon_fainted, count_move = attack(battle_window, battle_window.model.me,
                                                                               battle_window.model.enemy, move_me, True,
                                                                               battle_window.count_move_me,
                                                                               battle_window.special_moves_enemy,
                                                                               battle_window.count_move_enemy)
            utils.reset_special_attack(battle_window, count_move, True)
        if not first_pokemon_fainted and not second_pokemon_fainted:
            attack_move, count_move, special_attack = determine_special_attack(battle_window, move_enemy,
                                                                               battle_window.model.enemy.team[0],
                                                                               battle_window.count_move_enemy, False)
            battle_window.count_move_enemy = count_move
            utils.update_special_attack(battle_window, special_attack, move_enemy, False)
            if attack_move:
                second_pokemon_fainted, first_pokemon_fainted, count_move = attack(battle_window,
                                                                                   battle_window.model.enemy,
                                                                                   battle_window.model.me, move_enemy,
                                                                                   False,
                                                                                   battle_window.count_move_enemy,
                                                                                   battle_window.special_moves_me,
                                                                                   battle_window.count_move_me)
                utils.reset_special_attack(battle_window, count_move, False)
        if first_pokemon_fainted:
            battle_window.count_move_me = 0
        if second_pokemon_fainted:
            battle_window.count_move_enemy = 0
    else:
        attack_move, count_move, special_attack = determine_special_attack(battle_window, move_enemy,
                                                                           battle_window.model.enemy.team[0],
                                                                           battle_window.count_move_enemy, False)
        battle_window.count_move_enemy = count_move
        utils.update_special_attack(battle_window, special_attack, move_enemy, False)
        if attack_move:
            first_pokemon_fainted, second_pokemon_fainted, count_move = attack(battle_window, battle_window.model.enemy,
                                                                               battle_window.model.me, move_enemy,
                                                                               False, battle_window.count_move_enemy,
                                                                               battle_window.special_moves_me,
                                                                               battle_window.count_move_me)
            utils.reset_special_attack(battle_window, count_move, False)
        if not first_pokemon_fainted and not second_pokemon_fainted:
            attack_move, count_move, special_attack = determine_special_attack(battle_window, move_me,
                                                                               battle_window.model.me.team[0],
                                                                               battle_window.count_move_me, True)
            battle_window.count_move_me = count_move
            utils.update_special_attack(battle_window, special_attack, move_me, True)
            if attack_move:
                second_pokemon_fainted, first_pokemon_fainted, count_move = attack(battle_window,
                                                                                   battle_window.model.me,
                                                                                   battle_window.model.enemy, move_me,
                                                                                   True, battle_window.count_move_me,
                                                                                   battle_window.special_moves_enemy,
                                                                                   battle_window.count_move_enemy)
                utils.reset_special_attack(battle_window, count_move, True)
        if first_pokemon_fainted:
            battle_window.count_move_enemy = 0
        if second_pokemon_fainted:
            battle_window.count_move_me = 0


def determine_special_attack(battle_window, move, pokemon, count_move, player_me):
    attack_move = True
    special_attack = False
    utils.update_appearance_pokemon(battle_window, player_me, True)
    if move.name.lower() == 'solarbeam' and count_move == 0:
        battle_window.description_battle = pokemon.name + ' absorbed light!'
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'fly' and count_move == 0:
        battle_window.description_battle = pokemon.name + ' flew up high!'
        utils.update_appearance_pokemon(battle_window, player_me, False)
        attack_move = False
        special_attack = True
        count_move += 1
    elif move.name.lower() == 'dig' and count_move == 0:
        battle_window.description_battle = pokemon.name + ' dug underground!'
        utils.update_appearance_pokemon(battle_window, player_me, False)
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
        show_screen_elements.wait(battle_window, 30, False, False)
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


def attack(battle_window, attacker, defender, move, player_attacker, count_move_attacker, special_moves_defender,
           count_move_defender):
    # attacker and defender can be self.me or self.enemy
    # This modifier is used in damage calculations; it takes into account type advantage and STAB bonus
    modifier = 1
    # Calculating Type advantages using "Type Advantages.csv" file
    for key in battle_window.model.pokedex.type_advantages:
        # If the attacking and defending types match up, multiply the modifier by the damage multiplier from the list
        if battle_window.model.pokedex.type_advantages[key][0] == move.type and \
                battle_window.model.pokedex.type_advantages[key][1] == defender.team[0].type1:
            modifier *= float(battle_window.model.pokedex.type_advantages[key][2])

        # Didn't use elif; Just in case you get a 4x or 0.25x modifier based on double type
        if battle_window.model.pokedex.type_advantages[key][0] == move.type and \
                battle_window.model.pokedex.type_advantages[key][1] == defender.team[0].type2:
            modifier *= float(battle_window.model.pokedex.type_advantages[key][2])

    attacker_fainted = False
    defender_fainted = False
    always_miss_attack = False
    if special_moves_defender:
        if special_moves_defender.name.lower() == 'fly' and count_move_defender == 1:
            always_miss_attack = True
        elif special_moves_defender.name.lower() == 'dig' and count_move_defender == 1 and move.name.lower() != 'earthquake':
            always_miss_attack = True
        utils.update_appearance_pokemon(battle_window, player_attacker, True)

    if move.kind != "Physical" and move.kind != 'Special':
        move_accuracy = 100
    else:
        move_accuracy = int(move.accuracy.replace('%', ''))
    prob = random.random() * 100
    if prob > move_accuracy or always_miss_attack:
        count_move_attacker = 0
        battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + ' but missed attack!'
        show_screen_elements.wait(battle_window, 30, False, False)
    elif move.pp_remain <= 0:
        battle_window.description_battle = move.name + ' has no pp remain!'
        show_screen_elements.wait(battle_window, 30, False, False)
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
            modifier *= attacker.team[0].stab

        elif move.type == attacker.team[0].type2:
            modifier *= attacker.team[0].stab

        # Damage formula also has a random element
        critic_value = random.uniform(0.85, 1.0)
        modifier *= critic_value

        # Appending the useMove function to the output
        if move.kind == "Physical" or move.kind == "Special":
            if effectiveness == 'normal effective':
                battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + '.'
                if special_moves_defender:
                    if special_moves_defender.name.lower() != 'dig' and count_move_defender != 1 and move.name.lower() != 'earthquake':
                        show_screen_elements.explosion_animations(battle_window, False, False, not player_attacker)
                    else:
                        show_screen_elements.wait(battle_window, 30, False, False)
                else:
                    show_screen_elements.explosion_animations(battle_window, False, False, not player_attacker)
            elif effectiveness == 'not effect':
                battle_window.description_battle = move.name + ' has no effect on ' + defender.team[0].name + '.'
                show_screen_elements.wait(battle_window, 30, False, False)
            else:
                battle_window.description_battle = attacker.team[
                                                       0].name + ' used ' + move.name + '. It\'s ' + effectiveness + '.'
                if special_moves_defender:
                    if special_moves_defender.name.lower() != 'dig' and count_move_defender != 1 and move.name.lower() != 'earthquake':
                        show_screen_elements.explosion_animations(battle_window, False, False, not player_attacker)
                    else:
                        show_screen_elements.wait(battle_window, 30, False, False)
                else:
                    show_screen_elements.explosion_animations(battle_window, False, False, not player_attacker)
        else:
            battle_window.description_battle = attacker.team[0].name + ' used ' + move.name + '.'
            show_screen_elements.wait(battle_window, 30, False, False)

        if critic_value > 0.98 and (move.kind == "Physical" or move.kind == "Special"):
            battle_window.description_battle = 'A critical hit!'
            show_screen_elements.wait(battle_window, 30, False, False)

        # ATK/DEF or SpATK/SpDEF or Status? Using the Pokemon damage formula
        # If the move is "Physical", the damage formula will take into account attack and defense
        if move.kind == "Physical":
            damage = int((((2 * attacker.team[0].level) + 10) / 250 * (
                        attacker.team[0].battleATK / defender.team[0].battleDEF) * move.power + 2) * modifier)
            hp_lost = defender.team[0].loseHP(damage)
            if move.name == 'Bonemerang' or move.name == 'Double Kick':
                damage *= 2
                battle_window.description_battle = move.name + ' hits 2 times.'
                show_screen_elements.explosion_animations(battle_window, False, False, not player_attacker)
        # If the move is "Special", the damage formula will take into account special attack and special defense
        elif move.kind == "Special":
            damage = int((((2 * attacker.team[0].level) + 10) / 250 * (
                        attacker.team[0].battleSpATK / defender.team[0].battleSpDEF) * move.power + 2) * modifier)
            hp_lost = defender.team[0].loseHP(damage)
            if move.name == 'Giga Drain':
                gain_hp = abs(hp_lost) // 2
                gain_hp = attacker.team[0].gainHP(gain_hp)
        # Stat Changing moves
        else:
            # If the move is stat-changing, it does 0 damage and the modifier is set to 1 (so it doesn't return super effective or not very effective)
            hp_lost = 0
            if move.kind == "a+":
                attacker.team[0].atkStage += 1
                attacker.team[0].battleATK = attacker.team[0].originalATK * utils.statMod(attacker.team[0].atkStage)
                battle_window.description_battle = attacker.team[0].name + '\'s attack rose!'

            elif move.kind == "d+":
                attacker.team[0].defStage += 1
                attacker.team[0].battleDEF = attacker.team[0].originalDEF * utils.statMod(attacker.team[0].defStage)
                battle_window.description_battle = attacker.team[0].name + '\'s defense rose!'

            elif move.kind == "sa+":
                attacker.team[0].spAtkStage += 1
                attacker.team[0].battleSpATK = attacker.team[0].originalSpATK * utils.statMod(
                    attacker.team[0].spAtkStage)
                battle_window.description_battle = attacker.team[0].name + '\'s special attack rose!'

            elif move.kind == "sd+":
                attacker.team[0].spDefStage += 1
                attacker.team[0].battleSpDef = attacker.team[0].originalSpDEF * utils.statMod(
                    attacker.team[0].spDefStage)
                battle_window.description_battle = attacker.team[0].name + '\'s special defense rose!'

            elif move.kind == "s+":
                attacker.team[0].speedStage += 1
                attacker.team[0].battleSpeed = attacker.team[0].originalSpeed * utils.statMod(
                    attacker.team[0].speedStage)
                battle_window.description_battle = attacker.team[0].name + '\'s speed rose!'

            elif move.kind == "a+sa+":
                attacker.team[0].atkStage += 1
                attacker.team[0].spAtkStage += 1
                attacker.team[0].battleATK = attacker.team[0].originalATK * utils.statMod(attacker.team[0].atkStage)
                attacker.team[0].battleSpATK = attacker.team[0].originalSpATK * utils.statMod(
                    attacker.team[0].spAtkStage)
                battle_window.description_battle = attacker.team[0].name + '\'s attack and special attack rose!'

            elif move.kind == "a-":
                defender.team[0].atkStage -= 1
                defender.team[0].battleATK = defender.team[0].originalATK * utils.statMod(defender.team[0].atkStage)
                battle_window.description_battle = defender.team[0].name + ' attacks fell!'

            elif move.kind == "d-":
                defender.team[0].defStage -= 1
                defender.team[0].battleDEF = defender.team[0].originalDEF * utils.statMod(defender.team[0].defStage)
                battle_window.description_battle = defender.team[0].name + '\'s defense fell!'

            elif move.kind == "sa-":
                defender.team[0].spAtkStage -= 1
                defender.team[0].battleSpATK = defender.team[0].originalSpATK * utils.statMod(
                    defender.team[0].spAtkStage)
                battle_window.description_battle = defender.team[0].name + '\'s special attack fell!'

            elif move.kind == "sd-":
                defender.team[0].spDefStage -= 1
                defender.team[0].battleSpDEF = defender.team[0].originalSpDEF * utils.statMod(
                    defender.team[0].spDefStage)
                battle_window.description_battle = defender.team[0].name + '\'s special defense fell!'

            elif move.kind == "s-":
                defender.team[0].speedStage -= 1
                defender.team[0].battleSpeed = defender.team[0].originalSpeed * utils.statMod(
                    defender.team[0].speedStage)
                battle_window.description_battle = defender.team[0].name + '\'s speed fell!'

            if move.name == 'Synthesis' or move.name == 'Moonlight':
                gain_hp = attacker.team[0].battleHP // 2
                gain_hp = attacker.team[0].gainHP(gain_hp)
                battle_window.description_battle = attacker.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP.'

        if (move.kind == "Physical" or move.kind == 'Special') and hp_lost != 0:
            show_screen_elements.reduce_hp_bar(battle_window, False, False, player_attacker, hp_lost)
            if move.name == 'Giga Drain':
                battle_window.description_battle = attacker.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP and ' + \
                                                   defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            else:
                battle_window.description_battle = defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            show_screen_elements.wait(battle_window, 20, False, False)
        else:
            show_screen_elements.wait(battle_window, 30, False, False)
        if move.name == 'Selfdestruct':
            attacker.team[0].battleHP_actual = 0
            show_screen_elements.wait(battle_window, 15, False, False)
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
        show_screen_elements.wait(battle_window, 30, False, False)
        index = battle_window.model.enemy.search_pokemon_alive()
        if index != -1:
            battle_window.model.enemy.swap_position(0, index)
            battle_window.description_battle = 'The foe chooses ' + battle_window.model.enemy.team[0].name + '.'
            battle_window.pokemon_enemy_visible = False
            show_screen_elements.pokeball_animations(battle_window, 10, False, False, False,
                                                       battle_window.model.me.team[0],
                                                       battle_window.model.enemy.team[0], False, True)
            show_screen_elements.pokeball_animations(battle_window, 10, False, False, True,
                                                       battle_window.model.me.team[0],
                                                       battle_window.model.enemy.team[0], False, True)
            battle_window.pokemon_enemy_visible = True
        else:
            battle_window.description_battle = 'YOU WIN.'
            show_screen_elements.wait(battle_window, 30, False, False)
            battle_window.exit_battle = True
    else:
        battle_window.description_battle = pokemon.name + ' fainted!'
        show_screen_elements.wait(battle_window, 30, False, False)
        index = battle_window.model.me.search_pokemon_alive()
        if index != -1:
            battle_window.change_pokemon_menu = True
            # battle_window.pokemon_player_fainted = True
        else:
            battle_window.description_battle = 'YOU LOSE.'
            show_screen_elements.wait(battle_window, 30, False, False)
            battle_window.exit_battle = True
