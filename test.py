# coding=utf-8
import pymysql
from templates.teacher.create_class.create_features_table import connect_mysql
from templates.teacher.create_class.create_atendance_table import connect_mysql2


def get_student_info_sql():
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT class, classno FROM `class`".format()
    sql2 = "SHOW full COLUMNS FROM Student"
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()
    cursor.execute(sql2)
    conn.commit()
    tup2 = cursor.fetchall()

    all_list = []  # 数组列表
    tup2list = []  # 字段列表
    for item in tup2:  # 提取字段至字段列表
        tup2list.append(item[0])

    for i in range(len(tup1)):  # 把每个字段转为字典
        tup_list = list(tup1[i])
        all_dict = dict(zip(tup2list, tup_list))
        all_list.append(all_dict)

    cursor.close()
    conn.close()
    for i in range(len(all_list)):
        print(all_list[i]["Sno"])
        print(all_list[i]["username"])
        connect_mysql(all_list[i]["Sno"] + all_list[i]["username"])
        connect_mysql2(all_list[i]["Sno"] + all_list[i]["username"])


get_student_info_sql()
