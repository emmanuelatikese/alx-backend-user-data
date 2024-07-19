#!/usr/bin/env python3
"""
Main file
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str):
    '''Check for registration purposes.'''
    payload = {'email': email, 'password': password}
    url = 'http://localhost:5000/users'
    res = requests.post(url, data=payload)
    assert res.json() == {"email": email,
                          "message": "user created"}, 'Error has occurred'


def log_in_wrong_password(email: str, password: str):
    '''Test logging in with wrong password.'''
    password = 'wrong' + password
    payload = {'email': email, 'password': password}
    url = 'http://localhost:5000/sessions'
    res = requests.post(url, data=payload)
    assert res.status_code == 401, 'Error has occurred'


def profile_unlogged():
    '''profile_unlogged
    '''
    url = 'http://localhost:5000/profile'
    res = requests.get(url)
    assert res.status_code == 403, 'Error has occurred'


def log_in(email: str, password: str):
    '''check if user is logged in
    '''
    url = 'http://localhost:5000/sessions'
    payload = {'email': email, 'password': password}
    res = requests.post(url, data=payload)
    assert res.status_code == 200, 'Error has occurred'
    return res.cookies.get('session_id')


def profile_logged(session_id: str):
    ''' login in session
    '''
    cookie = {"session_id": session_id}
    url = 'http://localhost:5000/profile'
    res = requests.get(url, cookies=cookie)
    assert res.status_code == 200, 'Error has occurred'
    assert res.json() == {"email": EMAIL}, 'Error has occurred'


def log_out(session_id: str):
    '''logout from session
    '''
    cookie = {"session_id": session_id}
    url = 'http://localhost:5000/sessions'
    res = requests.delete(url, cookies=cookie)
    assert res.status_code == 200, 'Error has occurred'
    assert res.json() == {"message": "Bienvenue"}, 'Error has occurred'


def reset_password_token(email: str):
    '''checking reset password token
    '''
    payload = {"email": email}
    url = 'http://localhost:5000/reset_password'
    res = requests.post(url, data=payload)
    assert res.status_code == 200, 'Error has occurred'
    res = res.json()
    return res.get('reset_token')


def update_password(email: str, reset_token: str, password: str):
    '''updating password
    '''
    url = 'http://localhost:5000/reset_password'
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": password}
    res = requests.put(url, data=data)
    assert res.status_code == 200, 'Error has occurred'
    assert res.json() == {"email": email,
                          "message": "Password updated"}, 'Error has occurred'


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
