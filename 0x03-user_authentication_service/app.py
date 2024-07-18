#!/usr/bin/env python3
'''settting up flask
'''
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
