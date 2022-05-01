from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.geolocation import get_coordinates, is_within_range

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/")
def index():
    return {"message": "Hello World!"}

@app.route("/posts", methods=["GET"])
def get_posts():
    lat = request.args.get('lat')
    long = request.args.get('long')
    lat, long = float(lat), float(long)
    # return all posts
    posts = Post.query.all()
    result = []
    for post in posts:
        coord = get_coordinates(post.location)
        if is_within_range(lat, long, coord[0], coord[1], 10000):
            result.append(post.as_dict())
    return jsonify(result)

@app.route("/post/create", methods=["POST"])
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

if __name__ == "__main__":
    app.run(debug=True)