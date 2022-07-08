from android_auto_test.zhiya_app.common import device_info
from appium import webdriver
d=webdriver.Remote('http://localhost:4723/wd/hub', device_info.devices_info())
driver=d
