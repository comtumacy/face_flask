# coding=utf-8
from flask import Flask, current_app
from flask_cors import CORS
from redis import StrictRedis
import os
# 导入蓝图子模块
# public
from templates.public_api.get_college.get_college import get_college
from templates.public_api.get_class.get_class import get_class
# user
from templates.user.login.login import login
from templates.user.login.login_teacher import login_teacher
from templates.user.login.out_login import out_login
from templates.user.register.register import register
from templates.user.register.verification_code.verification_code import verification_code
from templates.user.modify.modify import modify
from templates.user.modify.modify_teacher import modify_teacher


# 设置SECRET_KEY为随机数
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
appContent = app.app_context()
appContent.push()
# 将SECRET_KEY存入Redis数据库
redis = StrictRedis(host='localhost', port=6379, db=0, password='Liyitong97!')
redis.set('SECRET_KEY', current_app.config['SECRET_KEY'])
appContent.pop()


# 跨域请求设置
CORS(app, resources=r'/*')


# 注册蓝图,蓝图添加链接前缀
# 公共接口
app.register_blueprint(get_college, url_prefix='/public')  # 获取学院信息
app.register_blueprint(get_class, url_prefix='/public')  # 获取班级信息
# 用户接口
app.register_blueprint(login, url_prefix='/user')  # 学生登录
app.register_blueprint(login_teacher, url_prefix='/user')  # 老师登录
app.register_blueprint(out_login, url_prefix='/user')  # 退出登录
app.register_blueprint(register, url_prefix='/user')  # 注册
app.register_blueprint(verification_code, url_prefix='/user')  # 获取验证码
app.register_blueprint(modify, url_prefix='/user')  # 修改学生个人信息
app.register_blueprint(modify_teacher, url_prefix='/user')  # 修改老师个人信息


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 0.0.0.0用于外部域访问
