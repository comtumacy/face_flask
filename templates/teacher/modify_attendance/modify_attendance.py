# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
import json
from teacher.modify_attendance.modify_attendance_sql import modify_attendance_sql


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
modify_attendance = Blueprint("modify_attendance", __name__)


@modify_attendance.route('/modify_attendance', methods=['POST', 'GET'])
def modify_attendance_fun():
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
        if get_data['sign'] == '是' or get_data['sign'] == '否':
            status = modify_attendance_sql(get_data['class'] + get_data['classno'], get_data['Sno'], get_data['sign'], get_data['date'])
            if status == 1:
                post_data = {'info': '修改成功'}
                #  返回的内容
                response = make_response(json.dumps(post_data))
                #  返回的json格式设定
                response.content_type = 'application/json'
                #  设置HTTP状态码
                response.status_code = 200
            else:
                post_data = {'info': '未知错误，请联系开发人员'}
                #  返回的内容
                response = make_response(json.dumps(post_data))
                #  返回的json格式设定
                response.content_type = 'application/json'
                #  设置HTTP状态码
                response.status_code = 401
        else:
            post_data = {'info': '修改失败，请重新检查你输入的数据正确性'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 401
    return response
