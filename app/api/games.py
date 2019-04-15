from app.api import bp
from flask import jsonify
from app.models import Game

@bp.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    return jsonify(Game.query.get_or_404(id).to_dict())

@bp.route('/games', methods=['GET'])
def get_games():
    data = Game.to_collection_dict(Game.query.all())
    return jsonify(data)

@bp.route('/games', methods=['POST'])
def create_games():
    pass

@bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    pass
