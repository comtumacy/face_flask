# coding=utf-8
import pymysql


# 在人脸特征数据库中的班级表内查询该学生是否已经存在人脸数据（修改）
def find_features_sql(Sno):
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "SELECT * FROM Features WHERE Fno = {};".format(Sno)
    sql2 = "SHOW full COLUMNS FROM Features"
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()
    cursor.execute(sql2)
    conn.commit()
    tup2 = cursor.fetchall()

    all_list = []  # 数组列表
    tup2list = []  # 字段列表
    for item in tup2:  # 提取字段至字段列表
        tup2list.append(item[0])

    for i in range(len(tup1)):  # 把每个字段转为字典
        tup_list = list(tup1[i])
        all_dict = dict(zip(tup2list, tup_list))
        all_list.append(all_dict)

    cursor.close()
    conn.close()
    return all_list
