from flask import Flask,render_template,request
from ipykernel import connect_qtconsole
import requests
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

url_endpoint = "https://api.npoint.io/16275a14f720fade2a81"
post_json = requests.get(url_endpoint)
post_json = post_json.json()

@app.route("/")
def get_all_posts():
    return render_template("index.html",data=post_json)

@app.route("/<int:id>")
def full_posts(id):
    # title/subtitle/image/date/author/body
    author_post = [post for post in post_json if post['id'] == id]
    return render_template("post.html",ind_data=author_post[0])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/form-input", methods=["POST","GET"])
def recieve_data():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        print(name,email)
        send_email(name,email,phone,message)
        return render_template("contact.html")
    else:
        return render_template("error.html")
    

def send_email(name,email,phone,message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    OWN_EMAIL = "yssodhas@gmail.com"
    OWN_PASSWORD = "znmuhcibyxfdxblo"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=OWN_EMAIL, password=OWN_PASSWORD)
        connection.sendmail(email, OWN_EMAIL, email_message)
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)