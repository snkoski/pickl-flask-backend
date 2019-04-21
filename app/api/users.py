from flask import jsonify, url_for, abort, request
from app import db, guard
from app.models import User
from app.api import bp
from app.api.errors import bad_request
from app.schemas import UserSchema
from flask_praetorian import auth_required, roles_required, current_user

@bp.route('/login', methods=['POST'])
def login():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user), 'id': user.id}
    return jsonify(ret), 200

@bp.route('/users/<int:id>', methods=['GET'])
@auth_required
def get_user(id):
    if current_user().id != id:
        abort(403)
    one_user = User.query.get_or_404(id)
    user_schema = UserSchema()
    output = user_schema.dump(one_user).data
    return jsonify({'user' : output})

@bp.route('/users', methods=['GET'])
@roles_required('admin')
def get_users():
    all_users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(all_users).data
    return jsonify({'users': output})

@bp.route('/users', methods=['POST'])
def create_user():
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
    user_schema = UserSchema()
    output = user_schema.dump(user).data
    response = jsonify({'user': output})
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
@auth_required
def update_user(id):
    if current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    user_schema = UserSchema()
    output = user_schema.dump(user).data
    return jsonify({'user': output})
