import json
import re

from flask import Blueprint, Response, request, current_app, make_response
from flask.views import MethodView

from sqlalchemy.orm import class_mapper, subqueryload
from sqlalchemy.orm.exc import NoResultFound

from piper.database import get_session, Model
from piper.models import Transaction, Split, Category


blueprint = Blueprint('api', __name__, url_prefix='/api')


class ModelView(MethodView):

    model = None

    @classmethod
    def _json_dumps(cls, obj):
        if isinstance(obj, basestring):
            return obj

        def to_json_patch(obj):
            if hasattr(obj, 'for_json'):
                return obj.for_json()
            raise TypeError

        return json.dumps(obj, default=to_json_patch)

    @classmethod
    def _jsonify(cls, obj, status=200, headers={}):
        body = cls._json_dumps(obj)
        real_headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
        real_headers.update(headers)
        return make_response((body, status, real_headers))

    @classmethod
    def url(cls, id=None):
        name = cls.__name__.lower()
        name = re.sub(r'view$', '', name)
        url = '/' + name + '/'
        if id is not None:
            url += str(id)
        return url

    def get(self, id):
        if id is None:
            return self.get_list()
        else:
            return self.get_one(id)

    def get_one(self, id):
        db = get_session(current_app)
        try:
            inst = db.query(self.model).filter(self.model.id == id).one()
            return self._jsonify(inst)
        except NoResultFound:
            return make_response(('', 404, {}))

    def get_list(self):
        db = get_session(current_app)
        inst_list = db.query(self.model).all()
        return self._jsonify(inst_list)

    def post(self):
        db = get_session(current_app)

        data = request.get_json()
        inst = self.model(**data)
        db.add(inst)
        db.commit()

        return self._jsonify(inst, 201, {
            'Location': blueprint.url_prefix + self.url(inst.id)
        })


    def delete(self, id):
        db = get_session(current_app)

        inst = db.query(self.model).filter(self.model.id == id).one()
        db.delete(inst)
        db.commit()

        return make_response(('', 204, {}))

    def put(self, id):
        db = get_session(current_app)

        data = request.get_json()
        inst = db.query(self.model).filter(self.model.id == id).one()
        try:
            inst.update(data)
        except TypeError:
            return make_response(('', 403, {}))
        db.add(inst)
        db.commit()

        return self._jsonify(inst, 200, {
            'Location': blueprint.url_prefix + self.url(inst.id)
        })


def register_model_view(blueprint):
    """Register a ModelView onto `blueprint`."""

    def inner(cls):
        view_func = cls.as_view(cls.__name__)
        base_url = cls.url()

        blueprint.add_url_rule(cls.url(), view_func=view_func,
                               methods=['GET'], defaults={'id': None})
        blueprint.add_url_rule(cls.url(), view_func=view_func,
                               methods=['POST'])
        blueprint.add_url_rule(cls.url(id='<int:id>'), view_func=view_func,
                               methods=['GET', 'PUT', 'DELETE'])
        return cls

    return inner


@register_model_view(blueprint)
class TransactionView(ModelView):
    model = Transaction

    def get_list(self):
        db = get_session(current_app)
        inst_list = (db.query(self.model)
                     .options(subqueryload(Transaction.splits))
                     .all())
        #raise
        return self._jsonify(inst_list)


    def post(self):
        db = get_session(current_app)
        data = request.get_json()
        splits = data.pop('splits', [])
        trans = self.model(**data)

        for split_data in splits:
            split = Split(transaction=trans, **split_data)
            db.add(split)

        db.add(trans)
        db.commit()

        return self._jsonify(trans, 201, {
            'Location': blueprint.url_prefix + self.url(trans.id)
        })



@register_model_view(blueprint)
class CategoryView(ModelView):
    model = Category


@register_model_view(blueprint)
class SplitView(ModelView):
    model = Split
