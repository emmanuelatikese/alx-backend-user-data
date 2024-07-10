#!/usr/bin/env python3
''' This file contains function Basic Auth'''
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    '''this is function inherit from Auth'''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''extracting authorization header'''
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if "Basic " not in authorization_header:
            return
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''decoding authorization header'''
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        try:
            decoded_header = base64.b64decode(base64_authorization_header)
            return decoded_header.decode('utf-8')
        except Exception:
            return

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        '''extracting user credentials'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        _split = decoded_base64_authorization_header.split(':')
        return _split[0], _split[1]

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        '''extracting user object from credentials'''
        if not user_email or not isinstance(user_email, str):
            return
        if not user_pwd or not isinstance(user_pwd, str):
            return
        try:
            new_users = User.search({'email': user_email})
        except Exception:
            return

        for user in new_users:
            if user.is_valid_password(user_pwd):
                return user
        return None
