from flask import Flask, render_template
import random
from datetime import date, datetime
import requests

app = Flask(__name__)

age_url = "https://api.genderize.io?name="
gender_url= "https://api.agify.io?name="

age_url,gender_url = gender_url,age_url

@app.route("/")
def home():
    rnd_num = random.randint(1,9)
    crr_year  = datetime.now()
    crr_year = str(crr_year)[:4]
    return render_template("index.html",num=rnd_num,dt=crr_year)

@app.route("/<name>")
def guess(name):
    n_age_url = age_url+str(name)
    age = requests.get(n_age_url)
    age_res = age.json()
    user_age = age_res["age"]

    n_gender_url = gender_url+str(name)
    gender = requests.get(n_gender_url)
    gender_res = gender.json()
    user_gender = gender_res["gender"]

    crr_year  = datetime.now()
    crr_year = str(crr_year)[:4]

    return render_template("user.html",username = name, age = user_age, gender = user_gender,dt=crr_year)

    



if __name__ == "__main__":
    app.run(debug=True)

