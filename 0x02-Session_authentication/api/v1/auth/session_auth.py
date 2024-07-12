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
        self.user_id_by_session_id[user_id] = str(uuid4())
        return self.user_id_by_session_id[user_id]
