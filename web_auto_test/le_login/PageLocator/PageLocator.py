from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
class PageLocator:
    """页面元素定位封装"""
    def __init__(self,driver):
        self.driver = driver

    def find_element(self, *loc,warning_code=False):
        """
        定位单个元素
        :param loc: 传入的定位方式，id、name、xpath等
        :param warning_code: 用来判断登录页面的警告弹框，根据警告弹框判断图片验证码是否正确
        :return:
        """
        """
        单位时间内元素没找到，返回false
        """
        if warning_code is False:
            try:
                WebDriverWait(self.driver, 10).until(ec.visibility_of_all_elements_located(loc))
                return self.driver.find_element(*loc)
            except:
                print("页面中没有找到此元素：{}" .format(loc))
                return False
        else:
            try:
                WebDriverWait(self.driver, 2).until(ec.visibility_of_all_elements_located(loc))
                return self.driver.find_element(*loc)
            except:
                return False

    def find_elements(self,*loc):
        # 定位多个元素
        try:
            WebDriverWait(self.driver, 10).until(ec.visibility_of_all_elements_located(loc))
            return self.driver.find_elements(*loc)
        except:
            print("页面中没有找到此元素：{}" .format(loc))
            self.driver.execute_script("window.alert('没找到元素:{}');".format(*loc[1:]))
            return False
