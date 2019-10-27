from flask import Blueprint, make_response, request
from templates.public_api.get_class.get_class_sql import get_class_sql
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
get_class = Blueprint("get_class", __name__)


@get_class.route('/get_class', methods=['POST', 'GET'])
def get_class_fun():
    #  获取接收所选择的学院信息，转为dict格式
    get_data = request.json

    data = get_class_sql(get_data['college'])
    #  返回的内容
    response = make_response(json.dumps(data))
    #  返回的json格式设定
    response.content_type = 'application/json'
    return response
