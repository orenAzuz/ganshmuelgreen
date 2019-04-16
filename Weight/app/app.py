#!/usr/bin/env python
from __future__ import print_function
import flask
import json
import logging
import os
import mysql.connector
from mysql.connector import errorcode
from flask import Flask
#from flask_api import status

app = Flask(__name__)

@app.route('/health')
def health():
    ## code ...
    return "OK"

@app.route('/weight', methods=['POST'])
def weight():
    ## code ...
    return "OK"

@app.route('/batch-weight')
def batch_weight():
    ## code ...
    return "OK"

@app.route('/unknown')
def unknown():
    ## code ...
    return "OK"

@app.route('/item/<id>', methods=['GET'])
def item(id):
    t1 = flask.request.args.get("from")
    if str(t1) == "None":
        t1="000000"
    t2 = flask.request.args.get("to")
    if str(t2) == "None":
        t2="Now"
    mydb = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user="root",
        passwd="greengo",
        database="weight",
        auth_plugin='mysql_native_password'
    )
    sqlcursor = mydb.cursor()
    #sqlcursor.execute("SELECT id, truck, bruto, truckTara, neto FROM transactions WHERE id = " + id + " AND direction = 'out'")
    #results = sqlcursor.fetchall()
    sqlcursor.execute("SELECT id, truckTara FROM transactions WHERE id = " + str(id) )
    results = sqlcursor.fetchall()
    temp = ""
    if not results:
        temp = "na"
    else:
        temp = results[0][1]
    data = {}
    data = {
        'id': str(id),
        'tara': str(temp),
        'sessions': str(t2) ###
    }
    mydb.close()
    return str(data)

@app.route('/session/<id>')
def session(id):
    mydb = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user="root",
        passwd="greengo",
        database="weight",
        auth_plugin='mysql_native_password'
    )

    sqlcursor = mydb.cursor()

    sqlcursor.execute("SELECT id, truck, bruto, truckTara, neto FROM transactions WHERE id = " +
                      id + " AND direction = 'out'")
    results = sqlcursor.fetchall()
    if sqlcursor.rowcount > 0:
        print("Getting session values for 'out' session type")
        row_headers = [val[0] for val in sqlcursor.description]  # this will extract row headers

    else:
        sqlcursor.execute("SELECT id, truck, bruto FROM transactions WHERE id = " + id)
        results = sqlcursor.fetchall()
        if sqlcursor.rowcount > 0:
            print("Getting session values (not for 'out' session type)")
            row_headers = [val[0] for val in sqlcursor.description]  # this will extract row headers
        else:
            return "Session ID not found (404)", status.HTTP_404_NOT_FOUND

    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

    # SPEC:
    #
    # "id": < str >,
    # "truck": < truck - id > or "na",
    # "bruto": < int >,
    # ONLY
    # for OUT:
    #   "truckTara": < int >,
    #   "neto": < int > or "na" // na if some of containers unknown

    # previous hard-coded results for testing:
    # result="""
    # { "id": "mario",
    # "truck": 11238,
    # "bruto": 9999,
    # "produce":"tomato",
    # "truckTara": 654,
    # "neto": 64564
    # }



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)

mydb.close()
