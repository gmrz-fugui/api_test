from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from android_auto_test.zhiya_app.common import get_driver

#获取driver对象
driver=get_driver.driver

#显示等待3秒，找不到元素返回0
def wait(method,expr):
    if method=='id':#获取单个元素
        try:
            e=WebDriverWait(driver, 2, 0.5).until(EC.presence_of_element_located((By.ID, expr)))
            return e
        except:
            return 0
    elif method=='xpath':
        try:
            e=WebDriverWait(driver, 2, 0.5).until(EC.presence_of_element_located(expr))
            return e
        except:
            return 0
    elif method=='ID':#获取多个元素
        try:
            e=WebDriverWait(driver, 1, 0.5).until(EC.presence_of_all_elements_located((By.ID, expr)))
            return e
        except:
            return 0

def save_img(num,screen_name):
    # 截图
    driver.get_screenshot_as_file('D:\\App_UI_Auto\\zhiya_app\\screen_photo\\{}\\{}.png'.format(num,screen_name))
def up_swipe(width,height):
    # 向上滑动
    x1=width*0.25
    y1=height*0.75
    y2=height*0.25
    driver.swipe(x1,y1,x1,y2,500)
def down_swipe(width,height):
    #向下滑动
    x1 = width * 0.5
    y1 = height * 0.25
    y2 = height * 0.75
    driver.swipe(x1, y1, x1, y2, 500)
def left_swipe(width,height):
    #向左滑动
    x1 = width * 0.75
    y1 = height * 0.25
    x2 = width * 0.25
    driver.swipe(x1, y1, x2, y1, 500)
def right_swipe(width,height):
    #向右滑动
    x1 = width * 0.25
    y1 = height * 0.25
    x2 = width * 0.75
    driver.swipe(x1, y1, x2, y1, 500)