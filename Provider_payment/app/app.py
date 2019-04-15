#!/usr/bin/env python
import flask
import pymysql
import pymysql.cursors
from flask import Flask

app = Flask(__name__)


@app.route('/health')
def health():
    if checkDBConnection() == 1:
        return "Payment team is OK"
    return "Failure1"


@app.route('/provider/<name>', methods=['POST'])
def createProvider(name):
    query = "INSERT INTO Provider (`name`) VALUES ('" + name + "');"
    runQuery(query)
    return "Create provider: " + name


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
    return "Get Truck by id: " + str(id) + "and in range: " + str(t1) + ":" + str(t2)


@app.route('/bill/<id>', methods=['GET'])
def bill(id):
    t1 = flask.request.args.get("from")
    t2 = flask.request.args.get("to")
    return "Get Bill by id: " + str(id) + "and in range: " + str(t1) + ":" + str(t2)



#local functions

def checkDBConnection():
#    try:
    db = pymysql.connect(host="localhost",port=8082,user="root",passwd="greengo",db="billdb")
        #db = pymysql.connect(host="localhost",user="root",passwd="greengo",db="billdb")
#    except Exception:
#        print("Error in MySQL connection")
#        return 0
#    else:
#        print("Connection Good!")
#        db.close() 
    return 1
    #run query

def runQuery(query):
    # Connect to the database
    connection = pymysql.connect(host="localhost",port=8082,user="root",passwd="greengo",db="billdb", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

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
    app.run(host="0.0.0.0", port=8000, debug=True)
