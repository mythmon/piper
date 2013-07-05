from flask import Flask

from live_stylus import ConvStylus

from piper import api, angular


def create_app():
    app = Flask(__name__, static_folder='../app', static_url_path='/static')

    ConvStylus('app/style')

    app.register_blueprint(api.blueprint)
    app.register_blueprint(angular.blueprint)

    return app


def main():
    create_app().run(debug=True)


if __name__ == '__main__':
    main()
