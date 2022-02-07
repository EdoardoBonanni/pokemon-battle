import pygame

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


#colours types
water_color = (104, 144, 240)
steel_color = (184, 184, 208)
rock_color = (184, 160, 56)
psychic_color = (248, 88, 136)
poison_color = (160, 64, 160)
normal_color = (168, 168, 120)
ice_color = (152, 216, 216)
ground_color = (224, 192, 104)
grass_color = (120, 200, 80)
ghost_color = (112, 88, 152)
flying_color = (168, 144, 240)
fire_color = (240, 128, 48)
fight_color = (192, 48, 40)
electric_color = (248, 208, 48)
dragon_color = (112, 56, 248)
dark_color = (112, 88, 72)
bug_color = (168, 184, 32)
null_color = (104, 160, 144)
