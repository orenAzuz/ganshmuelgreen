#!/usr/bin/python3

from flask import Flask, render_template, request, json
from flask_mail import Mail, Message
import requests
import subprocess
import datetime
#PORT = 8000

from flask_mail import Mail, Message
HOST = "0.0.0.0"
app = Flask(__name__)


app.config.update(dict(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=587,
	MAIL_USE_TLS=True,
	MAIL_USE_SSL=False,
    MAIL_USERNAME='green.develeap@gmail.com',
    MAIL_PASSWORD='1j4u_ore'
))

mail = Mail()
mail.init_app(app)

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
	print('request.get_data : ',request.get_json())
	print('request.query_string : ',request.query_string)
	subprocess.call(['./reload.sh'])
	mestxt = "New deploy from git. branch -> master. "
	send_mail(mestxt)
	return render_template('index.html',message=mestxt)


def send_mail(message):
	weight_status = http_request(8081)
	billing_status = http_request(8080)
	today = datetime.datetime.now()
	today_now = "{:%Y-%m-%d %H:%M:%S}".format(today)
	status = (weight_status, billing_status, today_now)
	body_txt = 'The status for weight is: %s .\n The status for billing is %s . \n%s' % status
	msg = Message(message, sender='webmykitchen@gmail.com', recipients=get_mail_list())
	msg.body = body_txt
	mail.send(msg)
	return 'done'


def get_mail_list():
	return ['orezaz@gmail.com',
		    'yaniv.d@develeap.com',
			'nirdod@gmail.com',
			'giuliovnturi@gmail.com',
			'ilana.fisher.il@gmail.com',
			'razleshem3@gmail.com',
			'br.cohen@hotmail.fr',
			'emanaz.91@gmail.com',
			'sharontabakman@gmail.com',
			'stacnospam@gmail.com']


def http_request(port):
	url = "http://green.develeap.com:%s/health" % port
	try:
		r = requests.get(url)
		return r.status_code
	except requests.exceptions.RequestException:
		return 111


if __name__ == "__main__":
#	app.run(port=PORT, host = HOST, debug=True)
	app.run(host=HOST,debug=True)