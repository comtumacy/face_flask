# coding=utf-8
import pymysql


# 在总表查询是否存在个人信息
def login_sql(sno, username, password):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT `username`,`password` FROM Student WHERE `Sno` = {};".format(sno)
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()
    #  登录状态判定
    if tup1 == ():
        print('无此学号')
        status = 0
    else:
        username_sql = tup1[0][0]
        password_sql = tup1[0][1]
        if username_sql == username and password_sql == password:
            print('登录成功,学生账号:{}密码:{}'.format(username, password))
            status = 1
        else:
            print('账号密码错误')
            status = -1
    cursor.close()
    conn.close()
    return status
