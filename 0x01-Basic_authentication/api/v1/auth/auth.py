#!/usr/bin/env python3
from flask import request
from typing import  List


class Auth:
    """deals with everything auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """returns None
        """
        return

    def current_user(self, request=None) -> str:
        """returns Nones
        """
        return
