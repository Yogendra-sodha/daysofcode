from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"

db.init_app(app)

# create table
class books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# with app.app_context():
#     db.create_all()



@app.route('/')
def home():
    view_data = db.session.execute(db.select(books))
    view_data =view_data.scalars()
    view_data = [row for row in view_data]
    return render_template('index.html' , data = view_data)


@app.route("/add", methods=["POST","GET"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_data = books(name = request.form['bname'], author = request.form['author'], rating = request.form['rating'])
            db.session.add(new_data)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html')

# Edit
@app.route("/edit/<id>",methods=["POST","GET"])
def edit(id):
    edit_query = db.session.execute(db.select(books).where(books.id==id)).scalar()
    if request.method == "POST":
        edit_query.rating = float(request.form['rating'])
        db.session.add(edit_query)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', row = edit_query)

# delete
@app.route("/delete/<id>")
def delete_row(id):
    id = int(id)
    del_query = db.session.execute(db.select(books).where(books.id==id)).scalar()
    db.session.delete(del_query)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)