# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
from templates.student.get_face.save_photo import save_photo
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
get_photo = Blueprint("get_photo", __name__)


@get_photo.route('/get_photo', methods=['POST', 'GET'])
def get_photo_fun():
    #  获取接收的信息，转为dict格式
    get_data = request.json
    base64 = get_data['base64']

    # 获取头部信息
    Sno = request.headers.get('Sno')
    token = request.headers.get('token')
    number = request.headers.get('number')

    # 获取token
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    token_get = redis.get(Sno)
    token_get = str(token_get)
    token_get = token_get.replace("b'", "")
    token_get = token_get.replace("'", "")

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
        # 保存图片
        status = save_photo(Sno, number, base64)
        if status == 1:
            post_data = {'info': '保存成功'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            # 设置headers
            response.headers = {'Sno': Sno, 'number': number}
            #  设置HTTP状态码
            response.status_code = 200
        else:
            post_data = {'info': '保存失败'}
            #  返回的内容
            response = make_response(json.dumps(post_data))
            #  返回的json格式设定
            response.content_type = 'application/json'
            # 设置headers
            response.headers = {'Sno': Sno, 'number': number}
            #  设置HTTP状态码
            response.status_code = 401
    return response
