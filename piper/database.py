from datetime import datetime
from decimal import Decimal
from time import mktime

from flask import request, current_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.ext.declarative import declarative_base


class _BaseModel(object):

    def __init__(self, **kwargs):
        self.update(**kwargs)
        super(_BaseModel, self).__init__()

    def update(self, **kwargs):
        whitelist = self.column_whitelist()

        for key in kwargs.keys():
            if key not in whitelist:
                raise TypeError(
                    '{0} is an invalid keyword argument for {1}. '
                    'Valid choices are {2}'
                    .format(key, self.__class__.__name__, whitelist))

        for key, val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def column_whitelist(cls):
        return [c.key for c in class_mapper(cls).columns]

    def serialize(self, detail=False):
        return {c.key: getattr(self, c.key)
                for c in class_mapper(self.__class__).columns}

    def for_json(self, detail=False):
        data = self.serialize(detail=detail)

        try:
            for key, val in data.items():
                if isinstance(val, datetime):
                    data[key] = mktime(val.timetuple()) * 1000
                elif isinstance(val, InstrumentedList):
                    data[key] = list(val)
                elif isinstance(val, Decimal):
                    data[key] = float(val)
        except AttributeError:
            # This means that data isn't a dict, which is ok.
            pass

        return data


Model = declarative_base(name='Model', cls=_BaseModel)


def get_session():
    """Get a database session for the current request."""
    if not hasattr(current_app, 'Session'):
        engine = create_engine(current_app.config.get('DATABASE_URL'),
                               convert_unicode=True)
        current_app.Session = sessionmaker(bind=engine)

    if not hasattr(request, 'db_session'):
        request.db_session = current_app.Session()

    return request.db_session
