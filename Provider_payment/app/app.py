#!/usr/bin/env python
import flask
import pymysql
import pymysql.cursors
from flask import Flask
import urllib
import json
from flask import send_file
import csv
import logging

app = Flask(__name__)

# Consts
HOST = 'mysql-db'
#HOST = '0.0.0.0'


@app.route('/health')
def health():
	logInfoMessage("Received health check request")

	if checkDBConnection() == 1:
		logInfoMessage("Health response OK")
		return "Payment team is OK"

	logInfoMessage("Returned 'No Database Connection'")

	return "No Database Connection", 410


@app.route('/provider/<name>', methods=['POST'])
def createProvider(name):
	logInfoMessage("Received request to create a provider: " + name)
	connection = getConnection()
	query = "INSERT INTO Provider (`name`) VALUES ('" + name + "');"
	try:
		with connection.cursor() as cursor:
			cursor.execute(query)
			providerID = cursor.lastrowid
		connection.commit()
	except Exception as e:
		logDebugMessage(str(e))
		logErrorMessage("Failed to create provider: " + name)
		return "Failed to create provider", 430
	else:
		logInfoMessage("Provider: " + name + " created")
		return json.dumps({str(providerID): name})
	finally:
		connection.close()


@app.route('/provider/<id>/<name>', methods=['PUT'])
def updateProvider(id, name):
	logInfoMessage("Received request to update provider: " + id + " with new name: " + name)

	query = "update Provider set name='" + name + "' where id=" + str(id) + ";"
	logDebugMessage("Run query: " + query)
	if runQuery(query) == 0:
		logErrorMessage("Failed to update provider")
		return "Failed to update provider name", 430
	else:
		logInfoMessage("Provider name updated")
		return "Update provider name by id:" + str(id) + ". New name is: " + name


@app.route('/rates', methods=['GET'])
def rates():
	logInfoMessage("Received request to download rates file")
	try:
		return send_file('/in/rates.csv', attachment_filename='rates.csv')
	except Exception as e:
		logErrorMessage(str(e))
		return "File Not Found", 415
	else:
		logInfoMessage("File returned")


@app.route('/rates', methods=['POST'])
def getRates():
	logInfoMessage("Received request to update rates")
	query = "DELETE FROM Rates;"
	if runQuery(query) == 0:
		logErrorMessage("Failed to delete old rates")
		return "Failed to update rates", 430
	else:
		logDebugMessage("Rates table is cleaned")

	if insertNewRates() == 0:
		return "Failed to update new rates", 430

	return 'Rates Are Up To Date'


@app.route('/truck/<id>/<provider_id>', methods=['POST'])
def createTruck(id, provider_id):
	logInfoMessage("Received request to create new truck: " + id + " for provider: " + provider_id)

	query = "INSERT INTO Trucks (`id`, `provider_id`) VALUES ('" + id + "', " + provider_id + ");"

	if runQuery(query) == 0:
		logErrorMessage("Failed to create new truck")
		return "Failed to create new truck", 430
	else:
		logInfoMessage("New truck created")

	return "New truck crated"


@app.route('/truck/<id>/<provider_id>', methods=['PUT'])
def updateTruck(id, provider_id):
	logInfoMessage("Received request to update truck: " + id + " for provider: " + provider_id)
	query = "UPDATE Trucks SET provider_id=" + provider_id + " WHERE id='" + id + "';"

	if runQuery(query) == 0:
		logErrorMessage("Failed to update truck")
		return "Failed to update truck", 430
	else:
		logInfoMessage("Truck info updated")

	return "Truck info updated"


@app.route('/truck/<id>', methods=['GET'])
def getTruck(id):
	logInfoMessage("Received request to get info by truck id: " + id)

	t1 = flask.request.args.get("from")
	t2 = flask.request.args.get("to")
	weightUrl = "http://green,develeap.com:8081/item/%s?from=%s&to=%s" % (str(id), str(t1), str(t2))
	response = urllib.request.urlopen(weightUrl)
	return response.read()


@app.route('/bill/<providerId>', methods=['GET'])
def bill(providerId):
	logInfoMessage("Received request to get bill info by provider id: " + providerId)

	# Initialization
	t1 = flask.request.args.get("from")
	t2 = flask.request.args.get("to")
	truckCount = 0
	sessionCount = 0
	totalPay = 0
	products = {}

	# Establish connection
	connection = getConnection()

	try:
		with connection.cursor() as cursor:
			# Get provider name
			query = "SELECT name FROM Provider WHERE id=%s;"
			cursor.execute(query, (str(providerId)), )
			result = cursor.fetchone()
			providerName = result['name']

			# Get provider trucks
			query = "SELECT id FROM Trucks WHERE provider_id=%s;"
			cursor.execute(query, (str(providerId)), )
			truckRows = cursor.fetchall()
			for truckRow in truckRows:
				truckCount += 1  # count trucks
				truck = truckRow['id']
				# truckStr = getTruck(truck) TODO from weight team
				truckStr = '{"id":1234, "tara":85000, "sessions":[10]}'  # Get truck data from API
				truckData = json.loads(truckStr)  # Convert to json object
				sessions = truckData['sessions']
				sessionCount += len(sessions)  # accumulate sessions
				for sessionId in sessions:
					# sessionUrl = "http://green.develeap.com:8081/session/%s" % str(id) TODO from weight team
					# sessionStr = urllib.request.urlopen(sessionUrl) TODO from weight team
					sessionStr = '{"id":10, "truck":"134-33-443", "bruto":70000, "truckTara":85000, "produce":"Blood", "neto":60000}'  # Get session data
					sessionData = json.loads(sessionStr)  # Convert to json object

					# Initialize produce in products table
					if products.get(sessionData['produce']) is None:
						products[sessionData['produce']] = {}

					products[sessionData['produce']]['produce'] = sessionData['produce']  # Set product name

					# Set accumulation of product sessions count
					if products[sessionData['produce']].get('count'):
						products[sessionData['produce']]['count'] += 1
					else:
						products[sessionData['produce']]['count'] = 1

					# Set accumulation of product neto tara amount
					if products[sessionData['produce']].get('amount'):
						products[sessionData['produce']]['amount'] += sessionData['neto']
					else:
						products[sessionData['produce']]['amount'] = sessionData['neto']

					# Get provider rate
					query = "select rate,scope from Rates where scope in ('All',%s) and product_id=%s;"
					cursor.execute(query, (str(providerId), sessionData['produce']), )
					rateRows = cursor.fetchall()
					rate, rateAll = 0, 0
					for rateRow in rateRows:
						if [[rateRow['scope'] == str(providerId)]]:
							rate = rateRow['rate']
							logDebugMessage(rate)
							break;
						else:
							rateAll = rateRow['rate']
					if not rate:
						rate = rateAll
					products[sessionData['produce']]['rate'] = rate

					# Calc pay from rate and amount and accumulate product pay
					if products[sessionData['produce']].get('pay'):
						products[sessionData['produce']]['pay'] += products[sessionData['produce']]['amount'] * \
																   products[sessionData['produce']]['rate']
					else:
						products[sessionData['produce']]['pay'] = products[sessionData['produce']]['amount'] * \
																  products[sessionData['produce']]['rate']

					totalPay += products[sessionData['produce']]['pay']  # Accumulate all pays for all products

		connection.commit()
	finally:
		connection.close()

	# Build final data object
	data = {
		"id": "%s" % providerId,
		"name": "%s" % providerName,
		"from": "%s" % t1,
		"to": "%s" % t2,
		"truckCount": "%d" % truckCount,
		"sessionCount": "%d" % sessionCount,
		"products": [],
		"total": "%s" % str(totalPay)
	}
	# Add data object products array accumulated before
	for produce, produceData in products.items():
		data['products'].append(produceData)
	return json.dumps(data)


# local functions

def checkDBConnection():
	logInfoMessage("Checking DB connection")

	try:
		# db = pymysql.connect(host="mysql-db", port=3306, user="root", passwd="greengo", db="billdb", auth_plugin_map="")
		db = getConnection()
		if db is not None:
			logInfoMessage("Connection established")
			db.close()
			return 1
	except Exception:
		logErrorMessage("Error in MySQL connection")
	
	return 0


def getConnection():
	logDebugMessage("Getting DB connection")
	
	try:
		return pymysql.connect(host=HOST, port=3306, user="root", passwd="greengo", db="billdb", charset='utf8mb4',
						   cursorclass=pymysql.cursors.DictCursor)
	except Exception as e:
		logDebugMessage(str(e))
		logErrorMessage("Error in getting MySQL connection")
		return None
	else:
		logDebugMessage("Got connection")    


def runQuery(query):
	# Connect to the database
	connection = getConnection()

	try:
		with connection.cursor() as cursor:
			cursor.execute(query)

		connection.commit()
	except Exception as e:
		logDebugMessage(str(e))
		logErrorMessage("Failed to run query")
		return 0
	else:
		return 1
	finally:
		connection.close()


def insertNewRates():
	filename = "/in/rates.csv"
	# filename = "rates.csv"

	query = "INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES "

	try:
		with open(filename) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0

			for row in csv_reader:
				if line_count == 0:
					logDebugMessage('Column names are ' + ", ".join(row))
				elif line_count == 1:
					query += '(\'' + row[0] + '\',' + row[1] + ',\'' + row[2] + '\')'
				else:
					query += ', (\'' + row[0] + '\',' + row[1] + ',\'' + row[2] + '\')'
				line_count += 1
			if line_count > 1:
				query += ';'
				runQuery(query)
			else:
				logInfoMessage("No rates found in file")

	except Exception as e:
		logDebugMessage(str(e))
		logErrorMessage("Failed to update new rates")
		return 0
	else:
		logInfoMessage('Processed ' + str(line_count - 1) + ' lines.')
		return 1


def createJsonResponse():
	return ""
	pass


def initLogger():
	handler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)


def getLogger():
	return logger


def logDebugMessage(msg):
	logger = getLogger()
	logger.debug(msg)


def logInfoMessage(msg):
	logger = getLogger()
	logger.info(msg)


def logErrorMessage(msg):
	logger = getLogger()
	logger.error(msg)

logger = logging.getLogger()
initLogger()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
