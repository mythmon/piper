import json
import re

from flask import Blueprint, Response, request, current_app, make_response
from flask.views import MethodView

from sqlalchemy.orm import class_mapper, subqueryload
from sqlalchemy.orm.exc import NoResultFound

from piper import utils
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

    @utils.with_db
    def get_one(self, id, db):
        try:
            inst = db.query(self.model).filter(self.model.id == id).one()
            return self._jsonify(inst)
        except NoResultFound:
            return make_response(('', 404, {}))

    @utils.with_db
    def get_list(self, db):
        inst_list = db.query(self.model).all()
        return self._jsonify(inst_list)

    @utils.with_db
    def post(self, db):
        data = request.get_json(force=True)
        inst = self.model(**data)
        db.add(inst)
        db.commit()

        return self._jsonify(inst, 201, {
            'Location': blueprint.url_prefix + self.url(inst.id)
        })

    @utils.with_db
    def delete(self, id, db):
        inst = db.query(self.model).filter(self.model.id == id).one()
        db.delete(inst)
        db.commit()

        return make_response(('', 204, {}))

    @utils.with_db
    def put(self, id, db):
        data = request.get_json()
        inst = db.query(self.model).filter(self.model.id == id).one()
        try:
            inst.update(**data)
        except TypeError as e:
            raise
            return make_response((str(e), 403, {}))
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


@register_model_view(blueprint)
class CategoryView(ModelView):
    model = Category


@register_model_view(blueprint)
class SplitView(ModelView):
    model = Split
