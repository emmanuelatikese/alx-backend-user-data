#!/usr/bin/env python3
"""all basic authorizations"""
from flask import request, jsonify
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def session_auth():
    '''handles authentications'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        new_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"})
    for user in new_users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            sess_name = getenv('SESSION_NAME')
            res = jsonify(user.to_json())
            res.set_cookie(sess_name, sess_id)
            return res
    return jsonify({"error": "wrong password"})
