#!/usr/bin/env python3
'''working on personal data'''
import re
from typing import Union, List
import logging


def filter_datum(fields: List[Union[str, str]], redaction: str,
                 message: str, separator: str) -> str:
    '''here it begins'''
    sp_mes = message.split(separator)
    for x in range(len(sp_mes)):
        for y in fields:
            if y in sp_mes[x]:
                sp_mes[x] = re.sub(r'=\S*', f"={redaction}", sp_mes[x])
    return separator.join(sp_mes)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''Here goes nothing'''
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
