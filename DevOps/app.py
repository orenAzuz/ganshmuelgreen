#!/usr/bin/python3

from flask import Flask
from flask import render_template

PORT = 8000
HOST = "0.0.0.0"
app = Flask(__name__)

@app.route("/")
def root():
	mestxt = "ROOT OK"
	return render_template('index.html',message=mestxt)


@app.route("/health")
def health():
	mestxt = "OK"
	return render_template('index.html',message=mestxt)

if __name__ == "__main__":
	app.run(port=PORT, host = HOST, debug=True)