from BeautifulReport.BeautifulReport import result,data
import json
import requests

url = "https://oapi.dingtalk.com/robot/send?access_token=b1785c0fc03b862c95b019d02d00ae7f705241badbc6bb6fa28bbdd6da3eff6b "
header = {
    "Content-Type": "application/json"
}

def send_ding():
    """
    测试用例执行结果发送钉钉通知
    """
    if result:
        if result[2] > 0:
            data_fail = {
                "msgtype": "text", "text": {
                    "content": "测试结果：{}个接口用例执行完成，{}个接口有异常，详情请查阅邮箱附件！".format(
                        result[0], result[2])}, "at": {
                    "isAtAll": True}}
            r = requests.post(url, headers=header, data=json.dumps(data_fail))
            print(r.json())
            print('有错误，已发送钉钉通知')
        else:
            data_pass = {
                "msgtype": "text",
                "text": {
                    "content": "{}个接口用例执行完成，测试结果正常！".format(result[0])
                },
                "at": {
                    "isAtAll": True
                }
            }
            r = requests.post(url, headers=header, data=json.dumps(data_pass))
            print(r.json())
            print('全部正常，已发送钉钉通知')
    else:
        data_pass = {
            "msgtype": "text",
            "text": {
                "content": "没数据测试一下"
            },
            "at": {
                "isAtAll": True
            }
        }
        r = requests.post(url, headers=header, data=json.dumps(data_pass))
        print(r.json())
        print('没数据测试一下，已发送钉钉通知')

send_ding()
