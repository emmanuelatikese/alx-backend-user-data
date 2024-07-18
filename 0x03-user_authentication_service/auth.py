#!/usr/bin/env python3
'''File contains function for hashing pwd'''
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """function for hashing password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    '''generate uuid
    '''
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        '''validating password
        '''
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        ''' SESSION Id
        '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                sess = _generate_uuid()
                upd = self._db.update_user(user.id, session_id=sess)
                if not upd:
                    return sess
        except Exception:
            return

    def get_user_from_session_id(self, session_id: str) -> User:
        '''returns the user or None
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
            if not user or not session_id:
                return
            return user
        except Exception:
            return

    def destroy_session(self, user_id: int) -> None:
        '''destroy session
        '''
        try:
            self._db.update_user(user_id, session_id=None)
            return
        except Exception:
            return

    def get_reset_password_token(self, email: str) -> str:
        '''reset token
        '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token = _generate_uuid()
                upd = self._db.update_user(user.id, reset_token=token)
                if not upd:
                    return str(token)
        except ValueError:
            return
