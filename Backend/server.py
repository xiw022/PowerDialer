#! /usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """web server
"""

import json

from flask import Flask, request, send_from_directory, Response
from flask_cors import CORS, cross_origin

import service

app = Flask(__name__)
CORS(app)





def response_jsonp(data, callback):

    js = json.dumps(data, ensure_ascii=False).encode('utf8')
    if callback is not None:
        js = str(callback) + '(' + js + ')'
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/")
@cross_origin()
def api_index():
    """ 返回主页
    """
    return send_from_directory('./view/','index.html')


# @app.route('/result',methods = ['POST', 'GET'])
# def result():
#    if request.method == 'GET':
#       result = request.form
#       print (result['place'])


@app.route("/get_patient_data", methods=['GET'])
def api_get_patient_data():

    callback = request.args.get('callback')
    #request_data = json.loads(request.data)
    #num_list = request_data['num_list']

    u, err = service_imp.get_patient_data(20)
    msg = ''
    data = []
    if u is None:
        msg = err
    else:
        data = u
    result = dict()
    result['MSG'] = msg
    result['DATA'] = data
    print data
    return response_jsonp(result, callback)


@app.route("/<path:path>")
def api_file(path):
    return send_from_directory('./view/', path)

if __name__ == '__main__':
    print 'hello labelme'
    global service_imp
    service_imp = service.Service()
    app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)
