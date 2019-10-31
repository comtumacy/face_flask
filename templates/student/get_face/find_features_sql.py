# coding=utf-8
import pymysql


# 在人脸特征数据库中的班级表内查询该学生是否已经存在人脸数据（修改）
def find_features_sql(Sno, table_name):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='features',
                           charset='utf8')
    cursor = conn.cursor()
    sql_find = "SELECT Fno FROM `{}` WHERE Fno = {}".format(table_name, Sno)
    cursor.execute(sql_find)
    conn.commit()
    tup_find = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(tup_find) == 0:
        return 0
    else:
        return 1
