import datetime
from flask import Flask, render_template, request, send_file
import os.path
import logging
import io
import sys
app = Flask(__name__, static_url_path='', static_folder='',
            template_folder='')

file_name = "general"


@app.route('/', defaults={'path_name': ''})
@app.route("/<string:path_name>", methods=['GET'])
def start(path_name):
    if path_name != "":
        path_name = "general"
    return render_template('index.html')


text = "general"


@app.route("/api/chat/<string:path_name>/", methods=['GET'])
def general(path_name):
    list_request = path_name.split()
    app.file_name = list_request[-1]
    send = 'data/%s.txt' % app.file_name
    if os.path.isfile(send):
        return send_file(send)
    else:
        file = open(send, 'w')
        file.close()
        return send_file(send)


@app.route("/api/chat/<string:path_name>/", methods=['POST'])
def post_chat(path_name):
    name = path_name
    send = 'data/%s.txt' % name
    f = open('data/%s.txt' % name, 'a')
    user = request.form.get('username')
    msg = request.form.get('msg')
    date = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
    data = (date, user, msg)
    string_to_write = "[%s] %s : %s \n" % data
    f.write(string_to_write)   # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    return send_file(send)


if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        port = sys.argv[1]

    app.run(host='0.0.0.0', port=port)



# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if flask.request.method == 'POST':
#         username = flask.request.values.get('user') # Your form's
#         password = flask.request.values.get('pass') # input names
#         your_register_routine(username, password)
#     else:
#         # You probably don't have args at this route with GET
#         # method, but if you do, you can access them like so:
#         yourarg = flask.request.args.get('argname')
#         your_register_template_rendering(yourarg)