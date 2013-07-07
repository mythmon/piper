import os

from flask import Blueprint, send_file


blueprint = Blueprint('angular', __name__, url_prefix='/')


@blueprint.route('', defaults={'path': ''})
@blueprint.route('<path:path>')
def index(path):
    return send_file('../app/index.html')
