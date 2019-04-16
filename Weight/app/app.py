#!/usr/bin/env python
from flask import Flask
import mysql.connector
app = Flask(__name__)

@app.route('/health')
def health():
    return "OK"

@app.route('/weight')
def weight():
    return "OK"

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
