import os
from flask import Blueprint, make_response, request
from redis import StrictRedis


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
get_photo = Blueprint("get_photo", __name__)


@get_photo.route('/get_photo', methods=['POST', 'GET'])
def get_photo_fun():
    path = 'D:\\face\\static'
    isExists = os.path.exists(path)
    print(isExists)
