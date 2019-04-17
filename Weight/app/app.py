#!/usr/bin/env python
#from __future__ import print_function
from flask import Flask, request
import mysql.connector, time
import json
import flask
import json
import logging
import os
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request
import datetime
# from flask_api import status

app = Flask(__name__)

logging.basicConfig(filename='Weight_Log.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def connect_or_reconnect_db(mydb):
    # Initially DB is disconnected, but we want to retain one connection & only reconnect when necessary since
    # some functionality requires a more persistent connection - not repeated connect/disconnect cycles
    if not mydb.is_connected():
        mydb = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user="root",
            passwd="greengo",
            database="weight",
            auth_plugin='mysql_native_password'
        )
    logging.debug('mySQL connection created successfully, mydb:'+str(mydb))
    return mydb

def run_select(mydb, sql):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()
    sql_cursor.execute(sql)
    results = sql_cursor.fetchall()
    logging.debug('run_select successfully finished, results:'+ str(results))
    return results


def run_select_json(mydb, sql):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()
    sql_cursor.execute(sql)
    results = sql_cursor.fetchall()
    row_headers = [val[0] for val in sql_cursor.description]  # this will extract row headers
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    logging.debug('run_select_json successfully finished, json_data:'+json_data)
    return json.dumps(json_data)


def run_select_one_value(mydb, sql):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()
    sql_cursor.execute(sql)
    results = sql_cursor.fetchall()
    if len(results) > 0:
        logging.debug('run_select_json successfully finished,results[0][0]:'+str(results[0][0]))
        return results[0][0]
    else:
        logging.debug('run_select_json successfully finished,"":')
        return ""


def run_insert(mydb, sql):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()
    sql_cursor.execute(sql)
    mydb.commit()
    logging.debug("Record inserted successfully")


def run_update(mydb, sql):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()
    sql_cursor.execute(sql)
    mydb.commit()
    logging.debug("Record updated successfully")


def weight_json_in_or_none(mydb, session_id):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()

    sql_cursor.execute("SELECT id, truck, bruto FROM transactions WHERE id = " + str(session_id))
    results = sql_cursor.fetchall()
    if sql_cursor.rowcount > 0:
        print("Getting session values (not for 'in' or 'none' session type)")
        row_headers = [val[0] for val in sql_cursor.description]  # this will extract row headers
    else:
        logging.error(str(last_insert_id)+" was not found in table 'transactions'")
        return "Session ID not found (404)", 404

    json_data = []
    for result in results:
        # TODO for na values
        # "truck": <license> or "na",
        # "neto": <int> or "na" // na if some of containers have unknown tara
        json_data.append(dict(zip(row_headers, result)))
    logging.debug("Found id in 'transactions': "+str(json.dumps(json_data)[1:][:-1]))
    return json.dumps(json_data)[1:][:-1] # strip first and last character


def weight_json_out(mydb, session_id):
    # if connection dropped, reconnect
    mydb = connect_or_reconnect_db(mydb)
    sql_cursor = mydb.cursor()

    sql_cursor.execute("SELECT id, truck, bruto, truckTara, neto FROM transactions WHERE id = " +
                       str(session_id) + " AND direction = 'out'")
    results = sql_cursor.fetchall()
    if sql_cursor.rowcount > 0:
        logging.debug("Getting session values (not for 'out' session type)")
        row_headers = [val[0] for val in sql_cursor.description]  # this will extract row headers
    else:
        logging.error(str(truck_previous_session_id)+" was not found in table 'transactions'")
        return "Session ID not found (404)", 404

    json_data = []
    for result in results:
        # TODO for na values
        # "truck": <license> or "na",
        # "neto": <int> or "na" // na if some of containers have unknown tara
        json_data.append(dict(zip(row_headers, result)))
    logging.debug("Found id in 'transactions': "+str(json.dumps(json_data)[1:][:-1]))
    return json.dumps(json_data)[1:][:-1] # strip first and last character



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
    logging.debug("Showing index")
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
        logging.debug("Status check: OK 200")
        return 'OK', 200
    except:
        logging.fatal("No server connection: Failure 500")
        return 'Failure', 500


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
                    logging.debug("insert to table containers_registered id, weight and unit")
                    sqlcursor.execute("INSERT INTO containers_registered (container_id,weight,unit) VALUES (%s,%s,%s)", (container_id,weight,unit))
                    mydb.commit()
                    results+= container_id + " " + weight + " " + unit + "<br>"
                except mysql.connector.IntegrityError:
                    logging.error("mysql connector IntegrityError error")
                    pass


        elif file.lower().endswith(('.json')):
            new_batch = open("in/"+file)
            lines = json.load(new_batch)
            for line in lines:
                container_id = line["id"]
                weight = line["weight"]
                unit = line["unit"]

                try:
                    logging.debug("insert to table containers_registered id, weight and unit")
                    sqlcursor.execute("INSERT INTO containers_registered (container_id,weight,unit) VALUES (%s,%s,%s)", (container_id,weight,unit))
                    mydb.commit()
                    results+= container_id + " " + str(weight) + " " + unit + "<br>"
                except mysql.connector.IntegrityError:
                    logging.error("mysql connector IntegrityError error")
                    pass 


        new_batch.close()

    mydb.close()
    logging.debug("Returning file containing: "+str(results))
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
    mycursor.execute("SELECT container_id from containers_registered where weight is NULL")
    result = mycursor.fetchall()
    ret = ""
    ret = '\n'.join(map(str, result))
    logging.debug("Returning UNKNOWN weight: "+ret)
    if ret=="":
        return "There is none UNKNOWN weight"
    else:
        return ret


@app.route('/item/<idarg>', methods=['GET'])
def item(idarg):

    mydb = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user="root",
        passwd="greengo",
        database="weight",
        auth_plugin='mysql_native_password'
    )


    now = datetime.datetime.now()
    t1 = now.strftime("%Y%m0100000")
    t2 = now.strftime("%Y%m%d%H%M%S")[:-1]

    arg1 = request.args.get("from")
    arg2 = request.args.get("to")

    if arg1:
        if arg1.isdigit() and len(arg1) == 13:
            t1 = arg1
    if arg2:
        if arg2.isdigit() and len(arg2) == 13:
            t2 = arg2


    sqlcursor = mydb.cursor()

    

    sqlcursor.execute("SELECT id, datetime, direction, truck, truckTara FROM transactions WHERE truck = %s AND datetime > %s AND datetime < %s", (idarg, t1, t2))
    query_result = sqlcursor.fetchall()

    if not query_result:
        sqlcursor.execute("SELECT id, datetime, direction, containers, truckTara FROM transactions WHERE containers like '%" + idarg + "%' AND datetime > %s AND datetime < %s", (t1, t2))
        query_result = sqlcursor.fetchall()

        there_is_container = False

        if query_result:
            sessions = []
            for line in query_result:
                container_list = line[3].split(",")

                for container in container_list:
                    if idarg == container:
                        if line[2] == "in" or line[2] == None:
                            sessions.append(line[0])
                            there_is_container = True

                if there_is_container == False:
                    query_result = None


    mydb.close()


    if query_result:
        tara = query_result[-1][4]

        sessions = []
        for line in query_result:
            if line[2] == "in" or line[2] == None:
                sessions.append(line[0])

        data = {
                'id': idarg,
                'tara': tara,
                'sessions': sessions
        }

        result = json.dumps(data)
        # result = line[3]

    else:
        logging.error("Not found correct setion for id: "+str(idarg))
        result = "Session ID not found (404)", 404
    logging.debug("Returning final result: "+str(result))
    return result


@app.route('/session/<id>')
def session(id):
    mydb = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user="root",
        passwd="greengo",
        database="weight",
        auth_plugin='mysql_native_password'
    )

    sql_cursor = mydb.cursor()

    sql_cursor.execute("SELECT id, truck, bruto, truckTara, neto, produce FROM transactions WHERE id = " +
                      id + " AND direction = 'out'")
    results = sql_cursor.fetchall()
    if sql_cursor.rowcount > 0:
        logging.debug("Getting session values for 'out' session type")
        row_headers = [val[0] for val in sql_cursor.description]  # this will extract row headers

    else:
        sql_cursor.execute("SELECT id, truck, bruto, produce FROM transactions WHERE id = " + id)
        results = sql_cursor.fetchall()
        if sql_cursor.rowcount > 0:
            logging.debug("Getting session values (for 'in' or 'none' session type)")
            row_headers = [val[0] for val in sql_cursor.description]  # this will extract row headers
        else:
            logging.error("Session ID not found: 404")
            return "Session ID not found", 404

    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    logging.debug("Returning json file: "+str(json.dumps(json_data)[1:][:-1]))
    return json.dumps(json_data)[1:][:-1] # strip first and last character


@app.route('/weight', methods=['POST', 'GET'])
def weight():
    if request.method == 'GET':

        mydb = mysql.connector.connect(
            host="mysql-db",
            user="root",
            passwd="greengo",
            database="weight",
            auth_plugin='mysql_native_password'
        )
        tim = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        timt = time.strftime("%Y%m%d000000", time.gmtime())
        t1 = request.args.get('from', default=timt)
        t2 = request.args.get('to', default=tim)
        f = request.args.get('filter', default="'in','out','none'")
        mycursor = mydb.cursor()
        arg = mycursor.execute(
            "SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE direction IN ('" + f + "') AND datetime BETWEEN " + t1 + " AND " + t2)
        result = mycursor.fetchall()
        json_data = []
        row_headers = [val[0] for val in mycursor.description]
        # json_data.append(dict(zip(row_headers, result)))
        for x in result:
            content = {'id': x[0], 'direction': x[1], 'bruto': x[2], 'neto': x[3], 'produce': x[4], 'containers': x[5]}
            json_data.append(content)
            content = {}
        logging.debug("Returning json file: "+str(json.dumps(json_data)))
        return json.dumps(json_data)


    if request.method == 'POST':

        direction = request.form.get('direction')
        truck = request.form.get('truck')
        containers = request.form.get('containers')
        weight = request.form.get('weight')
        unit = request.form.get('unit') # Convert to KG for storing in "transactions" table
        force = request.form.get('force')
        produce = request.form.get('produce')

        if unit == "lbs":
            weight_kg = int(weight) * 2.205
        elif unit == "kg":
            weight_kg = int(weight)
        else:
            return "Invalid unit - 'kg' or 'lbs' required (400)", 400

        mydb = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user="root",
            passwd="greengo",
            database="weight",
            auth_plugin='mysql_native_password'
        )

        # Initially DB is disconnected, but we want to retain one connection & only reconnect when necessary since
        # some functionality requires a more persistent connection - not repeated connect/disconnect cycles
        mydb = connect_or_reconnect_db(mydb)

        if direction == 'none':
            in_or_out = run_select(mydb, "SELECT id, direction FROM transactions " + #WHERE truck = '"+truck+"' " \
                                   "ORDER BY datetime DESC LIMIT 1")

            if len(in_or_out) > 0 and in_or_out[0][1] == 'in':
                # in after none
                print("'none' after 'in' not allowed (400)")
                logging.error("'none' after 'in' not allowed: 400")
                return "'none' after 'in' not allowed (400)", 400
            else:
                print("'none' - normal")
                run_insert(mydb, "INSERT INTO transactions (datetime, direction, containers, bruto, produce) VALUES (now(), " \
                           "'" + direction + "', '" + containers + "', " + str(weight_kg) + ", '" + produce + "' )")
                logging.debug("Returning weight infornation: "+str(weight_json_in_or_none(mydb, run_select_one_value(mydb, "SELECT LAST_INSERT_ID()"))))
                return weight_json_in_or_none(mydb, run_select_one_value(mydb, "SELECT LAST_INSERT_ID()"))

        if direction == 'in':
            if not truck:
                return "Required 'truck' value not supplied (400)", 400

            in_or_out = run_select(mydb, "SELECT id, direction FROM transactions " + #WHERE truck = '"+truck+"' " \
                                   "ORDER BY datetime DESC LIMIT 1")

            if in_or_out[0][1] == 'in':
                # in after in
                if force == 'true':
                    print("in after in - force")
                    truck_previous_session_id = in_or_out[0][0]
                    # overwrite bruto if forced
                    run_update(mydb, "UPDATE transactions SET bruto = "+str(weight_kg)+" "
                               "WHERE id = "+str(truck_previous_session_id))
                    # return info - only for in
                    logging.debug("changing value")
                    return weight_json_in_or_none(mydb, truck_previous_session_id)
                elif in_or_out[0][1] == 'none':
                    logging.error("'in' after 'none' not allowed (400)")
                    return "'in' after 'none' not allowed (400)", 400
                else:
                    logging.error("'in' after 'in' without force not allowed (400)")
                    return "'in' after 'in' without force not allowed (400)", 400

            elif in_or_out[0][1] == 'out':
                # in after out
                logging.debug("in after out")
                # normal new session
                run_insert(mydb, "INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce) VALUES (now(), " \
                             "'"+direction+"', '"+truck+"', '"+containers+"', "+str(weight_kg)+", '"+produce+"' )")
                # return info - only for in
                logging.debug("changing value")
                return weight_json_in_or_none(mydb, run_select_one_value(mydb, "SELECT LAST_INSERT_ID()"))

            elif in_or_out[0][1] == 'none':
                # in after none
                print("in after none")
                # normal new session
                run_insert(mydb, "INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce) VALUES (now(), " \
                             "'"+direction+"', '"+truck+"', '"+containers+"', "+str(weight_kg)+", '"+produce+"' )")
                # return info - only for in
                logging.debug("changing value")
                return weight_json_in_or_none(mydb, run_select_one_value(mydb, "SELECT LAST_INSERT_ID()"))

            else:
                logging.error("Operation unknown - not allowed (400)")
                return "Operation unknown - not allowed (400)", 400


        if direction == 'out':
            if not truck:
                return "Required 'truck' value not supplied (400)", 400

            in_or_out = run_select(mydb, "SELECT id, direction FROM transactions WHERE truck = '"+truck+"' " \
                                   "ORDER BY datetime DESC LIMIT 1")

            if in_or_out[0][1] == 'in' or (in_or_out[0][1] == 'out' and force == 'true'):
                # this implies 'in' then 'out' ...
                # update info for truck ... with empty containers on truck
                print("out after in OR out after out - forced")
                truck_previous_session_id = in_or_out[0][0]

                bruto_was = run_select_one_value(mydb, "SELECT bruto FROM transactions WHERE id = "+str(truck_previous_session_id))

                total_weight_of_containers = 0
                for container_id in str(containers).split(",") :
                    result = run_select(mydb, "SELECT weight, unit FROM containers_registered " \
                                        "WHERE container_id = '"+str(container_id)+"'")[0]
                    if result[1] == 'kg':
                        total_weight_of_containers += result[0]
                    else:
                        total_weight_of_containers += result[0] * 2.205

                if total_weight_of_containers > 0:
                    # update data in previous 'in' record - all container weights were known:
                    run_update(mydb, "UPDATE transactions SET direction = 'out', truckTara = "+str(weight_kg)+
                               ", neto = "+str(bruto_was-weight_kg-total_weight_of_containers)+" WHERE id = "+str(truck_previous_session_id))
                    # return info - only for in
                    logging.debug("returning value: "+weight_json_out(mydb, truck_previous_session_id))
                    return weight_json_out(mydb, truck_previous_session_id)
                else:
                    # some container weights unknown - don't update 'neto'
                    run_update(mydb, "UPDATE transactions SET direction = 'out', truckTara = "+str(weight_kg)+" "
                               "WHERE id = "+str(truck_previous_session_id))
                    # return info - only for in
                    logging.debug("returning value: "+weight_json_out(mydb, truck_previous_session_id))
                    return weight_json_out(mydb, truck_previous_session_id)

            elif in_or_out[0][1] == 'out' and force != 'true':
                # out after out ... not forced
                logging.error("'out' after 'out' without force not allowed (400)")
                return "'out' after 'out' without force not allowed (400)", 400

            else:
                logging.error("'out' without 'in' not allowed (400)")
                return "'out' without 'in' not allowed (400)", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)

