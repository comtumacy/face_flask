# coding=utf-8
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
from io import BytesIO
import base64


def get_random_color():
    # 获取一个随机颜色(r,g,b)格式的
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return c1, c2, c3


def get_random_str():
    # 获取一个随机字符串，每个字符的颜色也是随机的
    random_num = str(random.randint(0, 9))
    random_low_alpha = chr(random.randint(97, 122))
    random_upper_alpha = chr(random.randint(65, 90))
    random_text = random.choice([random_num, random_low_alpha, random_upper_alpha])
    return random_text


def pil_base64(ima):
    #  把PIL的image对象转为base64编码字符串
    img_buffer = BytesIO()
    ima.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    base64_str = str(base64_str, 'utf-8')
    return base64_str


def get_verification_code_base64():
    # 获取验证码base64编码

    str = ''

    # 获取一个Image对象，参数分别是RGB模式。宽150，高30，随机颜色
    image = Image.new('RGB', (150, 30), get_random_color())

    # 获取一个画笔对象，将图片对象传过去
    draw = ImageDraw.Draw(image)

    # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
    font = ImageFont.truetype("FRADM.TTF", size=26)

    # 循环5次，获取4个随机字符串
    for i in range(4):
        random_char = get_random_str()
        str = str + random_char
        # 在图片上一次写入得到的随机字符串,参数是：定位，字符串，颜色，字体
        draw.text((10 + i * 30, 0), random_char, get_random_color(), font=font)

    # 噪点噪线
    width = 150
    height = 30
    # 划线
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(30):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    base_str = pil_base64(image)

    return base_str, str
