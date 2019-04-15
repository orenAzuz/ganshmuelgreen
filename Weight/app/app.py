#!/usr/bin/env python
from __future__ import print_function
import flask
import json
import logging
import mysql.connector
from mysql.connector import errorcode
from flask import Flask
from flask_api import status
# from flask import jsonify

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="greengo",
  database="weight",
  auth_plugin='mysql_native_password'
)


app = Flask(__name__)

@app.route('/health')
def health():
    mydb.close()
    return "OK"

@app.route('/weight')
def weight():
    mydb.close()
    return "OK"

@app.route('/batch-weight')
def batch_weight():
    mydb.close()
    return "OK"

@app.route('/unknown')
def unknown():
    mydb.close()
    return "OK"

@app.route('/item/<id>', methods=['GET'])
def item(id):
    data = {}
    
    data = {
        'id': str(id),
        'tara': '000',  ###
        'sessions': '???' ###
    }
    mydb.close()
    return str(data)

@app.route('/session/<id>')
def session(id):
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
