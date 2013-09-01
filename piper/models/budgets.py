import json
from decimal import Decimal
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, String

from piper import utils
from piper.api.search import S as Search
from piper.database import Model


class Budget(Model):
    """A saved search with a limit."""
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    search = Column(String(10240), nullable=False)
    limit = Column(utils.DecimalString(Numeric(15, 2)), nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)

    def serialize(self, detail=False):
        data = super(Budget, self).serialize()

        data['remaining'] = '%.2f' % self.remaining
        if detail:
            data['transactions'] = self.transactions

        return data

    def update(self, **kwargs):
        for key in ['transactions', 'remaining']:
            kwargs.pop(key, None)

        for field in ['start', 'end']:
            if field in kwargs:
                kwargs[field] = utils.coerce_datetime(kwargs[field])

        super(Budget, self).update(**kwargs)

    @property
    def search_parsed(self):
        if not hasattr(self, '_search_parsed'):
            parsed = json.loads(self.search)
            self._search_parsed = {"and": [parsed]}

            if self.start:
                self._search_parsed['and'].append({
                    'greater-equal': {'date': self.start},
                })
            if self.end:
                self._search_parsed['and'].append({
                    'less': {'date': self.end},
                })

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
            # Expenses are negative.
            for t in self.transactions:
                total += sum(Decimal(s.amount) for s in t['splits'])
            self._remaining = self.limit + total
        return self._remaining
