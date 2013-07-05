import json

from flask import Blueprint, jsonify, Response


blueprint = Blueprint('api', __name__, url_prefix='/api')


mock_transactions = [
    {
        'id': 0,
        'date': '1372896000000',
        'name': 'Fourth of July Snacks!',
        'category': 'Food',
        'amount': 12.34,
    }, {
        'id': 1,
        'date': '1372809600000',
        'name': 'Cute outfit',
        'category': 'Clothes',
        'amount': 20.01,
    }, {
        'id': 2,
        'date': '1372550400000',
        'name': 'Sandals',
        'category': 'Clothes',
        'amount': 48.25,
    }, {
        'id': 2,
        'date': '1372464000000',
        'name': 'Awesome app',
        'category': 'Software',
        'amount': 0.99,
    }
]


@blueprint.route('/transaction', methods=['GET'])
def transaction_list():
    return Response(json.dumps(mock_transactions), mimetype='application/json')


@blueprint.route('/transaction/<int:id>', methods=['GET'])
def transaction_detail(id):
    return jsonify(mock_transactions[id])
