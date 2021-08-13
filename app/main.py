from flask import Flask, render_template, request, Response, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nvjakxzsrsqont:8f2fb7d914222456dcba76358b954ac2beaf67c55e72537df610bc6991403e17@ec2-52-72-125-94.compute-1.amazonaws.com:5432/dd7ln5hctfhhv9'
app.config['SECRET_KEY'] = "982370fnkjdlfakjsdh2iuhf2nj23ijnfij32u3nb2tikj32"
db = SQLAlchemy(app)

class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column('games_id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(70))
    year = db.Column('year', db.String(4))
    description = db.Column('description', db.String(255))
    type = db.Column('type', db.String(20))

    def __init__(self, name, year, description, type):
        self.name = name
        self.year = year
        self.desc = description
        self.type = type

        db.create_all()



@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        page = request.form.get('page', 1, type=int)
        if request.form.get("col") == "name":
            games = Games.query.filter_by(name=request.form.get("term")).paginate(page=page, per_page=20)
        elif request.form.get("col") == "description":
            games = Games.query.filter(Games.description.contains(request.form.get("term"))).paginate(page=page, per_page=20)
        else:
            games = Games.query.filter_by(type=request.form.get("term")).paginate(page=page, per_page=20)
    else:
        page = request.args.get('page', 1, type=int)
        games = Games.query.paginate(page=page, per_page=20)
    # results = [
    #     {
    #         "name": game.name,
    #         "year": game.year,
    #         "desc": game.description,
    #         "type": game.type
    #     } for game in games.items]
    return render_template('index.html', games=games)


@app.route('/insert-games/<name>/<year>/<desc>/<type>')
def insert(name, year, desc, type):
    insertion = f'{name} ({year}) - {desc} #{type}'
    name.replace("'", "''")
    desc.replace("'", "''")
    game = Games(name=name, year=year, description=desc, type=type)
    db.session.add(game)
    db.session.commit()
    return render_template('success.html', insertion=insertion)


@app.route('/v1/insert', methods=["POST"])
def api_insert():
    name = request.form.get("name")
    year = request.form.get("year")
    desc = request.form.get("desc")
    type = request.form.get("type")
    name.replace("'", "''")
    desc.replace("'", "''")
    game = Games(name=name, year=year, description=desc, type=type)
    try:
        db.session.add(game)
        db.session.commit()
    except:
        return Response(status=417)

    return Response(status=201)

@app.route('/v1/games/board', methods=["POST", "GET"])
def api_games_select():
    if request.method == "POST":
        term = request.form.get("keyword")
    elif request.method == "GET":
        term = request.args.get("keyword")
    if term is None:
        abort(419)
    games = Games.query.filter(Games.description.contains(term)).filter_by(type="board_game")
    results = [
        {
            "name": game.name,
            "year": game.year,
            "desc": game.description,
            "type": game.type
        } for game in games]
    return jsonify(results), 200