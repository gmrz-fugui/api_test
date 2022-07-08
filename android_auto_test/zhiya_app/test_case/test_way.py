from android_auto_test.zhiya_app.common import get_driver, common_fun
import unittest
import time
import random
driver= get_driver.driver
class Test_App_Teacher(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loc = ("xpath", "//*[@text='始终允许']")
        for i in range(6):
            allow= common_fun.wait('xpath', loc)
            if allow:
                allow.click()# 应用启动时获取手机权限并允许

    def test_app_start(self):
        """路径1：启动app，验证隐私授权是否白屏，并滑动协议"""
        content_id='tv_rules_content'#隐私授权
        content= common_fun.wait('id', content_id)
        common_fun.save_img(1, '隐私授权')
        #隐私授权是否弹出
        if content:
            width=content.size['width']
            height=content.size['height']
            if len(content.text)==0:
                common_fun.save_img(1, '隐私协议空白')#隐私协议空白截图
            else:
                for i in range(50):
                    common_fun.up_swipe(width, height)#隐私协议滑动到底部
                    if i==49:
                        common_fun.save_img(1, '隐私协议滑动的截图')
            agree_id = 'tv_agree'  # 同意隐私授权
            driver.find_element_by_id(agree_id).click()
        else:
            common_fun.save_img(1, '隐私授权没有弹出')
        close_id='iv_dia_close'
        result= common_fun.wait('id', close_id)
        if result:
            result.click()#关闭会员赠送弹框
        else:
            common_fun.save_img(1, '赠送会员弹框x号')
        read_id = 'rb_read'  # 读书页面id
        read = common_fun.wait('id', read_id)
        read.click()  # 切换到读书页面
        time.sleep(3)
    def test_read_search(self):
        """路径2：切到读书页，点击搜索框->发送搜索请求->点击搜索结果"""
        # read_id = 'rb_read'  # 读书页面id
        # read = common_fun.wait('id', read_id)
        # read.click()  # 切换到读书页面
        seach_id = 'et_search_kw'  # 搜索框id
        seach = common_fun.wait('id', seach_id)
        if seach:
            seach.click()
            hot_id = 'tv_hot_search_txt'  # 热门搜索id
            hot = common_fun.wait('id', hot_id)
            if hot==0:
                common_fun.save_img(2, '热门搜索标签没有')
            seach.send_keys('老师')#输入老师并搜索
            sea_button='tv_do_search'#搜索按钮
            driver.find_element_by_id(sea_button).click()
            more_id='tv_watch_more_article'#查看更多
            more= common_fun.wait('id', more_id)
            if more==0:
                common_fun.save_img(2, '搜索结果页面')
            driver.find_elements_by_id(more_id)[0].click()#点击第一个查看更多
            title_id='tv_title'
            title= common_fun.wait('id', title_id)
            if title==0:
                common_fun.save_img(2, '查看更多详情页面')
            driver.find_elements_by_xpath('//*')[0].click()#查看更多详情列表点击第一个
            share_id='iv_right_sus'
            if share_id==0:
                common_fun.save_img(2, '点击搜索结果')
            back_id='iv_back_sus'
            driver.find_elements_by_id(back_id)[0].click()#详情后退
            back='iv_back'
            driver.find_element_by_id(back).click()#列表后退
            time.sleep(1)
            driver.find_element_by_id(back).click()#清空搜索框
            time.sleep(1)
            driver.find_element_by_id(back).click()  # 搜索页后退到读书页
        else:
            common_fun.save_img(2, '读书页搜索框')

    def test_book(self):
        """路径3：经典导读--5个导航切换--点击某一个导航--上下左右滑动--点击进入详情--浏览目录"""
        lst=['现代进阶','全球史观','知识领域','精选书单','名师导读']
        book_id='all_menu_twelve'
        common_fun.wait('id', book_id).click()
        title_id='tv_title'#经典导读页面标题
        book='iv_item_dire_book_cover'#经典导读书籍id
        b= common_fun.wait('id', book)
        if b==0:
            for i in range(3):
                common_fun.save_img(3, '经典导读详情加载失败{}'.format(i))
                time.sleep(2)
        if common_fun.wait('id', title_id)==0:
            common_fun.save_img(3, '经典导读页面标题')
        tab_id='tv_tab_title'
        for j in range(20):
            #经典导读各个标签切换
            t = common_fun.wait('ID', tab_id)
            rd = random.randint(0, 4)
            t[rd].click()
            if t==0:
                for i in range(3):
                    common_fun.save_img(3, '经典导读找不到标签截图{}'.format(i))
                    time.sleep(2)
                break
            else:
                if t[rd].text!=lst[rd]:
                    for i in range(3):
                        common_fun.save_img(3, '经典导读切换标签截图{}'.format(i))
                        time.sleep(2)
                    break
            if j==19:
                t[0].click()
        #上下左右滑动
        width=driver.get_window_size()['width']
        height=driver.get_window_size()['height']
        for _ in range(10):
            #上滑
            common_fun.up_swipe(width, height)
            time.sleep(1)
        for _ in range(11):
            #下滑
            common_fun.down_swipe(width, height)
            time.sleep(1)
        for _ in range(3):
            #左滑
            common_fun.left_swipe(width, height)
            time.sleep(1)
        for _ in range(3):
            #右滑
            common_fun.right_swipe(width, height)
            time.sleep(1)
        lst_book='iv_item_dire_book_cover'
        lst= common_fun.wait(lst_book)
    @classmethod
    def tearDownClass(cls):
        pass
def get_teacher_case():
    lst=[
        Test_App_Teacher('test_app_start'),
        Test_App_Teacher('test_read_search'),
        Test_App_Teacher('test_book')
    ]
    return lst
if __name__ == '__main__':
    suit=unittest.TestSuite()
    suit.addTest(Test_App_Teacher('test_app_start'))
    # suit.addTest(Test_App_Teacher('test_read_search'))
    suit.addTest(Test_App_Teacher('test_book'))
    runner=unittest.TextTestRunner()
    runner.run(suit)