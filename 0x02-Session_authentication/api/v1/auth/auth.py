#!/usr/bin/env python3
"""
File contains auth class
"""
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    '''this is class deals with authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False or True
        """
        if path is None or excluded_paths is None:
            return True
        path = path + '/' if path[len(path) - 1] != '/' else path
        for pt in excluded_paths:
            if fnmatch.fnmatch(path, pt):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns Nones
        """
        return None

    def session_cookie(self, request=None):
        '''dealing with session cookies'''
        if not request:
            return
        _my_session_id = getenv('SESSION_NAME')
        dict_cookie = dict(request.cookies)
        val = dict_cookie.get(_my_session_id)
        return val if val else None
