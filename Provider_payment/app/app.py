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
    weightUrl = "http://0.0.0.0:8081/item/" + str(id)
    response = urllib.request.urlopen(weightUrl)
    return response.read()


@app.route('/bill/<id>', methods=['GET'])
def bill(id):
    t1 = flask.request.args.get("from")
    t2 = flask.request.args.get("to")
    return "Get Bill by id: " + str(id) + "and in range: " + str(t1) + ":" + str(t2)
    data = {
    "id": "",
    "name": "",
    "from": "",
    "to": "",
    "truckCount": "",
    "sessionCount": "",
    "products": [
            {"product": "",
        "count": "", 
        "amount": "", 
        "rate": "", 
        "pay": "" 
             }, ...
    ],
    "total": "" 
}


#local functions

def checkDBConnection():
    try:
        db = pymysql.connect(host="mysql-db",port=3306,user="root",passwd="greengo",db="billdb", auth_plugin_map="")
    except Exception:
        print("Error in MySQL connection")
        return 0
    else:
        print("Connection Good!")
        db.close() 
    return 1

def getConnection():
    return pymysql.connect(host="mysql-db", port=3306, user="root", passwd="greengo", db="billdb", charset='utf8mb4',
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
