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
    splits = relationship('Split', backref='transaction', cascade='all,delete')

    def __init__(self, **kwargs):
        for field in ['purchase_date', 'created']:
            if field in kwargs:
                kwargs[field] = utils.coerce_datetime(kwargs[field])

        real_splits = []
        for s in kwargs.pop('splits', []):
            if isinstance(s, Split):
                real_splits.append(s)
            else:
                real_splits.append(Split(transaction=self, **s))

        super(Transaction, self).__init__(splits=real_splits, **kwargs)

    def serialize(self, detail=False):
        data = super(Transaction, self).serialize()
        data['splits'] = self.splits
        return data

    @utils.with_db
    def update(self, db, **kwargs):
        splits_raw = kwargs.pop('splits', [])
        kwargs['splits'] = []

        for split_raw in splits_raw:
            if split_raw.get('id') is None:
                s = Split(transaction=self, **split_raw)
                kwargs['splits'].append(s)
                db.add(s);
            else:
                s = db.query(Split).filter(Split.id == split_raw['id']).one()
                s.update(**split_raw)
                kwargs['splits'].append(s)
                db.add(s)

        for field in ['purchase_date', 'created']:
            if field in kwargs:
                kwargs[field] = utils.coerce_datetime(kwargs[field])

        super(Transaction, self).update(**kwargs)

    @classmethod
    def column_whitelist(cls):
        whitelist = super(Transaction, cls).column_whitelist()
        return whitelist + ['splits']

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
    categories = relationship('Category', secondary=split_category_table,
                              lazy='join')

    def __init__(self, **kwargs):
        kwargs['categories'] = [Category.get(c)
                                for c in kwargs.get('categories', [])]
        super(Split, self).__init__(**kwargs)

    def serialize(self, detail=False):
        data = super(Split, self).serialize()
        data['categories'] = self.categories
        return data

    @classmethod
    def column_whitelist(cls):
        whitelist = super(Split, cls).column_whitelist()
        return whitelist + ['categories']

    def update(self, **kwargs):
        if 'categories' in kwargs:
            kwargs['categories'] = [Category.get(name)
                                    for name in kwargs['categories']]
        super(Split, self).update(**kwargs)



class Category(Model):
    """An item in the category tree."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    subcategories = relationship('Category', remote_side='parent')
    subcategories = relationship('Category', backref=backref("parent", remote_side=id)) 

    @utils.with_db
    def serialize(self, db, detail=False):
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
    def _coerce(cls, spec):
        if isinstance(spec, basestring):
            return spec.split('/')
        if isinstance(spec, dict) and 'name' in spec:
            return cls._coerce(spec['name'])
        return spec

    @classmethod
    @utils.with_db
    def get(cls, spec, create=True, db=None):
        """Get a category that matches `spec`.

        `spec` is something like 'foo/bar/baz', or ['foo', 'bar', 'baz'].
        These are both equivalent, and mean to get the category 'baz' who's
        parent is the category 'bar' who's parent is the category 'foo'.

        `create` is whether or not to create new categories, if no existing categoires match.
        If `create` is False and no matching category is found, then a
        `sqlalchemy.orm.exc.NoResultFound` error will be raised.
        """

        spec = cls._coerce(spec)
        if not isinstance(spec, list):
            raise TypeError("%s isn't right, it is a %s" % (spec, type(spec)))

        try:
            cat = (db.query(Category)
                     .filter(Category.name == spec[0], Category.parent == None))
            for n in spec[1:]:
                cat = (db.query(Category).filter(Category.name == n,
                                                 Category.parent == cat.one()))
            cat = cat.one()
        except NoResultFound:
            if create:
                parent = None
                for n in spec:
                    cat = (db.query(Category)
                             .filter(Category.name == n,
                                     Category.parent == parent)
                             .all())
                    if len(cat) == 0:
                        cat = Category(name=n, parent=parent)
                        db.add(cat)
                    else:
                        cat = cat[0]
                    parent = cat
            else:
                return None

        db.commit()

        return cat
