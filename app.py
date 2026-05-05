from flask import Flask, render_template, request, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "emmet-guessing-game"

MAX_TRIES = 10

def new_game():
    session["secret"] = random.randint(1, 100)
    session["tries"] = 0
    session["game_over"] = False
    session["won"] = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    if "secret" not in session or session.get("game_over"):
        new_game()
    return render_template("game.html")

def respond(message, status):
    return jsonify({"message": message, "status": status, "tries": session["tries"], "tries_left": MAX_TRIES - session["tries"]})

@app.route("/guess", methods=["POST"])
def guess():
    if session.get("game_over"):
        return respond("Game is over. Start a new game!", "over")

    user_input = request.json.get("guess", "").strip()
    secret = session["secret"]

    # Easter eggs — no guess cost
    if user_input.lower() == "konami code":
        return respond(f"🎮 Konami code accepted! You get a free peek: the secret is {secret}", "playing")

    if user_input.lower() == "let the cat out of the bag":
        return respond(f"🐱 The cat is out of the bag! The secret number is {secret}", "playing")

    try:
        guess_val = int(user_input)
        session["tries"] += 1
    except ValueError:
        session["tries"] += 1
        if session["tries"] >= MAX_TRIES:
            session["game_over"] = True
        return respond("Type a number bub! hahahahaha! You lost 1 guess!", "lose" if session["game_over"] else "playing")

    if guess_val < 1 or guess_val > 100:
        session["tries"] += 1
        if session["tries"] >= MAX_TRIES:
            session["game_over"] = True
        return respond("That's not even in the range! You lost 1 guess!", "lose" if session["game_over"] else "playing")

    if guess_val == secret:
        session["game_over"] = True
        session["won"] = True
        return respond(f"You guessed it! It was... {secret} 🎉 You win!", "win")

    if session["tries"] >= MAX_TRIES:
        session["game_over"] = True
        return respond(f"You suck! Keep trying! I like to see you fail! Oh by the way, the secret number was {secret}!", "lose")

    if guess_val < secret:
        return respond("Too low! 📉", "playing")
    return respond("Too high! 📈", "playing")

@app.route("/new-game", methods=["POST"])
def new_game_route():
    new_game()
    return jsonify({"message": "New game started! Guess a number between 1 and 100.", "tries_left": MAX_TRIES})

if __name__ == "__main__":
    import os
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
