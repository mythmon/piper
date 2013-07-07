import json
from datetime import datetime
from time import mktime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.ext.declarative import declarative_base


class _BaseModel(object):

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in class_mapper(self.__class__).columns}

    def for_json(self):
        data = self.serialize()

        for key, val in data.items():
            if isinstance(val, datetime):
                # JSON uses milliseconds since the epoch for datetimes.
                data[key] = mktime(val.timetuple()) * 1000

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
