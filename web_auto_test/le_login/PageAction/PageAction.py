from web_auto_test.le_login.PageLocator import PageLocator
from selenium.webdriver.common.keys import Keys
from web_auto_test.le_login.Common import common
import time
import os


class PageAction:
    """登录页面动作封装"""
    def __init__(self, driver):
        self.driver = driver
        self.loginpage = PageLocator.PageLocator(self.driver)  # 实例化LoginPageLocator

    @classmethod
    def time_sleep(cls, t):
        # 强制等待
        time.sleep(t)

    @staticmethod
    def del_img():
        # 循环删除img下所有图片
        if len(os.listdir(common.img_dir)) == 0:
            pass
        else:
            for i in os.listdir(common.img_dir):
                os.remove(common.img_dir + '/' + i)

    def save_img(self, img_name):
        # 页面截图，截图展示在测试报告
        self.driver.get_screenshot_as_file('{}/{}.png'.format(common.img_dir, img_name))

    def input_text(self, text, *loc):
        # 输入框定位后输入
        document = self.loginpage.find_element(*loc)
        if document:
            document.click() # 点击文本框
            document.send_keys(Keys.CONTROL, 'a') # 全选文本框内容
            document.send_keys(Keys.BACK_SPACE) # 删除文本框内容
            document.clear()
            PageAction.time_sleep(1)
            document.send_keys(text)
        return document

    def button_click(self, *loc):
        # 定位单个按钮并点击
        document = self.loginpage.find_element(*loc)
        if document:
            document.click()
        return document

    def buttons_click(self,num, *loc):
        # 定位多个按钮，根据下标点击
        document = self.loginpage.find_elements(*loc)
        if document:
            self.driver.execute_script("arguments[0].click();", document[num]) # 使用js点击
            # document[num].click()
        return document

    def click_dom(self,dom):
        # 不用定位，直接点击
        dom.click()
        return self

    def vercode_pic(self, *loc):
        # 定位验证码图片，用到复数定位方法
        document = self.loginpage.find_elements(*loc)[0]
        return document

    def warning_code(self, *loc):
        # 判断图片验证码输入错误时调用
        document = self.loginpage.find_element(*loc, warning_code=True)
        return document

    def no_action(self,*loc):
        """定位单个元素，什么动作都不做"""
        return self.loginpage.find_element(*loc)

    def no_actions(self,*loc):
        """定位多个元素，什么动作都不做"""
        return self.loginpage.find_elements(*loc)

    def frame_in(self,name):
        """进入frame"""
        self.driver.switch_to.frame(name)

    def frame_out(self):
        """退出frame，切回主文档"""
        self.driver.switch_to.default_content()




