from flask import Flask

from posts.model import db

from weather.routes import weather_bp
from posts.routes import post_bp
from flask_migrate import Migrate
from decouple import config
import psycopg2

DATABASE_USERNAME = config('DATABASE_USERNAME')
DATABASE_USER_PASSWORD = config('DATABASE_USER_PASSWORD')
DATABASE_NAME = config('DATABASE_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_USERNAME}:{DATABASE_USER_PASSWORD}@localhost:5432/{DATABASE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(weather_bp, url_prefix='')
app.register_blueprint(post_bp, url_prefix='')


if __name__ == "__main__":
    app.run(debug=True)
