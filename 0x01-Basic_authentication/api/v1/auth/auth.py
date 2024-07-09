#!/usr/bin/env python3
import flask
from typing import TypeVar, List


class Auth:
    """deals with everything auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False for now
        """
        return False

    def authorization_header(self, request = None) -> None:
        """ returns None
        """
        return None

    def current_user(self, request = None) -> None:
        """Returns None
        """
        return None
