from api_auto_test.uaf_api_test.Config import config
import urllib3
import requests
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 去掉警告信息

def get_header():
    """
    固定请求头
    :return:
    """
    header = {
        "Content-Type": "application/fido+uaf"
    }
    return header


def http_request(method, api, header=None, data=None):
    """
    :param method: 传入请求方法：get、post、put、delete，必传
    :param api: 传入请求的接口地址，不包含域名，必传
    :param header: 传入请求头，和固定头拼接，可传可不传
    :param data: 请求参数，可传可不传
    :return:
    """
    host = config.conf['tomcat']['host']  # 域名
    port = config.conf['tomcat']['port']  # 端口号
    url = "http://{}:{}{}".format(host, port , api)
    if header is None:
        headers = get_header()
    else:
        headers = dict(get_header(), **header)
    if method == 'post':
        return requests.post(url, headers=headers, data=json.dumps(data))
    elif method == 'get':
        return requests.get(url, headers=headers)
    elif method == 'put':
        if data is None:
            return requests.put(url, headers=headers)
        return requests.put(url, headers=headers, data=json.dumps(data))
    elif method == 'delete':
        if data is None:
            return requests.delete(url, headers=headers)
        return requests.delete(url, headers=headers, data=json.dumps(data))
    else:
        raise '传递的请求方法有误：{}'.format(method)

