from datetime import datetime
from decimal import Decimal
from numbers import Number
from functools import wraps

from flask import current_app

import sqlalchemy

from piper.database import get_session


def coerce_datetime(input):
    if isinstance(input, datetime):
        return input

    if isinstance(input, basestring):
        try:
            input = float(input)
        except ValueError:
            # Not a float
            pass

    if isinstance(input, Number):
        # This is ~ 1971 in millisecond format, and ~ 2969 in seconds
        # format. It makes a lot more sense to considers numbers over this
        # to be in millisecond format.
        if input > 3.15e10:
            input /= 1000
        return datetime.fromtimestamp(input)

    raise NotImplementedError


class DecimalString(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.types.String

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return Decimal(value)


def with_db(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        db = get_session(current_app)
        return f(*args, db=db, **kwargs)
    return wrapper
