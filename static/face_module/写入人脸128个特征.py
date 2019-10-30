import pymysql
import pandas as pd

conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='LuoHongSheng336!', db='face',
                       charset='utf8')
cursor = conn.cursor()
data = pd.read_csv("features_all.csv", nrows=1)
for i in range(1, 129):
    print(data.values.tolist()[0][i-1], i)
    sql1 = "update Features set `{}` = '{}' where `Fno` = 201606401243;".format(i, data.values.tolist()[0][i-1])
    cursor.execute(sql1)
    conn.commit()
    tup1 = cursor.fetchall()
cursor.close()
conn.close()
