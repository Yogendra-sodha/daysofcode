from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField,URLField
from wtforms.validators import DataRequired, URL,InputRequired
from flask_ckeditor import CKEditor, CKEditorField
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

db = SQLAlchemy()

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db.init_app(app)

# CKEDITOR
ckeditor = CKEditor(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    


# add Blog form

class blogForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    name = StringField("Author Name", validators=[InputRequired()])
    url = URLField("BG-Image URL", validators=[URL()])
    body = CKEditorField("Body")
    submit = SubmitField("Add Blog")

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    result = db.session.execute(db.select(BlogPost)).scalars()
    posts = [i for i in result]
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalar()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add_post',methods=["GET","POST"])
def add_post():
    blog = blogForm()
    if request.method == "POST":
        add_data = BlogPost(title = request.form['title'], subtitle = request.form['subtitle'], \
                            date = (datetime.datetime.now().strftime("%B %d,%Y")), \
                            body = request.form['body'], author = request.form['name'],\
                            img_url = request.form['url'])  
        db.session.add(add_data)
        db.session.commit()
        return redirect(url_for('get_all_posts'))        

    return render_template("make-post.html", form = blog, is_edit = False)


# TODO: edit_post() to change an existing blog post
@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit_post(id):
    edit_query = db.session.execute(db.select(BlogPost).where(BlogPost.id==id)).scalar()
    if request.method == "GET":
        edit_form = blogForm(
            title = edit_query.title,
            subtitle = edit_query.subtitle,
            url = edit_query.img_url,
            body = edit_query.body,
            name = edit_query.author
        )
        return render_template("make-post.html", form = edit_form, is_edit = True, id = id)
    else:
        edit_query.title = request.form['title']
        edit_query.subtitle = request.form['subtitle']
        edit_query.body = request.form['body']
        edit_query.author = request.form['name']
        edit_query.img_url = request.form['url']
        
        db.session.commit()
        return redirect(url_for('get_all_posts'))  


    

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
def del_post(post_id):
    del_query = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(del_query)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
