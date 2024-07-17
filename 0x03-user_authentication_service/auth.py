#!/usr/bin/env python3
'''File contains function for hashing pwd'''
from db import DB
import bcrypt
from user import User


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
        fd_user = self._db._session.query(User).filter_by(email=email).first()
        if fd_user:
            raise ValueError("User <user's email> already exists")
        hash_pwd = _hash_password(password)
        new_user = self._db.add_user(email=email, hashed_password=hash_pwd)
        return new_user
