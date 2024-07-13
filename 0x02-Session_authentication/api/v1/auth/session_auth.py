#!/usr/bin/env python3
''' This file contains sessions class'''
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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

    def destroy_session(self, request=None):
        '''destroy the session'''
        if not request:
            return
        val_cookie = self.session_cookie(request)
        if not val_cookie:
            return False
        cur_id = self.user_id_for_session_id(val_cookie)
        if not cur_id:
            return False
        if not User.get(cur_id):
            return False
        try:
            del self.user_id_by_session_id[val_cookie]
        except Exception as e:
            return
        return True
