from flask import Blueprint, make_response
from Face_attendance_system.src.components.user.register.verification_code.get_verification_code_base64 import get_verification_code_base64
from redis import StrictRedis
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json


# 创建一个蓝图的对象，蓝图就是一个小模块的概念
verification_code = Blueprint("verification_code", __name__)


# 获取base64图片流， 验证码， 根据验证码加密的ctoken
@verification_code.route('/verification_code', methods=['POST', 'GET'])
def get_base_code():
    # 获取base64图片流， 验证码
    base_str, code = get_verification_code_base64()
    print(code)
    # 获取SECRET_KEY
    redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
    secret_key = redis.get('SECRET_KEY')

    # 生成ctoken， 120s后过期
    expiration = 3600
    s = Serializer(secret_key, expires_in=expiration)  # expiration是过期时间
    ctoken = s.dumps({'code': code})
    ctoken = str(ctoken, 'utf-8')

    # 存入redis
    redis.set(str(ctoken), str(code))
    redis.expire(str(ctoken), 3600)

    # 设置JSON返回base64图片流
    data = {'base64': base_str}
    data = json.dumps(data)
    #  返回的内容
    response = make_response(data)
    #  返回的json格式设定
    response.content_type = 'application/json'
    #  设置ctoken
    response.headers = {'ctoken': ctoken}

    return response
