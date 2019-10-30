# coding=utf-8
import pymysql


def insert_class_to_class(college, class_name, class_no):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    try:
        sql1 = "INSERT INTO class (college, class, classno) VALUES ('{}', '{}', '{}');".format(college, class_name, class_no)
        cursor.execute(sql1)
        conn.commit()
        status = 1
    except Exception as e:
        print(e)
        status = 0
    finally:
        cursor.close()
        conn.close()
    return status
