#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return "OK"

@app.route('/weight')
def weight():
    return "OK"

@app.route('/batch-weight')
def batch_weight():
    return "OK"

@app.route('/unknown')
def unknown():
    return "OK"

@app.route('/item/<id>')
def item():
    return "OK"

@app.route('/session/<id>')
def session():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
