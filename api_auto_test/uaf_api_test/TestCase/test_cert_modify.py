from api_auto_test.uaf_api_test.TestCase import *
import yaml

reg_uafRequest = None  # 证书注册时testclient请求需要的uafRequest，通过/uaf/reg/receive接口获取
send_uafRequest = None  # 证书注册时，保存证书需要的uafRequest，通过/uaf/reg/send接口获取
auth_uafRequest = None  # 证书认证时testclient请求需要的参数uafRequest，通过/uaf/auth/receive接口获取


class TestCertModify(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 创建CheckResult类对象
        cls.ch = check_result.CheckResult()

    @parameterized.expand(check_result.data.test_data_modify('test_cert_reg_receive1'))
    # @unittest.skip
    def test_cert_reg_receive1(self, params, expect):
        """证书：注册发起，可手动修改用例"""
        self.ch.check_result(casename = 'test_cert_reg_receive1', api = url[ 'reg_receive' ], body = params,
                             expect = expect)

    @parameterized.expand(check_result.data.test_data_modify('test_cert_reg_send2'))
    # @unittest.skip
    def test_cert_reg_send2(self, params, expect):
        """证书：注册完成，可手动修改用例"""
        self.ch.check_result(casename = 'test_cert_reg_send2', api = url[ 'reg_send' ], body = params,
                             expect = expect)

    @parameterized.expand(check_result.data.test_data_modify('test_cert_auth_receive3'))
    # @unittest.skip
    def test_cert_auth_receive3(self, params, expect):
        """证书：认证发起，可手动修改用例"""
        self.ch.check_result(casename = 'test_cert_auth_receive3', api = url[ 'auth_receive' ], body = params,
                             expect = expect)

    @parameterized.expand(check_result.data.test_data_modify('test_cert_auth_send4'))
    # @unittest.skip
    def test_cert_auth_send4(self, params, expect):
        """证书：认证完成，可手动修改用例"""
        self.ch.check_result(casename = 'test_cert_auth_send4', api = url[ 'auth_send' ], body = params,
                             expect = expect)

if __name__ == '__main__':
    from uaf_api_test.CheckResult import case_sort
    test_client.new_testclient_obj().jvmStart()
    unittest.main(testLoader = case_sort.MyTestLoader())
