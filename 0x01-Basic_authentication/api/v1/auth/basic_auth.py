#!/usr/bin/env python3
''' This file contains function Basic Auth'''
from api.v1.auth.auth import Auth


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
