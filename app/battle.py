import math

def attack(attacker, defender, move_name):
    defense = defender['def']
    damage = attacker['atk'] * (1 - (0.1 * math.log10(defense) + 0.002 * defense))
    print(damage)
    true_damage = round(damage ** ((math.log10(10-move_name["pp"])) / 2.5) * 10)
    print(true_damage)
    return true_damage


def switch_defeated_character(team):
    for i, defender in enumerate(team):
        if defender["current_hp"] > 0:
            return i
    return -1
