#!/usr/bin/env python
from flask import Flask,request
import mysql.connector, time
import json
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

@app.route('/')
def index():
    services='''
    /health <br>
    /weight <br>
    /batch-weight/&lt;file&gt; <br>
    /unknown <br>
    /item/&lt;id&gt; <br>
    /session/&lt;id&gt; <br>
    '''
    return services

@app.route('/health')
def health():
    try:
        mydb = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user="root",
            passwd="greengo",
            database="weight",
            auth_plugin='mysql_native_password'
        )
        sqlcursor = mydb.cursor()
        sqlcursor.execute("SELECT 1;")
        mydb.close()
        return 'OK', 200
    except:
        return 'Failure', 500

@app.route('/weight',methods = ['GET'])
@app.route('/weight')
@app.route('/weight', methods=['POST'])
def weight():
    mydb = mysql.connector.connect(
      host="mysql-db",
      user="root",
      passwd="greengo",
      database="weight",
      auth_plugin='mysql_native_password'
    )
    tim = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    timt = time.strftime("%Y%m%d000000", time.gmtime())
    t1 = request.args.get('from', default = timt)
    t2 = request.args.get('to', default = tim)
    f = request.args.get('filter', default = "'in','out','none'")
    mycursor = mydb.cursor()
    arg = mycursor.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE direction IN (" + f + ") AND datetime BETWEEN "+t1+" AND " +t2)
    result = mycursor.fetchall()
    json_data = []
    row_headers = [val[0] for val in mycursor.description]
    #json_data.append(dict(zip(row_headers, result)))
    for x in result:
        content = {'id': x[0], 'direction': x[1], 'bruto': x[2], 'neto': x[3], 'produce': x[4], 'containers':x[5]}
        json_data.append(content)
        content = {}
    return json.dumps(json_data)
    return "OK"
    ## code ...
    # mydb.close()
    return "OK"

@app.route('/batch-weight/<file>')
def batch_weight(file):

    results="Field added:<br>"

    mydb = mysql.connector.connect(
      host=os.environ['DB_HOST'],
      user="root",
      passwd="greengo",
      database="weight",
      auth_plugin='mysql_native_password'
    )

    sqlcursor = mydb.cursor()

    if file in os.listdir("in/"):
        if file.lower().endswith(('.csv')):
            new_batch = open("in/"+file)
            lines = new_batch.readlines()
            unit = lines[0][:-1].split(',')[1]
            if unit[0] == '"' and unit[-1] == '"':
                unit = unit[1:-1]
            for line in lines[1:]:
                container_id = line.split(',')[0]
                weight = line.split(',')[1]

                try:
                    # insert to table containers_registered id, weight and unit
                    sqlcursor.execute("INSERT INTO containers_registered (container_id,weight,unit) VALUES (%s,%s,%s)", (container_id,weight,unit))
                    results+= container_id + " " + weight + " " + unit + "<br>"
                except mysql.connector.IntegrityError:
                    pass




        elif file.lower().endswith(('.json')):
            new_batch = open("in/"+file)
            lines = json.load(new_batch)
            for line in lines:
                container_id = line["id"]
                weight = line["weight"]
                unit = line["unit"]

                try:
                    # insert to table containers_registered id, weight and unit
                    sqlcursor.execute("INSERT INTO containers_registered (container_id,weight,unit) VALUES (%s,%s,%s)", (container_id,weight,unit))
                    results+= container_id + " " + str(weight) + " " + unit + "<br>"
                except mysql.connector.IntegrityError:
                    pass 


        new_batch.close()

    mydb.close()
    return results

@app.route('/unknown')
def unknown():
    mydb = mysql.connector.connect(
      host="mysql-db",
      user="root",
      passwd="greengo",
      database="weight",
      auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT container_id from containers_registered where weight like NULL")
    result = mycursor.fetchall()
    ret = ""
    ret = '\n'.join(map(str, result))
    if ret=="":
        return "There is none UNKNOWN weight"
    else:
        return ret
    return "OK"
    ## code ...
    # mydb.close()
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
    # mydb.close()
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
    return json.dumps(json_data)[1:][:-1]

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

