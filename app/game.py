import random
from apis import get_superhero, get_anime_character

url = "https://pokeapi.co/api/v2/pokemon/"

def random_team(what):
    x = 0
    list = []
    while x <= 5:
        if what == "anime":
            hero = get_anime_character(0)
        else:
            hero = get_superhero(0)
        # hero = make_random_fighter()
        if hero == None:
            return None
        list.append(hero)
        x+=1
    return list

"""
being written in the init because stored in session 
def re_roll(list, x):
    hero = make_random_fighter()
    list[x] = hero
    print(list)
    return list
"""

#playerone = player()

#print(playerone.list)
