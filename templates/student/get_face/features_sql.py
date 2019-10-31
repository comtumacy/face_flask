# coding=utf-8
import pymysql


# 保存特征值到人脸特征数据库的班级表下，直接插入新行，每个学号一行
def features_sql(Sno, result, table_name):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='features',
                           charset='utf8')
    status = 0
    try:
        cursor = conn.cursor()
        sql_find = "SELECT Fno FROM `{}` WHERE Fno = {}".format(table_name, Sno)
        cursor.execute(sql_find)
        conn.commit()
        tup_find = cursor.fetchall()
        if len(tup_find) == 0:
            print('创建{}记录'.format(Sno))
            sql_create = 'INSERT INTO `{}` (`Fno`) VALUES ("{}")'.format(table_name, Sno)
            cursor.execute(sql_create)
            conn.commit()
            for i in range(1, 129):
                pass
                print('第{}次保存成功'.format(i))
                sql1 = "update {} set `{}` = '{}' where `Fno` = {};".format(table_name, i, result[i-1], Sno)
                cursor.execute(sql1)
                conn.commit()
        else:
            for i in range(1, 129):
                pass
                print('第{}次保存成功'.format(i))
                sql1 = "update {} set `{}` = '{}' where `Fno` = {};".format(table_name, i, result[i-1], Sno)
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
