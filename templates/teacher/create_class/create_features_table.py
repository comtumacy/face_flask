# coding=utf-8
import pymysql
from teacher.create_class.content_replacement_before import content_replacement_before
from teacher.create_class.content_replacement_after import content_replacement_after


# 读取SQL文件
def get_sql_files():
    sql_files = ["/home/flask/templates/teacher/create_class/sql/Features.sql"]
    return sql_files


# 批量执行SQL文件
def connect_mysql(table_name):
    # 替换SQL文件Table名
    content_replacement_before('/home/flask/templates/teacher/create_class/sql/Features.sql', 'Features', table_name)
    # 打开数据库连接
    db = pymysql.connect(host='106.54.119.102', port=2707, user='root', password='Luohongsheng336!', db='features',
                           charset='utf8')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    for file in get_sql_files():
        execute_scripts_from_file(file, cursor, table_name)
    db.close()


def execute_scripts_from_file(filename, cursor, table_name):
    fd = open(filename, 'r', encoding='utf-8')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(';')

    for command in sql_commands:
        try:
            cursor.execute(command)
        except Exception as msg:
            print(msg)
    # 替换回SQL文件Table名初始值
    content_replacement_after('/home/flask/templates/teacher/create_class/sql/Features.sql', table_name, 'Features')
    print('sql执行完成')
