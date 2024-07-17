#!/usr/bin/env python3
'''File contains function for hashing pwd'''
import bcrypt


def _hash_password(password: str) -> bcrypt.hashpw:
    """function for hashing password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
