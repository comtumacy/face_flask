# coding=utf-8
from flask import Blueprint, make_response
from public_api.get_college.get_college_sql import get_college_sql
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
get_college = Blueprint("get_college", __name__)


@get_college.route('/get_college', methods=['POST', 'GET'])
def get_college_fun():
    data = get_college_sql()
    #  返回的内容
    response = make_response(json.dumps(data))
    #  返回的json格式设定
    response.content_type = 'application/json'
    return response
