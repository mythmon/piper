import operator

from flask import Blueprint, request

from sqlalchemy.orm import joinedload

from piper import utils
from piper.api import blueprint
from piper.models.transactions import Transaction, Split, Category


@blueprint.route('/search', methods=['GET', 'POST'])
@utils.with_db
def search(db):
    query = request.get_json() or {}
    transactions = S(query)
    return utils.json_response(list(transactions))


@utils.with_db
def S(query, db):
    splits = (db.query(Split)
              .join(Split.categories)
              .options(joinedload(Split.transaction))
              .filter(S_actions(query)))
    transactions = set(s.transaction for s in splits)
    transactions = [t.for_json() for t in transactions]

    for t in transactions:
        t['splits'] = [s.for_json()
                       for s in filter(lambda s: s in splits, t['splits'])]
    db.rollback()

    return transactions


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
        all_cats.append(cat)
        stack.update(cat.subcategories)

    return Split.categories.any(Category.id.in_(c.id for c in all_cats))

def S_and(args):
    return reduce(operator.and_, (S_actions(a) for a in args))


def S_or(args):
    return reduce(operator.or_, (S_actions(a) for a in args))


def S_not(args):
    return ~S_actions(args)


S_parts = {
    'contains': S_contains,
    'and': S_and,
    'or': S_or,
    'not': S_not,
    'contains_tag': S_contains_tag,
}
