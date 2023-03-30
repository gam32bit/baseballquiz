from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import random
from Levenshtein import distance
import json
import jsonschema
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

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
        session["player_ids"] = list(players_data.keys())
        return redirect(url_for("index"))   
    # Initialize session variables if they don't exist yet
    if "player_ids" not in session:
        session["player_ids"] = list(players_data.keys())
    if "score" not in session:
        session["score"] = 0
        session["guesses"] = 0
        
    # Select a random player ID from the list of available IDs stored in the session
    random_player_id = random.choice(session["player_ids"])
    
    # Retrieve the player object using the selected ID
    random_player = players_data[random_player_id]
    
    # Update the current_player_id stored in the session
    session["current_player_id"] = random_player_id
    
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
    player_id = session.get("current_player_id")
    player = players_data[player_id]
    guessed_name = request.form["name"].strip().lower()
    last_name = player["name"].split()[-1].lower()
    distance_score = distance(guessed_name.lower(), last_name)
    if distance_score <= 2:
        session["score"] += 1
        message = "Correct!"
        # Remove the guessed player from the players dictionary
        session["player_ids"].remove(player_id)
        session["guesses"] += 1
        guesses = 20 - session.get("guesses")
    else:
        message = "Incorrect!"
        session["player_ids"].remove(player_id)
        session["guesses"] += 1
        guesses = 20 - session.get("guesses")
    if session["guesses"] >= 20:
        percentage = session.get("score") / 20 * 100
        if percentage >= 65:
            pass_fail = "Congratulations, you passed!"
        else:
            pass_fail = "Try again?"
        return render_template(
            "final.html", 
            score=session.get("score"),
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
            score=session.get("score"),
            guesses=guesses
        )

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)