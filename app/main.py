"""
    Routes and Games database model and API-ing, oh my!
    Creates database model for games database
"""

from flask import Flask, render_template, request, Response, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = "982370fnkjdlfakjsdh2iuhf2nj23ijnfij32u3nb2tikj32"
db = SQLAlchemy(app)

"""
    Set games table to hold games_id as primary key, name as game title, year as release date, description as game description, and type as defined:
        
        CREATE TYPE game_type AS ENUM ('board game','dice game','card game','RPG','strategy game','tile game');

    
"""
class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column('games_id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(70))
    year = db.Column('year', db.String(4))
    description = db.Column('description', db.String(255))  # highly inconvenient constraint
    type = db.Column('type', db.String(20))

    def __init__(self, name, year, description, type):
        self.name = name
        self.year = year
        self.desc = description
        self.type = type

        db.create_all()


"""
    Main call allows for full list of games or results of form input keyword constraint
"""
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
    return render_template('index.html', games=games)


"""
    Returns the index.html template with results from a board games-only query
"""
@app.route('/board-games')
def board_games():
    page = request.args.get('page', 1, type=int)
    games = Games.query.filter_by(type="board_game").paginate(page=page, per_page=20)
    return render_template('index.html', games=games)

"""
    Returns the index.html template with results from a strategy games-only query
"""
@app.route('/strategy-games')
def strategy_games():
    page = request.args.get('page', 1, type=int)
    games = Games.query.filter_by(type="strategy_game").paginate(page=page, per_page=20)
    return render_template('index.html', games=games)

"""
    Returns the index.html template with results from a tile games-only query
"""
@app.route('/tile-games')
def tile_games():
    page = request.args.get('page', 1, type=int)
    games = Games.query.filter_by(type="tile_game").paginate(page=page, per_page=20)
    return render_template('index.html', games=games)

"""
    Returns the index.html template with results from a dice games-only query
"""
@app.route('/dice-games')
def dice_games():
    page = request.args.get('page', 1, type=int)
    games = Games.query.filter_by(type="dice_game").paginate(page=page, per_page=20)
    return render_template('index.html', games=games)

"""
    Returns the index.html template with results from a card games-only query
"""
@app.route('/card-games')
def card_games():
    page = request.args.get('page', 1, type=int)
    games = Games.query.filter_by(type="card_game").paginate(page=page, per_page=20)
    return render_template('index.html', games=games)

"""
    Returns the index.html template with results from a role playing games-only query
"""
@app.route('/RPG')
def rpg_games():
    page = request.args.get('page', 1, type=int)
    games = Games.query.filter_by(type="RPG").paginate(page=page, per_page=20)
    return render_template('rpg.html', games=games)

"""
    Runs a GET insert with a CRAZY holy bananas URL
"""
@app.route('/insert-games/<name>/<year>/<desc>/<type>')
def insert(name, year, desc, type):
    insertion = f'{name} ({year}) - {desc} #{type}'
    name.replace("'", "''")
    desc.replace("'", "''")
    game = Games(name=name, year=year, description=desc, type=type)
    db.session.add(game)
    db.session.commit()
    return render_template('success.html', insertion=insertion)


"""
    API call for a POST insert of a game row
"""
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

"""
    Returns POST or GET query response as JSON
"""
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