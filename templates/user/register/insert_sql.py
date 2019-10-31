# coding=utf-8
import pymysql


# 为班级考勤表加上个人学号字段
def insert_sql(Sno, class_name):
    status = 0
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='attendance',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "ALTER TABLE `attendance`.`{}` ADD COLUMN `{}` varchar(255) NULL AFTER `date`;".format(class_name, Sno)
    try:
        cursor.execute(sql1)
        conn.commit()
        status = 1
    except BaseException as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return status
