from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'api@123'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'files')


# user class which store user properties like is authenticated, is active, is anonyumous  more https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# user_prop = UserMixin()

# Connecting to login manager to use it
login_manager = LoginManager()
login_manager.init_app(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLE IN DB  Usermixin will create a id for user that is created or logged then this user will be used in load user function to check if that user id exist in session
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 
 
with app.app_context():
    db.create_all()



# Login Manager

# user loader checks user id associated with user table in db stored in sesison and will reload user object
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/')
def home():
    return render_template("index.html", logged_in = current_user.is_authenticated)


@app.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        email_check = db.session.execute(db.select(User).where(User.email == request.form['email'])).scalar()
        if email_check:
            flash("Email ID already exist")
            return redirect(url_for("register"))
        
        user_password = request.form['password']
        hash_pass = generate_password_hash(user_password)
        register_data = User(name = request.form['name'], email = request.form['email'],\
                             password = hash_pass)
        
        db.session.add(register_data)
        db.session.commit()
        login_user(register_data)
        return redirect(url_for("secrets", name = request.form["name"]))
    
    return render_template("register.html", logged_in = current_user.is_authenticated)


@app.route('/login',methods = ["POST","GET"])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        user_password = request.form['password']
        result_email = db.session.execute(db.select(User).where(User.email == user_email)).scalar()
        if result_email:
            if check_password_hash(result_email.password, user_password):
                login_user(result_email)
                return redirect(url_for('secrets'))
            else:
                flash("Password is wrong, Try again")
                return redirect(url_for('login'))
        else:
            flash("The email does not exist!")
            return redirect("register")
        
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", username = current_user.name, logged_in = True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'], path = "cheat_sheet.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
