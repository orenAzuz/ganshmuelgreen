#!/usr/bin/env python
import flask
import pymysql
import pymysql.cursors
from flask import Flask
import urllib
import http.client
import json
from flask import send_file
import csv

app = Flask(__name__)

# Consts
HOST = 'mysql-db'
#HOST = '0.0.0.0'


@app.route('/health')
def health():
    if checkDBConnection() == 1:
        return "Payment team is OK"
    return "No Database Connection", 410


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


@app.route('/rates', methods=['GET'])
def rates():
    return getRateFile()


@app.route('/rates', methods=['POST'])
def getRates():
    query = "DELETE FROM Rates;"
    runQuery(query)
    insertNewRates()
    return 'Rates Are Up To Date'


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
    try:
        weightUrl = "http://18.222.236.224/item/%s?from=%s&to=%s" % (str(id), str(t1), str(t2))
        response = urllib.request.urlopen(weightUrl)
        return response.read()
    except (urllib.HTTPError, urllib.URLError, http.client.HTTPException, Exception):
        return '{"id":1234, "tara":85000, "sessions":[10]}'


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
                truckStr = '{"id":10000, "tara":1200, "sessions":[11]}'  # Get truck data from API
                truckData = json.loads(truckStr)  # Convert to json object
                sessions = truckData['sessions']
                sessionCount += len(sessions)  # accumulate sessions
                for sessionId in sessions:
                    # sessionUrl = "http://18.222.236.224:8081/session/%s" % str(id) TODO change to production
                    sessionUrl = "http://0.0.0.0:8081/session/%s" % str(id)
                    sessionStr = urllib.request.urlopen(sessionUrl)
                    #sessionStr = '{"id":10, "truck":"134-33-443", "bruto":70000, "truckTara":85000, "produce":"Blood", "neto":60000}'  # Get session data
                    sessionData = json.loads(sessionStr)  # Convert to json object

                    # Initialize produce in products table
                    if products.get(sessionData['produce']) is None:
                        products[sessionData['produce']] = {}

                    # Set product name
                    products[sessionData['produce']]['produce'] = sessionData['produce']

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
                            print(rate)
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
    try:
        # db = pymysql.connect(host="mysql-db", port=3306, user="root", passwd="greengo", db="billdb", auth_plugin_map="")
        db = getConnection()
    except Exception:
        print("Error in MySQL connection")
        return 0
    else:
        print("Connection Good!")
        db.close()
    return 1


def getConnection():
    return pymysql.connect(host=HOST, port=3306, user="root", passwd="greengo", db="billdb", charset='utf8mb4',
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
    try:
        return send_file('/in/rates.csv', attachment_filename='rates.csv')
    except Exception as e:
        print(str(e))
        return "File Not Found", 415


def insertNewRates():
    filename = "/in/rates.csv"
    # filename = "rates.csv"

    query = "INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES "

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                print('Column names are ' + ", ".join(row))
            elif line_count == 1:
                query += '(\'' + row[0] + '\',' + row[1] + ',\'' + row[2] + '\')'
            else:
                query += ', (\'' + row[0] + '\',' + row[1] + ',\'' + row[2] + '\')'
            line_count += 1
        if line_count > 1:
            query += ';';
            print('Query is: ' + query)
            runQuery(query)

    print('Processed ' + str(line_count - 1) + ' lines.')


def createJsonResponse():
    return ""
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
