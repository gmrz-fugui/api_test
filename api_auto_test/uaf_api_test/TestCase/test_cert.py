from api_auto_test.uaf_api_test.TestCase import *

reg_uafRequest = None  # 证书注册时testclient请求需要的uafRequest，通过/uaf/reg/receive接口获取
send_uafRequest = None  # 证书注册时，保存证书需要的uafRequest，通过/uaf/reg/send接口获取
auth_uafRequest = None  # 证书认证时testclient请求需要的参数uafRequest，通过/uaf/auth/receive接口获取

ch = check_result.CheckResult()

class TestCert(unittest.TestCase):
    """
    调用check_result时需要指定casename、api，校验key时指定key
    """
    @classmethod
    def setUpClass(cls) -> None:
        # 创建CheckResult类对象
        cls.ch = check_result.CheckResult()
        # cls.reg_rec_key = 'uaf.req.context*' # 注册发起key
        # cls.reg_send_key = 'uaf.unique.req*' # 注册完成key
        # cls.auth_rec_key = 'uaf.auth.context*' # 认证发起key

    def test_cert_reg_receive(self):
        """证书：注册发起"""
        global reg_uafRequest
        r = self.ch.check_result(casename = 'test_cert_reg_receive', api = url[ 'reg_receive' ])
        reg_uafRequest = r[ 1 ].json()[ 'uafRequest' ]  # cert_testclient请求需要的uafRequest

    # @unittest.skip
    def test_cert_reg_client(self):
        """证书：注册发起调用client"""
        self.assertNotEqual(reg_uafRequest, None, "证书：注册发起接口返回的uafRequest为空")
        reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
        logging.info("response：" + reg_client_response)
        self.assertTrue(len(reg_client_response) > 1000, "client返回的数据：{}".format(reg_client_response))
        check_result.data.send_uafResponse('test_cert_reg_send', reg_client_response)  # 组装send接口请求报文

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
        r = self.ch.check_result(casename = 'test_cert_reg_send', api = url[ 'reg_send' ])
        username = r[ 0 ][ 'context' ][ 'userName' ]
        sql = "select cust_no from t_authenticators where cust_no='{}'".format(username)
        self.assertTrue('description' in r[ 1 ].json())
        self.assertTrue('uafRequest' in r[ 1 ].json())
        cust_no = check_result.database.db_uap(sql)
        self.assertEqual(cust_no[ 0 ][ 0 ], username, "cust_no为t_authenticators查出来的数据，username为请求数据")
        send_uafRequest = r[ 1 ].json()[ 'uafRequest' ]  # 存储证书调用java方法时传的参数

    # @unittest.skip
    def test_save_cert_client(self):
        """证书：存储证书调用client"""
        send_client_response = test_client.new_testclient_obj().save_cert_client(uafRequest = send_uafRequest)
        logging.info("client--response：" + json.dumps(send_client_response))
        self.assertTrue(type(send_client_response) == dict, "save_cert_client返回数据：{}".format(send_client_response))
        keyid = send_client_response[ 'keyId' ]
        data_save_cert = check_result.data.test_data('test_update_cert_status')  # 获取更新证书状态为已安装的数据
        data_save_cert[ 'context' ][ 'keyID' ] = keyid  # 替换keid
        dic = {
            "uafResponse": "[{%s}]" % keyid
        }
        check_result.data.send_uafResponse('test_update_cert_status', dic)  # 组装更新证书接口的数据

    # @unittest.skip
    def test_update_cert_status(self):
        """证书：更新证书状态为已安装"""
        self.ch.check_result(casename = 'test_update_cert_status', api = url[ 'cert_update' ])

    # @unittest.skip
    def test_cert_auth_receive(self):
        """证书：认证发起"""
        global auth_uafRequest
        r = self.ch.check_result(casename = 'test_cert_auth_receive', api = url[ 'auth_receive' ])
        auth_uafRequest = r[ 1 ].json()[ 'uafRequest' ]  # cert_testclient请求需要的uafRequest

    # @unittest.skip
    def test_cert_auth_client(self):
        """证书：认证发起调用client"""
        self.assertTrue(auth_uafRequest is not None, '证书：认证发起接口返回的uafRequest为空')
        __auth_client_response = test_client.new_testclient_obj().cert_auth_client(uafRequest = auth_uafRequest)
        logging.info("response：" + __auth_client_response)
        self.assertTrue(len(__auth_client_response) > 1000, "cert_auth_client返回：{}".format(__auth_client_response))
        check_result.data.send_uafResponse('test_cert_auth_send', __auth_client_response)

    # @unittest.skip
    def test_cert_auth_send(self):
        """证书：认证完成"""
        self.ch.check_result(casename = 'test_cert_auth_send', api = url[ 'auth_send' ])

if __name__ == '__main__':
    from uaf_api_test.CheckResult import case_sort
    test_client.new_testclient_obj().jvmStart()
    unittest.main(testLoader = case_sort.MyTestLoader())
