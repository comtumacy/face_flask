import pymysql


def login_sql(tno, username, password):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='LuoHongSheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT `username`,`password` FROM teacher WHERE `Tno` = {};".format(tno)
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()
    #  登录状态判定
    if tup1 == ():
        print('无此老师账号')
        status = 0
    else:
        username_sql = tup1[0][0]
        password_sql = tup1[0][1]
        if username_sql == username and password_sql == password:
            print('登录成功,老师账号:{}密码:{}'.format(username, password))
            status = 1
        else:
            print('账号密码错误')
            status = -1
    cursor.close()
    conn.close()
    return status
