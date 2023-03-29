from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
from Levenshtein import distance

app = Flask(__name__)


class Player(object):
    def __init__(self, id, name, picture_file_name):
        self.name = name
        self.picture_file_name = picture_file_name
        self.id = id


# TODO: Read this in from players.json, once on app startup, instaed of hardcoding
players = {
    1: Player(1, "Doe, John", "jon_doe.jpg"),
}
players_keys = list(players.keys())


@app.route("/")
def index():
    if request.method == "POST" and "restart" in request.form:
        session["score"] = 0
        session["total_guesses"] = 0
        return redirect(url_for("index"))

    # players = BaseballPlayer.query.all()
    random_player = players[random.choice(players_keys)]
    session["current_player_id"] = random_player.id
    # Check if 'score' is already present in the session
    if "score" in session:
        score = session["score"]
    else:
        score = 0
        session["score"] = score

    if not session:
        session["score"] = 0
        session["guesses"] = 0

    return render_template(
        "index.html",
        player={
            "name": random_player.name,
            "id": random_player.id,
            "picture_file_name": random_player.picture_file_name,
        },
        score=session["score"],
    )


@app.route("/submit", methods=["POST"])
def submit():
    player_id = session["current_player_id"]
    player = players[player_id]
    guessed_name = request.form["name"]
    # Calculate the Levenshtein distance between the guessed name and the actual name
    distance_score = distance(guessed_name.lower(), player.name.lower())
    # If the distance is less than or equal to 2 (i.e., the guessed name is mostly right), consider it correct
    if distance_score <= 2:
        session["score"] += 1
        message = "Correct!"
    else:
        message = "Incorrect!"
    # Increment the guess counter
    session["guesses"] = session.get("guesses", 0)
    session["guesses"] += 1
    # Check if the user has made 20 guesses
    if session["guesses"] >= 20:
        # Calculate the percentage of correct answers
        percentage = session["score"] / 20 * 100
        # Set the message and pass/fail status based on the percentage
        if percentage >= 65:
            pass_fail = "Congratulations, you passed!"
        else:
            pass_fail = "Try again?"
        # Reset the score and guess counter
        session["score"] = 0
        session["guesses"] = 0
        # Render the final page
        return render_template("final.html", percentage=percentage, pass_fail=pass_fail)
    # If the user hasn't made 20 guesses yet, render the submit page
    else:
        return render_template(
            "submit.html",
            message=message,
            player={
                "name": player.name,
                "id": player.id,
                "picture_file_name": player.picture_file_name,
            },
            score=session["score"],
        )


@app.route("/restart")
def restart():
    # Reset the score and guess counter
    session["score"] = 0
    session["guesses"] = 0
    # Redirect the user to the index page as if they were starting a new session
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = "some_secret_key"
    app.run(debug=True)
