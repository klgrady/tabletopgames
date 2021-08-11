from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nvjakxzsrsqont:8f2fb7d914222456dcba76358b954ac2beaf67c55e72537df610bc6991403e17@ec2-52-72-125-94.compute-1.amazonaws.com:5432/dd7ln5hctfhhv9'
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

