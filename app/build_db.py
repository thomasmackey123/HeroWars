import sqlite3

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

#create tables if it isn't there already
c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL COLLATE NOCASE, password TEXT NOT NULL, wins INTEGER, losses INTEGER, rizu_coin INTEGER, profile_pic TEXT, UNIQUE(name))")
