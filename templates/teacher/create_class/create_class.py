# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
import json
from templates.teacher.create_class.find_is_exist_sql import find_is_exist_sql
from templates.teacher.create_class.insert_class_to_class import insert_class_to_class
from templates.teacher.create_class.create_features_table import connect_mysql
from templates.teacher.create_class.create_atendance_table import connect_mysql2


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
create_class = Blueprint("create_class", __name__)


@create_class.route('/create_class', methods=['POST', 'GET'])
def create_class_fun():
    # 获取头部信息
    Tno = request.headers.get('Tno')
    token = request.headers.get('token')

    # 获取token
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    token_get = redis.get(Tno)
    token_get = str(token_get)
    token_get = token_get.replace("b'", "")
    token_get = token_get.replace("'", "")

    #  获取接收的信息，转为dict格式
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
        status = find_is_exist_sql(get_data['class'], get_data['classno'])
        if status == 1:
            insert_class_to_class(get_data['college'], get_data['class'], get_data['classno'])
            if status == 1:
                connect_mysql(get_data['class'] + get_data['classno'])
                connect_mysql2(get_data['class'] + get_data['classno'])
                post_data = {'info': '创建班级属性、创建班级面部特征表和班级考勤记录表成功'}
                #  返回的内容
                response = make_response(json.dumps(post_data))
                #  返回的json格式设定
                response.content_type = 'application/json'
                #  设置HTTP状态码
                response.status_code = 200
            else:
                post_data = {'info': '未知错误，请联系网络还管理员'}
                #  返回的内容
                response = make_response(json.dumps(post_data))
                #  返回的json格式设定
                response.content_type = 'application/json'
                #  设置HTTP状态码
                response.status_code = 500
        else:
            post_data = {'info': '班级已经存在，无法再创建'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 401
    return response
