from flask import redirect, url_for

import json, urllib.request, time, os, uuid
import random, math

Jikan_page_cache = {}
Jikan_id_cache = {}

def get_random_profile_pic():
    randomint = random.randint(1, 1025)
    with urllib.request.urlopen(f"https://pokeapi.co/api/v2/pokemon/{randomint}/") as response:
        data = response.read()
    result = json.loads(data.decode('utf-8'))

    imgurl = result["sprites"]["other"]["official-artwork"]["front_default"]
    return imgurl

def get_pokemon(id):
    if id == 0:
        id = random.randint(1,1025)
    with urllib.request.urlopen(f"https://pokeapi.co/api/v2/pokemon/{id}/") as response:
        data = response.read()
    result = json.loads(data.decode('utf-8'))
    return result

def get_random_moves():
    moves = []
    for i in range(4):
        move_number = random.randint(1,750)
        with urllib.request.urlopen(f"https://pokeapi.co/api/v2/move/{move_number}/") as response:
            data = response.read()
        result = json.loads(data.decode('utf-8'))
        move = {}
        move["name"] = result["name"]
        move["pp"] = math.ceil(result["pp"] / 5)
        moves.append(move)
    return moves

def check_stat(val):
    if val is None or (isinstance(val, str) and not val.isdigit()):
        return random.randint(1, 100)
    return int(val)

def get_superhero2(id):
    if id == 0:
        id = random.randint(1,613)

    path = "keys/key_SuperheroAPI.txt"
    # path DNE
    if not os.path.exists(path):
        return None

    with open(path) as file:
        superhero_key = file.read()
    with urllib.request.urlopen(f"https://www.superheroapi.com/api.php/{superhero_key}/{id}") as response:
        data = response.read()
    result = json.loads(data.decode('utf-8'))

    # handles missing/wrong key
    if result["response"] == "error":
        return None

    stats = result["powerstats"]
    hp = check_stat(stats["durability"])
    atk = check_stat(stats["power"])
    speed = check_stat(stats["speed"])
    defense = check_stat(stats["strength"])

    return {
        "name": result["name"],
        "image": result["image"]["url"],
        "hp": hp,
        "atk": atk,
        "speed": speed,
        "def": defense
    }

def get_superhero(id):
    while True:
        try:
            if id == 0:
                id = random.randint(1,613)

            with urllib.request.urlopen(f"https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/id/{id}.json") as response:
                data = response.read()
            result = json.loads(data.decode('utf-8'))

            pokemon = get_pokemon(id)

            stats = result["powerstats"]
            hp = check_stat(stats["durability"])
            atk = check_stat(stats["power"])
            speed = check_stat(stats["speed"])
            defense = check_stat(stats["strength"])

            moves = get_random_moves()

            return {
                "id": str(uuid.uuid4()),
                "name": result["name"],
                "image": result["images"]["md"],
                "hp": hp,
                "current_hp": hp,
                "atk": atk,
                "speed": speed,
                "def": defense,
                "moves": moves,
                "reroll": False
            }
        except urllib.error.HTTPError:
            id = 0
            continue


def check_rate(url):
    while True:
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("reached quota! waiting 3 seconds...")
                time.sleep(3)
            else:
                return redirect(url_for('home'))

def get_anime_character(id):
    if id == 0:
        id = random.randint(1,612)
    count = id % 25 + 1
    page = id // 25 + 1

    if page in Jikan_page_cache:
        result = Jikan_page_cache[page]
    else:
        data = check_rate(f"https://api.jikan.moe/v4/characters?order_by=favorites&sort=desc&limit=25&page={page}")
        result = json.loads(data.decode('utf-8'))["data"]
        Jikan_page_cache[page] = result

    chosen = random.choice(result)
    mal_id = chosen["mal_id"]

    if mal_id in Jikan_id_cache:
        character = Jikan_id_cache[mal_id]
    else:
        data2 = check_rate(f"https://api.jikan.moe/v4/characters/{mal_id}/full")
        character = json.loads(data2.decode('utf-8'))["data"]
        Jikan_id_cache[mal_id] = character

    moves = get_random_moves()

    return {
        "id": str(uuid.uuid4()),
        "name": character["name"],
        "image": character["images"]["jpg"]["image_url"],
        "hp": round(0.5 * character["favorites"] ** 0.5), # hp = 0.5 * #favorites ** 0.5
        "current_hp": round(0.5 * character["favorites"] ** 0.5),
        "atk": random.randint(5,10) * len(character["anime"]), # atk = #anime * random.randint(5,10)
        "speed": random.randint(5,10) * len(character["manga"]), # speed = #manga * random.randint(5,10)
        "def": random.randint(5,10) * len(character["voices"]), # defense = #voice * random.randint(5,10)
        "moves": moves,
        "reroll": False
    }

def get_insult():
    try:
        with urllib.request.urlopen("https://evilinsult.com/generate_insult.php?lang=en&type=json") as response:
            data = response.read()
        result = json.loads(data.decode('utf-8'))
        insult = result["insult"]
        encode_insult = urllib.parse.quote(insult)
        with urllib.request.urlopen(f"https://www.purgomalum.com/service/json?text={encode_insult}") as response:
            data = response.read()
        result = json.loads(data.decode('utf-8'))
        filtered = result["result"]
        return filtered
    except Exception as e:
        print("Insult error: ", e)
        return "oops no insult for you"
