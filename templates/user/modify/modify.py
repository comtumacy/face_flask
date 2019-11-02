# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
from templates.user.modify.modify_sql import register_sql
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
modify = Blueprint("modify", __name__)


@modify.route('/modify', methods=['POST', 'GET'])
def modify_fun():
    # 获取头部信息
    Sno = request.headers.get('Sno')
    token = request.headers.get('token')

    # 获取code
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    token_get = redis.get(str(Sno))
    token_get = str(token_get)
    token_get = token_get.replace("b'", "")
    token_get = token_get.replace("'", "")

    # 判断token是否正确
    if token != token_get:
        #  设置响应体
        response = make_response()
        post_data = {"info": "登录信息失效，请重新登录"}
        post_data = json.dumps(post_data, ensure_ascii=False)
        response.set_data(post_data)
        # 设置HTTP状态码
        response.status_code = 401
    else:
        data = request.json
        status = register_sql(Sno, data['username'], data['password'], data['Sname'], data['Ssex'], data['Birth'], data['Saddress'], data['Stime'])
        if status == 1:
            #  设置响应体
            response = make_response()
            post_data = {"info": "修改个人信息成功"}
            post_data = json.dumps(post_data, ensure_ascii=False)
            response.set_data(post_data)
            # 设置HTTP状态码
            response.status_code = 200
        else:
            response = make_response()
            post_data = {"info": "修改个人信息失败，请检查输入的信息是否有误"}
            post_data = json.dumps(post_data, ensure_ascii=False)
            response.set_data(post_data)
            # 设置HTTP状态码
            response.status_code = 401
    return response
