from web_auto_test.le_login.Common import common
import yaml



def mobile():
    with open(common.data, encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)  # 获取yalm手机号
    return data['test_login']['mobile']