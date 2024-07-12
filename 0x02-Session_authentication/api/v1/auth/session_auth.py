#!/usr/bin/env python3
''' This file contains sessions class'''
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify
from os import getenv


class SessionAuth(Auth):
    '''this is class inherit from Auth'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''create a new session'''
        if user_id is None or not isinstance(user_id, str):
            return
        key = str(uuid4())
        self.user_id_by_session_id[key] = user_id
        return key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns the user'''
        if not session_id or not isinstance(session_id, str):
            return
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''creating overload of current_user'''
        if not request:
            return
        _cookie = self.session_cookie(request)
        _key = self.user_id_for_session_id(_cookie)
        return User.get(_key) if _key else None


@app_views.route("/auth_session/login",  methods=['GET'], strict_slashes=False)
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
