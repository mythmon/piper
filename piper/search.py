import json
import re

from flask import Blueprint, Response, request, current_app, make_response
from flask.views import MethodView
from flask.json import jsonify

from sqlalchemy.orm import class_mapper, subqueryload
from sqlalchemy.orm.exc import NoResultFound

from piper import utils
from piper.database import get_session, Model
from piper.models import Transaction, Split, Category

import q

blueprint = Blueprint('search', __name__, url_prefix='/search')


@blueprint.route('/', methods=['GET', 'POST'])
@utils.with_db
def search(db):
    query = request.get_json()

    category = Category.get(query['contains']['tag'])
    splits = db.query(Split).filter(Split.categories.contains(category)).all()
    transactions = set(s.transaction for s in splits)

    for t in transactions:
        t.splits = filter(lambda s: s in splits, t.splits)

    return utils.json_response(list(transactions))