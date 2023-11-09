from flask import Flask
app = Flask(__name__)


def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper

def make_underline(function):
    def underline():
        return f"<u>{function()}</u>"
    return underline

# @app.route("/")
# def hello_world():
#     return "Home page"

@app.route("/username/<name>/<int:number>")
def user(name,number):
    return f"Hello {name} and you are {number}"

@app.route("/bye")
@make_underline
@make_bold
def bye():
    return "Bye"


if __name__ == "__main__":
    app.run(debug=True)