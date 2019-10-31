# coding=utf-8
import pymysql


def student_number_matching_sql(table_name, no):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='features',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT Fno FROM `{}` limit {},1;".format(table_name, no)
    cursor.execute(sql1)
    conn.commit()
    no = int(cursor.fetchall()[0][0])
    return no
