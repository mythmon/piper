import operator

from flask import Blueprint, request

from piper import utils
from piper.models import Split, Category

blueprint = Blueprint('search', __name__, url_prefix='/search')


@blueprint.route('/ping', methods=['GET', 'SEARCH'])
def ping():
    return 'pong'


@blueprint.route('/', methods=['GET', 'POST'])
@utils.with_db
def search(db):
    query = request.get_json() or {}

    splits = S(query).all()
    transactions = set(s.transaction for s in splits)

    for t in transactions:
        t.splits = filter(lambda s: s in splits, t.splits)

    res = utils.json_response(list(transactions))
    db.rollback()
    return res


@utils.with_db
def S(query, db):
    return db.query(Split).join(Split.categories).filter(S_actions(query))


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

    import q
    q(list(c.name for c in all_cats))

    return Category.id.in_(c.id for c in all_cats)


def S_and(args):
    return reduce(operator.and_, (S_actions(a) for a in args))


def S_or(args):
    return reduce(operator.or_, (S_actions(a) for a in args))


S_parts = {
    'contains': S_contains,
    'and': S_and,
    'or': S_or,
    'contains_tag': S_contains_tag,
}
