from api_auto_test.uaf_api_test.TestCase import *

testcases={} # 获取所有以test_开头的用例
reg_uafRequest = None  # 证书注册时testclient请求需要的uafRequest，通过/uaf/reg/receive接口获取
send_uafRequest = None # 证书注册时，保存证书需要的uafRequest，通过/uaf/reg/send接口获取
auth_uafRequest = None  # 证书认证时testclient请求需要的参数uafRequest，通过/uaf/auth/receive接口获取

class TestCert(unittest.TestCase):
    testcases['TestCert'] = [i for i in sys._getframe().f_code.co_names if 'test_' in i] #  收集test开头的用例

    def post(self,casename ,api, key=None):
        """
        casename:用例名称
        api：接口地址
        result:如果为True，返回请求数据和响应结果，否则什么都不返回
        """
        # redis = redis_conn.Rdis()
        body = test_data.test_data(casename)
        self.assertTrue(body is not False, '找不到测试数据，请检查参数名或用例名称！--{}'.format(casename))
        if key:
            first = redis.query_num_key(key) # 先获取key的数量
            r = httprequest.http_request('post', api = api, data = body)
            logging.info("request：" + json.dumps(body))
            logging.info("response：" + json.dumps(r.json()))
            print(casename+":",body)
            print(casename+":",r.json())
            second = redis.query_num_key(key) # 请求发起之后获取key的数量
            self.assertEqual(r.status_code, 200, "服务器响应状态有误！")
            self.assertEqual(r.json()[ 'statusCode' ], 1200, "接口返回状态有误！{}".format(r.json()))
            self.assertEqual(first+1,second,'redis查询不到key：{}'.format(key)) #请求发起后验证key是否+1
        else:
            r = httprequest.http_request('post', api = api, data = body)
            logging.info("request：" + json.dumps(body))
            logging.info("response：" + json.dumps(r.json()))
            print(casename + ":", body)
            print(casename + ":", r.json())
            self.assertEqual(r.status_code, 200, "服务器响应状态有误！")
            self.assertEqual(r.json()[ 'statusCode' ], 1200, "接口返回状态有误！{}".format(r.json()))
        return [body,r]

    # @unittest.skip
    def test_cert_reg_receive(self):
        """证书：注册发起"""
        global reg_uafRequest
        r = self.post('test_cert_reg_receive',api =url['reg_receive'],key = 'uaf.req.context*')
        reg_uafRequest = r[1].json()['uafRequest']  # cert_testclient请求需要的uafRequest

    # @unittest.skip
    def test_cert_reg_client(self):
        """证书：注册发起调用client"""
        self.assertNotEqual(reg_uafRequest, None, "证书：注册发起接口返回的uafRequest为空")
        reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest=reg_uafRequest)
        logging.info("response："+reg_client_response)
        self.assertTrue(len(reg_client_response)>1000,"client返回的数据：{}".format(reg_client_response))
        test_data.send_uafResponse('test_cert_reg_send', reg_client_response)  # 组装send接口请求报文

    # @unittest.skip
    def test_cert_reg_send(self):
        """证书：注册完成"""
        """
        1、校验http状态码
        2、校验statusCode
        3、校验response数据结构
        4、校验数据库数据
        """
        global send_uafRequest
        r = self.post('test_cert_reg_send',api = url['reg_send'],key='uaf.unique.req*')
        username = r[0]['context']['userName']
        sql = "select cust_no from {}.t_authenticators where cust_no='{}'".format(conf['mysql']['db'][0],username)
        self.assertTrue('description' in r[1].json())
        self.assertTrue('uafRequest' in r[1].json())
        cust_no = database.db_uap(sql)
        self.assertEqual(cust_no[ 0 ][ 0 ], username, "cust_no为t_authenticators查出来的数据，username为请求数据")
        send_uafRequest = r[1].json()['uafRequest'] #存储证书调用java方法时传的参数

    # @unittest.skip
    def test_save_cert_client(self):
        """证书：存储证书调用client"""
        send_client_response = test_client.new_testclient_obj().save_cert_client(uafRequest=send_uafRequest)
        logging.info("response：" + json.dumps(send_client_response))
        self.assertTrue(type(send_client_response) == dict,"save_cert_client返回数据：{}".format(send_client_response))
        keyid = send_client_response['keyId']
        data_save_cert = test_data.test_data('test_update_cert_status') # 获取更新证书状态为已安装的数据
        data_save_cert['context']['keyID'] = keyid # 替换keid
        dic={
            "uafResponse":"[{%s}]"%keyid
        }
        test_data.send_uafResponse('test_update_cert_status', dic) # 组装更新证书接口的数据

    # @unittest.skip
    def test_update_cert_status(self):
        """证书：更新证书状态为已安装"""
        self.post('test_update_cert_status',api = url['cert_update'])

    # @unittest.skip
    def test_cert_auth_receive(self):
        """证书：认证发起"""
        global auth_uafRequest
        r = self.post('test_cert_auth_receive', api = url['auth_receive'],key = 'uaf.auth.context*')
        auth_uafRequest = r[1].json()['uafRequest']  # cert_testclient请求需要的uafRequest

    # @unittest.skip
    def test_cert_auth_client(self):
        """证书：认证发起调用client"""
        self.assertTrue(auth_uafRequest is not None, '证书：认证发起接口返回的uafRequest为空')
        __auth_client_response = test_client.new_testclient_obj().cert_auth_client(uafRequest=auth_uafRequest)
        logging.info("response：" + __auth_client_response)
        self.assertTrue(len(__auth_client_response)>1000,"cert_auth_client返回：{}".format(__auth_client_response))
        test_data.send_uafResponse('test_cert_auth_send', __auth_client_response)

    # @unittest.skip
    def test_cert_auth_send(self):
        """证书：认证完成"""
        self.post('test_cert_auth_send',api = url['auth_send'])

def get_cert_case():
    # 按unittest要求组装用例格式
    list_case = []
    for k, v in testcases.items():
        for j in v:
            list_case.append(eval(k)(j))
    return list_case

if __name__ == '__main__':
    suit = unittest.TestSuite()
    test_client.new_testclient_obj().jvmStart()
    for i in get_cert_case():
        suit.addTest(i)
    runner = unittest.TextTestRunner()
    runner.run(suit)
    pass

