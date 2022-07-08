from selenium import webdriver
import os

"""各文件目录"""
img_dir = os.path.dirname(os.path.dirname(__file__)) + '/img'  # 验证码截图目录
report_path = os.path.dirname(os.path.dirname(__file__)) + '/TestReport/'  # 测试报告路径
data = os.path.dirname(os.path.dirname(__file__)) + '/data/test_datas.yalm'  # 测试数据yalm文件
plug_file = os.path.dirname(os.path.dirname(__file__)) + '/dist/dist.crx' # 插件

""""各页面url"""
login_page_url = 'https://id.nationauth.cn:1443/lelogin-portal/login'  # 登录页
login_net_url = 'https://id.nationauth.cn:1443/lelogin-portal/loginSelectUrl' # 登录后选择url页面
home_page_url = 'https://id.nationauth.cn:1443/lelogin/dashboard/analysis'  # 登录后的主页

"""安装插件并，定义Chrome浏览器驱动"""
options = webdriver.ChromeOptions()
options.add_extension(plug_file)
driver = webdriver.Chrome(options=options)
