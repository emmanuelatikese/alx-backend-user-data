#!/usr/bin/env python3
"""all basic authorizations"""
from flask import request, jsonify, abort
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def session_auth():
    '''handles authorization'''
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        all_users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not all_users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in all_users:
        cur_user = user if user.is_valid_password(password) else None
    if not cur_user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(cur_user.id)
    session_name = getenv('SESSION_NAME')
    res = jsonify(cur_user.to_json())
    res.set_cookie(session_name, session_id)
    return res


@app_views.route("/api/v1/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout_session():
    '''basic login method'''
    from api.v1.app import auth
    _des = auth.destroy_session(request)
    if not _des:
        abort(404)
    return jsonify({}), 200
