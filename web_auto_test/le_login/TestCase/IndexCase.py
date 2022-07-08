from web_auto_test.le_login.TestCase import *

driver = common.driver
all_list = appList.appList  # 应用列表

class ApplicationList(unittest.TestCase):
    """应用列表"""
    pageaction = PageAction.PageAction(driver)  # 实例化LoginAction传入webdriver驱动
    applist = (By.CLASS_NAME, 'anticon-deployment-unit')  # 应用列表按钮
    add = (By.CLASS_NAME, 'ant-btn-primary')  # 添加应用按钮
    frame = 'iframe'  # irame框架id
    span_left = (By.XPATH, "//div[@class='leftMenuWrap']//span")  # 左边菜单span标签
    list_right = (By.XPATH,"//div[@class='rightContentWrap']//div[@class='lists']//p")  # 右边p标签列表
    set_pwd_btn = (By.XPATH,'//*[@id="protocolType"]/label[1]') # 管理员设置账户名、口令
    username = (By.XPATH,'//*[@id="username"]') # 用户名
    password = (By.XPATH,'//*[@id="cryptoCredential"]') # 密码
    confpwd = (By.XPATH,'//*[@id="checkPass"]') # 确认密码
    submit = (By.CLASS_NAME,'ant-btn-primary') # 确定按钮
    antbtn = (By.XPATH,'/html/body/div[7]/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div[4]/button') # 取消按钮
    count = (By.CLASS_NAME,'el-pagination__total') # 应用总数
    btn_next = (By.CLASS_NAME,'btn-next') # 下一页
    def test_add_application(self):
        """应用列表"""
        applist = self.pageaction.buttons_click(0, *self.applist)  # 点击应用列表
        self.assertTrue(applist is not False)  # 校验应用列表
        add = self.pageaction.button_click(*self.add)  # 点击添加应用
        self.assertTrue(add is not False)  # 校验添加应用按钮
        try:
            self.pageaction.frame_in(self.frame)  # 进入frame
        except Exception as e:
            driver.execute_script("window.alert('进入frame失败');")
            print(e)
        app_count= self.pageaction.no_action(*self.count) # 获取应用总数元素
        self.assertTrue(app_count is not False) # 校验应用总数元素
        # num = int(re.findall("\d+", app_count.text)[0]) # 提取应用数量并转换类型：int
        while True:
            # 循环翻页
            lst = self.pageaction.no_actions(*self.list_right) # 当前页面应用
            btn_next = self.pageaction.no_action(*self.btn_next) # 下一页按钮
            self.assertTrue( btn_next is not False) # 校验下一页按钮
            next_enabled = btn_next.is_enabled() # 下一页按钮是否置灰
            print(next_enabled)
            n = 0 # 控制进入frame
            for i in lst:
                # 循环点击当前页面的9个应用
                if n!=0:
                    self.pageaction.frame_in(self.frame) # 进入frame
                username = 'admin'
                password = 'admin'
                confpwd = 'admin'
                self.pageaction.click_dom(i) # 点击应用
                self.pageaction.frame_out() # 退出frame
                self.pageaction.button_click(*self.set_pwd_btn)  # 点击管理员设置口令
                self.pageaction.input_text(username, *self.username)  # 输入用户名
                self.pageaction.input_text(password, *self.password)  # 输入密码
                self.pageaction.input_text(confpwd, *self.confpwd)  # 确认密码
                self.pageaction.button_click(*self.submit)  # 点击确定
                ant = self.pageaction.no_actions(*self.antbtn) # 授权页面点击取消
                self.pageaction.click_dom(ant[0]) # 点击授权页面取消按钮
                n += 1
            if next_enabled:
                self.pageaction.click_dom(*btn_next) # 点击下一页
            else:
                break
            # lst = self.pageaction.no_actions(*self.list_right) # 当前页面应用
            # if len(lst) != len(all_list):
            #     print('我的列表长度：{}，页面返回的列表长度{}'.format(len(all_list), len(lst)))
            # n = 0
            # for i in lst:
            #     if n!=0:
            #         self.pageaction.frame_in(self.frame) # 进入frame
            #     for k,v in all_list.items():
            #         if i.text == k:
            #             username = v['username']
            #             password = v['password']
            #             confpwd = v['confpwd']
            #             self.pageaction.click_dom(i) # 点击应用
            #             self.pageaction.frame_out() # 退出frame
            #             self.pageaction.button_click(*self.set_pwd_btn)  # 点击管理员设置口令
            #             self.pageaction.input_text(username, *self.username)  # 输入用户名
            #             self.pageaction.input_text(password, *self.password)  # 输入密码
            #             self.pageaction.input_text(confpwd, *self.confpwd)  # 确认密码
            #             self.pageaction.button_click(*self.submit)  # 点击确定
            #             ant = self.pageaction.no_actions(*self.antbtn) # 授权页面点击取消
            #             self.pageaction.click_dom(ant[0]) # 点击授权页面取消按钮
            #             break
            #     n += 1


def get_index_case():
    """
    组装测试用例
    :return:
    """
    list_case = [
        ApplicationList("test_add_application")
        # ApplicationList("test_add_data")
    ]
    return list_case
