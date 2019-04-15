from app.api import bp
from flask import jsonify
from app.models import User
from flask import request

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    data = User.to_collection_dict(User.query)
    return jsonify(data)

@bp.route('/users', methods=['POST'])
def create_users():
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
