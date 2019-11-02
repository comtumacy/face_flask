# coding=utf-8
import pymysql
import sys


# 在学生总表修改个人数据
def register_sql(Sno, username, password, Sname, Ssex, Birth, Saddress, Stime):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "UPDATE Student SET username='{}', password='{}', Sname='{}', Ssex='{}', Birth='{}', Saddress='{}', Stime='{}' WHERE Sno={};".format(username, password, Sname, Ssex, Birth, Saddress, Stime, Sno)
    sql2 = "SELECT * FROM Student WHERE Sno={};".format(Sno)
    try:
        # 依次提交查询语句
        cursor.execute(sql1)
        conn.commit()
        # data1 = cursor.fetchall()
        cursor.execute(sql2)
        conn.commit()
        data2 = cursor.fetchall()
        # 判断是否存在该学号的学生
        if data2 != ():
            status = 1
        else:
            status = 0
    except:
        # 捕获异常
        info = sys.exc_info()
        print(info)
        status = 0
        # info_num = str(info[1])[1:5]
        # if info_num == '1062':
        #     status = 0
    finally:
        cursor.close()
        conn.close()
    return status
