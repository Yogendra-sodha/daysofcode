from flask import Flask, render_template, redirect, url_for, request, flash,abort
from functools import wraps
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor, CKEditorField
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, current_user, logout_user
from form import RegisterForm,blogForm, LoginForm, CommentForm
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FK')

Bootstrap5(app)

db = SQLAlchemy()
# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI',"sqlite:///posts.db")
db.init_app(app)

# Start Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CKEDITOR
ckeditor = CKEditor(app)

gravtar = Gravatar(app, size = 50, rating='g',default ='retro',force_default = False, force_lower = False, use_ssl = False,base_url = None)


# New table user entry  -- Parent table
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(250), nullable = False)
    email = db.Column(db.String(250), unique = True, nullable = False)
    password = db.Column(db.String(250), nullable = False)
    posts = relationship("BlogPost", back_populates = "author")
    comment_link = relationship("Comment", back_populates="user_link")


# New table for author blog post  -- Child Table
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User",back_populates = "posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comment_link = relationship("Comment",back_populates="author_link")

# Foreign key blog id, user id, for a comment

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String, nullable = False)
    user_link = relationship("User", back_populates="comment_link")
    uid = db.Column(db.Integer, db.ForeignKey("users.id"))
    author_link = relationship("BlogPost",back_populates="comment_link")
    pid = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))



with app.app_context():
    db.create_all()

# Wrapper for admin
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args,**kwargs)
    return decorated


# Registeration route
@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET","POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email_check = db.session.execute(db.select(User).where(User.email == register_form.email.data)).scalar()
        if email_check:
            flash("Email aldready exists")
            return redirect(url_for('login'))
        else:
            secure_pass = generate_password_hash(register_form.password.data, salt_length=12)
            new_user = User(name = register_form.name.data, email = register_form.email.data,\
                            password = secure_pass)
            db.session.add(new_user)
            db.session.commit()
            flash("Thanks for registering now login!")
            return redirect(url_for('login'))

    return render_template("register.html",register_form = register_form, logged_in = current_user)


# Login Route
@app.route("/login", methods = ["POST","GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        u_email = login_form.email.data
        u_password = login_form.password.data
        user_cred = db.session.execute(db.select(User).where(User.email == u_email)).scalar()
        if user_cred:
            hash_password = user_cred.password
            if check_password_hash(hash_password, u_password):
                login_user(user_cred)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Wrong password")
                return redirect(url_for('login'))
        else:
            flash('Invalid Email')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', login_form = LoginForm(), \
                               logged_in = current_user)


@app.route('/posts')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    result = db.session.execute(db.select(BlogPost)).scalars()
    posts = [i for i in result]
    return render_template("index.html", all_posts=posts, \
                           logged_in = current_user)


# TODO: Add a route so that you can click on individual posts.
@app.route('/<int:post_id>', methods=["GET","POST"])
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    comment = CommentForm()
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalar()
    all_comments = db.session.execute(db.select(Comment).where(Comment.pid == requested_post.id)).scalars()
    if comment.validate_on_submit():
        if not current_user.is_anonymous:
            if len(request.form['comment_body']) == 0:
                print(request.form['comment_body'])
                print(len(request.form['comment_body']))
                return render_template("post.html", post=requested_post, abc = all_comments, form = comment, logged_in = current_user)
            else :
                user_comment = Comment( text = request.form['comment_body'], uid = current_user.id, pid = requested_post.id)
                db.session.add(user_comment)
                db.session.commit()
               
                flash('Comment posted successfully!', 'success')
                return redirect(url_for("show_post", post_id = post_id))
        else:
            flash("Please login or create account to add comment")
            return redirect(url_for("login"))
    return render_template("post.html", post=requested_post, abc = all_comments, form = comment, logged_in = current_user)


# TODO: add_new_post() to create a new blog post
@app.route('/add_post',methods=["GET","POST"])
@login_required
@admin_required
def add_post():
    blog = blogForm()
    if request.method == "POST":
        add_data = BlogPost(author = current_user,title = request.form['title'], 
                            subtitle = request.form['subtitle'], \
                            date = (datetime.datetime.now().strftime("%B %d,%Y")), \
                            body = request.form['body'], \
                            img_url = request.form['url'])  
        db.session.add(add_data)
        db.session.commit()
        return redirect(url_for('get_all_posts'))        
    return render_template("make-post.html", form = blog, is_edit = False, logged_in = current_user)


# TODO: edit_post() to change an existing blog post
@app.route("/edit/<int:id>", methods=["POST","GET"])
@login_required
@admin_required
def edit_post(id):
    edit_query = db.session.execute(db.select(BlogPost).where(BlogPost.id==id)).scalar()
    if request.method == "GET":
        edit_form = blogForm(
            title = edit_query.title,
            subtitle = edit_query.subtitle,
            url = edit_query.img_url,
            body = edit_query.body,
            name = edit_query.author.name
        )
        return render_template("make-post.html", form = edit_form,\
                                is_edit = True, id = id,\
                                logged_in = current_user)
    else:
        edit_query.title = request.form['title']
        edit_query.subtitle = request.form['subtitle']
        edit_query.body = request.form['body']
        edit_query.author.name = request.form['name']
        edit_query.img_url = request.form['url']
        db.session.commit()
        return redirect(url_for('get_all_posts'))  


# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
@login_required
@admin_required
def del_post(post_id):
    del_query = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(del_query)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Delete comment
@app.route("/delete_comment/<int:id>")
@login_required
def delete_comment(id):
    if not current_user.is_anonymous:
        del_comm = db.session.execute(db.select(Comment).where((Comment.id == id) & (Comment.uid == current_user.id))).scalar()
        if del_comm:
            pid = del_comm.pid
            db.session.delete(del_comm)
            db.session.commit()
            return redirect(url_for("show_post", post_id = pid))
        else:
            return "You cannot delete others comment only del yours"
    else:
        return "You cannot delete comment login to del your comment"

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html", logged_in = current_user)

@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in = current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)