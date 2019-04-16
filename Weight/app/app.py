#!/usr/bin/env python
from flask import Flask,request
import mysql.connector, time
import json
app = Flask(__name__)

@app.route('/health')
def health():
    return "OK"

@app.route('/weight',methods = ['GET'])
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

@app.route('/batch-weight')
def batch_weight():
    return "OK"

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

@app.route('/item/<id>')
def item(id):
    result="""
    { "id": 11,
    "tara": 112,
    "sessions": [1,2,3] 
    }
    """
    return result

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
