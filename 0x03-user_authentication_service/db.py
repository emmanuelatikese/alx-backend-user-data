#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''finding user by email'''
        if not kwargs:
            raise InvalidRequestError
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise InvalidRequestError
        filtered_user = self._session.query(User).filter_by(**kwargs).first()
        if not filtered_user:
            raise NoResultFound
        return filtered_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """function to update user"""
        filter_user = self.find_user_by(id=user_id)
        for ky in kwargs.keys():
            if not hasattr(User, ky):
                raise ValueError
        for k, v in kwargs.items():
            setattr(filter_user, k, v)
        return
