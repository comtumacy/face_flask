# coding=utf-8
from flask import Flask, current_app
from flask_cors import CORS
from redis import StrictRedis
import os

# 导入蓝图子模块
# public
from public_api.get_college.get_college import get_college
from public_api.get_class.get_class import get_class
# user
from user.login.login import login
from user.login.login_teacher import login_teacher
from user.login.out_login import out_login
from user.register.register import register
from user.register.verification_code.verification_code import verification_code
from user.modify.modify import modify
from user.modify.modify_teacher import modify_teacher
# student
from student.get_face.get_student_info import get_student_info
from student.get_face.get_photo import get_photo
from student.get_face.features_train_person import features_train_person
from student.get_face.find_features import find_features
from student.attendance_results.attendance_results import attendance_results
# teacher
from teacher.create_class.create_class import create_class
from teacher.face_distinguish.face_distinguish import face_distinguish
from teacher.attendance_results_teacher.attendance_results_teacher import attendance_results_teacher
from teacher.modify_attendance.modify_attendance import modify_attendance
from teacher.modify_attendance.get_modify_date import get_modify_date

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
# 学生接口
app.register_blueprint(get_student_info, url_prefix='/student')  # 获取当前学生的个人信息
app.register_blueprint(get_photo, url_prefix='/student')  # 保存照片
app.register_blueprint(features_train_person, url_prefix='/student')  # 获取保存人脸特征
app.register_blueprint(find_features, url_prefix='/student')  # 查询是否该学生已经存在人脸特征
app.register_blueprint(attendance_results, url_prefix='/student')  # 个人考勤情况查询
# 教师接口
app.register_blueprint(create_class, url_prefix='/teacher')  # 创建班级
app.register_blueprint(face_distinguish, url_prefix='/teacher')  # 人脸考勤
app.register_blueprint(attendance_results_teacher, url_prefix='/teacher')  # 班级考勤情况查询
app.register_blueprint(modify_attendance, url_prefix='/teacher')  # 班级考勤数据修改
app.register_blueprint(get_modify_date, url_prefix='/teacher')  # 获取班级考勤日期


if __name__ == '__main__':
    app.run(host='172.27.0.13', port=5001, debug=False)  # 0.0.0.0用于外部域访问

