import os

from flask import Blueprint, send_file, make_response


blueprint = Blueprint('angular', __name__, url_prefix='/')


@blueprint.route('', defaults={'path': ''})
@blueprint.route('<path:path>')
def index(path):
    if path.startswith('api/') or path.startswith('static/'):
        return make_response('', 404)
    return send_file('../app/index.html')
