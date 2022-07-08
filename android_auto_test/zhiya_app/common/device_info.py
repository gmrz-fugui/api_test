
def devices_info():
    desired_caps = {
        # 系统名
        "platformName" : "Android",
        # 安卓版本
        "platformVersion" : "9",
        # 设备名称
        "deviceName" : "1137d34",#8cd3990d
        "automationName": "UiAutomator1",
        # zhiya_app 包名
        "appPackage" : "com.zongxueguan.naochanle_android",
        # app启动页
        "appActivity" : "com.zongxueguan.naochanle_android.ui.guide.ACT_Splash",
        "unicodeKeyboard": True,
        "resetKeyboard": True
    }
    return desired_caps

