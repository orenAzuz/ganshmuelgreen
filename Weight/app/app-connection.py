#!/usr/bin/env python

## INSTALL:
# mysql-connector-python

from flask import Flask

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="greengo",
  auth_plugin='mysql_native_password'
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

#
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `containers_registered` (`container_id`, `weight`, `unit`) VALUES (%s, %s)"
#         cursor.execute(sql, ('111', 1000, 'kg'))
#
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
#
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `*` FROM `containers_registered`" # WHERE `email`=%s"
#         #cursor.execute(sql, ('webmaster@python.org',))
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)
# finally:
#     connection.close()
#


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
    return "OK"

@app.route('/item/<id>')
def item():
    return "OK"

@app.route('/session/<id>')
def session():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
