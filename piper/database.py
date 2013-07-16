import json
from datetime import datetime
from decimal import Decimal
from time import mktime

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

        if any(lambda k: k not in whitelist, kwargs.keys()):
            raise TypeError('{0} is an invalid keyword argument for {1}'
                            .format(key, self.__class__.__name__))

        for key ,val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def column_whitelist(cls):
        return [c.key for c in class_mapper(cls).columns]

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in class_mapper(self.__class__).columns}

    def for_json(self):
        data = self.serialize()

        for key, val in data.items():
            if isinstance(val, datetime):
                data[key] = mktime(val.timetuple()) * 1000
            elif isinstance(val, InstrumentedList):
                data[key] = list(val)
            elif isinstance(val, Decimal):
                data[key] = float(val)

        return data


Model = declarative_base(name='Model', cls=_BaseModel)


def get_session(app):
    """Get a database session for `app`."""
    if not hasattr(app, 'db_session'):
        engine = create_engine(app.config.get('DATABASE_URL'),
                               convert_unicode=True)
        Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        app.db_session = Session()

    return app.db_session
