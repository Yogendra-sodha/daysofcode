from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Guess a number between 0 and 9</h1> \
            <img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' \
            width='500' height='600'>"

rnd_num = random.randint(0,9)

@app.route("/<int:num>")
def user_input(num):
    if num>rnd_num:
        return "<h1> Too high </h1> \
            <img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif' \
            width='500' height='600'>"
    elif num < rnd_num:
        return "<h1> Too Low!! </h1> \
            <img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif' \
            width='500' height='600'>"
    else:
        return "<h1> You found me </h1> \
            <img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif' \
            width='500' height='600'>"

if __name__ == "__main__":
    app.run(debug=True)