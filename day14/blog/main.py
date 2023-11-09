from urllib import response
from flask import Flask, render_template
import requests

app = Flask(__name__)
url = "https://api.npoint.io/c790b4d5cab58020d391"


@app.route("/")
def main():
    response = requests.get(url)
    all_blog = response.json()
    return render_template("index.html",blog = all_blog)



if __name__=="__main__":
    app.run(debug=True)