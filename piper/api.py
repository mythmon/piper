import json

from flask import Blueprint, jsonify, Response, request


blueprint = Blueprint('api', __name__, url_prefix='/api')


transactions = []


@blueprint.route('/transaction', methods=['GET'])
def transaction_list():
    return Response(json.dumps(transactions), mimetype='application/json')


@blueprint.route('/transaction/<int:id>', methods=['GET'])
def transaction_detail(id):
    return jsonify(transactions[id])


@blueprint.route('/transaction', methods=['POST'])
def transaction_create():
    data = request.get_json()
    trans = {
        'date': data['date'],
        'name': data['name'],
        'category': data['category'],
        'amount': data['amount'],
        'id': len(transactions),
    }
    print 'Adding', trans
    transactions.append(trans)
