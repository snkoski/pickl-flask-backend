from app.api import bp
from flask import jsonify
from app.models import Game
from app.schemas import GameSchema

@bp.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    one_game = Game.query.get(id)
    game_schema = GameSchema()
    output = game_schema.dump(one_game).data
    return jsonify({'game': output})

@bp.route('/games', methods=['GET'])
def get_games():
    all_games = Game.query.all()
    game_schema = GameSchema(many=True)
    output = game_schema.dump(all_games).data
    return jsonify({'game': output})

@bp.route('/games', methods=['POST'])
def create_games():
    pass

@bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    pass
