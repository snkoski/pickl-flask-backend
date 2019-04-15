from app.api import bp
from flask import jsonify
from app.models import Team
from app.schemas import TeamSchema

@bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    one_team = Team.query.get(id)
    team_schema = TeamSchema()
    output = team_schema.dump(one_team).data
    return jsonify({'team': output})
@bp.route('/teams', methods=['GET'])
def get_teams():
    all_teams = Team.query.all()
    team_schema = TeamSchema(many=True)
    output = team_schema.dump(all_teams).data
    return jsonify({'team': output})

@bp.route('/teams', methods=['POST'])
def create_teams():
    pass

@bp.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    pass
