from flask import request
from flask_sqlalchemy import SQLAlchemy
from posts.model import Post

db = SQLAlchemy()


def index():
    return {"message": "Hello World!"}


def create_post():
    text = request.form.get("text")
    location = request.form.get("location")
    return Post.create_post(text, location)


def get_posts():
    page = 1
    per_page = 2

    try:
        page = int(request.args.get("page"))
    except:
        pass

    location = request.args.get('location')

    return Post.get_posts(location, page, per_page)
