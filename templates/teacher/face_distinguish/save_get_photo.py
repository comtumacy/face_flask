# coding=utf-8
import os
import base64


def save_get_photo(Tno, base64_str):
    # 创建用户文件夹(linux change)
    path = 'D:\\face\\static\\photo\\teacher\\{}'.format(Tno)
    is_exists = os.path.exists(path)
    if is_exists:
        pass
    else:
        os.mkdir(path)

    # 保存照片
    status = 0
    try:
        img = base64.b64decode(base64_str)
        file = open('D:\\face\\static\\photo\\teacher\\{}\\teacher.jpg'.format(Tno), 'wb')
        file.write(img)
        file.close()
        status = 1
    except Exception as e:
        print('Error:', e)
        status = 0
    finally:
        return status
