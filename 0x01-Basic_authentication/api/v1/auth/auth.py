#!/usr/bin/env python3
"""
File contains auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    '''this is class deals with authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """returns None
        """
        return

    def current_user(self, request=None) -> TypeVar('User'):
        """returns Nones
        """
        return
