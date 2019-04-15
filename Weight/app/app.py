#!/usr/bin/env python
from __future__ import print_function
import flask
import json
import logging
import mysql.connector
from mysql.connector import errorcode
from flask import Flask 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="greengo",
  auth_plugin='mysql_native_password'
)

cursor = mydb.cursor()

query = "SELECT container_id FROM containers_registered"

cursor.execute(query)

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
    result="""
    { "id": "mario", 
    "truck": 11238,
    "bruto": 9999,
    "produce":"tomato",
    "truckTara": 654,
    "neto": 64564
    }
    """
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
mydb.close()
