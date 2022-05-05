from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.geolocation import get_coordinates, is_within_range
from decouple import config
import requests
import json

API_KEY = config('WEATHER_API_KEY')

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

@app.route('/posts', methods=['GET'], defaults={"page": 1}) 
@app.route("/posts/<int:page>", methods=["GET"])
def get_posts(page=1):
    per_page = 2
    print(page)
    lat = request.args.get('lat')
    long = request.args.get('long')
    lat, long = float(lat), float(long)
    posts = Post.query.order_by(Post.date_created).paginate(page,per_page,error_out=False)
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

@app.route("/post/create", methods=["POST"])
def create_post():
    text = request.form.get("text")
    location = request.form.get("location")
    post = Post(text=text, location=location)
    print(post.as_dict())
    try:
        db.session.add(post)
        db.session.commit()
        return {"message": "Post created successfully!"}
    except:
        return {"message": "Something went wrong!"}


@app.route("/weather", methods=["GET"])
def get_weather():
    lat = request.args.get('lat')
    long = request.args.get('long')
    print(lat, long)
    response_API = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}")
    data = json.loads(response_API.text)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)