# coding=utf-8
import sys
from flask import Blueprint, make_response, request
from redis import StrictRedis
from student.get_face.features_sql import features_sql
import json
sys.path.append("..")
from static.face_module.features_extraction import return_features_mean_person

# 创建一个蓝图的对象，蓝图就是一个小模块的概念
features_train_person = Blueprint("features_train_person", __name__)


@features_train_person.route('/features_train_person', methods=['POST', 'GET'])
def features_train_person_fun():
    # 获取头部信息
    Sno = request.headers.get('Sno')
    token = request.headers.get('token')

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
        # linux (change this)
        result = return_features_mean_person(Sno)
        status = features_sql(Sno, result, get_data['class'] + get_data['classno'])
        if status == 1:
            post_data = {'info': '128组人脸特征值训练保存成功'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            # 设置headers
            response.headers = {'Sno': Sno}
            #  设置HTTP状态码
            response.status_code = 200
        else:
            post_data = {'info': '128组人脸特征值训练保存失败'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            # 设置headers
            response.headers = {'Sno': Sno}
            #  设置HTTP状态码
            response.status_code = 401
    return response
