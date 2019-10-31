# coding=utf-8
import pymysql


def attendance_sql(table_name, date, no):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='attendance',
                           charset='utf8')
    try:
        cursor = conn.cursor()
        sql1 = "SELECT date FROM `{}` WHERE date = '{}';".format(table_name, date)
        cursor.execute(sql1)
        conn.commit()
        tup1 = cursor.fetchall()
        if len(tup1) == 0:
            print('创建{}记录'.format(date))
            sql_create = 'INSERT INTO `{}` (`date`) VALUES ("{}")'.format(table_name, date)
            cursor.execute(sql_create)
            conn.commit()
            sql1 = "update {} set `{}` = '{}' where `date` = '{}';".format(table_name, no, 1, date)
            cursor.execute(sql1)
            conn.commit()
        else:
            sql1 = "update {} set `{}` = '{}' where `date` = '{}';".format(table_name, no, 1, date)
            cursor.execute(sql1)
            conn.commit()
        status = 1
    except BaseException as e:
        print(e)
        status = 0
    finally:
        cursor.close()
        conn.close()
    return status
