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
    #number = request.args.get('phone')
    #changenumber = number.replace("-","")
    #nn = '+1'+ changenumber
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


# @app.route('/result',methods = ['POST', 'GET'])
# def result():
#    if request.method == 'GET':
#       result = request.form
#       print (result['place'])


@app.route("/get_patient_data", methods=['GET'])
def api_get_patient_data():
    """  功能： 获取未标注数据
         地址： http://ip:port/get_unlabeled_data
         方式： POST
         参数：
             {
                "task_name":"20170903keyword",  // 任务名称
                "rtx":"richardsun",  // rtx
                "num_samples": 2  // 需要的待标注数据数量
             }
         返回：
             {
                "ret":0,  // 返回码, 0表示正常调用，1表示异常，异常信息在msg给出
                "msg":"",  // 返回信息
                "data":[
                    {"text":"10新网游推荐","candidate_tags":[{"predicted_tag":"网游推荐","predicted_weight":0.4},{"predicted_tag":"10新","predicted_weight":0.3}],"id":1},
                    {"text":"10暑假pk网络游戏排行榜","candidate_tags":[{"predicted_tag":"10暑假pk网络游","predicted_weight":0.455},{"predicted_tag":"网络游戏","predicted_weight":0.33}],"id":3}
                ]
            }
    """

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

    return response_jsonp(result, callback)



@app.route("/load_newpatient_data", methods=['GET'])
def api_load_calledpatient_data():

    #callback = request.args.get('callback')
    #request_data = json.loads(request.data)
    file = request.args.get("file")

    lines = file.split("\r")

    Lines=lines[1:]

    for line in Lines:
        


        service_imp.load_newpatient_data(line)


    return "Correct"
        
    
    
    
    




    # ret = 0
    # msg = ''
    # ok, err = service_imp.load_calledpatient_data(task_name, id, artificial_tags, rtx)
    # if not ok:
    #     ret = 1
    #     msg = err

    # result = dict()
    # result[RET] = ret
    # result[MSG] = msg
    # return response_jsonp(result, callback)

'''
@app.route("/get_task_confs", methods=['POST'])
def api_get_task_confs():
    """  功能：获取所有任务配置
         地址：http://ip:port/get_task_confs
         方式：POST
         参数：{}
         返回：
             {
                "ret":0,  // 返回码, 0表示正常调用，1表示异常，异常信息在msg给出
                "msg":"",  // 返回信息
                "data":[
                    {"owners":["richardsun","marvinmu"],"name":"20170903keyword","active_learning_on":false,"keyword_score_lowerbound":0,"labelers":["v_hxzhao","v_siyutian"],"type":"KEYWORD","keyword_score_upperbound":3},
                    {"owners":["lijiewang","marvinmu"],"name":"20170903category","active_learning_on":false,"taxonomy":"0\troot\t-1\t0\n1\t教育\t0\t1\n2\t旅游\t0\t1\n3\t金融\t0\t1\n4\t汽车\t0\t1\n5\t房产\t0\t1\n6\t家居\t0\t1\n","labelers":["v_hxzhao","v_siyutian"],"type":"CATEGORY"}
                ]
             }
    """

    callback = request.args.get('callback')
    task_confs = service_imp.get_task_confs()

    result = dict()
    result[RET] = 0
    result[MSG] = ""
    result[DATA] = task_confs
    return response_jsonp(result, callback)


@app.route("/get_unlabeled_data", methods=['POST'])
def api_get_unlabeled_data():
    """  功能： 获取未标注数据
         地址： http://ip:port/get_unlabeled_data
         方式： POST
         参数：
             {
                "task_name":"20170903keyword",  // 任务名称
                "rtx":"richardsun",  // rtx
                "num_samples": 2  // 需要的待标注数据数量
             }
         返回：
             {
                "ret":0,  // 返回码, 0表示正常调用，1表示异常，异常信息在msg给出
                "msg":"",  // 返回信息
                "data":[
                    {"text":"10新网游推荐","candidate_tags":[{"predicted_tag":"网游推荐","predicted_weight":0.4},{"predicted_tag":"10新","predicted_weight":0.3}],"id":1},
                    {"text":"10暑假pk网络游戏排行榜","candidate_tags":[{"predicted_tag":"10暑假pk网络游","predicted_weight":0.455},{"predicted_tag":"网络游戏","predicted_weight":0.33}],"id":3}
                ]
            }
    """
    callback = request.args.get('callback')
    request_data = json.loads(request.data)
    task_name = request_data['task_name']
    rtx = request_data['rtx']
    num_samples = request_data['num_samples']

    u, err = service_imp.get_unlabeled_data(task_name, rtx, num_samples)
    ret = 0
    msg = ''
    data = []
    if u is None:
        ret = 1
        msg = err
    else:
        data = u
    result = dict()
    result[RET] = ret
    result[MSG] = msg
    result[DATA] = data
    return response_jsonp(result, callback)


@app.route("/update_aritificial_tag", methods=['POST'])
def api_update_aritificial_tag():
    """  功能：上传标注结果，如果已经存在于系统中，则覆盖
         地址：http://ip:port/update_aritificial_tag
         方式：POST
         参数：
             {
                "task_name":"20170903keyword",  // 任务名称
                "id":2 ,  // 样本id
                "artificial_tags": [{"artificial_tag": "游戏", "score": 3}, {"artificial_tag": "排行榜", "score": 2}, {"artificial_tag": "网页游戏", "score": 1}],  // 标注的标签和分数
                "rtx":"richardsun"  // rtx
             }
         返回：
             {
                "ret" : 0,  // 返回码, 0表示正常调用，1表示异常，异常信息在msg给出
                "msg" : ""  // 返回信息
             }
    """
    callback = request.args.get('callback')
    request_data = json.loads(request.data)
    task_name = request_data['task_name']
    id = request_data['id']
    artificial_tags = request_data['artificial_tags']
    rtx = request_data['rtx']

    ret = 0
    msg = ''
    ok, err = service_imp.update_aritificial_tag(task_name, id, artificial_tags, rtx)
    if not ok:
        ret = 1
        msg = err

    result = dict()
    result[RET] = ret
    result[MSG] = msg
    return response_jsonp(result, callback)
'''

@app.route("/<path:path>")
def api_file(path):
    """ 返回静态文件，譬如js, css
        注意：该route写在最后
    """
    return send_from_directory('./view/', path)

if __name__ == '__main__':
    print 'hello Andy'
    global service_imp
    service_imp = service.Service()
    app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)
