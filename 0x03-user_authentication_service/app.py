#!/usr/bin/env python3
'''settting up flask
'''
from flask import Flask, jsonify, request
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
            return jsonify({"email": "<registered email>",
                            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
