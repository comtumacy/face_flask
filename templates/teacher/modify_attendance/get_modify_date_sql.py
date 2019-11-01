# coding=utf-8
import pymysql


def get_modify_date_sql(table_name):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='attendance',
                           charset='utf8')
    try:
        cursor = conn.cursor()
        sql1 = "SELECT date FROM `{}`;".format(table_name)
        cursor.execute(sql1)
        conn.commit()
        tup1 = cursor.fetchall()
        all_list = []  # 数组列表
        tup2list = list()  # 字段列表
        tup2list.append('date')
        for i in range(len(tup1)):  # 把每个字段转为字典
            tup_list = list(tup1[i])
            all_dict = dict(zip(tup2list, tup_list))
            all_list.append(all_dict)
    except BaseException as e:
        all_list = []
        print(e)
    finally:
        cursor.close()
        conn.close()
    return all_list
