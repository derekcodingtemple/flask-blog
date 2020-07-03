from flask import jsonify, g
from app import db
from . import api
from .auth import basic_auth, token_auth

@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@api.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.delete_token()
    db.session.commit()
    return '', 204