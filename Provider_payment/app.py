#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)


@app.route('/health')
def health():
    return "OK"


@app.route('/provider', methods=['POST'])
def createProvider():
    return "OK"


@app.route('/provider/<id>', methods=['PUT'])
def updateProvider(id):
    return "OK"


@app.route('/rates', methods=['GET', 'POST'])
def rates():
    return "OK"


@app.route('/truck', methods=['POST'])
def createTruck():
    return "OK"


@app.route('/truck/<id>', methods=['PUT'])
def updateTruck(id):
    return "OK"


@app.route('/truck/<id>?from=<t1>&to=<t2>')
def getTruck(id, t1, t2):
    return "OK"


@app.route('/item/<id>')
def item():
    return "OK"


@app.route('/session/<id>')
def session():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
