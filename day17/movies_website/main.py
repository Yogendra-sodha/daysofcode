from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, URLField, TextAreaField
from wtforms.validators import DataRequired,InputRequired

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
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie_rankings.db"
db = SQLAlchemy()


db.init_app(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    title = db.Column(db.String, unique=True,nullable=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    url = db.Column(db.String)

class AddForm(FlaskForm):
    title = StringField("Title",validators=[InputRequired()])
    year = IntegerField("Year",validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    rating = FloatField("Rating",validators=[InputRequired()])
    ranking = IntegerField("Ranking",validators=[InputRequired()])
    review = StringField("Review", validators=[InputRequired()])
    image_url = URLField("Image", validators=[InputRequired()])
    submit = SubmitField("ADD")

class EditForm(FlaskForm):
    rating = FloatField("Rating",validators=[InputRequired()])
    review = StringField("Your review", validators=[InputRequired()])
    submit = SubmitField("ADD")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    # select query
    select_movie = db.session.execute(db.select(Movies).order_by(Movies.rating.desc())).scalars()
    select_movie = [movie for movie in select_movie]
    return render_template("index.html",movie_list=select_movie)

# Add movies
@app.route("/add",methods=["POST","GET"])
def add_movies():
    add_movie_form = AddForm()
    if request.method == "GET":
        return render_template("add.html",form = add_movie_form)
    else:
        add_query = Movies(title = request.form['title'], year = request.form['year'], \
                           description = request.form['description'], rating = request.form['rating'],\
                            ranking = request.form['ranking'], \
                            review = request.form['review'], url = request.form['image_url']
                        )
        db.session.add(add_query)
        db.session.commit()
        return redirect(url_for('home')) 


# Update Reviews
@app.route("/update/<int:id>",methods=["POST","GET"])
def update_movies(id):
    # id = int(id)
    edit_movie = db.session.execute(db.select(Movies).where(Movies.id == id)).scalar()
    if request.method == "POST":
        edit_movie.rating = request.form['rating']
        edit_movie.review = request.form['review']
        db.session.add(edit_movie)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        edit_form = EditForm()
        return render_template("edit.html",movie = edit_movie,form=edit_form)
    
# Delete movies
@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete_movie(id):
    delete_query = db.session.execute(db.select(Movies).where(Movies.id == id)).scalar()
    db.session.delete(delete_query)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
