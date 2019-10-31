# coding=utf-8
from flask import Blueprint, make_response, request
from redis import StrictRedis
from templates.user.register.register_sql import register_sql
from templates.user.register.insert_sql import insert_sql
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
register = Blueprint("register", __name__)


@register.route('/register', methods=['POST', 'GET'])
def register_fun():
    # 获取data
    data = request.json
    # 获取头部信息
    code = request.headers.get('code')
    ctoken = request.headers.get('ctoken')

    # 获取code
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    code_get = redis.get(ctoken)
    code_get = str(code_get)
    code_get = code_get.replace("'", "")
    code_get = code_get.replace("b", "")

    #  设置响应体
    response = make_response()

    # 判断验证码是否正确
    if code != code_get:
        post_data = {"info": "验证码错误"}
        post_data = json.dumps(post_data)
        response.set_data(post_data)
        # 设置HTTP状态码
        response.status_code = 401
    else:
        status1 = register_sql(data['Sno'], data['username'], data['password'], data['Sname'], data['Ssex'], data['Sclass'], data['Sclassno'], data['Sdept'])
        status2 = insert_sql(data['Sno'], data['Sclass'] + data['Sclassno'])
        if status1 == 1 & status2 == 1:
            post_data = {"info": "注册成功"}
            post_data = json.dumps(post_data)
            response.set_data(post_data)
        else:
            post_data = {"info": "学号或用户名已经存在"}
            post_data = json.dumps(post_data)
            response.set_data(post_data)
    #  返回的json格式设定
    response.content_type = 'application/json'
    return response
