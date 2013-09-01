import operator
import json

from flask import request

from sqlalchemy.orm import contains_eager

from piper import utils
from piper.api import blueprint
from piper.models.transactions import Transaction, Split, Category


@blueprint.route('/search', methods=['GET', 'POST'])
@utils.with_db
def search(db):
    query = request.get_json() or json.loads(request.data)
    transactions = S(query)
    return utils.json_response(list(transactions))


@utils.with_db
def S(query, db):
    q = (db.query(Transaction)
         .join(Split, Transaction.splits)
         .join(Category, Split.categories)
         .options(contains_eager(Transaction.splits))
         .filter(S_actions(query))
         )

    return [t.for_json() for t in q.all()]


attrs = {
    'date': (Transaction.purchase_date, utils.coerce_datetime),
    'created': (Transaction.created, utils.coerce_datetime),
}


def S_actions(query):
    filters = [S_parts[action](args) for action, args in query.items()]
    return reduce(operator.and_, filters)


def S_contains(args):
    filters = [S_parts['contains_' + k](v) for k, v in args.items()]
    return reduce(operator.and_, filters)


def S_contains_tag(val):
    all_cats = []
    stack = set([Category.get(val, False)])
    while stack:
        cat = stack.pop()
        if cat:
            all_cats.append(cat)
            stack.update(cat.subcategories)

    if not all_cats:
        return Split.categories.any(Category.id == -1)

    return Split.categories.any(Category.id.in_(c.id for c in all_cats))


def S_attr_op(op):
    def f(spec):
        filters = (op(attrs[key][0], attrs[key][1](val))
                   for key, val in spec.items())
        return reduce(operator.and_, filters)
    return f


def S_and(args):
    return reduce(operator.and_, (S_actions(a) for a in args))


def S_or(args):
    return reduce(operator.or_, (S_actions(a) for a in args))


def S_not(args):
    return ~S_actions(args)


S_parts = {
    'contains': S_contains,
    'contains_tag': S_contains_tag,

    'equals': S_attr_op(operator.eq),
    'not-equals': S_attr_op(operator.ne),
    'greater': S_attr_op(operator.gt),
    'greater-equal': S_attr_op(operator.ge),
    'less': S_attr_op(operator.lt),
    'less-equal': S_attr_op(operator.le),

    'and': S_and,
    'or': S_or,
    'not': S_not,
}
