# import sqlite3

# db = sqlite3.connect("demo_collections.db")

# cursor = db.cursor()

# # cursor.execute(" CREATE TABLE demo ( id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250), rating float not null) ")

# cursor.execute(" INSERT INTO demo VALUES(1, 'Harry Porter', 'Prans Savani', 5.8 ) ")
# db.commit()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

# Create Database in flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# Intialize app for sqlalchemy
db.init_app(app)

# Create table for database
class demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable = False)
    author = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.String, nullable=False)


# creating table in context of flask application so flask will be ready for database operation
with app.app_context():
    db.create_all()

# create a record
with app.app_context():
    new_book = demo( title="Ha Pter", author=" owling", rating=3)
    db.session.add(new_book)
    db.session.commit()

# select a record
with app.app_context():
    query = db.session.execute(db.select(demo).order_by(demo.id)).scalars()
    print(len(query.all()))
    

# # update a record
# with app.app_context():
#     query = db.session.execute(db.select(demo).where(demo.id==2)).scalar()
#     query.title = "Harry Singh"
#     db.session.commit()

# Delete a record
# with app.app_context():
#     query = db.session.execute(db.select(demo)).scalar()
#     db.session.delete(query)
#     db.session.commit()


    