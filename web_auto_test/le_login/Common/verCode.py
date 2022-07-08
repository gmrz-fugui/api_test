from PIL import Image
from web_auto_test.le_login.Common import common
import os
import pytesseract

def get_vercode():
    scr_dir = os.listdir(common.img_dir)
    if bool(len(scr_dir)):
        img = Image.open(common.img_dir + '/code.png')
    else:
        print("验证码目录为空")
        return 0
    img = img.convert('L')  # P模式转换为L模式(灰度模式默认阈值127)
    count = 165  # 设定阈值
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)
    img = img.point(table, '1')
    img.save(common.img_dir + '/code1.png')  # 保存处理后的验证码图片
    ##################################################################
    # 读取图片内容
    pic = Image.open(common.img_dir + '/code1.png')
    text = pytesseract.image_to_string(pic, lang='eng')
    r = text.replace('\n','')
    if len(r)==4:
        return r
    else:
        # print('验证码识别错误，需要刷新页面重新识别:get_vercode方法')
        return -1