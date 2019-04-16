from app import db
from app.api import bp
from app.api.errors import bad_request
from flask import jsonify, url_for
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
def create_user():
    user_schema = UserSchema()
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email, and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    output = user_schema.dump(user).data
    response = jsonify({'user': output})
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
