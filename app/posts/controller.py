from flask import request
from flask_sqlalchemy import SQLAlchemy
from posts.model import Post

db = SQLAlchemy()

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

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))

    return Post.get_posts(lat, long, page, per_page)