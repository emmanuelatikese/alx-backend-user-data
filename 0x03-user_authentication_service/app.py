#!/usr/bin/env python3
'''settting up flask
'''
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from user import User


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    '''return json
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''registration purposes
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return
    try:
        new_user = AUTH.register_user(email, password)
        if new_user:
            return jsonify({"email": email,
                            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''all logins
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    lg_user = AUTH.valid_login(email, password)
    if lg_user:
        sess = AUTH.create_session(email)
        res = make_response(jsonify({"email": email,
                                     "message": "logged in"}))
        res.set_cookie('session_id', sess)
        return res
    return abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    '''does everything logout
    '''
    _cookie = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(_cookie)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    '''return str of profile
    '''
    _cookie = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(_cookie)
    if user and _cookie:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''reset password token
    '''
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email,
                        "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    '''update password
    '''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('new_password')
    if not email or not reset_token or not password:
        abort(403)
    try:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email,
                        "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
