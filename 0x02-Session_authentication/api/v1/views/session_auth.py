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
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        all_users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 401
    if not all_users:
        return jsonify({"error": "no user found for this email"}), 401
    for user in all_users:
        cur_user = user if user.is_valid_password(password) else None
    if not cur_user:
        return jsonify({"error": "wrong password"}), 401
    session_name = getenv('SESSION_NAME')
    res = jsonify(cur_user.to_json())
    res.set_cookie(session_name, cur_user.id)
    return res
