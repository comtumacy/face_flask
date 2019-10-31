# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
import json
from templates.student.get_face.find_features_sql import find_features_sql


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
find_features = Blueprint("find_features", __name__)


@find_features.route('/find_features', methods=['POST', 'GET'])
def find_features_fun():
    # 获取头部信息
    Sno = request.headers.get('Sno')
    token = request.headers.get('token')

    # 获取token
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
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
        status = find_features_sql(Sno, get_data['class'] + get_data['classno'])
        if status == 0:
            data = {'info': '无记录'}
            #  返回的内容
            response = make_response(json.dumps(data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 200
        else:
            data = {'info': '已经存在'}
            #  返回的内容
            response = make_response(json.dumps(data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 200
    return response
