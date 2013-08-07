import json
from datetime import datetime
from decimal import Decimal
from numbers import Number

from flask import current_app

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric, String,
                        Table)
from sqlalchemy.orm import joinedload

from piper import utils
from piper.api.search import S as Search
from piper.database import Model
from piper.models.transactions import Transaction, Split


class Budget(Model):
    """A saved search with a limit."""
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    search = Column(String(10240))
    limit = Column(utils.DecimalString(Numeric(15, 2)))

    def serialize(self, detail=False):
        data = super(Budget, self).serialize()

        data['remaining'] = self.remaining
        if detail:
            data['transactions'] = self.transactions

        return data

    @property
    def search_parsed(self):
        if not hasattr(self, '_search_parsed'):
            self._search_parsed = json.loads(self.search)
        return self._search_parsed

    @property
    def transactions(self):
        if not hasattr(self, '_transactions'):
            self._transactions = Search(self.search_parsed)
        return self._transactions
    
    @property
    def remaining(self):
        if not hasattr(self, '_remaining'):
            total = Decimal(0)
            for t in self.transactions:
                total += sum(Decimal(s['amount']) for s in t['splits'])
            self._remaining = self.limit - total
        return self._remaining
    