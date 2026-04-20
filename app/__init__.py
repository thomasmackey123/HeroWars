from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for

import sqlite3, random

from apis import get_random_profile_pic, get_insult, get_anime_character, get_superhero
from game import random_team
from battle import attack, switch_defeated_character

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for("home"))

    return redirect(url_for("login"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # reload page if no username or password was entered
        if not username or not password:
            return render_template("register.html", error="No username or password inputted")

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # check if username already exists and reload page if it does
        exists = c.execute("SELECT 1 FROM users WHERE name = ?", (username,)).fetchone()
        if exists:
            db.close()
            return render_template("register.html", error="Username already exists")

        profile_pic = get_random_profile_pic()
        c.execute("INSERT INTO users (name, password, wins, losses, rizu_coin, profile_pic) VALUES (?, ?, ?, ?, ?, ?)", (username, password, 0, 0, 67, profile_pic))
        db.commit()
        db.close()

        session['username'] = username
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # store username and password as a variable
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # render login page if username or password box is empty
        if not username or not password:
            return render_template('login.html', error="No username or password inputted")

        #search user table for password from a certain username
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        account = c.execute("SELECT password FROM users WHERE name = ?", (username,)).fetchone()
        db.close()

        #if there is no account then reload page
        if account is None:
            return render_template("login.html", error="Username or password is incorrect")

        # check if password is correct, if not then reload page
        if account[0] != password:
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    return render_template('login.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    session.pop('team1', None) # remove loadout
    session.pop('team2', None) # remove loadout
    session.pop('team1_which', None)
    session.pop('team2_which', None)
    session.pop('game_state', None)
    if "username" not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    user = session["username"]
    wins, losses, rizu_coin, profile_pic = c.execute("SELECT wins, losses, rizu_coin, profile_pic FROM users WHERE name=?", (user,)).fetchone()

    return render_template('home.html',
                           username = user,
                           wins = wins,
                           losses = losses,
                           rizu_coin = rizu_coin,
                           profile_pic = profile_pic)

@app.route("/loadingpage")
def loadingpage():
    redirect_to = url_for('menu')
    return render_template('loadingpage.html',
                           redirect_to = redirect_to)

@app.route("/menu", methods=['GET', 'POST'])
def menu():
    which = ["anime", "superhero"]
    random.shuffle(which)
    if 'which' not in session:
        session['which'] = which[0]
    if "team1" not in session:
        team1 = random_team(which[0])
        if team1 == None:
            return redirect(url_for('error'))
        #dispaly gif
        session["team1"] = team1
        session["team1_which"] = which[0]
        #hide gif
    if "team2" not in session:
        team2 = random_team(which[1])
        if team2 == None:
            return redirect(url_for('error'))
        #display gif
        session["team2"] = team2
        session["team2_which"] = which[1]
        #hide gif

    if request.method == "POST":
        print("post")
        indices = request.form.getlist("reroll")
        print(indices)
        cost = len(indices)
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        rizu_coin = c.execute("SELECT rizu_coin FROM users WHERE name=?", (session['username'],)).fetchone()[0]
        if rizu_coin < cost:
            return redirect(url_for('menu'))
        for idx in indices:
            index = int(idx)
            if index <= 6:
                print("swapped")
                if session['team1_which'] == "anime":
                    session['team1'][index - 1] = get_anime_character(0)
                else:
                    session['team1'][index - 1] = get_superhero(0)
            else:
                print("swapped")
                if session['team2_which'] == "anime":
                    session['team2'][index - 7] = get_anime_character(0)
                else:
                    session['team2'][index - 7] = get_superhero(0)
            session.modified = True
        # hide gif
        c.execute("UPDATE users SET rizu_coin=? WHERE name=?", (rizu_coin-cost, session['username']))
        db.commit()
        db.close()

    return render_template('menu.html',
                           player = session["username"],
                           card_list1 = session["team1"],
                           card_list2 = session["team2"])


@app.route("/reroll", methods=['GET', 'POST']) #p is player int, c is character int
def reroll():
    newteam1 = session["team1"]
    newteam2 = session["team2"]
    '''
    if request.method == "POST":
        indices = request.form.get("reroll")
    for index in indices:
        if index <= 6:
    '''

    # one are two are lists retrieved from html, will have rerollCheck1_{{ card }} or rerollCheck2_{{ card }}
    # if list is not empty, for each card in list, reroll it and assign new value
    '''
    for card in list:
        if card > 12 =:
            newteam[x] = newcharacter

    for x in one:
        if x == 1:
            newteam = session["team1"]
            newcharacter = make_random_fighter()
            newteam[x] = newcharacter
            session["team1"] = newteam
    for x in two:
        if x == 1:
            newteam = session["team2"]
            newcharacter = make_random_fighter()
            newteam[x] = newcharacter
            session["team2"] = newteam
    '''
    return render_template(menu.html,
                           card_list1 = session["team1"],
                           card_list2 = session["team2"])

@app.route("/game", methods=['GET', 'POST'])
def game():
    if "game_state" not in session:
        session["game_state"] = {
            "p1_team": session["team1"],
            "p2_team": session["team2"],
            "p1_active_index": 0,
            "p2_active_index": 0,
            "p1_insult": "",
            "p2_insult": "",
            "turn": random.choice(["p1", "p2"]),
            "log": ["3.. 2.. 1.. Start!"],
            "round": 0
        }

    game = session["game_state"]
    p1_active = game["p1_team"][game['p1_active_index']]
    p2_active = game["p2_team"][game['p2_active_index']]
    if game['round'] == 0:
        speed1 = p1_active['speed']
        speed2 = p2_active['speed']
        if speed1 > speed2:
            game['turn'] = "p1"
        else:
            game['turn'] = "p2"
        game['round'] += 1

    if request.method == "POST":
        action = request.form.get("action")

        if action == "p1_taunt":
            game['p1_insult'] = get_insult()
            print(game['p1_insult'])
        elif action == "p2_taunt":
            game['p2_insult'] = get_insult()
        else:

            if game["turn"] == "p1":
                if action.startswith("switch_"):
                    char_id = action.replace("switch_", "")
                    for i, char in enumerate(game['p1_team']):
                        if char['id'] == char_id and char['current_hp'] > 0:
                            game['p1_active_index'] = i
                            p1_active = game["p1_team"][game['p1_active_index']]
                            break
                    game["turn"] = "p2"
                    game['log'].append(f"{session['username']} switched to {p1_active['name']}")
                else:
                    moves = p1_active["moves"]
                    for move in moves:
                        if move['name'] == action:
                            attack_move = move
                    dmg = attack(p1_active, p2_active, attack_move) #need attack function
                    attack_move['pp'] -= 1
                    p2_active['current_hp'] -= dmg
                    game["turn"] = "p2"
                    game['log'].append(f"{p1_active['name']} used {action}")
                    game['log'].append(f"{p2_active['name']} took {dmg} damage")
                    if p2_active['current_hp'] <= 0:
                        index = switch_defeated_character(game['p2_team'])
                        if index == -1:
                            db = sqlite3.connect(DB_FILE)
                            c = db.cursor()
                            wins, rizu_coin = c.execute("SELECT wins, rizu_coin FROM users WHERE name=?", (session['username'],)).fetchone()
                            c.execute("UPDATE users SET wins=?, rizu_coin=? WHERE name=?", (wins+1, rizu_coin+10, session['username']))
                            db.commit()
                            db.close()
                            return redirect(url_for("gameover", winner = session['username']))
                        else:
                            prev_active = p2_active['name']
                            game['p2_active_index'] = index
                            p2_active = game['p2_team'][index]
                            game['log'].append(f"{prev_active} fainted.. Player 2 switched to {p2_active['name']}")

            elif game["turn"] == "p2":
                if action.startswith("switch_"):
                    char_id = action.replace("switch_", "")
                    for i, char in enumerate(game['p2_team']):
                        if char['id'] == char_id and char['current_hp'] > 0:
                            game['p2_active_index'] = i
                            p2_active = game["p2_team"][game['p2_active_index']]
                            break
                    game["turn"] = "p1"
                    game['log'].append(f"Player 2 switched to {p2_active['name']}")
                else:
                    moves = p2_active["moves"]
                    for move in moves:
                        if move['name'] == action:
                            attack_move = move
                    dmg = attack(p2_active, p1_active, attack_move) # need atk func
                    attack_move['pp'] -= 1
                    p1_active['current_hp'] -= dmg
                    game["turn"] = "p1"
                    game['log'].append(f"{p2_active['name']} used {action}")
                    game['log'].append(f"{p1_active['name']} took {dmg} damage")
                    if p1_active['current_hp'] <= 0:
                        index = switch_defeated_character(game['p1_team'])
                        if index == -1:
                            db = sqlite3.connect(DB_FILE)
                            c = db.cursor()
                            losses = c.execute("SELECT losses FROM users WHERE name=?", (session['username'],)).fetchone()[0]
                            c.execute("UPDATE users SET losses=? WHERE name=?", (losses+1, session['username']))
                            db.commit()
                            db.close()
                            return redirect(url_for("gameover", winner = "Player 2"))
                        else:
                            prev_active = p1_active['name']
                            game['p1_active_index'] = index
                            p1_active = game['p1_team'][index]
                            game['log'].append(f"{prev_active} fainted.. {session['username']} switched to {p1_active['name']}")



        session["game_state"] = game
        session.modified = True
        return redirect(url_for("game"))

    return render_template('game.html',
                           player = session['username'],
                           p1_team = game["p1_team"],
                           p2_team = game["p2_team"],
                           p1_active = p1_active,
                           p2_active = p2_active,
                           p1_hp_percent = int((p1_active["current_hp"] / p1_active["hp"]) * 100),
                           p2_hp_percent = int((p2_active["current_hp"] / p2_active["hp"]) * 100),
                           p1_insult = game['p1_insult'],
                           p2_insult = game['p2_insult'],
                           turn = game["turn"],
                           log = game['log'])

@app.route("/gameover", methods=['GET', 'POST'])
def gameover():
    winner = request.args.get('winner')
    return render_template('gameover.html',
                           winner = winner)

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    session.pop('team1', None) # remove loadout
    session.pop('team2', None) # remove loadout
    session.pop('team1_which', None)
    session.pop('team2_which', None)
    session.pop('game_state', None)
    return redirect(url_for('login'))


if __name__=='__main__':
    app.debug = True
    app.run()
