from utility import utils, show_screen_elements


def checks_2_turns_attack(BattleWindow, move_me, move_enemy, prob_accuracies, critic_values):
    """
    Check if Pokemon of player me or enemy do a special move in two turns.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param move_me: Pokemon move player me.
    :param move_enemy: Pokemon move player enemy.
    :param prob_accuracies: [prob_accuracies_me, prob_accuracies_enemy] = accuracy probabilities of both players.
    :param critic_values: [critic_values_me, critic_values_enemy] = critic values of both players.
    :return:
    """
    if BattleWindow.special_moves_me and BattleWindow.special_moves_enemy:
        check_turn_type(BattleWindow, BattleWindow.special_moves_me, BattleWindow.special_moves_enemy, prob_accuracies,
                        critic_values)
    elif BattleWindow.special_moves_me:
        check_turn_type(BattleWindow, BattleWindow.special_moves_me, move_enemy, prob_accuracies, critic_values)
    elif BattleWindow.special_moves_enemy:
        check_turn_type(BattleWindow, move_me, BattleWindow.special_moves_enemy, prob_accuracies, critic_values)
    else:
        check_turn_type(BattleWindow, move_me, move_enemy, prob_accuracies, critic_values)


def check_turn_type(BattleWindow, move_me, move_enemy, prob_accuracies, critic_values):
    """
    Check the type of move (change Pokemon, normal attack, special attack).
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param move_me: Pokemon move player me.
    :param move_enemy: Pokemon move player enemy.
    :param prob_accuracies: [prob_accuracies_me, prob_accuracies_enemy] = accuracy probabilities of both players.
    :param critic_values: [critic_values_me, critic_values_enemy] = critic values of both players.
    :return:
    """
    BattleWindow.pokemon_changed_not_fainted = False
    # if None the Pokemon in battle (player me or enemy) is not fainted and changed from game.
    if move_me is None and move_enemy is not None:
        attack_move, count_move, special_attack = utils.determine_special_attack(BattleWindow, move_enemy,
                                                                                 BattleWindow.model.enemy.team[0],
                                                                                 BattleWindow.count_move_enemy, False)
        BattleWindow.count_move_enemy = count_move
        utils.update_special_attack(BattleWindow, special_attack, move_enemy, False)

        if attack_move:
            second_pokemon_fainted, first_pokemon_fainted, count_move = attack(BattleWindow, BattleWindow.model.enemy,
                                                                               BattleWindow.model.me, move_enemy,
                                                                               False, BattleWindow.count_move_enemy,
                                                                               BattleWindow.special_moves_me,
                                                                               BattleWindow.count_move_me,
                                                                               prob_accuracies[1], critic_values[1])
            utils.reset_special_attack(BattleWindow, count_move, False)
    elif move_me is not None and move_enemy is None:
        attack_move, count_move, special_attack = utils.determine_special_attack(BattleWindow, move_me,
                                                                                 BattleWindow.model.me.team[0],
                                                                                 BattleWindow.count_move_me, True)
        BattleWindow.count_move_me = count_move
        utils.update_special_attack(BattleWindow, special_attack, move_me, True)
        if attack_move:
            second_pokemon_fainted, first_pokemon_fainted, count_move = attack(BattleWindow, BattleWindow.model.me,
                                                                               BattleWindow.model.enemy, move_me, True,
                                                                               BattleWindow.count_move_me,
                                                                               BattleWindow.special_moves_enemy,
                                                                               BattleWindow.count_move_enemy,
                                                                               prob_accuracies[0], critic_values[0])
            utils.reset_special_attack(BattleWindow, count_move, True)
    elif move_me is not None and move_enemy is not None:
        classic_turn(BattleWindow, move_me, move_enemy, prob_accuracies, critic_values)


def classic_turn(BattleWindow, move_me, move_enemy, prob_accuracies, critic_values):
    """
    It allows to do a classic turn with moves without Pokemon changes.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param move_me: Pokemon move player me.
    :param move_enemy: Pokemon move player enemy.
    :param prob_accuracies: [prob_accuracies_me, prob_accuracies_enemy] = accuracy probabilities of both players.
    :param critic_values: [critic_values_me, critic_values_enemy] = critic values of both players.
    :return:
    """
    first_attack_me = determine_first_attacker(BattleWindow, move_me, move_enemy)
    pokemon_fainted_me = False
    pokemon_fainted_enemy = False
    # first attack player me.
    if first_attack_me:
        attack_move, count_move, special_attack = utils.determine_special_attack(BattleWindow, move_me,
                                                                                 BattleWindow.model.me.team[0],
                                                                                 BattleWindow.count_move_me, True)
        BattleWindow.count_move_me = count_move
        utils.update_special_attack(BattleWindow, special_attack, move_me, True)
        # check if the move is an attack.
        if attack_move:
            pokemon_fainted_me, pokemon_fainted_enemy, count_move = attack(BattleWindow, BattleWindow.model.me,
                                                                               BattleWindow.model.enemy, move_me, True,
                                                                               BattleWindow.count_move_me,
                                                                               BattleWindow.special_moves_enemy,
                                                                               BattleWindow.count_move_enemy,
                                                                               prob_accuracies[0], critic_values[0])
            utils.reset_special_attack(BattleWindow, count_move, True)
        BattleWindow.description_battle = ""
        show_screen_elements.wait(BattleWindow, 10, False, False)
        # check if a Pokemon is fainted and the enemy attacks.
        if not pokemon_fainted_me and not pokemon_fainted_enemy:
            attack_move, count_move, special_attack = utils.determine_special_attack(BattleWindow, move_enemy,
                                                                                     BattleWindow.model.enemy.team[0],
                                                                                     BattleWindow.count_move_enemy,
                                                                                     False)
            BattleWindow.count_move_enemy = count_move
            utils.update_special_attack(BattleWindow, special_attack, move_enemy, False)
            # check if the move is an attack.
            if attack_move:
                pokemon_fainted_enemy, pokemon_fainted_me, count_move = attack(BattleWindow,
                                                                                   BattleWindow.model.enemy,
                                                                                   BattleWindow.model.me, move_enemy,
                                                                                   False,
                                                                                   BattleWindow.count_move_enemy,
                                                                                   BattleWindow.special_moves_me,
                                                                                   BattleWindow.count_move_me,
                                                                                   prob_accuracies[1], critic_values[1])
                utils.reset_special_attack(BattleWindow, count_move, False)
            BattleWindow.description_battle = ""
            show_screen_elements.wait(BattleWindow, 10, False, False)
        # reset special move count if Pokemon fainted.
        if pokemon_fainted_me:
            BattleWindow.count_move_me = 0
            BattleWindow.special_moves_me = None
        if pokemon_fainted_enemy:
            BattleWindow.count_move_enemy = 0
            BattleWindow.special_moves_enemy = None
    # first attack player enemy.
    else:
        attack_move, count_move, special_attack = utils.determine_special_attack(BattleWindow, move_enemy,
                                                                                 BattleWindow.model.enemy.team[0],
                                                                                 BattleWindow.count_move_enemy, False)
        BattleWindow.count_move_enemy = count_move
        utils.update_special_attack(BattleWindow, special_attack, move_enemy, False)
        # check if the move is an attack.
        if attack_move:
            pokemon_fainted_enemy, pokemon_fainted_me, count_move = attack(BattleWindow, BattleWindow.model.enemy,
                                                                               BattleWindow.model.me, move_enemy,
                                                                               False, BattleWindow.count_move_enemy,
                                                                               BattleWindow.special_moves_me,
                                                                               BattleWindow.count_move_me,
                                                                               prob_accuracies[1], critic_values[1])
            utils.reset_special_attack(BattleWindow, count_move, False)
        BattleWindow.description_battle = ""
        show_screen_elements.wait(BattleWindow, 10, False, False)
        # check if a Pokemon is fainted and the enemy attacks.
        if not pokemon_fainted_enemy and not pokemon_fainted_me:
            attack_move, count_move, special_attack = utils.determine_special_attack(BattleWindow, move_me,
                                                                                     BattleWindow.model.me.team[0],
                                                                                     BattleWindow.count_move_me, True)
            BattleWindow.count_move_me = count_move
            utils.update_special_attack(BattleWindow, special_attack, move_me, True)
            # check if the move is an attack.
            if attack_move:
                pokemon_fainted_me, pokemon_fainted_enemy, count_move = attack(BattleWindow,
                                                                                   BattleWindow.model.me,
                                                                                   BattleWindow.model.enemy, move_me,
                                                                                   True, BattleWindow.count_move_me,
                                                                                   BattleWindow.special_moves_enemy,
                                                                                   BattleWindow.count_move_enemy,
                                                                                   prob_accuracies[0], critic_values[0])
                utils.reset_special_attack(BattleWindow, count_move, True)
            BattleWindow.description_battle = ""
            show_screen_elements.wait(BattleWindow, 10, False, False)
        # reset special move count if Pokemon fainted.
        if pokemon_fainted_enemy:
            BattleWindow.count_move_enemy = 0
            BattleWindow.special_moves_enemy = None
        if pokemon_fainted_me:
            BattleWindow.count_move_me = 0
            BattleWindow.special_moves_me = None


def determine_first_attacker(battle_window, move_me, move_enemy):
    """
    Determine the first attacker (player me or enemy).
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param move_me: Pokemon move me.
    :param move_enemy: Pokemon move enemy.
    :return: first_attack_me = first attack of player me or enemy.
    """
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
            if battle_window.model.me.team[0].battleSpeed > battle_window.model.enemy.team[0].battleSpeed:
                first_attack_me = True
            elif battle_window.model.me.team[0].battleSpeed == battle_window.model.enemy.team[
                0].battleSpeed and battle_window.player == 0:
                first_attack_me = True
            else:
                first_attack_me = False
    return first_attack_me


def attack(BattleWindow, attacker_model, defender_model, move, player_attacker, count_move_attacker, special_moves_defender,
           count_move_defender, prob_accuracy, critic_value):
    """
    It allows to handle all Pokemon move types and the relative features.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param attacker_model: attacker_model (player me or enemy).
    :param defender_model: defender_model (player me or enemy)
    :param move: Pokemon move.
    :param player_attacker: attacker (player me or enemy).
    :param count_move_attacker: counter of special move for attacker.
    :param special_moves_defender: check if defender do a special move.
    :param count_move_defender: counter of special move for defender.
    :param prob_accuracy: attacker accuracy probability.
    :param critic_value: attacker critic value.
    :return: [attacker_fainted, defender_fainted, count_move_attacker] = check if attacker fainted, check if defender fainted and the move counter of attacker.
    """

    # this modifier is used in damage calculations; it takes into account type advantage and STAB bonus.
    modifier = 1
    for key in BattleWindow.model.pokedex.type_advantages:
        # if the attacking and defending types match up, multiply the modifier by the damage multiplier from the list.
        if BattleWindow.model.pokedex.type_advantages[key][0] == move.type and \
                BattleWindow.model.pokedex.type_advantages[key][1] == defender_model.team[0].type1:
            modifier *= float(BattleWindow.model.pokedex.type_advantages[key][2])

        if BattleWindow.model.pokedex.type_advantages[key][0] == move.type and \
                BattleWindow.model.pokedex.type_advantages[key][1] == defender_model.team[0].type2:
            modifier *= float(BattleWindow.model.pokedex.type_advantages[key][2])

    attacker_fainted = False
    defender_fainted = False
    always_miss_attack = False
    gain_hp = 0
    # check if defender uses a special move.
    if special_moves_defender:
        # if defender uses fly or dig and the attacker doesn't use earthquake, then the attacker's move always misses.
        if special_moves_defender.name.lower() == 'fly' and count_move_defender == 1:
            always_miss_attack = True
        elif special_moves_defender.name.lower() == 'dig' and count_move_defender == 1 and move.name.lower() != 'earthquake':
            always_miss_attack = True
        utils.update_appearance_pokemon(BattleWindow, player_attacker, True)

    # check move type and define move accuracy.
    if move.kind != "Physical" and move.kind != 'Special':
        move_accuracy = 100
        always_miss_attack = False
    else:
        move_accuracy = int(move.accuracy.replace('%', ''))
    if prob_accuracy > move_accuracy or always_miss_attack:
        count_move_attacker = 0
        BattleWindow.description_battle = attacker_model.team[0].name + ' used ' + move.name + ' but missed attack!'
        show_screen_elements.wait(BattleWindow, 30, False, False)
    elif move.pp_remain <= 0:
        BattleWindow.description_battle = move.name + ' has no pp remain!'
        show_screen_elements.wait(BattleWindow, 30, False, False)
    else:
        # the modifier value defines the effectiveness of moves.
        if modifier >= 2:
            effectiveness = 'super effective'
        elif modifier == 1:
            effectiveness = 'normal effective'
        elif modifier == 0:
            effectiveness = 'not effect'
        else:
            effectiveness = 'not very effective'

        # calculating STAB (Same-type Attack Bonus).
        if move.type == attacker_model.team[0].type1:
            modifier *= attacker_model.team[0].stab

        elif move.type == attacker_model.team[0].type2:
            modifier *= attacker_model.team[0].stab

        modifier *= critic_value

        # check move types, show battle descriptions and the animations.
        if move.kind == "Physical" or move.kind == "Special":
            if effectiveness == 'normal effective':
                BattleWindow.description_battle = attacker_model.team[0].name + ' used ' + move.name + '.'
                if special_moves_defender:
                    if special_moves_defender.name.lower() != 'dig' and count_move_defender != 1 and move.name.lower() != 'earthquake':
                        show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
                    elif (special_moves_defender.name.lower() == 'solarbeam' or special_moves_defender.name.lower() == 'hyper beam') and count_move_defender == 1:
                        show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
                    else:
                        show_screen_elements.wait(BattleWindow, 30, False, False)
                else:
                    show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
            elif effectiveness == 'not effect':
                BattleWindow.description_battle = move.name + ' has no effect on ' + defender_model.team[0].name + '.'
                show_screen_elements.wait(BattleWindow, 30, False, False)
            else:
                BattleWindow.description_battle = attacker_model.team[0].name + ' used ' + move.name + '. It\'s ' + effectiveness + '.'
                if special_moves_defender:
                    if special_moves_defender.name.lower() != 'dig' and count_move_defender != 1 and move.name.lower() != 'earthquake':
                        show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
                    elif (special_moves_defender.name.lower() == 'solarbeam' or special_moves_defender.name.lower() == 'hyper beam') and count_move_defender == 1:
                        show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
                    else:
                        show_screen_elements.wait(BattleWindow, 30, False, False)
                else:
                    show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
        else:
            BattleWindow.description_battle = attacker_model.team[0].name + ' used ' + move.name + '.'
            show_screen_elements.wait(BattleWindow, 30, False, False)

        # check if attack does a critical hit.
        if critic_value > 0.98 and (move.kind == "Physical" or move.kind == "Special") and effectiveness != 'not effect':
            BattleWindow.description_battle = 'A critical hit!'
            show_screen_elements.wait(BattleWindow, 30, False, False)

        # if the move is "Physical", the damage formula will take into account attack and defense.
        if move.kind == "Physical" and effectiveness != 'not effect':
            damage = int((((2 * attacker_model.team[0].level) + 10) / 250 * (
                    attacker_model.team[0].battleATK / defender_model.team[0].battleDEF) * move.power + 2) * modifier)
            if move.name == 'Bonemerang' or move.name == 'Double Kick':
                damage *= 2
                BattleWindow.description_battle = move.name + ' hits 2 times.'
                show_screen_elements.explosion_animations(BattleWindow, False, False, not player_attacker)
            hp_lost = defender_model.team[0].loseHP(damage)
        # if the move is "Special", the damage formula will take into account special attack and special defense.
        elif move.kind == "Special" and effectiveness != 'not effect':
            damage = int((((2 * attacker_model.team[0].level) + 10) / 250 * (
                    attacker_model.team[0].battleSpATK / defender_model.team[0].battleSpDEF) * move.power + 2) * modifier)
            hp_lost = defender_model.team[0].loseHP(damage)
            if move.name == 'Giga Drain':
                gain_hp = abs(hp_lost) // 2
                gain_hp = attacker_model.team[0].gainHP(gain_hp)
        # stat changing moves.
        elif move.kind != "Physical" and move.kind != "Special":
            # if the move is stat-changing, it does 0 damage and the modifier is set to 1 (so it doesn't return the effectiveness).
            hp_lost = 0
            # check the stat-changing move type.
            if move.kind == "a+":
                attacker_model.team[0].atkStage += 1
                attacker_model.team[0].battleATK = attacker_model.team[0].originalATK * utils.statMod(attacker_model.team[0].atkStage)
                BattleWindow.description_battle = attacker_model.team[0].name + '\'s attack rose!'

            elif move.kind == "d+":
                attacker_model.team[0].defStage += 1
                attacker_model.team[0].battleDEF = attacker_model.team[0].originalDEF * utils.statMod(attacker_model.team[0].defStage)
                BattleWindow.description_battle = attacker_model.team[0].name + '\'s defense rose!'

            elif move.kind == "sa+":
                attacker_model.team[0].spAtkStage += 1
                attacker_model.team[0].battleSpATK = attacker_model.team[0].originalSpATK * utils.statMod(
                    attacker_model.team[0].spAtkStage)
                BattleWindow.description_battle = attacker_model.team[0].name + '\'s special attack rose!'

            elif move.kind == "sd+":
                attacker_model.team[0].spDefStage += 1
                attacker_model.team[0].battleSpDef = attacker_model.team[0].originalSpDEF * utils.statMod(
                    attacker_model.team[0].spDefStage)
                BattleWindow.description_battle = attacker_model.team[0].name + '\'s special defense rose!'

            elif move.kind == "s+":
                attacker_model.team[0].speedStage += 1
                attacker_model.team[0].battleSpeed = attacker_model.team[0].originalSpeed * utils.statMod(
                    attacker_model.team[0].speedStage)
                BattleWindow.description_battle = attacker_model.team[0].name + '\'s speed rose!'

            elif move.kind == "a+sa+":
                attacker_model.team[0].atkStage += 1
                attacker_model.team[0].spAtkStage += 1
                attacker_model.team[0].battleATK = attacker_model.team[0].originalATK * utils.statMod(attacker_model.team[0].atkStage)
                attacker_model.team[0].battleSpATK = attacker_model.team[0].originalSpATK * utils.statMod(
                    attacker_model.team[0].spAtkStage)
                BattleWindow.description_battle = attacker_model.team[0].name + '\'s attack and special attack rose!'

            elif move.kind == "a-":
                defender_model.team[0].atkStage -= 1
                defender_model.team[0].battleATK = defender_model.team[0].originalATK * utils.statMod(defender_model.team[0].atkStage)
                BattleWindow.description_battle = defender_model.team[0].name + ' attacks fell!'

            elif move.kind == "d-":
                defender_model.team[0].defStage -= 1
                defender_model.team[0].battleDEF = defender_model.team[0].originalDEF * utils.statMod(defender_model.team[0].defStage)
                BattleWindow.description_battle = defender_model.team[0].name + '\'s defense fell!'

            elif move.kind == "sa-":
                defender_model.team[0].spAtkStage -= 1
                defender_model.team[0].battleSpATK = defender_model.team[0].originalSpATK * utils.statMod(
                    defender_model.team[0].spAtkStage)
                BattleWindow.description_battle = defender_model.team[0].name + '\'s special attack fell!'

            elif move.kind == "sd-":
                defender_model.team[0].spDefStage -= 1
                defender_model.team[0].battleSpDEF = defender_model.team[0].originalSpDEF * utils.statMod(
                    defender_model.team[0].spDefStage)
                BattleWindow.description_battle = defender_model.team[0].name + '\'s special defense fell!'

            elif move.kind == "s-":
                defender_model.team[0].speedStage -= 1
                defender_model.team[0].battleSpeed = defender_model.team[0].originalSpeed * utils.statMod(
                    defender_model.team[0].speedStage)
                BattleWindow.description_battle = defender_model.team[0].name + '\'s speed fell!'

            if move.name == 'Synthesis' or move.name == 'Moonlight':
                gain_hp = attacker_model.team[0].battleHP // 2
                gain_hp = attacker_model.team[0].gainHP(gain_hp)
                BattleWindow.description_battle = attacker_model.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP.'
        else:
            hp_lost = 0
        # if the attack does damage to defender then the reduce_hp_bar animation is shown.
        if (move.kind == "Physical" or move.kind == 'Special') and hp_lost != 0:
            show_screen_elements.reduce_hp_bar(BattleWindow, False, False, player_attacker, hp_lost)
            if move.name == 'Giga Drain':
                BattleWindow.description_battle = attacker_model.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP and ' + \
                                                  defender_model.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            else:
                BattleWindow.description_battle = defender_model.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            show_screen_elements.wait(BattleWindow, 20, False, False)
        else:
            show_screen_elements.wait(BattleWindow, 30, False, False)

        # check for "Selfdestruct" move.
        if move.name == 'Selfdestruct':
            attacker_model.team[0].battleHP_actual = 0
            show_screen_elements.wait(BattleWindow, 15, False, False)
        move.pp_remain -= 1
        # check if attacker/defender Pokemon are fainted.
        if defender_model.team[0].battleHP_actual == 0:
            pokemon_fainted(BattleWindow, player_attacker, defender_model.team[0])
            defender_fainted = True
        if attacker_model.team[0].battleHP_actual == 0:
            pokemon_fainted(BattleWindow, not player_attacker, attacker_model.team[0])
            attacker_fainted = True
    return attacker_fainted, defender_fainted, count_move_attacker


def pokemon_fainted(BattleWindow, player_me_attacker, pokemon):
    """
    Check if a Pokemon in battle is fainted.
    :param BattleWindow: BattleWindow singleplayer/multiplayer.
    :param player_me_attacker: attacker (player me or enemy).
    :param pokemon: Pokemon.
    :return:
    """
    if player_me_attacker:
        BattleWindow.description_battle = 'The foe\'s ' + pokemon.name + ' fainted!'
        show_screen_elements.wait(BattleWindow, 30, False, False)
        index = BattleWindow.model.enemy.search_pokemon_alive()
        # if there is a Pokemon alive in the player enemy team.
        if index != -1:
            BattleWindow.pokemon_fainted = True
            BattleWindow.pokemon_enemy_fainted = True
        else:
            # player me win.
            BattleWindow.description_battle = 'YOU WIN'
            show_screen_elements.wait(BattleWindow, 30, False, False)
            BattleWindow.exit_battle = True
    else:
        BattleWindow.description_battle = pokemon.name + ' fainted!'
        show_screen_elements.wait(BattleWindow, 30, False, False)
        index = BattleWindow.model.me.search_pokemon_alive()
        # if there is a Pokemon alive in the player me team.
        if index != -1:
            BattleWindow.pokemon_fainted = True
            BattleWindow.pokemon_me_fainted = True
        else:
            # player me loses.
            BattleWindow.description_battle = 'YOU LOSE'
            show_screen_elements.wait(BattleWindow, 30, False, False)
            BattleWindow.exit_battle = True
