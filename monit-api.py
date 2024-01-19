from flask import Flask, jsonify, abort, request
import json
from pymongo import MongoClient
from flasgger import Swagger

app = Flask(__name__)
client = MongoClient('localhost', 27017, username='monitoring', password='azerty')
swagger = Swagger(app)

db = client.flask_db
todos = db.todos


@app.route('/reports', methods=['GET'])
def get_all_reports():
    output = []
    for s in todos.find():
        output.append({'id': s['id'], 'date': s['date'], 'cpu': s['cpu'], 'ram': s['ram'], 'disk': s['disk'], 'port': s['port']})
    return jsonify({'result': output})


@app.route('/reports/<id>', methods=['GET'])
def get_one_report(id):
    s = todos.find_one({'id': id})
    if s:
        output = {'id': s['id'], 'date': s['date'], 'cpu': s['cpu'], 'ram': s['ram'], 'disk': s['disk'], 'port': s['port']}
        return jsonify({'result': output})
    else:
        abort(404)


@app.route('/reports', methods=['POST'])
def add_report():
    if not request.json or not 'date' in request.json:
        abort(400)
    check = {
        'id': request.json['id'],
        'date': request.json['date'],
        'cpu': request.json['cpu'],
        'ram': request.json['ram'],
        'disk': request.json['disk'],
        'port': request.json['port']
    }
    todos.insert_one(check)
    return jsonify({'result': check}), 201


@app.route('/reports/<id>', methods=['DELETE'])
def delete_report(id):
    result = todos.delete_one({'id': id})
    if result.deleted_count == 1:
        return jsonify({'result': True})
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80 , debug=True)