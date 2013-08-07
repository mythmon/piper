import sys

from flask import Flask

from live_stylus import ConvStylus
from werkzeug.utils import ImportStringError

from piper import api, angular
from piper.api import transactions, search, budgets


def create_app():
    app = Flask(__name__, static_folder='../app', static_url_path='/static')
    app.url_map.strict_slashes = False

    app.config.from_object('piper.settings.default')
    try:
        app.config.from_object('piper.settings.local')
    except ImportStringError:
        print ('You must create piper/settings/local.py. '
               'Use piper/settings/local.py-dist as an example.')
        sys.exit(1)

    ConvStylus('app/style')

    app.register_blueprint(api.blueprint)
    app.register_blueprint(search.blueprint)
    app.register_blueprint(angular.blueprint)

    return app


if __name__ == '__main__':
    create_app().run()
