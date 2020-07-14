from . import api
from flask import jsonify, request
from app.models import User, Post
from app import db
from .auth import token_auth

@api.route('/users', methods=['GET'])
def users():
    """
    [GET] /api/users
    """
    users = User.query.all()
    return jsonify(users=[user.to_dict() for user in users]), 200

@api.route('/user/<int:id>', methods=['GET'])
@token_auth.login_required
def user(id):
    """
    [GET] /api/user/<id>
    """
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200

@api.route('/user', methods=['POST'])
def create_user():
    """
    [POST] /api/user
    """
    response = request.get_json()
    u = User(
        name=response['name'],
        email=response['email'],
        password=response['password']
    )
    u.create_user()
    return jsonify([user.to_dict() for user in User.query.all()]), 201

@api.route('/user/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    """
    [PUT] /api/user/<id>
    """
    response = request.get_json()
    u = User.query.get(id)
    u.name = response['name']
    u.email = response['email']
    u.password = response['password']
    u.generate_password(u.password)
    db.session.commit()
    return jsonify(u.to_dict())

@api.route('/user/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    """
    [DELETE] /api/user/<id>
    """
    u = User.query.get(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify([u.to_dict() for u in User.query.all()])


@api.route('/blog/posts', methods=['GET'])
def get_posts():
    """
    [GET] /api/blog/posts
    """
    return jsonify([p.to_dict() for p in Post.query.all()])