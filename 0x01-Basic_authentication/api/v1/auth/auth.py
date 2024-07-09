#!/usr/bin/env python3
"""
File contains auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    '''this is class deals with authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False or True
        """
        if path is None or excluded_paths is None:
            return True
        path = path + '/' if path[len(path) - 1] != '/' else path
        if path in excluded_paths:
            return False
        else:
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
