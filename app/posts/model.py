from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from utils.geolocation import get_coordinates, is_within_range

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_posts(lat, long, page=1, per_page = 5):
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
        return jsonify({'posts': result, 'meta': meta})
    
    def create_post(text, location):
        post = Post(text=text, location=location)
        try:
            db.session.add(post)
            db.session.commit()
            return {"message": "Post created successfully!"}
        except:
            return {"message": "Something went wrong!"}
