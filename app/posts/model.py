from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from geoalchemy2.types import Geometry
from sqlalchemy import func
from utils.geolocation import get_coordinates, is_within_range
from shapely import wkb

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    location = db.Column(Geometry('POINT'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text, location):
        self.text = text
        self.location = location

    def __repr__(self):
        return '<Post %r>' % self.location

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}
    def as_dict(self):
        d = {}
        for column in self.__table__.columns:
            if(column.name == 'location'):
                d[column.name] = wkb.loads(
                    bytes(getattr(self, column.name).data))
            else:
                d[column.name] = str(getattr(self, column.name))

        return d

    def get_posts(location, page=1, per_page=5):
        hundred_km = 100 * 10000
        posts_within_ten_km = Post.query.filter(
            func.ST_DistanceSphere(Post.location, f'POINT({location})') < hundred_km).order_by(
            func.ST_DistanceSphere(Post.location, f'POINT({location})')).paginate(
            page, per_page, error_out=False)
        result = []
        for post in posts_within_ten_km.items:
            result.append(post.as_dict())

        meta = {
            "total_pages": posts_within_ten_km.pages,
            "total_posts_within_ten_km": posts_within_ten_km.total,
            "current_page": posts_within_ten_km.page,
            "per_page": per_page
        }
        return jsonify({'meta': meta, 'posts': result})

    def create_post(text, location):
        post = Post(text=text, location='POINT({})'.format(location))
        try:
            db.session.add(post)
            db.session.commit()
            return {"message": "Post created successfully!"}
        except:
            return {"message": "Something went wrong!"}
