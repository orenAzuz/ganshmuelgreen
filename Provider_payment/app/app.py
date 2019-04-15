#!/usr/bin/env python
import flask
from flask import Flask
import urllib
import json 
app = Flask(__name__)


@app.route('/health')
def health():
    if checkDBConnection() == 1:
        return "Payment team is OK"
    return "Failure"


@app.route('/provider/<name>', methods=['POST'])
def createProvider(name):
    runInsertQuery("INSERT INTO Provider (`name`) VALUES ('" + name + "');")
    #query = "SELECT * FROM Provider WHERE Provider.name IN name;"
    #cur.execute(query, 'Provider')
    #result = cur.fetchall()
    #for row in result:
    #return "Create provider: " + name
    data = {}
    id=9999
    data = {
     id: name, 
    }
    return str(data)


@app.route('/provider/<id>/<name>', methods=['PUT'])
def updateProvider(id, name):
    query = "update Provider set name=" + name + " where id=" + str(id) + ";"
    runUpdateQuery(query)
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
    runInsertQuery(query)
    return "Create Truck: " + id + " for provider: " + provider_id


@app.route('/truck/<id>/<provider_id>', methods=['PUT'])
def updateTruck(id, provider_id):
    query = "UPDATE Trucks SET provider_id='" + provider_id + "' WHERE id=" + id + ";"
    runUpdateQuery(query)
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
      { "product":"",
        "count": "", 
        "amount": "", 
        "rate": "", 
        "pay": "" 
      },...
    ],
    "total": "" 
}



#local functions

def checkDBConnection():
    return 1
    #run query

def runUpdateQuery(query):
    pass
    #run query

def runInsertQuery(query):
    pass
    #run query

def getRateFile():
    pass

def createJsonResponse():
    return ""
    pass



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
