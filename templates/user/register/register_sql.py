import pymysql
import sys


def register_sql(Sno, username, password, Sname, Ssex, Sclass, Sdept):
    status = 0
    conn = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='LuoHongSheng336!', db='face',
                           charset='utf8')
    cursor = conn.cursor()
    sql1 = "INSERT INTO Student ( Sno, username, password, Sname, Ssex, Sclass, Sdept ) VALUES ( {}, '{}', '{}', '{}', '{}', '{}', '{}');".format(Sno, username, password, Sname, Ssex, Sclass, Sdept)
    try:
        cursor.execute(sql1)
        conn.commit()
        status = 1
    except:
        # 捕获异常
        info = sys.exc_info()
        info_num = str(info[1])[1:5]
        if info_num == '1062':
            status = 0
    finally:
        cursor.close()
        conn.close()
    return status