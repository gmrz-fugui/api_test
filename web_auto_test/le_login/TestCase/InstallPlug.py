from web_auto_test.le_login.TestCase import *

class InstallPlug(unittest.TestCase):
    driver = common.driver
    pageaction = PageAction.PageAction(driver)  # 实例化LoginAction传入webdriver驱动
    driver.maximize_window()
    allow = (By.ID, 'allow')  # 允许按钮
    success = (By.ID, 'allowHint')

    @BeautifulReport.add_test_img('/plug')
    def test_install_plug(self):
        """安装登录插件"""
        """
        1、浏览器启动，安装插件时会打开两个页面
        2、先关闭当前空白的data页面
        3、close关闭后，窗口句柄返回还是两个，需要切换到协议页面
        4、同意协议
        """
        windows = self.driver.window_handles  # 获取当前浏览器所有窗口的句柄
        self.driver.close()  # 关闭当前空白的data页面
        self.driver.switch_to.window(windows[0])  # 切换到协议页面
        self.pageaction.time_sleep(1)
        allow_btn = self.pageaction.button_click(*self.allow)  # 定位允许按钮
        self.assertTrue(allow_btn is not False)  # 校验允许按钮
        succ = self.pageaction.no_actions(*self.success)  # 定位点击允许后的页面
        self.assertTrue(succ is not False)  # 校验点击允许后的页面
        self.pageaction.time_sleep(1)
        self.pageaction.save_img('plug') # 允许之后截图
        self.pageaction.time_sleep(1)

def get_install_case():
    list_case = [
        InstallPlug("test_install_plug")
    ]
    return list_case


if __name__ == '__main__':
    unittest.main()
