# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
import json
from templates.student.attendance_results.attendance_results_sql import attendance_results_sql


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
attendance_results = Blueprint("attendance_results", __name__)


@attendance_results.route('/attendance_results', methods=['POST', 'GET'])
def attendance_results_fun():
    # 获取头部信息
    Sno = request.headers.get('Sno')
    token = request.headers.get('token')
    number = request.headers.get('number')

    # 获取token
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Luohongsheng336!')
    token_get = redis.get(Sno)
    token_get = str(token_get)
    token_get = token_get.replace("b'", "")
    token_get = token_get.replace("'", "")

    #  获取接收的账号密码信息，转为dict格式
    get_data = request.json

    # token失效
    if token != token_get:
        post_data = {'info': '登录失效，请重新登录'}
        #  返回的内容
        response = make_response(json.dumps(post_data))
        #  返回的json格式设定
        response.content_type = 'application/json'
        #  设置HTTP状态码
        response.status_code = 401
    else:
        all_list, status, page_number = attendance_results_sql(get_data['class'] + get_data['classno'], Sno, int(number) - 1)
        if status != 0:
            post_data = {'data': all_list, 'page_number': page_number}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 200
        else:
            post_data = {'info': '未查询到任何信息'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 401
    return response
