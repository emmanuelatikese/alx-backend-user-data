#!/usr/bin/env python3
'''working on personal data'''
import re
from typing import Union, List


def filter_datum(fields: List[Union[str, str]], redaction: str,
                 message: str, separator: str) -> str:
    '''here it begins'''
    sp_mes = message.split(separator)
    for x in range(len(sp_mes)):
        for y in fields:
            if y in sp_mes[x]:
                sp_mes[x] = re.sub(r'=\S*', f"={redaction}", sp_mes[x])
    return separator.join(sp_mes)
