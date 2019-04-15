from app.api import bp
from flask import jsonify
from app.models import Team

@bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    return jsonify(Team.query.get_or_404(id).to_dict())

@bp.route('/teams', methods=['GET'])
def get_teams():
    data = Team.to_collection_dict(Team.query.all())
    return jsonify(data)

@bp.route('/teams', methods=['POST'])
def create_teams():
    pass

@bp.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    pass
