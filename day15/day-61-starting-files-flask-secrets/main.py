from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Email,Length
from flask_bootstrap import Bootstrap5


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.secret_key = "anythingispublic"


class userForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email(check_deliverability=True)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=25)])
    submit = SubmitField('Submit')


@app.route("/",methods=["POST","GET"])
def home():
    return render_template('index.html')

@app.route("/login",methods=["POST","GET"])
def login():
    user_form = userForm()
    email_id = "admin@email.com"
    pid = "12345"
    if user_form.validate_on_submit():
        if user_form.email.data == email_id and user_form.password.data == pid:
            return render_template('success.html')
        else:
            return render_template('denied.html')
    else:
        return render_template('login.html', form=user_form)


if __name__ == '__main__':
    app.run(debug=True)
