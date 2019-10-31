# coding=utf-8
import pymysql


def get_student_features_sql(table_name):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='features',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT * FROM `{}`;".format(table_name)
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()

    all_list = []
    for i in range(len(tup1)):
        tup_list = list(tup1[i])
        del tup_list[0]
        new_tup1_list = []
        for j in range(len(tup_list)):
            new_tup1_list.append(float(tup_list[j]))
        all_list.append(new_tup1_list)

    return all_list


# get_student_info_sql('计算机科学与技术162')
