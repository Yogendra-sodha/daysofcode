from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, EmailField, PasswordField
from wtforms.validators import InputRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTF form for creating blog
class blogForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    name = StringField("Author Name", validators=[InputRequired()])
    url = URLField("BG-Image URL", validators=[URL()])
    body = CKEditorField("Body")
    submit = SubmitField("Add Blog")


# Registration form for new user
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email-ID", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Register")


# Login form:
class LoginForm(FlaskForm):
    email = EmailField("Email-ID", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")

# Comment Form
class CommentForm(FlaskForm):
    comment_body = CKEditorField("Comment")
    submit = SubmitField("Post Comment")