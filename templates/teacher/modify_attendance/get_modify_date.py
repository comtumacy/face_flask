# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
import json
from teacher.modify_attendance.get_modify_date_sql import get_modify_date_sql


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
get_modify_date = Blueprint("get_modify_date", __name__)


@get_modify_date.route('/get_modify_date', methods=['POST', 'GET'])
def get_modify_date_fun():
    # 获取头部信息
    Tno = request.headers.get('Tno')
    token = request.headers.get('token')

    # 获取token
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Luohongsheng336!')
    token_get = redis.get(Tno)
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
        all_list = get_modify_date_sql(get_data['class'] + get_data['classno'])
        if len(all_list) != 0:
            post_data = all_list
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 200
        else:
            post_data = {'info': '查询失败'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 401
    return response
