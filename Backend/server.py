#! /usr/bin/env python
# -*- coding: utf-8 -*-


__doc__ = """web server
"""

import json
from twilio.rest import Client
from twilio import twiml
from flask import Flask, request, send_from_directory, Response
from flask_cors import CORS, cross_origin

import service


account_sid = 'AC95fd277d38fbfe2cdbe6b35f1f7996a6'
auth_token = '743fd6872ffb78d697c7ee130462d956'
call_id = ""
start_time = ""
end_time = ""

app = Flask(__name__)
CORS(app)





def response_jsonp(data, callback):

    js = json.dumps(data, ensure_ascii=False).encode('utf8')
    if callback is not None:
        js = str(callback) + '(' + js + ')'
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/call_patient", methods=['GET'])
def call():
    global call_id, start_time
    number = request.args.get('phone')
    changenumber = number.replace("-","")
    nn = '+1'+ changenumber
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                       machine_detection='Enable',
                       url='http://demo.twilio.com/docs/voice.xml',
                       to='+18586665289',  #placeholder number grab this from the number column in table
                       from_='+13143107942'    #purchased twilio number

                   )
    #sid = call()
    call_id = call.sid
    callrec = client.calls(call.sid).fetch()
    #print(callrec.duration)
    duration = callrec.duration
    if duration is None:
        duration = str(0)
    start_time = callrec.start_time.strftime("%Y-%m-%d %H:%M:%S")
    return "Called!"


@app.route("/patient_stats", methods=['GET'])
def patient_stats():
    global end_time
    p_id = request.args.get("id")
    outcome = request.args.get('result')
    client = Client(account_sid, auth_token)
    callrec = client.calls(call_id).fetch()
    end_time = callrec.end_time.strftime("%Y-%m-%d %H:%M:%S")
    service_imp.load_calledpatient_data(p_id, start_time, end_time, outcome)
    return "Sent stats!"

@app.route("/")
@cross_origin()
def api_index():

    return send_from_directory('./view/','index.html')





@app.route("/get_patient_data", methods=['GET'])
def api_get_patient_data():
    

    callback = request.args.get('callback')
    

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

    return response_jsonp(result, callback)



@app.route("/load_newpatient_data", methods=['GET'])
def api_load_calledpatient_data():

    
    file = request.args.get("file")

    lines = file.split("\r")

    Lines=lines[1:]

    for line in Lines:
        


        service_imp.load_newpatient_data(line)


    return "Correct"
        

@app.route("/<path:path>")
def api_file(path):

    return send_from_directory('./view/', path)

if __name__ == '__main__':
    global service_imp
    service_imp = service.Service()
    app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)
