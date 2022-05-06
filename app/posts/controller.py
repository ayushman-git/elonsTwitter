from flask import request
from flask_sqlalchemy import SQLAlchemy
from posts.model import Post

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