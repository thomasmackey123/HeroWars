# Description
Hero Wars is a local two-player Pokemon showdown game, where we use anime characters and superheroes instead of Pokemons using the Jikan API and the Superheroes API. For the in-game stats, we will get data from those API’s and convert those info into in-game stats. Those stats will be assigned to random Pokemon moves and be given to the superheroes and anime characters.
# Install Guide
1. Clone the repository
```
git clone git@github.com:SadgeCat/p01_Teem_sqrt4469.git HeroWars
```
2. Navigate into the cloned directory
```
cd HeroWars
```
3. Create virtual environment
```
python -m venv venv
```
4. Activate virtual environment (macOS/Linux)
```
. venv/bin/activate
```
5. Install packages
```
pip install -r requirements.txt
```
# Launch Codes
1. Create database
```
python app/build_db.py
```
2. Launch app
```
python app/__init__.py
```
3. In a browser, open the running app on
```
http://127.0.0.1:5000
```
