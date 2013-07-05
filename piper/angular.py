import os

from flask import Blueprint, make_response


blueprint = Blueprint('angular', __name__, url_prefix='/')


@blueprint.route('')
@blueprint.route('<path:path>')
def index(path=''):
    print os.curdir
    with open('app/index.html') as f:
        return make_response(f.read())
