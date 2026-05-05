# Number guessing game logic
import random

MAX_TRIES = 10

def new_game():
    return {"secret": random.randint(1, 100), "tries": 0, "game_over": False, "won": False}

def process_guess(state, user_input):
    secret = state["secret"]
    user_input = user_input.strip()

    if user_input.lower() == "konami code":
        return f"🎮 Konami code accepted! You get a free peek: the secret is {secret}"

    if user_input.lower() == "let the cat out of the bag":
        return f"🐱 The cat is out of the bag! The secret number is {secret}"

    try:
        guess = int(user_input)
        state["tries"] += 1
    except ValueError:
        state["tries"] += 1
        if state["tries"] >= MAX_TRIES:
            state["game_over"] = True
            return f"Type a number bub! Game over. The secret was {secret}."
        return "Type a number bub! hahahahaha! You lost 1 guess!"

    if guess < 1 or guess > 100:
        state["tries"] += 1
        if state["tries"] >= MAX_TRIES:
            state["game_over"] = True
            return f"That's not even in the range! Game over. The secret was {secret}."
        return "That's not even in the range! You lost 1 guess!"

    if guess == secret:
        state["game_over"] = True
        state["won"] = True
        return f"You guessed it! It was... {secret} 🎉 You win!"

    if state["tries"] >= MAX_TRIES:
        state["game_over"] = True
        return f"You suck! Keep trying! I like to see you fail! Oh by the way, the secret number was {secret}!"

    if guess < secret:
        return "Too low! 📉"
    return "Too high! 📈"
