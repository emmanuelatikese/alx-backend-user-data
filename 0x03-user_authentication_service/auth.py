#!/usr/bin/env python3
'''File contains function for hashing pwd'''
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """function for hashing password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """for registration of user
        """
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                raise ValueError("User <user's email> already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=hash_pwd)
            return new_user
