from datetime import datetime
from numbers import Number

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric, String,
                        Table)
from sqlalchemy.orm import backref, relationship

from piper import utils
from piper.database import Model


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

        super(Transaction, self).__init__(**kwargs)

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
    amount = Column(Numeric(15, 2))
    transaction_id = Column(Integer, ForeignKey('transaction.id'),
                            nullable=False)
    categories = relationship('Category', secondary=split_category_table)


class Category(Model):
    """An item in the category tree."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    subcategories = relationship('Category')
