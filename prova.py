# def check_attacks(self, move_me, move_enemy):
#     self.pokemon_changed_not_fainted = False
#     if move_me == None:
#         _ = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#     elif move_me.name == 'SolarBeam':
#         self.solarbeam_my_move(move_me, move_enemy)
#     elif move_enemy.name == 'SolarBeam':
#         self.solarbeam_enemy_move(move_me, move_enemy)
#     else:
#         self.normal_turn(move_me, move_enemy)
#
# def solarbeam_my_move(self, move_me, move_enemy):
#     if move_enemy.name == 'ExtremeSpeed' or move_enemy.name == 'Quick Attack':
#         first_attack_me = False
#     else:
#         if self.model.me.team[0].battleSpeed >= self.model.enemy.team[0].battleSpeed:
#             first_attack_me = True
#         else:
#             first_attack_me = False
#     if first_attack_me:
#         defender_fainted = self.attack(self.model.me, self.model.enemy, move_me, True)
#         if not defender_fainted:
#             _ = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#     else:
#         defender_fainted = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#         if not defender_fainted:
#             _ = self.attack(self.model.me, self.model.enemy, move_me, True)
#
# def solarbeam_enemy_move(self, move_me, move_enemy):
#     if move_me.name == 'ExtremeSpeed' or move_me.name == 'Quick Attack':
#         first_attack_me = True
#     else:
#         if self.model.me.team[0].battleSpeed >= self.model.enemy.team[0].battleSpeed:
#             first_attack_me = True
#         else:
#             first_attack_me = False
#     if first_attack_me:
#         defender_fainted = self.attack(self.model.me, self.model.enemy, move_me, True)
#         if not defender_fainted:
#             _ = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#     else:
#         defender_fainted = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#         if not defender_fainted:
#             _ = self.attack(self.model.me, self.model.enemy, move_me, True)
#
# def normal_turn(self, move_me, move_enemy):
#     if move_me.name == 'ExtremeSpeed' and move_enemy.name != 'ExtremeSpeed':
#         first_attack_me = True
#     elif move_enemy.name == 'ExtremeSpeed' and move_me.name != 'ExtremeSpeed':
#         first_attack_me = False
#     else:
#         if move_me.name == 'Quick Attack' and move_enemy.name != 'Quick Attack':
#             first_attack_me = True
#         elif move_enemy.name == 'Quick Attack' and move_me.name != 'Quick Attack':
#             first_attack_me = False
#         else:
#             if self.model.me.team[0].battleSpeed >= self.model.enemy.team[0].battleSpeed:
#                 first_attack_me = True
#             else:
#                 first_attack_me = False
#     if first_attack_me:
#         defender_fainted = self.attack(self.model.me, self.model.enemy, move_me, True)
#         if not defender_fainted:
#             _ = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#     else:
#         defender_fainted = self.attack(self.model.enemy, self.model.me, move_enemy, False)
#         if not defender_fainted:
#             _ = self.attack(self.model.me, self.model.enemy, move_me, True)



def attack(self, attacker, defender, move, player_attacker):
    # attacker and defender can be self.me or self.enemy

    # This modifier is used in damage calculations; it takes into account type advantage and STAB bonus
    modifier = 1
    # Calculating Type advantages using "Type Advantages.csv" file
    for key in self.model.type_advantages:
        # If the attacking and defending types match up, multiply the modifier by the damage multiplier from the list
        if self.model.type_advantages[key][0] == move.type and self.model.type_advantages[key][1] == defender.team[0].type1:
            modifier *= float(self.model.type_advantages[key][2])

        # Didn't use elif; Just in case you get a 4x or 0.25x modifier based on double type
        if self.model.type_advantages[key][0] == move.type and self.model.type_advantages[key][1] == defender.team[0].type2:
            modifier *= float(self.model.type_advantages[key][2])

    defender_fainted = False
    if move.kind != "Physical" and move.kind != 'Special':
        move_accuracy = 100
    else:
        move_accuracy = int(move.accuracy.replace('%', ''))
    prob = random.random() * 100
    if prob > move_accuracy:
        self.description_battle = attacker.team[0].name + ' used ' + move.name + ' but missed attack!'
        self.wait(30, False, False)
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
                self.description_battle = attacker.team[0].name + ' used ' + move.name + '.'
            elif effectiveness == 'not effect':
                self.description_battle = move.name + ' has no effect on ' + defender.team[0].name + '.'
            else:
                self.description_battle = attacker.team[0].name + ' used ' + move.name + '. It\'s ' + effectiveness + '.'
        else:
            self.description_battle = attacker.team[0].name + ' used ' + move.name + '.'
        self.wait(30, False, False)

        if critic_value > 0.98 and (move.kind == "Physical" or move.kind == "Special"):
            self.description_battle = 'A critical hit!'
            self.wait(30, False, False)

        # ATK/DEF or SpATK/SpDEF or Status? Using the Pokemon damage formula
        # If the move is "Physical", the damage formula will take into account attack and defense
        level = 100
        if move.kind == "Physical":
            damage = int((((2*level) + 10)/250 * (attacker.team[0].battleATK/defender.team[0].battleDEF) * move.power + 2) * modifier)
            hp_lost = defender.team[0].loseHP(damage)
            if move.name == 'Bonemerang' or move.name == 'Double Kick':
                damage *= 2
                self.description_battle = move.name + ' hits 2 times.'
                self.wait(30, False, False)
            elif move.name == 'Selfdestruct':
                attacker.team[0].battleHP_actual = 0
            self.description_battle = defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
        # If the move is "Special", the damage formula will take into account special attack and special defense
        elif move.kind == "Special":
            damage = int((((2*level) + 10)/250 * (attacker.team[0].battleSpATK/defender.team[0].battleSpDEF) * move.power + 2) * modifier)
            hp_lost = defender.team[0].loseHP(damage)
            if move.name == 'Giga Drain':
                gain_hp = abs(hp_lost) // 2
                gain_hp = attacker.team[0].gainHP(gain_hp)
                self.description_battle = attacker.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP and ' + defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
            else:
                self.description_battle = defender.team[0].name + ' lost ' + str(abs(hp_lost)) + ' HP.'
        # Stat Changing moves
        else:
            # If the move is stat-changing, it does 0 damage and the modifier is set to 1 (so it doesn't return super effective or not very effective)
            if move.kind == "a+":
                attacker.team[0].atkStage +=1
                attacker.team[0].battleATK = attacker.team[0].originalATK * utils.statMod(attacker.team[0].atkStage)
                self.description_battle = attacker.team[0].name + '\'s attack rose!'

            elif move.kind == "d+":
                attacker.team[0].defStage +=1
                attacker.team[0].battleDEF = attacker.team[0].originalDEF * utils.statMod(attacker.team[0].defStage)
                self.description_battle = attacker.team[0].name + '\'s defense rose!'

            elif move.kind == "sa+":
                attacker.team[0].spAtkStage +=1
                attacker.team[0].battleSpATK = attacker.team[0].originalSpATK * utils.statMod(attacker.team[0].spAtkStage)
                self.description_battle = attacker.team[0].name + '\'s special attack rose!'

            elif move.kind == "sd+":
                attacker.team[0].spDefStage +=1
                attacker.team[0].battleSpDef = attacker.team[0].originalSpDEF * utils.statMod(attacker.team[0].spDefStage)
                self.description_battle = attacker.team[0].name + '\'s special defense rose!'

            elif move.kind == "s+":
                attacker.team[0].speedStage +=1
                attacker.team[0].battleSpeed = attacker.team[0].originalSpeed * utils.statMod(attacker.team[0].speedStage)
                self.description_battle = attacker.team[0].name + '\'s speed rose!'

            elif move.kind == "a+sa+":
                attacker.team[0].atkStage +=1
                attacker.team[0].spAtkStage +=1
                attacker.team[0].battleATK = attacker.team[0].originalATK * utils.statMod(attacker.team[0].atkStage)
                attacker.team[0].battleSpATK = attacker.team[0].originalSpATK * utils.statMod(attacker.team[0].spAtkStage)
                self.description_battle = attacker.team[0].name + '\'s attack and special attack rose!'

            elif move.kind == "a-":
                defender.team[0].atkStage -= 1
                defender.team[0].battleATK = defender.team[0].originalATK * utils.statMod(defender.team[0].atkStage)
                self.description_battle = defender.team[0].name + ' attacks fell!'

            elif move.kind == "d-":
                defender.team[0].defStage -=1
                defender.team[0].battleDEF = defender.team[0].originalDEF * utils.statMod(defender.team[0].defStage)
                self.description_battle = defender.team[0].name + '\'s defense fell!'

            elif move.kind == "sa-":
                defender.team[0].spAtkStage -=1
                defender.team[0].battleSpATK = defender.team[0].originalSpATK * utils.statMod(defender.team[0].spAtkStage)
                self.description_battle = defender.team[0].name + '\'s special attack fell!'

            elif move.kind == "sd-":
                defender.team[0].spDefStage -=1
                defender.team[0].battleSpDEF = defender.team[0].originalSpDEF * utils.statMod(defender.team[0].spDefStage)
                self.description_battle = defender.team[0].name + '\'s special defense fell!'

            elif move.kind == "s-":
                defender.team[0].speedStage -=1
                defender.team[0].battleSpeed = defender.team[0].originalSpeed * utils.statMod(defender.team[0].speedStage)
                self.description_battle = defender.team[0].name + '\'s speed fell!'

            if move.name == 'Synthesis' or move.name == 'Moonlight':
                gain_hp = attacker.team[0].battleHP // 2
                gain_hp = attacker.team[0].gainHP(gain_hp)
                self.description_battle = attacker.team[0].name + ' gained ' + str(abs(gain_hp)) + ' HP.'

        self.wait(30, False, False)
        move.pp_remain -= 1
        if defender.team[0].battleHP_actual == 0:
            self.pokemon_fainted(player_attacker, defender.team[0])
            defender_fainted = True
        if attacker.team[0].battleHP_actual == 0:
            self.pokemon_fainted(not player_attacker, attacker.team[0])
    return defender_fainted