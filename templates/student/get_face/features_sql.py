# coding=utf-8
import pymysql


# 保存特征值到数据库
def features_sql(Sno, result):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    status = 0
    try:
        for i in range(1, 129):
            pass
            print('第{}次保存成功'.format(i))
            sql1 = "update Features set `{}` = '{}' where `Fno` = {};".format(i, result[i-1], Sno)
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