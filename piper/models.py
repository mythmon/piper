from datetime import datetime
from numbers import Number

from flask import current_app

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric, String,
                        Table)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.exc import NoResultFound

from piper import utils
from piper.database import get_session, Model


class Transaction(Model):
    """A single purchase with cash, credit, or debit."""
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    merchant = Column(String(128))
    purchase_date = Column(DateTime, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    splits = relationship('Split', backref='transaction')

    def __init__(self, **kwargs):
        for field in ['purchase_date', 'created']:
            if field in kwargs:
                kwargs[field] = utils.coerce_datetime(kwargs[field])

        real_splits = []
        for s in kwargs.pop('splits', []):
            if isinstance(s, Split):
                real_splits.append(s)
            else:
                real_splits.append(Split(**s))

        super(Transaction, self).__init__(splits=real_splits, **kwargs)

    def serialize(self):
        data = super(Transaction, self).serialize()
        data['splits'] = self.splits
        return data

split_category_table = Table(
    'association',
    Model.metadata,
    Column('split_id', Integer, ForeignKey('split.id'), nullable=False),
    Column('category_id', Integer, ForeignKey('category.id'), nullable=False),
)


class Split(Model):
    """An amount and a category within a split."""
    __tablename__ = 'split'

    id = Column(Integer, primary_key=True)
    note = Column(String(512))
    amount = Column(utils.DecimalString(Numeric(15, 2)))
    transaction_id = Column(Integer, ForeignKey('transaction.id'),
                            nullable=False)
    categories = relationship('Category', secondary=split_category_table)

    def __init__(self, **kwargs):
        real_categories = []

        for c in kwargs.pop('categories', []):
            real_categories.append(Category.get(c, create=True))

        super(Split, self).__init__(categories=real_categories, **kwargs)

    def serialize(self):
        data = super(Split, self).serialize()
        data['categories'] = self.categories
        return data


class Category(Model):
    """An item in the category tree."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    subcategories = relationship('Category', remote_side='parent')
    subcategories = relationship('Category', backref=backref("parent", remote_side=id)) 

    @utils.with_db
    def serialize(self, db):
        data = super(Category, self).serialize()

        full_name = []
        point = self
        while point:
            full_name.insert(0, point.name)
            if point.parent_id:
                point = point.parent
            else:
                point = None

        data['name'] = '/'.join(full_name)

        return data

    @classmethod
    @utils.with_db
    def get(cls, spec, create=False, db=None):
        """Get a category that matches `spec`.

        `spec` is something like 'foo/bar/baz', or ['foo', 'bar', 'baz'].
        These are both equivalent, and mean to get the category 'baz' who's
        parent is the category 'bar' who's parent is the category 'foo'.

        `create` is whether or not to create new categories, if no existing categoires match.
        If `create` is False and no matching category is found, then a
        `sqlalchemy.orm.exc.NoResultFound` error will be raised.
        """

        if isinstance(spec, cls):
            return spec
        if isinstance(spec, basestring):
            spec = filter(None, spec.split('/'))
        if not spec:
            return None

        parent = cls.get(spec[:-1], create)
        try:
            cat = db.query(cls).filter(cls.name == spec[-1]).one()
        except NoResultFound:
            if create:
                cat = Category(name=spec[-1])
                if parent:
                    parent.subcategories.append(cat)
                db.add(cat)
            else:
                raise

        return cat
