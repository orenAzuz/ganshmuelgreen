#!/usr/bin/python3

from flask import Flask, render_template, request, json
import subprocess

#PORT = 8000
HOST = "0.0.0.0"
app = Flask(__name__)

@app.route('/')
def api_root():
	mestxt = "ROOT OK"
	return render_template('index.html',message=mestxt)


@app.route("/health")
def api_health():
	mestxt = "HEALTH OK"
	return render_template('index.html',message=mestxt)

@app.route("/reload",methods=['POST'])
def api_reload():
	subprocess.call(['./reload.sh'])
	mestxt = "RELOAD OK"
	return render_template('index.html',message=mestxt)

if __name__ == "__main__":
#	app.run(port=PORT, host = HOST, debug=True)
	app.run(host=HOST,debug=True)