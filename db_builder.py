from cs50 import SQL
from helpers import read_json, write_json
db = SQL("sqlite:///auto_aid.db")

info = read_json("static/assets.json")
locations = info["states"]

for location in locations:
    db.execute("INSERT INTO locations (name) VALUES (?);", location)
