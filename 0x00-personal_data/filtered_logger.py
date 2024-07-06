#!/usr/bin/env python3
'''working on personal data'''
import re
from typing import Union, List
import logging
import mysql.connector
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[Union[str, str]], redaction: str,
                 message: str, separator: str) -> str:
    '''here it begins'''
    sp_mes = message.split(separator)
    for x in range(len(sp_mes)):
        for y in fields:
            if y in sp_mes[x]:
                sp_mes[x] = re.sub(r'=\S*', f"={redaction}", sp_mes[x])
    return separator.join(sp_mes)


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''getting db using sql lib'''
    _host = os.getenv('PERSONAL_DATA_DB_HOST'),
    _user = os.getenv('PERSONAL_DATA_DB_USERNAME'),
    _password = os.getenv('PERSONAL_DATA_DB_PASSWORD'),
    _database = os.getenv('my_db')
    cred = mysql.connector.connection.MySQLConnection(
        host=_host,
        user=_user,
        password=_password,
        database=_database,
    )
    return cred


def get_logger() -> logging.Logger:
    '''getting logger'''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[Union[str, str]]):
        '''this is the init function'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''here"s where the format begins'''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
