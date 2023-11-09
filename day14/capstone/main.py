# from atoti import is_temporal_type
from flask import Flask, render_template, request
from post import Post

app = Flask(__name__)

user = Post()
blog_json = user.blog_locater()

@app.route('/')
def home():
    return render_template("index.html",blog = blog_json)


@app.route("/post/<num>")
def get_blog(num):
    pst = [ (i["title"],i["body"]) for i in blog_json if i["id"] == int(num) ]
    print(pst)
    title = pst[0][0]
    body = pst[0][1]
    return render_template("post.html",blog_title = title, blog_body = body)


if __name__ == "__main__":
    app.run(debug=True)
