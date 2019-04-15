#!/usr/bin/env python
import flask
from flask import Flask

app = Flask(__name__)


@app.route('/health')
def health():
    return "Payment team is OK"


@app.route('/provider', methods=['POST'])
def createProvider():
    return "Create provider"


@app.route('/provider/<id>', methods=['PUT'])
def updateProvider(id):
    return "Update provider name by id:" + str(id)


@app.route('/rates', methods=['GET', 'POST'])
def rates():
    if flask.request.method == 'POST':
        return "Post rates"
    else:
        return "Get rates"


@app.route('/truck', methods=['POST'])
def createTruck():
    return "Create Truck"


@app.route('/truck/<id>', methods=['PUT'])
def updateTruck(id):
    return "Update Truck provider by license: " + str(id)


@app.route('/truck/<id>', methods=['GET'])
def getTruck(id):
    t1 = flask.request.args.get("from")
    t2 = flask.request.args.get("to")
    return "Get Truck by id: " + str(id) + "and in range: " + str(t1) + ":" + str(t2)


@app.route('/bill/<id>', methods=['GET'])
def bill(id):
    t1 = flask.request.args.get("from")
    t2 = flask.request.args.get("to")
    return "Get Bill by id: " + str(id) + "and in range: " + str(t1) + ":" + str(t2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
