#!/usr/bin/env python3
''' This file contains sessions class'''
from api.v1.auth.auth import Auth
from uuid import uuid4


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
