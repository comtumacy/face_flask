# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
import json
import time
from static.face_module.features_distinguish import features_distinguish
from templates.teacher.face_distinguish.student_number_matching_sql import student_number_matching_sql
from templates.teacher.face_distinguish.attendance_sql import attendance_sql


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
face_distinguish = Blueprint("face_distinguish", __name__)


@face_distinguish.route('/face_distinguish', methods=['POST', 'GET'])
def face_distinguish_fun():
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
        status, no = features_distinguish(get_data['class'] + get_data['classno'])
        if status is True:
            # a
            Sno = student_number_matching_sql(get_data['class'] + get_data['classno'], no)
            # a
            date = time.strftime("%Y-%m-%d", time.localtime())
            status = attendance_sql(get_data['class'] + get_data['classno'], date, Sno)
            if status == 1:
                post_data = {'info': '人脸识别考勤成功，此学生学号为{}'.format(Sno)}
                #  返回的内容
                response = make_response(json.dumps(post_data))
                #  返回的json格式设定
                response.content_type = 'application/json'
                #  设置HTTP状态码
                response.status_code = 200
            else:
                post_data = {'info': '人脸识别失败，请重试'}
                #  返回的内容
                response = make_response(json.dumps(post_data))
                #  返回的json格式设定
                response.content_type = 'application/json'
                #  设置HTTP状态码
                response.status_code = 401
        else:
            post_data = {'info': '人脸识别失败，请重试'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            #  设置HTTP状态码
            response.status_code = 401
    return response
