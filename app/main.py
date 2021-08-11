from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

class games(db.Model):
    id = db.Column('games_id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(255))
    year = db.Column('year', db.String(4))
    description = db.Column('description', db.String(255))
    type = db.Column('type', db.String(20))

    def __init__(self, name, year, description, type):
        self.name = name
        self.year = year
        self.desc = description
        self.type = type

        db.create_all()



@app.route('/')
def index():
    return render_template('index.html', env=games.query.all())

