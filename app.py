from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)