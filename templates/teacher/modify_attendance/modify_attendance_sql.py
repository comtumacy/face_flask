# coding=utf-8
import pymysql


def modify_attendance_sql(table_name, Sno, sign, date):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='attendance',
                           charset='utf8')
    try:
        cursor = conn.cursor()
        sql1 = "UPDATE `{}` SET `{}` = '{}' WHERE date = '{}'".format(table_name, Sno, sign, date)
        cursor.execute(sql1)
        conn.commit()
        status = 1
    except BaseException as e:
        status = 1
        print(e)
    finally:
        cursor.close()
        conn.close()
    return status
