from flask import Flask

from posts.model import db

from weather.routes import weather_bp
from posts.routes import post_bp

print(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db.init_app(app)

app.register_blueprint(weather_bp, url_prefix='')
app.register_blueprint(post_bp, url_prefix='')

@app.route("/")
def index():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    app.run(debug=True)