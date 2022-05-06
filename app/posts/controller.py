from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from posts.model import Post
from utils.geolocation import get_coordinates, is_within_range

db = SQLAlchemy()

def create_post():
  text = request.form.get("text")
  location = request.form.get("location")
  post = Post(text=text, location=location)
  try:
      db.session.add(post)
      db.session.commit()
      return {"message": "Post created successfully!"}
  except:
      return {"message": "Something went wrong!"}

def get_posts():
    page = 1
    try:
        page = int(request.args.get("page"))
    except:
        pass
    per_page = 2

    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))

    return Post.get_posts(lat, long, page, per_page)