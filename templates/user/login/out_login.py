from flask import Blueprint, request, make_response
from redis import StrictRedis
import json

# 创建一个蓝图的对象，蓝图就是一个小模块的概念
out_login = Blueprint("out_login", __name__)


@out_login.route('/out_login', methods=['POST', 'GET'])
def out_login_fun():
    #  获取接收的账号密码信息，转为dict格式
    get_data = request.json
    print('接收到的用户退出登录数据：{}'.format(get_data))
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    redis.set(get_data['Sno'], '')
    #  退出登录信息返回前端
    post_data = {'info': '已经成功退出'}
    #  返回的内容
    response = make_response(json.dumps(post_data))
    #  返回的json格式设定
    response.content_type = 'application/json'
    #  设置HTTP状态码
    response.status_code = 200
    return response
