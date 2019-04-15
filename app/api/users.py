from app.api import bp
from flask import jsonify
from app.models import User
from flask import request
from app.schemas import UserSchema

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    one_user = User.query.get(id)
    user_schema = UserSchema()
    output = user_schema.dump(one_user).data
    return jsonify({'user' : output})

@bp.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(all_users).data
    return jsonify({'user': output})

@bp.route('/users', methods=['POST'])
def create_users():
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
