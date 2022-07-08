from web_auto_test.le_login.TestCase import *

class LoginCase(unittest.TestCase):
    driver = common.driver # 获取浏览器驱动
    pageaction = PageAction.PageAction(driver)  # 实例化LoginAction传入webdriver驱动
    pageaction.del_img() # 启动测试，删除img下图片
    phone = (By.ID, 'phone')  # 手机号输入框
    vercode_pic= (By.ID, 'changeRandom') # 图片验证码
    vercode_input = (By.ID, 'inputCode')  # 图片验证码输入框
    phonecode = (By.ID, 'password')  # 手机验证码输入框
    get_phone_btn = (By.ID,'smsButton') # 获取手机验证码按钮
    login_button =(By.ID,'loginBtn') #登录按钮
    warning_code = (By.CLASS_NAME,'el-message--error') # 点击获取手机验证码时，提示图片验证码错误，弹出的警告
    loginUrl = (By.CLASS_NAME,'loginUrl') # 登陆后页面，需要点击的url按钮
    @classmethod
    def setUpClass(cls):
        cls.driver.get(common.login_page_url)  # 加载登录页面地址

    @classmethod
    def tearDownClass(cls):
        # 登陆后等待3秒退出
        cls.pageaction.time_sleep(3)

    @BeautifulReport.add_test_img('/test_login','test_login1')
    def test_login(self):
        """用户登录"""
        """
        测试流程说明
        1、输入手机号  
        2、图片验证码截图并识别图片验证码 
        3、输入图片验证码 
        4、点击获取手机验证码，如果提示图片验证码错误，刷新图片验证码，重新截图，识别，输入，此步骤最多重复10次
        5、从reids取到手机验证码，redis如果20秒查不到,返回-1
        6、输入手机验证码，点击登录
        7、校验登录成功后的页面并截图
        """
        phone = self.pageaction.input_text(data.mobile(), *self.phone)  # 输入手机号
        self.assertTrue(phone is not False)  # 校验手机号输入框
        for i in range(10):
            # 验证码如果连续识别错误10次，退出测试
            vercode_pic = self.pageaction.vercode_pic(*self.vercode_pic)  # 定位图片验证码
            self.assertTrue(vercode_pic is not False)  # 校验图片验证码
            vercode_pic.screenshot(common.img_dir+'/code.png') # 图片验证码截图
            vercode = verCode.get_vercode() # 获取解析的图片验证码
            if type(vercode)==str:
                vercode_input = self.pageaction.input_text(vercode, *self.vercode_input)  # 定位图片验证码输入框并输入
                self.assertTrue(vercode_input is not False)  # 校验图片验证码输入框
                get_phone_btn = self.pageaction.button_click(*self.get_phone_btn)  # 点击获取手机验证码
                self.assertTrue(get_phone_btn is not False)  # 校验获取手机验证码按钮
                warning_code = self.pageaction.warning_code(*self.warning_code) # 提示手机验证码获取失败的警告
                if warning_code is False:
                    break
                else:
                    if i==9:
                        self.pageaction.save_img('test_login')
                        self.assertTrue(False==True,'图片验证码连续10次识别错误，退出测试！')
            vercode_pic.click() # 刷新图片验证码
            self.pageaction.time_sleep(0.5)
        rediscode = redisCode.execute_redis(data.mobile())  # redis返回的手机验证码
        self.assertTrue(type(rediscode)==str,'手机验证码获取失败：{}'.format(rediscode)) # 校验redis返回的手机验证码
        phonecode = self.pageaction.input_text(rediscode, *self.phonecode) # 定位手机验证码输入框并输入手机验证码
        self.assertTrue(phonecode is not False) # 校验手机验证码输入框
        login_button = self.pageaction.button_click(*self.login_button) # 定位登录按钮并登录
        self.assertTrue(login_button is not False) # 校验登录按钮
        for i in range(5):
            # 点击登录后，判断5秒内页面是否跳转成功，未跳转则退出测试
            if self.driver.current_url == common.login_net_url:
                self.pageaction.save_img('test_login')
                break
            if i==4:
                self.pageaction.save_img('test_login')
                self.assertTrue(False==True,'点击登录，5秒没跳转成功，退出测试！')
            self.pageaction.time_sleep(1)
        self.pageaction.save_img('test_login1')
        loginurl = self.pageaction.button_click(*self.loginUrl) # 点击跳转主页
        self.assertTrue(loginurl is not False) # 校验url跳转元素
        for i in range(5):
            # 点击url跳转，未跳转则退出测试
            if self.driver.current_url == common.home_page_url:
                self.pageaction.save_img('test_login1')
                break
            if i==4:
                self.assertTrue(False==True,'点击url，5秒没跳转成功，退出测试！')
            self.pageaction.time_sleep(1)
def get_login_case():
    """
    组装测试用例
    :return:
    """
    list_case = [
        LoginCase("test_login")
    ]
    return list_case

if __name__ == '__main__':
    # unittest.main()
    pass

