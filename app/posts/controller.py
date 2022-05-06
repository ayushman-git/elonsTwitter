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

def get_posts(page=1):
    per_page = 5
    lat = request.args.get('lat')
    long = request.args.get('long')
    lat, long = float(lat), float(long)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page,per_page,error_out=False)
    result = []
    for post in posts.items:
        coord = get_coordinates(post.location)
        print(is_within_range(lat, long, coord[0], coord[1], 10000))
        if is_within_range(lat, long, coord[0], coord[1], 10000):
            result.append(post.as_dict())
    meta = {
        "total_pages": posts.pages,
        "total_posts": posts.total,
        "current_page": posts.page,
        "per_page": per_page
    }
    print(result)
    return jsonify({'posts': result, 'meta': meta})