# coding=utf-8
import pymysql


def find_is_exist_sql(class_name, class_no):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT * FROM class WHERE class = '{}' AND classno = '{}';".format(class_name, class_no)
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()
    #  判定班级是否存在
    if len(tup1) == 0:
        status = 1
    else:
        status = 0
    cursor.close()
    conn.close()
    return status
