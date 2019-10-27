# coding=utf-8
from flask import Blueprint, make_response, request
from templates.user.login.login_teacher_sql import login_sql
from redis import StrictRedis
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
login_teacher = Blueprint("login_teacher", __name__)


@login_teacher.route('/login_teacher', methods=['POST', 'GET'])
def login_teacher_fun():
    #  获取接收的账号密码信息，转为dict格式
    get_data = request.json
    print('接收到的数据：{}'.format(get_data))

    # 获取头部信息
    code = request.headers.get('code')
    ctoken = request.headers.get('ctoken')

    # 获取code
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    code_get = redis.get(ctoken)
    code_get = str(code_get)
    code_get = code_get.replace("b'", "")
    code_get = code_get.replace("'", "")

    # 判断验证码是否正确
    if code != code_get:
        #  设置响应体
        response = make_response()
        post_data = {"info": "验证码错误"}
        post_data = json.dumps(post_data, ensure_ascii=False)
        response.set_data(post_data)
        # 设置HTTP状态码
        response.status_code = 401
    else:
        #  查询数据库
        status = login_sql(get_data['Tno'], get_data['username'], get_data['password'])
        #  查询结果返回前端
        post_data = {'info': ''}
        if status == -1:
            post_data = {'info': '账号密码错误，请重新输入'}
        elif status == 0:
            post_data = {'info': '无此老师账号，请重新输入'}
        elif status == 1:
            post_data = {'info': '登录成功，欢迎{}用户'.format(get_data['Tno'])}
        #  返回的内容
        response = make_response(json.dumps(post_data))
        #  设置headers
        if status == 1:
            redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
            expiration = 3600
            s = Serializer(redis.get('SECRET_KEY'), expires_in=expiration)  # expiration是过期时间
            token = s.dumps({'username': get_data['username'], 'password': get_data['password']})
            token = str(token, 'utf-8')
            redis.set(str(get_data['Tno']), token)
            redis.expire(str(get_data['Tno']), 3600)
            response.headers = {'token': token}
        #  返回的json格式设定
        response.content_type = 'application/json'
        #  设置HTTP状态码
        if status == 1:
            response.status_code = 200
        else:
            response.status_code = 401
    return response
