import os

# 服务器配置
conf = {
    "tomcat": {
        "host": "192.168.3.203",
        "port": 8080
    },
    "mysql": {
        "host": "192.168.3.211",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "charset": "utf8mb4",
        "database": "uap" # 业务库
    },
    "redis": {
        "host": "192.168.3.207",
        "port": 6379,
        "password": '123456'
    },
    "case_mysql": {
        "host": "192.168.3.211",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "charset": "utf8mb4",
        "database": "test"
    }
}
#########################################################################
dir_path = os.path.dirname(os.path.dirname(__file__))  # uaf_api_test目录
path = {
    "report_path": dir_path + '/TestReport/TestReport.html',  # 测试报告html文件
    "report_dir": dir_path + '/TestReport',  # 测试报告路径
    "case_yalm": dir_path + '/TestData/data/test_data.yalm',  # 测试用例源文件
    'cert_modify_yalm': dir_path + '/TestData/data/test_data1.yalm',  # 证书可修改用例
    "log_path": dir_path + '/Logs/log/',  # 日志存放目录
    "client_dir": {
        # test_cleint文件位置
        "pro_path": dir_path + '/TestClient/data/client.properties',
        "auth_json_path": dir_path + '/TestClient/AuthenticatorInfo.json',
        "client_dirname": dir_path + '/TestClient',
        "jar_dir": dir_path + '/TestClient/jar',
    }
}
# 接口地址 27个
url = {
    "reg_receive": '/uaf/reg/receive',  # 注册发起
    "reg_send": '/uaf/reg/send',  # 注册完成
    "auth_receive": '/uaf/auth/receive',  # 认证发起
    "auth_send": '/uaf/auth/send',  # 认证完成
    "delete": "/uaf/reg/delete",  # 注销
    "deleteall": "/uaf/reg/deleteall",  # 注销多个
    "cert_update": '/uaf/cert/updatestatus',  # 更新证书状态为已安装
    "device_list": '/uaf/device/list',  # 设备查询
    "support": '/uaf/device/support',  # 能力支持查询
    "support_v2": '/uaf/v2/device/support',  # 查能力支持查询_V2
    "reg_status": '/uaf/reg/status',  # 用户开通状态查询
    "dev_costed": '/uaf/device/costed',  # 计费设备查询
    "idauth_receive": "/uaf/idauth/receive",  # 实名认证发起
    "idauth_send": "/uaf/idauth/send",  # 实名认证完成
    "oob_generate": "/uaf/oob/generate",  # 生成二维码
    "oob_status": "/uaf/oob/status",  # 获取二维码状态
    "oob_receive": "/uaf/oob/receive",  # 扫码发起
    "oob_send": "/uaf/oob/send",  # 扫码完成
    "allinfo": "/uaf/user/allinfo",  # 获取用户所有证书注册信息
    "user_info": '/uaf/user/info',  # 获取用户注册信息
    "appid_info": "/uaf/device/info",  # 获取appID信息
    "getinfo": "/uaf/cert/getinfo",  # 获取证书信息
    "activate": "/uaf/cert/activate",  # 证书激活
    "update": "/uaf/cert/update",  # 证书更新
    "adduvi": "/uaf/reg/adduvi",  # 新增指纹接口
    "extend": "/uaf/extend",  # 扩展接口
    "reg_list": "/uaf/reg/list"  # 用户注册信息查询
}
