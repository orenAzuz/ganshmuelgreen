#!/usr/bin/env python
import flask
import pymysql
import pymysql.cursors
from flask import Flask
import urllib
import json

app = Flask(__name__)

# CONSTS
HOST = "0.0.0.0"


@app.route('/health')
def health():
    if checkDBConnection() == 1:
        return "Payment team is OK"
    return "410 No Database Connection"


@app.route('/provider/<name>', methods=['POST'])
def createProvider(name):
    connection = getConnection()
    query = "INSERT INTO Provider (`name`) VALUES ('" + name + "');"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            providerID = cursor.lastrowid
        connection.commit()
    finally:
        connection.close()
    return json.dumps({str(providerID): name})


@app.route('/provider/<id>/<name>', methods=['PUT'])
def updateProvider(id, name):
    query = "update Provider set name='" + name + "' where id=" + str(id) + ";"
    print(query)
    runQuery(query)
    return "Update provider name by id:" + str(id) + ". New name is: " + name


@app.route('/rates', methods=['GET', 'POST'])
def rates():
    if flask.request.method == 'POST':
        return "Post rates"
    else:
        return getRateFile()


@app.route('/truck/<id>/<provider_id>', methods=['POST'])
def createTruck(id, provider_id):
    query = "INSERT INTO Trucks (`id`, `provider_id`) VALUES ('" + id + "', " + provider_id + ");"
    runQuery(query)
    return "Create Truck: " + id + " for provider: " + provider_id


@app.route('/truck/<id>/<provider_id>', methods=['PUT'])
def updateTruck(id, provider_id):
    query = "UPDATE Trucks SET provider_id=" + provider_id + " WHERE id='" + id + "';"
    runQuery(query)
    return "Update Truck provider by license: " + str(id) + " new provider id is: " + provider_id


@app.route('/truck/<id>', methods=['GET'])
def getTruck(id):
    t1 = flask.request.args.get("from")
    t2 = flask.request.args.get("to")
    weightUrl = "http://green,develeap.com:8081/item/%s?from=%s&to=%s" % (str(id), str(t1), str(t2))
    response = urllib.request.urlopen(weightUrl)
    return response.read()


@app.route('/bill/<providerId>', methods=['GET'])
def bill(providerId):
    # Initialization
    t1 = flask.request.args.get("from")
    t2 = flask.request.args.get("to")
    truckCount = 0
    sessionCount = 0
    totalPay = 0
    products = {}

    # Establish connection
    connection = getConnection()

    # Get trucks by provider id
    query = "SELECT id FROM Trucks WHERE provider_id=%s;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (str(providerId)), )
            result = cursor.fetchall()
            for row in result:
                truckCount += 1  # count trucks
                truck = row['id']
                # truckData = getTruck(truck) TODO from weight team
                truckStr = '{"id":1234, "tara":85000, "sessions":[10]}'  # Get truck data from API
                truckData = json.loads(truckStr)  # Convert to json object
                sessions = truckData['sessions']
                sessionCount += len(sessions)  # accumulate sessions
                for sessionId in sessions:
                    # sessionUrl = "http://green.develeap.com:8081/session/%s" % str(id) TODO from weight team
                    # sessionStr = urllib.request.urlopen(sessionUrl) TODO from weight team
                    sessionStr = '{"id":10, "truck":1, "bruto":70000, "truckTara":85000, "produce":"tomato", "neto":60000}'  # Get session data
                    sessionData = json.loads(sessionStr)  # Convert to json object

                    products[sessionData['produce']]['produce'] = sessionData['produce']  # Set product name

                    # Set accumulation of product sessions count
                    if products[sessionData['produce']]['count']:
                        products[sessionData['produce']]['count'] += 1
                    else:
                        products[sessionData['produce']]['count'] = 1

                    # Set accumulation of product neto tara amount
                    if products[sessionData['produce']]['amount']:
                        products[sessionData['produce']]['amount'] += sessionData['neto']
                    else:
                        products[sessionData['produce']]['amount'] = sessionData['neto']

                    # products[sessionData['produce']]['rate'] TODO bring from table of rates by provider id and produce

                    # Calc pay from rate and amount and accumulate product pay
                    if products[sessionData['produce']]['pay']:
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
        "name": "",  # TODO take from table of providers by provider id
        "from": "%s" % t1,
        "to": "%s" % t2,
        "truckCount": "%d" % truckCount,
        "sessionCount": "%d" % sessionCount,
        "products": [],
        "total": "%s" % str(totalPay)
    }
    # Add data object products array accumulated before
    for product in products:
        data['products'].append(product)
    return json.dumps(data)
    return "OK"


# local functions

def checkDBConnection():
    try:
        db = pymysql.connect(host="0.0.0.0", port=3306, user="root", passwd="greengo", db="billdb", auth_plugin_map="")
    except Exception:
        print("Error in MySQL connection")
        return 0
    else:
        print("Connection Good!")
        db.close()
    return 1


def getConnection():
    return pymysql.connect(host="0.0.0.0", port=3306, user="root", passwd="greengo", db="billdb", charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def runQuery(query):
    # Connect to the database
    connection = getConnection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

        connection.commit()
    finally:
        connection.close()


def getRateFile():
    pass


def createJsonResponse():
    return ""
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
