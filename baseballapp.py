from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import random
from Levenshtein import distance
import json
import jsonschema
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Define the JSON schema for the players data
players_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "patternProperties": {
        "^[0-9]+$": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "picture_file_name": {"type": "string"}
            },
            "required": ["name", "picture_file_name"]
        }
    }
}

# Load the players data from the file
with open("players.json", "r") as f:
    players_data = json.load(f)

# Validate the players data against the schema
try:
    jsonschema.validate(players_data, players_schema)
    print("Players data is valid!")
except jsonschema.ValidationError as e:
    print("Players data is invalid:")
    print(e)

players_keys = list(players_data.keys())

@app.route("/")
def index():
    if "restart" in request.form:
        session["score"] = 0
        session["guesses"] = 0
        return redirect(url_for("index"))
    
    random_player_id = random.choice(players_keys)
    if random_player_id not in players_data:
        # If the current player was already removed from the dictionary, choose a new random player
        random_player_id = random.choice(players_keys)
        session["current_player_id"] = random_player_id
    random_player = players_data[random_player_id]
    session["current_player_id"] = random_player_id

    if "score" in session:
        score = session["score"]
    else:
        score = 0
        session["score"] = score
        session["guesses"] = 0

    if not session:
        session["score"] = 0
        session["guesses"] = 0

    return render_template(
        "index.html",
        player={
            "name": random_player["name"],
            "picture_file_name": random_player["picture_file_name"]
        },
        score=session["score"],
    )

@app.route("/submit", methods=["POST"])
def submit():
    player_id = session["current_player_id"]
    player = players_data[player_id]
    guessed_name = request.form["name"].strip().lower()
    last_name = player["name"].split()[-1].lower()
    distance_score = distance(guessed_name.lower(), last_name)
    if distance_score <= 2:
        session["score"] += 1
        message = "Correct!"
        # Remove the guessed player from the players dictionary
        players_data.pop(player_id)
        session["guesses"] += 1
        guesses = 20 - session["guesses"]
    else:
        message = "Incorrect!"
        players_data.pop(player_id)
        session["guesses"] += 1
        guesses = 20 - session["guesses"]
    if session["guesses"] >= 20:
        percentage = session["score"] / 20 * 100
        if percentage >= 65:
            pass_fail = "Congratulations, you passed!"
        else:
            pass_fail = "Try again?"
        return render_template(
            "final.html", 
            score=session["score"],
            percentage=percentage, 
            pass_fail=pass_fail)
    else:
        return render_template(
            "submit.html",
            message=message,
            player={
                "name": player["name"],
                "picture_file_name": player["picture_file_name"]
            },
            score=session["score"],
            guesses=guesses
        )

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)